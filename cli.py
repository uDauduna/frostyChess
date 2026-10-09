"""Terminal chess interface.

Examples:
    python cli.py
    python cli.py --fen "8/8/8/8/8/8/4K3/4k2R w - - 0 1"
    python cli.py --random-games 100
    python cli.py -c
"""
import argparse
import random
from game.chess_game import ChessGame
from game.fen import square_name
import time

def print_board(game):
    print()
    for r,row in enumerate(game.board.pieces):
        cells=[]
        for p in row:
            cells.append("." if p is None else {"pawn":"P","knight":"N","bishop":"B","rook":"R","queen":"Q","king":"K"}[p.piece_type] if p.color=="white" else {"pawn":"p","knight":"n","bishop":"b","rook":"r","queen":"q","king":"k"}[p.piece_type])
        print(f"{8-r}  " + " ".join(cells))
    print("   a b c d e f g h")
    print(f"Turn: {game.turn} | FEN: {game.to_fen()}")
    print()

def interactive(fen=None):
    game=ChessGame.from_fen(fen) if fen else ChessGame()
    print("frostyChess CLI — enter UCI moves such as e2e4 or e7e8q.")
    print("Commands: fen, undo, moves, quit")
    while game.game_in_progress():
        print_board(game)
        command=input(f"{game.turn}> ").strip()
        if not command: 
            continue
        if command=="quit": 
            return
        if command=="fen": 
            print(game.to_fen())
            continue
        if command=="undo":
            print("Undone." if game.undo() else "Nothing to undo.")
            continue
        if command=="moves":
            print(" ".join(square_name(a)+square_name(b) for a,b in game.legal_move_pairs()))
            continue
        try:
            if not game.push_uci(command):
                print("Illegal move.")
        except ValueError as exc:
            print(exc)
    print_board(game)
    if game.is_checkmate():
        print(f"Checkmate — {game.opposite_color(game.turn)} wins.")
    else:
        print("Draw.")

def make_cpu_move(game):
    moves=game.legal_move_pairs()
    if moves: 
        start,end=random.choice(moves)
        promotion="queen" if game.board.get_piece(start).piece_type=="pawn" and end[0] in (0,7) else None
        game.make_move(start,end,promotion)
        if game.promotion_pending: 
            game.promote("queen")
    return

def make_player_move(game):
    command=""
    while not command: 
        command=input(f"{game.turn}> ").strip()
        if command=="quit": 
            return
        if command=="fen": 
            print(game.to_fen())
        if command=="undo":
            print("Undone." if game.undo() else "Nothing to undo.")
        if command=="moves":
            print(" ".join(square_name(a)+square_name(b) for a,b in game.legal_move_pairs()))
        try:
            if not game.push_uci(command):
                print("Illegal move.")
                command = None
        except ValueError as exc:
            print(exc)
            command=None
    return

def play_next_move(game,white = "player", black="cpu"):
    if white == "player":
        make_player_move(game)
        make_cpu_move(game)
        time.sleep(5)
    else:
        make_cpu_move(game)
        time.sleep(5)
        make_player_move(game)
    return
        
def play_against_cpu(fen=None):
    """
    Play a game against the cpu
    """
    print("frostyChess CLI — enter UCI moves such as e2e4 or e7e8q.")
    print("Commands: fen, undo, moves, quit")
    game=ChessGame.from_fen(fen) if fen else ChessGame()
    color = input("Enter Color. [W]hite or [B]lack ? ")
    if color == "B":
        white= "cpu"
        black = "player"
    else:
        white= "player"
        black="cpu"
    print("Start")
    while game.game_in_progress() and len(game.move_history)<400:
        print_board(game)
        play_next_move(game, white, black)
    print_board(game)
    if game.is_checkmate():
        print(f"Checkmate — {game.opposite_color(game.turn)} wins.")
    else:
        print("Draw.")

def random_self_play(games):
    counts={"white":0,"black":0,"draw":0}
    for _ in range(games):
        game=ChessGame()
        while game.game_in_progress() and len(game.move_history)<400:
            moves=game.legal_move_pairs()
            if not moves: 
                break
            start,end=random.choice(moves)
            promotion="queen" if game.board.get_piece(start).piece_type=="pawn" and end[0] in (0,7) else None
            game.make_move(start,end,promotion)
            if game.promotion_pending: game.promote("queen")
        if game.is_checkmate(): 
            counts[game.opposite_color(game.turn)]+=1
        else: 
            counts["draw"]+=1
    print(counts)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--fen")
    parser.add_argument("--random-games",type=int,default=0)
    parser.add_argument('-c', '--cpu', action='store_true') 
    args=parser.parse_args()
    if args.random_games: 
        random_self_play(args.random_games)
    elif args.cpu:
        play_against_cpu()
    else: 
        interactive(args.fen)
