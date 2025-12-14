from typing import List, Optional, Tuple
import math

Board = List[str]  # length 9, values: 'X', 'O', or ' '

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6)              # diagonals
]


def new_board() -> Board:
    return [' '] * 9


def print_board(b: Board) -> None:
    def c(i):
        return b[i] if b[i] != ' ' else str(i+1)
    print(f" {c(0)} | {c(1)} | {c(2)}")
    print("---+---+---")
    print(f" {c(3)} | {c(4)} | {c(5)}")
    print("---+---+---")
    print(f" {c(6)} | {c(7)} | {c(8)}")


def available_moves(b: Board) -> List[int]:
    return [i for i, v in enumerate(b) if v == ' ']


def winner(b: Board) -> Optional[str]:
    for a, c, d in WIN_LINES:
        if b[a] == b[c] == b[d] and b[a] != ' ':
            return b[a]
    return None


def is_terminal(b: Board) -> bool:
    return winner(b) is not None or all(cell != ' ' for cell in b)


# Minimax with alpha-beta pruning. Returns (score, move_index)
# Scores are from perspective of ai_player.

def minimax(b: Board, depth: int, alpha: int, beta: int, maximizing: bool, ai_player: str, human_player: str) -> Tuple[int, Optional[int]]:
    w = winner(b)
    if w == ai_player:
        return (10 - depth, None)  # prefer faster wins
    elif w == human_player:
        return (depth - 10, None)  # prefer slower losses
    elif all(cell != ' ' for cell in b):
        return (0, None)  # draw

    if maximizing:
        max_eval = -math.inf
        best_move = None
        for m in available_moves(b):
            b[m] = ai_player
            eval_score, _ = minimax(b, depth + 1, alpha, beta, False, ai_player, human_player)
            b[m] = ' '
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = m
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return (max_eval, best_move)
    else:
        min_eval = math.inf
        best_move = None
        for m in available_moves(b):
            b[m] = human_player
            eval_score, _ = minimax(b, depth + 1, alpha, beta, True, ai_player, human_player)
            b[m] = ' '
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = m
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return (min_eval, best_move)


def ai_move(b: Board, ai_player: str, human_player: str) -> int:
    score, move = minimax(b, 0, -math.inf, math.inf, True, ai_player, human_player)
    if move is None:
        # fallback (shouldn't normally happen)
        moves = available_moves(b)
        return moves[0]
    return move


def human_turn(b: Board, human_player: str) -> None:
    while True:
        try:
            raw = input(f"Your move ({human_player}). Enter position 1-9: ").strip()
            if raw.lower() in ('q', 'quit', 'exit'):
                print("Goodbye!")
                raise SystemExit
            pos = int(raw) - 1
            if pos < 0 or pos > 8:
                print("Invalid position. Choose 1-9.")
                continue
            if b[pos] != ' ':
                print("Cell already taken. Choose another.")
                continue
            b[pos] = human_player
            break
        except ValueError:
            print("Please enter a number 1-9 or 'q' to quit.")


def play_game() -> None:
    print("Welcome to Tic-Tac-Toe (Unbeatable AI)")
    b = new_board()

    # Let player choose symbol
    human_player = ''
    while human_player not in ('X', 'O'):
        choice = input("Choose your symbol (X goes first). Enter X or O: ").strip().upper()
        if choice in ('X', 'O'):
            human_player = choice
    ai_player = 'O' if human_player == 'X' else 'X'

    current = 'X'  # X always starts
    print("\nBoard positions: 1-9 as shown below")
    print_board(new_board())
    print()

    while True:
        print_board(b)
        if is_terminal(b):
            w = winner(b)
            if w is None:
                print("It's a draw!")
            elif w == human_player:
                print("You win! Congratulations!")
            else:
                print("AI wins. Better luck next time.")
            break

        if current == human_player:
            human_turn(b, human_player)
        else:
            print(f"AI ({ai_player}) is thinking...")
            m = ai_move(b, ai_player, human_player)
            b[m] = ai_player
            print(f"AI plays position {m+1}")

        # switch
        current = ai_player if current == human_player else human_player
        print()


if __name__ == '__main__':
    try:
        play_game()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
