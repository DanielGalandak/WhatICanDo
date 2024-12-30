// Písmena pro sloupce od 'a' do 'h'
const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

// Mapování symbolů na základě barvy a typu figury
const pieceSymbols = {
    white: {
        'Rook': '♖',
        'Knight': '♘',
        'Bishop': '♗',
        'Queen': '♕',
        'King': '♔',
        'Pawn': '♙'
    },
    black: {
        'Rook': '♜',
        'Knight': '♞',
        'Bishop': '♝',
        'Queen': '♛',
        'King': '♚',
        'Pawn': '♟'
    }
};

let selectedPiece = null; // Uchovává vybranou figurku
let draggedPiece = null; // Uchovává přetahovanou figurku

// Výchozí pozice figurek (bílé a černé) s inicializací tříd
const initialPosition = {
    'a1': new Rook('a1', 'white'),
    'b1': new Knight('b1', 'white'),
    'c1': new Bishop('c1', 'white'),
    'd1': new Queen('d1', 'white'),
    'e1': new King('e1', 'white'),
    'f1': new Bishop('f1', 'white'),
    'g1': new Knight('g1', 'white'),
    'h1': new Rook('h1', 'white'),
    'a2': new Pawn('a2', 'white'),
    'b2': new Pawn('b2', 'white'),
    'c2': new Pawn('c2', 'white'),
    'd2': new Pawn('d2', 'white'),
    'e2': new Pawn('e2', 'white'),
    'f2': new Pawn('f2', 'white'),
    'g2': new Pawn('g2', 'white'),
    'h2': new Pawn('h2', 'white'),

    'a8': new Rook('a8', 'black'),
    'b8': new Knight('b8', 'black'),
    'c8': new Bishop('c8', 'black'),
    'd8': new Queen('d8', 'black'),
    'e8': new King('e8', 'black'),
    'f8': new Bishop('f8', 'black'),
    'g8': new Knight('g8', 'black'),
    'h8': new Rook('h8', 'black'),
    'a7': new Pawn('a7', 'black'),
    'b7': new Pawn('b7', 'black'),
    'c7': new Pawn('c7', 'black'),
    'd7': new Pawn('d7', 'black'),
    'e7': new Pawn('e7', 'black'),
    'f7': new Pawn('f7', 'black'),
    'g7': new Pawn('g7', 'black'),
    'h7': new Pawn('h7', 'black')
};

// Vytvoření šachovnice
function renderBoard() {
    let tableContent = ''; // Inicializuje tableContent jako prázdný string
    const table = document.getElementById('chess-board'); // Odkaz na šachovnici (tabulku)

    for (let rank = 8; rank >= 1; rank--) { // Řádky 8-1, aby a1 bylo dole vlevo
        tableContent += "<tr>";
        for (let file = 0; file < 8; file++) { // Prochází písmena sloupců 'a' až 'h'
            const cellId = files[file] + rank; // ID je jako a1, b1, ..., h8
            const piece = initialPosition[cellId]; // Získá instanci figury na tomto poli

            // Zjistí, jaký symbol zobrazit na základě třídy a barvy figury
            let pieceSymbol = '';
            if (piece) {
                const pieceType = piece.constructor.name; // Typ figury (Rook, Knight, etc.)
                pieceSymbol = pieceSymbols[piece.color][pieceType]; // Symbol na základě typu a barvy
            }

            // Určování barvy pole a; přidání draggable atributu, pokud je tam figura
            if ((rank + file) % 2 === 0) {
                tableContent += `<td id="${cellId}" class="white" draggable="${piece ? 'true' : 'false'}">${pieceSymbol}</td>`;
            } else {
                tableContent += `<td id="${cellId}" class="black" draggable="${piece ? 'true' : 'false'}">${pieceSymbol}</td>`;
            }
        }
        tableContent += "</tr>";
    }

    table.innerHTML = tableContent; // Vloží generovaný obsahu do tabulky
    addEventListeners(); // Přidání event listenerů pro klikání a přetahování
}

// Přidání EventListenerů pro drag-and-drop funkce a click
let hasMoved = false; // Flag to ensure turn switches only once

function addEventListeners() {
    document.querySelectorAll('td').forEach(cell => {
        // Drag and drop
        cell.addEventListener('dragstart', function (event) {
            const fromCellId = event.target.id;
            const piece = initialPosition[fromCellId];

            if (!piece) {
                event.preventDefault();
                return;
            }

            console.log(`Turn: ${isWhiteTurn ? 'White' : 'Black'}, Piece: ${piece.color}`);

            // Only allow dragging if it's the player's turn
            if ((isWhiteTurn && piece.color !== 'white') || (!isWhiteTurn && piece.color !== 'black')) {
                event.preventDefault(); // Prevent dragging if it's not the player's turn
                alert(`It's ${isWhiteTurn ? 'white' : 'black'}'s turn!`);
            } else {
                draggedPiece = piece;
                event.dataTransfer.setData('text', fromCellId);
                hasMoved = false; // Reset the flag for this move
            }
        });

        cell.addEventListener('dragover', function (event) {
            event.preventDefault(); // Allow the drag-over action
        });

        cell.addEventListener('drop', function (event) {
            event.preventDefault();
            const toCellId = event.target.id;
            const fromCellId = event.dataTransfer.getData('text');

            if (draggedPiece && !hasMoved) { // Ensure this only runs once
                const possibleMoves = draggedPiece.getPossibleMoves(initialPosition);

                if (possibleMoves.includes(toCellId)) {
                    initialPosition[toCellId] = draggedPiece;
                    delete initialPosition[fromCellId];
                    draggedPiece.position = toCellId;

                    // Handle promotion for pawns
                    if (draggedPiece.constructor.name === 'Pawn' && (toCellId[1] === '8' || toCellId[1] === '1')) {
                        draggedPiece.promotion();
                    }

                    renderBoard(); // Re-render the board
                    addMove(fromCellId, toCellId); // Log the move

                    // Switch turns only once
                    console.log(`Switching turn from ${isWhiteTurn ? 'White' : 'Black'}`);
                    isWhiteTurn = !isWhiteTurn; // Toggle the turn
                    console.log(`Turn is now: ${isWhiteTurn ? 'White' : 'Black'}`);
                    hasMoved = true; // Mark that the move has been made
                }
            }

            draggedPiece = null;
        });

        // Click event for moving pieces
        cell.addEventListener('click', function () {
            const clickedCellId = cell.id;
            const clickedPiece = initialPosition[clickedCellId];

            if (selectedPiece === null && clickedPiece) {
                console.log(`Turn: ${isWhiteTurn ? 'White' : 'Black'}, Piece: ${clickedPiece.color}`);

                if ((isWhiteTurn && clickedPiece.color !== 'white') || (!isWhiteTurn && clickedPiece.color !== 'black')) {
                    alert(`It's ${isWhiteTurn ? 'white' : 'black'}'s turn!`);
                    return;
                }
                selectedPiece = clickedPiece;
                cell.classList.add('selected');
                hasMoved = false; // Reset the flag for this move
            } else if (selectedPiece !== null && selectedPiece !== clickedPiece && !hasMoved) { // Ensure this only runs once
                const possibleMoves = selectedPiece.getPossibleMoves(initialPosition);

                if (possibleMoves.includes(clickedCellId)) {
                    const fromPosition = selectedPiece.position;
                    const toPosition = clickedCellId;

                    initialPosition[toPosition] = selectedPiece;
                    delete initialPosition[fromPosition];
                    selectedPiece.position = toPosition;

                    // Handle promotion for pawns
                    if (selectedPiece.constructor.name === 'Pawn' && (toPosition[1] === '8' || toPosition[1] === '1')) {
                        selectedPiece.promotion();
                    }

                    renderBoard(); // Re-render the board
                    addMove(fromPosition, toPosition); // Log the move

                    // Switch turns only once
                    console.log(`Switching turn from ${isWhiteTurn ? 'White' : 'Black'}`);
                    isWhiteTurn = !isWhiteTurn;
                    console.log(`Turn is now: ${isWhiteTurn ? 'White' : 'Black'}`);
                    hasMoved = true; // Mark that the move has been made

                    selectedPiece = null;
                } else {
                    alert('Invalid move!');
                    selectedPiece = null;
                    renderBoard(); // Re-render to reset selections
                }
            } else if (selectedPiece === clickedPiece) {
                selectedPiece = null;
                cell.classList.remove('selected'); // Remove highlight
            }
        });
    });
}

// Notace a tahy
let movesHistory = [];
let isWhiteTurn = true; // Sleduje, zda je na tahu bílý nebo černý

function addMove(fromPosition, toPosition) {
    let piece = initialPosition[toPosition] || initialPosition[fromPosition]; // Získáme figuru z cílového nebo zdrojového pole
    let pieceNotation = '';

    // Určíme notaci pro každou figuru
    switch (piece.constructor.name) {
        case 'Rook':
            pieceNotation = 'R'; // Věž
            break;
        case 'Knight':
            pieceNotation = 'N'; // Jezdec
            break;
        case 'Bishop':
            pieceNotation = 'B'; // Střelec
            break;
        case 'Queen':
            pieceNotation = 'Q'; // Dáma
            break;
        case 'King':
            pieceNotation = 'K'; // Král
            break;
        case 'Pawn':
            pieceNotation = ''; // Pěšec nemá žádnou notaci
            break;
    }

    // Notace obsahuje pouze cíl tahu (přidáme písmeno figury, pokud to není pěšec)
    const move = `${pieceNotation}${toPosition}`;

    if (isWhiteTurn) {
        movesHistory.push({ white: move, black: null });
    } else {
        movesHistory[movesHistory.length - 1].black = move;
    }

    renderMovesTable(); // Vykreslení tabulky s tahy
    console.log(`It's now ${isWhiteTurn ? 'white' : 'black'}'s turn.`);
}


function renderMovesTable() {
    const movesBody = document.getElementById('moves-body');
    movesBody.innerHTML = ''; // Vyčistíme tabulku

    movesHistory.forEach((move, index) => {
        const row = document.createElement('tr');
        const moveNumberCell = document.createElement('td');
        moveNumberCell.textContent = index + 1; // Pořadí tahu

        const whiteMoveCell = document.createElement('td');
        whiteMoveCell.textContent = move.white || '';

        const blackMoveCell = document.createElement('td');
        blackMoveCell.textContent = move.black || '';

        row.appendChild(moveNumberCell);
        row.appendChild(whiteMoveCell);
        row.appendChild(blackMoveCell);
        movesBody.appendChild(row);
    });
}

// Načti a vykresli šachovnici při načtení stránky
document.addEventListener('DOMContentLoaded', function () {
    renderBoard();
});
