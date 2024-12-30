# projekt má pod sebou slovník, kde klíče jsou názvy činností (ty uživatel doplňuje vstupem (tlačítko nová činnost) a hodnotou je tupl/slovník, který obsahuje začátek a konec činnosti, opět zadané uživatelem)
# střed je vždy dnešní den - import datetime


# import knihoven
import json
import os
from datetime import datetime
import plotly.express as px
from flask import Flask, render_template, url_for, request, redirect, session, jsonify
import pandas as pd


# import dalších modulů aplikace
from data_management import nacti_json_soubor, uloz_json_soubor
from project_list import pridat_projekt, file_path as project_path

# Cesty k souborům
program_path = os.path.dirname(os.path.abspath(__file__))
projects_database_path = os.path.join(program_path, "project_list.json")

# Flask app
app = Flask(__name__)
app.secret_key = "587fca9d5437db51c4c35e3438b430327a7d34ecd337f9162f69af41d1fb41cd"

@app.route("/")
def index():
    return redirect(url_for("home"))

@app.route("/home", methods=["GET", "POST"])
def home():
    project_file_path = session.get('database_path', 'default_database.json')  # Defaultní cesta k souboru projektů

    if request.method == "POST":
        new_project = request.form["new_project"]
        if new_project:
            project_file_path, _ = pridat_projekt(new_project)
            session["database_path"] = project_file_path  # Uložení cesty k souboru nově vytvořeného projektu do session

    # Načtení seznamu projektů pro výběr
    try:
        with open(project_path, "r") as jsonfile:
            temata = json.load(jsonfile)
    except FileNotFoundError:
        temata = {}  # Případ, kdy neexistují žádné projekty

    return render_template("home.html", temata=temata)

@app.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        note = request.form.get('note')

        # Konverze start_date a end_date na datetime objekty pro validaci
        start_date_dt = pd.to_datetime(start_date)
        end_date_dt = pd.to_datetime(end_date)

        if end_date_dt < start_date_dt:
            # Zobrazení chyby uživateli, pokud end_date je dříve než start_date
            return render_template('save.html', error="Datum konce nemůže být dříve než datum začátku")

        new_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "start_date": start_date,
            "end_date": end_date,
            "note": note
        }

        database_path = session.get('current_project_path', 'default_database.json')
        uloz_json_soubor(database_path, new_data)  # Ukládání do správného souboru
        return redirect(url_for('display_project', project_name=session.get('current_project')))

    return render_template('save.html')

@app.route('/delete_project', methods=['POST'])
def delete_project():
    if request.method == 'POST':
        project_to_delete = request.form.get('delete_project')

        try:
            with open(projects_database_path, 'r') as file:
                projects = json.load(file)

            project_file_path = projects.get(project_to_delete)
            if project_file_path:
                os.remove(project_file_path)  # Smazání souboru
                del projects[project_to_delete]  # Odebrání záznamu o projektu z databáze

                with open(projects_database_path, 'w') as file:
                    json.dump(projects, file, indent=4)

                return redirect(url_for('home'))
            else:
                return "Projekt neexistuje."
        except Exception as e:
            return f"Error deleting project: {str(e)}"

@app.route('/display_project/<project_name>', methods=['GET', 'POST'])
def display_project(project_name):
    session['current_project'] = project_name
    notes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'project_notes')
    note_file_path = os.path.join(notes_dir, f'note_{project_name}.json')

    # Pokud složka pro poznámky neexistuje, vytvoří ji
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir)

    # Načtení poznámek ze souboru JSON, pokud existuje
    if os.path.exists(note_file_path):
        with open(note_file_path, 'r') as note_file:
            notes = json.load(note_file)
    else:
        notes = {}

    if request.method == 'POST':
        note_text = request.form.get('note_text')
        if note_text:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            notes[timestamp] = note_text
            with open(note_file_path, 'w') as note_file:
                json.dump(notes, note_file)
            return jsonify({'timestamp': timestamp})  # Vrátíme JSON odpověď

    try:
        # Načtení dat projektu
        with open(projects_database_path, 'r') as file:
            projects = json.load(file)

        project_file_path = projects.get(project_name)
        if not project_file_path:
            raise ValueError("Projekt nebyl nalezen")

        session['current_project_path'] = project_file_path  # Uložení cesty k souboru do session

        if os.path.exists(project_file_path):
            with open(project_file_path, 'r') as file:
                project_data = json.load(file)
        else:
            project_data = []

        if project_data:
            # Podrobnější kontrola formátu aktivit
            for activity in project_data:
                missing_keys = [key for key in ['start_date', 'end_date', 'note', 'timestamp'] if key not in activity]
                if missing_keys:
                    raise ValueError(f"Aktivita nemá správný formát, chybějící klíče: {missing_keys}. Aktivita: {activity}")

            df = pd.DataFrame(project_data)
            df['start_date'] = pd.to_datetime(df['start_date'])
            df['end_date'] = pd.to_datetime(df['end_date'])

            # Seřazení DataFrame nejprve podle 'end_date' a pak podle 'start_date'
            df.sort_values(['end_date', 'start_date'], ascending=[True, True], inplace=True)

            fig = px.timeline(df, x_start="start_date", x_end="end_date", y="note", title=f"Gantt Chart for {project_name}")
            fig.update_yaxes(autorange="reversed")
            graph_html = fig.to_html(full_html=False)
        else:
            graph_html = ""

        return render_template('display_project.html', project_name=project_name, project_data=project_data, notes=notes, graph_html=graph_html)
    except Exception as e:
        return f"Error loading or processing project data: {str(e)}"



@app.route('/save_note', methods=['POST'])
def save_note():
    if request.method == 'POST':
        # Získání dat poznámky z formuláře
        note_text = request.form.get('note_text')

        # Získání aktuálního času a vytvoření timestampu ve formátu ISO 8601
        timestamp = datetime.datetime.now().isoformat()

        # Zkontroluje, zda existuje složka pro poznámky projektů, pokud ne, vytvoří ji
        notes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'project_notes')
        if not os.path.exists(notes_dir):
            os.makedirs(notes_dir)

        # Získání cesty k souboru pro uložení poznámky
        project_name = session.get('current_project')
        note_file_path = os.path.join(notes_dir, f'note_{project_name}.json')

        # Zkontroluje, zda soubor s poznámkami již existuje, pokud ne, vytvoří nový soubor
        if not os.path.exists(note_file_path):
            with open(note_file_path, 'w') as note_file:
                json.dump({}, note_file)

        # Načtení stávajících poznámek
        with open(note_file_path, 'r') as note_file:
            notes = json.load(note_file)

        # Přidání nové poznámky do slovníku poznámek
        notes[timestamp] = note_text

        # Uložení aktualizovaného slovníku poznámek zpět do souboru
        with open(note_file_path, 'w') as note_file:
            json.dump(notes, note_file, indent=4)

        return redirect(url_for('display_project', project_name=project_name))
    else:
        return "Metoda POST je povinná pro tuto routu."

@app.route('/display')
def display():
    try:
        with open(projects_database_path, 'r') as file:
            projects = json.load(file)

        activities = []
        for project_name, project_file_path in projects.items():
            with open(project_file_path, 'r') as file:
                project_data = json.load(file)
                for activity in project_data:
                    activity['project'] = project_name
                    activities.append(activity)

        df = pd.DataFrame(activities)
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])

        # Seřazení DataFrame nejprve podle 'end_date' a pak podle 'start_date'
        df.sort_values(['end_date', 'start_date'], ascending=[True, True], inplace=True)

        # Vypočítání počtu dnů do termínu
        df['days_to_deadline'] = (df['end_date'] - pd.to_datetime('today')).dt.days
        labels = ['red', 'orange', 'yellow', 'lightblue', 'blue']
        df['color'] = pd.qcut(df['days_to_deadline'], 5, labels=labels)

        # Vytvoření popisku pro osu y
        df['label'] = df['project'] + "/" + df['note']

        # Explicitně seřazené kategorie pro osu y
        category_orders = df['label'].tolist()

        # Vytvoření Ganttova diagramu
        fig = px.timeline(df, x_start="start_date", x_end="end_date", y="label", color='color',
                          color_discrete_map={label: label for label in labels},
                          title="Unified Gantt Chart",
                          category_orders={"label": category_orders})

        # Není potřeba obracet osu Y
        graph_html = fig.to_html(full_html=False)

        return render_template('display.html', graph_html=graph_html)
    except Exception as e:
        return f"Error loading or processing data: {str(e)}"

@app.route('/edit_project/<project_name>', methods=['GET', 'POST'])
def edit_project(project_name):
    # Načtení cesty k souboru projektu ze session
    project_file_path = session.get('current_project_path')
    if not project_file_path:
        return "Chyba: Cesta k projektu není v session."

    if request.method == 'POST':
        # Načtení existujících dat projektu
        try:
            with open(project_file_path, 'r') as file:
                project_data = json.load(file)
                if not isinstance(project_data, list):
                    raise ValueError("Data projektu nejsou ve správném formátu.")
        except FileNotFoundError:
            return "Projekt nebyl nalezen."

        # Načtení dat z formuláře
        activities = request.form.getlist('activity')
        start_dates = request.form.getlist('start_date')
        end_dates = request.form.getlist('end_date')
        timestamps = request.form.getlist('timestamp')

        # Modifikace existujících dat
        updated_project_data = []
        for i in range(len(activities)):
            updated_project_data.append({
                'timestamp': timestamps[i],
                'start_date': start_dates[i],
                'end_date': end_dates[i],
                'note': activities[i]
            })

        # Přepsání existujících dat v souboru
        try:
            with open(project_file_path, 'w') as file:
                json.dump(updated_project_data, file, indent=4)
        except IOError as e:
            return str(e)  # Vrací popis chyby, pokud dojde k nějaké při zápisu

        return redirect(url_for('display_project', project_name=project_name))

    # Načtení existujících dat projektu pro GET request
    try:
        with open(project_file_path, 'r') as file:
            project_data = json.load(file)
            if not isinstance(project_data, list):
                raise ValueError("Data projektu nejsou ve správném formátu.")
    except FileNotFoundError:
        return "Projekt nebyl nalezen."

    # Předání dat do šablony pro úpravu
    return render_template('edit_project.html', project_name=project_name, project_data=project_data)

# Spuštění aplikace
if __name__ == '__main__':
    app.run(debug=True)
