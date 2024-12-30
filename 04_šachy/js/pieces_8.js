class Piece {
    constructor(position, color) {
        this.position = position;
        this.color = color;
    }

    // Metoda pro kontrolu, zda je pole obsazené a případně soupeřovou figurkou
    isOccupied(targetField, actualPosition) {
        const piece = actualPosition[targetField];
        if (!piece) return { occupied: false, opponent: false }; // Pole je prázdné

        // Pokud je pole obsazené, vracíme také informaci, zda je obsazeno soupeřovou figurkou
        return {
            occupied: true,
            opponent: piece.color !== this.color // true, pokud je to soupeřova figurka
        };
    }

    // Placeholder pro konkrétní pohyby - přepíše každá figura
    getPossibleMoves(actualPosition) {
        return [];
    }
}

// bishop
//
//

class Bishop extends Piece {
    constructor(position, color) {
        super(position, color); // Volá konstruktor třídy Piece
    }

    getPossibleMoves(actualPosition) {
        const possibleMoves = [];
        const [file, rank] = [this.position.charCodeAt(0), parseInt(this.position[1])];

        const directions = [
            { fileOffset: 1, rankOffset: 1 },
            { fileOffset: 1, rankOffset: -1 },
            { fileOffset: -1, rankOffset: 1 },
            { fileOffset: -1, rankOffset: -1 }
        ];

        for (const direction of directions) {
            let newFile = file;
            let newRank = rank;

            while (true) {
                newFile += direction.fileOffset;
                newRank += direction.rankOffset;

                const targetField = String.fromCharCode(newFile) + newRank;

                if (newFile < 97 || newFile > 104 || newRank < 1 || newRank > 8) {
                    break; // Mimo šachovnici
                }

                const targetElement = document.getElementById(targetField); // Získáme <td> element cílového pole
                if (!targetElement) break; // Pokud element neexistuje, pokračujeme

                const { occupied, opponent } = this.isOccupied(targetField, actualPosition);

                if (!occupied) {
                    possibleMoves.push(targetField); // Přidáme volné pole
                } else if (opponent) {
                    possibleMoves.push(targetField); // Přidáme pole obsazené soupeřovou figurkou
                    break; // Nemůžeme jít dál přes soupeřovu figurku
                } else {
                    break; // Nemůžeme jít dál přes vlastní figurku
                }
            }
        }

        return possibleMoves;
    }
}

// rook
//
//

class Rook extends Piece {
    constructor(position, color) {
        super(position, color); // Volá konstruktor třídy Piece
    }

    getPossibleMoves(actualPosition) {
        const possibleMoves = [];
        const [file, rank] = [this.position.charCodeAt(0), parseInt(this.position[1])];

        // Směry pro věž: nahoru, dolů, doleva, doprava
        const directions = [
            { fileOffset: 0, rankOffset: 1 },  // Nahoru (stejný sloupec, vyšší řádky)
            { fileOffset: 0, rankOffset: -1 }, // Dolů (stejný sloupec, nižší řádky)
            { fileOffset: 1, rankOffset: 0 },  // Doprava (vyšší sloupce, stejný řádek)
            { fileOffset: -1, rankOffset: 0 }  // Doleva (nižší sloupce, stejný řádek)
        ];

        for (const direction of directions) {
            let newFile = file;
            let newRank = rank;

            while (true) {
                newFile += direction.fileOffset;
                newRank += direction.rankOffset;

                const targetField = String.fromCharCode(newFile) + newRank;

                if (newFile < 97 || newFile > 104 || newRank < 1 || newRank > 8) {
                    break; // Mimo šachovnici
                }

                // Kontrola obsazenosti cílového pole
                const targetElement = document.getElementById(targetField); // Získáme <td> element cílového pole
                if (!targetElement) break; // Ověříme, zda element existuje (může se stát, že je mimo šachovnici)

                const { occupied, opponent } = this.isOccupied(targetField, actualPosition);

                if (!occupied) {
                    possibleMoves.push(targetField); // Přidáme volné pole
                } else if (opponent) {
                    possibleMoves.push(targetField); // Přidáme pole obsazené soupeřovou figurkou
                    break; // Nemůžeme jít dál přes soupeřovu figurku
                } else {
                    break; // Nemůžeme jít dál přes vlastní figurku
                }
            }
        }

        return possibleMoves;
    }
}

// queen
//
//

class Queen extends Piece {
    constructor(position, color) {
        super(position, color); // Volá konstruktor třídy Piece
    }

    /**
     * Vrací seznam všech možných tahů pro figuru Dáma, je kombinací pohybu střelce a věže.
     * Využívá třídy Rook a Bishop
     * @param {*} actualPosition 
     * @returns {Array} - seznam možných tahů ve formátu polí (např. [e4, f5])
     */
    getPossibleMoves(actualPosition) {
        const rookMoves = new Rook(this.position, this.color).getPossibleMoves(actualPosition);
        const bishopMoves = new Bishop(this.position, this.color).getPossibleMoves(actualPosition);

        // Kombinace tahů věže a střelce
        return [...rookMoves, ...bishopMoves];
        // Metoda getPossibleMoves pro dámu vrací kombinaci tahů věže a střelce pomocí destrukturace a spojení polí ([...rookMoves, ...bishopMoves]).
        // CTRL + ú - pohyb o tab zpět, CTRL + ) - pohyb o tam vpřed
    }
}

// knight
//
//

class Knight extends Piece {
    constructor(position, color) {
        super(position, color); // Volá konstruktor třídy Piece
    }

    getPossibleMoves(actualPosition) {
        const possibleMoves = [];
        const [file, rank] = [this.position.charCodeAt(0), parseInt(this.position[1])];

        // Jezdec se pohybuje o 2 pole v jednom směru a 1 pole v kolmém směru
        const knightMoves = [
            { fileOffset: 1, rankOffset: 2 },
            { fileOffset: 1, rankOffset: -2 },
            { fileOffset: -1, rankOffset: 2 },
            { fileOffset: -1, rankOffset: -2 },
            { fileOffset: 2, rankOffset: 1 },
            { fileOffset: 2, rankOffset: -1 },
            { fileOffset: -2, rankOffset: 1 },
            { fileOffset: -2, rankOffset: -1 }
        ];

        for (const move of knightMoves) {
            const newFile = file + move.fileOffset;
            const newRank = rank + move.rankOffset;

            const targetField = String.fromCharCode(newFile) + newRank;

            // Kontrola, zda je tah v rámci šachovnice
            if (newFile >= 97 && newFile <= 104 && newRank >= 1 && newRank <= 8) {
                const { occupied, opponent } = this.isOccupied(targetField, actualPosition);

                if (!occupied || opponent) {
                    possibleMoves.push(targetField); // Přidáme volné pole nebo pole obsazené soupeřem
                }
            }
        }

        return possibleMoves;
    }
}


// pawn
//
//

class Pawn extends Piece {
    constructor(position, color) {
        super(position, color); // Volá konstruktor třídy Piece
        this.startRank = color === 'white' ? 2 : 7; // Výchozí řada pro pěšce
        this.direction = color === 'white' ? 1 : -1; // Směr pohybu (1 pro bílé, -1 pro černé)
    }

    getPossibleMoves(actualPosition) {
        const possibleMoves = [];
        const [file, rank] = [this.position.charCodeAt(0), parseInt(this.position[1])];

        // Kontrola pohybu o jedno pole vpřed
        const oneStepForward = String.fromCharCode(file) + (rank + this.direction);
        if (!this.isOccupied(oneStepForward, actualPosition).occupied) {
            possibleMoves.push(oneStepForward);

            // Kontrola pohybu o dvě pole vpřed při prvním tahu
            if (rank === this.startRank) {
                const twoStepsForward = String.fromCharCode(file) + (rank + 2 * this.direction);
                if (!this.isOccupied(twoStepsForward, actualPosition).occupied) {
                    possibleMoves.push(twoStepsForward);
                }
            }
        }

        // Kontrola braní diagonálně
        const diagonals = [
            { fileOffset: 1, rankOffset: this.direction },  // Vpravo dopředu
            { fileOffset: -1, rankOffset: this.direction }  // Vlevo dopředu
        ];

        for (const diagonal of diagonals) {
            const newFile = file + diagonal.fileOffset;
            const newRank = rank + diagonal.rankOffset;
            const targetField = String.fromCharCode(newFile) + newRank;

            // Kontrola, zda je pole napadané pěšcem obsazené soupeřovou figurkou
            const { occupied, opponent } = this.isOccupied(targetField, actualPosition);

            if (newFile >= 97 && newFile <= 104 && occupied && opponent) {
                possibleMoves.push(targetField); // Pěšec může brát pouze soupeřovu figurku
            }
        }

        return possibleMoves;
    }

    // Přesun pěšce s kontrolou promotion
    moveTo(targetField, actualPosition) {
        // Přesuň pěšce na nové pole
        this.position = targetField;

        // Zkontroluj, zda pěšec dosáhl 8. (bílí) nebo 1. (černí) řady
        const targetRank = parseInt(targetField[1]);
        if ((this.color === 'white' && targetRank === 8) || (this.color === 'black' && targetRank === 1)) {
            this.promotion(); // Spusť proměnu pěšce
        }
    }

    // Metoda pro proměnu pěšce
    promotion() {
        // Vytvoření vizuálního výběru pro proměnu pěšce
        const choice = prompt("Zvolte proměnu: q = Dáma, r = Věž, b = Střelec, n = Jezdec");

        let newPieceClass;
        switch (choice) {
            case 'q':
                newPieceClass = Queen;
                break;
            case 'r':
                newPieceClass = Rook;
                break;
            case 'b':
                newPieceClass = Bishop;
                break;
            case 'n':
                newPieceClass = Knight;
                break;
            default:
                newPieceClass = Queen; // Výchozí volba je dáma
        }

        // Vytvoření nové instance vybrané figury
        const newPiece = new newPieceClass(this.position, this.color);

        // Aktualizace stavu šachovnice (nahradíme pěšce novou figurkou)
        initialPosition[this.position] = newPiece;

        // Aktualizace grafického zobrazení na šachovnici
        const currentCell = document.getElementById(this.position);
        currentCell.innerHTML = pieceSymbols[this.color][newPiece.constructor.name]; // Změna symbolu na šachovnici

        console.log(`Pěšec byl proměněn na ${newPiece.constructor.name}`);
    }
}


// king
//
//

class King extends Piece {
    constructor(position, color) {
        super(position, color);
    }

    getPossibleMoves(actualPosition) {
        const possibleMoves = [];
        const [file, rank] = [this.position.charCodeAt(0), parseInt(this.position[1])];

        // Směry, kterými se může král pohybovat (o jedno pole všemi směry)
        const directions = [
            { fileOffset: 0, rankOffset: 1 },    // Nahoru
            { fileOffset: 0, rankOffset: -1 },   // Dolů
            { fileOffset: 1, rankOffset: 0 },    // Doprava
            { fileOffset: -1, rankOffset: 0 },   // Doleva
            { fileOffset: 1, rankOffset: 1 },    // Diagonálně vpravo nahoru
            { fileOffset: -1, rankOffset: 1 },   // Diagonálně vlevo nahoru
            { fileOffset: 1, rankOffset: -1 },   // Diagonálně vpravo dolů
            { fileOffset: -1, rankOffset: -1 }   // Diagonálně vlevo dolů
        ];

        for (const direction of directions) {
            const newFile = file + direction.fileOffset;
            const newRank = rank + direction.rankOffset;

            // Kontrola, zda je tah v rámci šachovnice
            if (newFile >= 97 && newFile <= 104 && newRank >= 1 && newRank <= 8) {
                const targetField = String.fromCharCode(newFile) + newRank;

                const { occupied, opponent } = this.isOccupied(targetField, actualPosition);

                // Král se může pohybovat na prázdné pole nebo pole obsazené soupeřem
                if (!occupied || opponent) {
                    possibleMoves.push(targetField);
                }
            }
        }

        return possibleMoves;
    }
}

// game
//
//

class Game {
    constructor(king, playerPieces, opponentPieces) {
        this.king = king;

        this.playerPieces = playerPieces;
        this.opponentPieces = opponentPieces;
    }

    // Kontrola šach matu
    isCheckMate() {
        // Pokud je král v šachu
        if (this.king.isInCheck(this.getCurrentPosition(), this.opponentPieces)) {
            // Projdeme všechny tahy všech hráčových figur
            for (const piece of this.playerPieces) {
                const possibleMoves = piece.getPossibleMoves(this.getCurrentPosition());

                // Pokud má některá z figur tah, kterým se král může dostat ze šachu, není to šach mat
                for (const move of possibleMoves) {
                    // Simulujeme tento tah a ověříme, zda by po něm král nebyl v šachu
                    const newPosition = this.simulateMove(piece, move);
                    if (!this.king.isInCheck(newPosition, this.opponentPieces)) {
                        return false; // Král má možnost uniknout, takže to není šach mat
                    }
                }
            }
            return true; // Pokud neexistuje žádný platný tah, je to šach mat
        }
        return false; // Král není v šachu, takže nemůže být šach mat
    }

    // Kontrola patu
    isStaleMate() {
        // Pokud král není v šachu
        if (!this.king.isInCheck(this.getCurrentPosition(), this.opponentPieces)) {
            // Zkontrolujeme, zda hráč má alespoň jeden platný tah
            for (const piece of this.playerPieces) {
                const possibleMoves = piece.getPossibleMoves(this.getCurrentPosition());

                // Pokud má hráč alespoň jeden platný tah, není to pat
                if (possibleMoves.length > 0) {
                    return false;
                }
            }
            return true; // Pokud hráč nemá žádné tahy, je to pat
        }
        return false; // Král je v šachu, takže to nemůže být pat
    }

    // Simulace tahu pro zjištění následků (např. při šachu a šach matu)
    simulateMove(piece, move) {
        // Vytvoříme kopii aktuálního stavu šachovnice
        const newPosition = JSON.parse(JSON.stringify(this.getCurrentPosition()));

        // Provedeme tah
        newPosition[move] = piece;
        delete newPosition[piece.position];

        return newPosition;
    }

    // Získání aktuální pozice všech figur na šachovnici
    getCurrentPosition() {
        // Vrátí objekt představující aktuální pozici všech figur na šachovnici
        const position = {};
        for (const piece of this.playerPieces.concat(this.opponentPieces)) {
            position[piece.position] = piece;
        }
        return position;
    }
}






