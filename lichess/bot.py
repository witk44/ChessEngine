import os

# bot.py
import requests
import chess
import json
import time
from ChessEngine.Engine.engine import get_best_move
import sys

depth = 4
TOKEN = os.getenv("LICHESS_TOKEN")
# TOKEN = "lip_qBfqsEXWnrXE5QpeuMri"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}
API_BASE = "https://lichess.org"




def stream_events():
    url = f"{API_BASE}/api/stream/event"
    with requests.get(url, headers=HEADERS, stream=True) as res:
        for line in res.iter_lines():
            if not line:
                continue  
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                print("Invalid JSON line:", line)
                continue


def stream_game(game_id):
    url = f"{API_BASE}/api/bot/game/stream/{game_id}"
    with requests.get(url, headers=HEADERS, stream=True) as res:
        for line in res.iter_lines():
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                print("Invalid game stream line:", line)
                continue


def make_move(game_id, move):
    url = f"{API_BASE}/api/bot/game/{game_id}/move/{move}"
    response = requests.post(url, headers=HEADERS)
    if response.status_code != 200:
        print("Failed to move:", response.text)
        return 0
    return 1

def handle_game(game_id):
    board = chess.Board()
    print(f"Starting game {game_id}")
    for event in stream_game(game_id):
        if event["type"] == "gameFull":
            state = event["state"]
            for move in state.get("moves", "").split():
                
                board.push_uci(move)
            if board.turn == my_color and board.fullmove_number == 1 and board.is_game_over() is False:
                    best_move = get_best_move(board, depth)
                    print("Opening move:", best_move)
                    if not make_move(game_id, best_move.uci()):
                        break
        elif event["type"] == "gameState":
            moves = event.get("moves", "").split()
            board = chess.Board()
            for move in moves:
                board.push_uci(move)
            if board.is_game_over():
                    print("Game over, skipping move.")
                    break
            if board.turn == my_color:
                best_move = get_best_move(board, depth)
                print("My move:", best_move)
                if not make_move(game_id, best_move.uci()):
                    break
        elif event["type"] == "chatLine":
            continue  # ignore chats


def challenge_bot(opponent_name):
    print(f"Challenging {opponent_name}...")
    url = f"{API_BASE}/api/challenge/{opponent_name}"
    data = {
        "clock.limit": 600,
        "clock.increment": 0,
        "rated": True,
        "variant": "standard"
    }
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print("Challenge sent successfully.")
    else:
        print("Failed to challenge bot:", response.status_code, response.text)


def main():
    if(len(sys.argv)>1):
        opponent = sys.argv[1]
        challenge_bot(opponent)
    print("Bot started. Listening for challenges...")

    for event in stream_events():
        if "type" not in event:
            continue 
        if event["type"] == "challenge":
            challenge = event["challenge"]
            if challenge["variant"]["key"] != "standard":
                print("Declined non-standard challenge.")
                requests.post(f"{API_BASE}/api/challenge/{challenge['id']}/decline", headers=HEADERS)
                continue
            print("Accepting challenge:", challenge["id"])
            requests.post(f"{API_BASE}/api/challenge/{challenge['id']}/accept", headers=HEADERS)

        elif event["type"] == "gameStart":
            game_id = event["game"]["id"]
            global my_color
            my_color = event["game"]["color"] == "white"
            handle_game(game_id)

if __name__ == "__main__":
    main()




