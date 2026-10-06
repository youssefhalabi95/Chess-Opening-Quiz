from flask import Flask, render_template, request
import chess
import random

app = Flask(__name__)


# =========================================================
# OPENING DATABASE
# =========================================================

OPENINGS = [
    {
        "name": "Ruy Lopez",
        "moves": ["e4", "e5", "Nf3", "Nc6", "Bb5"]
    },
    {
        "name": "Italian Game",
        "moves": ["e4", "e5", "Nf3", "Nc6", "Bc4"]
    },
    {
        "name": "Scotch Game",
        "moves": ["e4", "e5", "Nf3", "Nc6", "d4"]
    },
    {
        "name": "King's Gambit",
        "moves": ["e4", "e5", "f4"]
    },
    {
        "name": "Vienna Game",
        "moves": ["e4", "e5", "Nc3"]
    },
    {
        "name": "Sicilian Defense",
        "moves": ["e4", "c5"]
    },
    {
        "name": "French Defense",
        "moves": ["e4", "e6"]
    },
    {
        "name": "Caro-Kann Defense",
        "moves": ["e4", "c6"]
    },
    {
        "name": "Scandinavian Defense",
        "moves": ["e4", "d5"]
    },
    {
        "name": "Alekhine Defense",
        "moves": ["e4", "Nf6"]
    },
    {
        "name": "Pirc Defense",
        "moves": ["e4", "d6"]
    },
    {
        "name": "Queen's Gambit",
        "moves": ["d4", "d5", "c4"]
    },
    {
        "name": "Queen's Gambit Declined",
        "moves": ["d4", "d5", "c4", "e6"]
    },
    {
        "name": "Queen's Gambit Accepted",
        "moves": ["d4", "d5", "c4", "dxc4"]
    },
    {
        "name": "Slav Defense",
        "moves": ["d4", "d5", "c4", "c6"]
    },
    {
        "name": "King's Indian Defense",
        "moves": ["d4", "Nf6", "c4", "g6"]
    },
    {
        "name": "Nimzo-Indian Defense",
        "moves": ["d4", "Nf6", "c4", "e6", "Nc3", "Bb4"]
    },
    {
        "name": "London System",
        "moves": ["d4", "d5", "Nf3", "Nf6", "Bf4"]
    },
    {
        "name": "English Opening",
        "moves": ["c4"]
    },
    {
        "name": "Réti Opening",
        "moves": ["Nf3", "d5", "c4"]
    },
    {
        "name": "Trompowsky Attack",
        "moves": ["d4", "Nf6", "Bg5"]
    },
    {
        "name": "Danish Gambit",
        "moves": ["e4", "e5", "Nf3", "Nc6", "d4", "exd4", "c3"]
    }
]


# =========================================================
# CREATE A QUIZ POSITION
# =========================================================

def create_quiz():

    # Choose a random opening
    correct_opening = random.choice(OPENINGS)

    # Create a chess board
    board = chess.Board()

    # Play the opening moves
    for move_san in correct_opening["moves"]:
        move = board.parse_san(move_san)
        board.push(move)

    # -----------------------------------------------------
    # Create wrong answers
    # -----------------------------------------------------

    other_openings = [
        opening["name"]
        for opening in OPENINGS
        if opening["name"] != correct_opening["name"]
    ]

    wrong_answers = random.sample(other_openings, 3)

    choices = wrong_answers + [correct_opening["name"]]

    # Shuffle the choices
    random.shuffle(choices)

    # -----------------------------------------------------
    # Convert board to simple 8x8 array
    # -----------------------------------------------------

    board_data = []

    for rank in range(7, -1, -1):

        row = []

        for file in range(8):

            square = chess.square(file, rank)
            piece = board.piece_at(square)

            if piece:
                symbol = piece.symbol()
            else:
                symbol = ""

            row.append({
                "piece": symbol,
                "light": (file + rank) % 2 == 0
            })

        board_data.append(row)

    return {
        "opening": correct_opening["name"],
        "moves": correct_opening["moves"],
        "board": board_data,
        "choices": choices
    }


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    quiz = create_quiz()

    result = None
    selected_answer = None

    if request.method == "POST":

        selected_answer = request.form.get("answer")

        # The correct answer is sent with the form
        correct_answer = request.form.get("correct_answer")

        if selected_answer == correct_answer:
            result = "correct"
        else:
            result = "wrong"

        # Recreate the SAME board information
        opening = next(
            opening for opening in OPENINGS
            if opening["name"] == correct_answer
        )

        board = chess.Board()

        for move_san in opening["moves"]:
            move = board.parse_san(move_san)
            board.push(move)

        board_data = []

        for rank in range(7, -1, -1):

            row = []

            for file in range(8):

                square = chess.square(file, rank)
                piece = board.piece_at(square)

                if piece:
                    row.append(piece.symbol())
                else:
                    row.append("")

            board_data.append(row)

        quiz = {
            "opening": correct_answer,
            "moves": opening["moves"],
            "board": board_data,
            "choices": [
                request.form.get("choice1"),
                request.form.get("choice2"),
                request.form.get("choice3"),
                request.form.get("choice4")
            ]
        }

    return render_template(
        "index.html",
        quiz=quiz,
        result=result,
        selected_answer=selected_answer
    )


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)