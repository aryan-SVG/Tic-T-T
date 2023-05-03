import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

game_state = {
    "grid": {},
    "turn": "X",
    "status": "P",
}

def check_winner(grid):
    lines = [
        # Horizontal
        ["00", "01", "02"],
        ["10", "11", "12"],
        ["20", "21", "22"],
        # Vertical
        ["00", "10", "20"],
        ["01", "11", "21"],
        ["02", "12", "22"],
        # Diagonal
        ["00", "11", "22"],
        ["02", "11", "20"]
    ]

    for line in lines:
        if grid.get(line[0]) == grid.get(line[1]) == grid.get(line[2]) and grid[line[0]] in ["X", "O"]:
            return grid[line[0]]

    return None

def x(request):
    return render(request, 'tictactoe/x.html')

def o(request):
    return render(request, 'tictactoe/o.html')

@csrf_exempt
def game(request):
    global game_state
    if request.method == "POST":
        if "reset" in request.POST:
            game_state = {
                "grid": {},
                "turn": "X",
                "status": "P",
            }
        elif "move" in request.POST and "player" in request.POST:
            move = json.loads(request.POST["move"])
            player = request.POST["player"]
            if game_state["turn"] == player and f"{move[0]}{move[1]}" not in game_state["grid"]:
                game_state["grid"][f"{move[0]}{move[1]}"] = player
                winner = check_winner(game_state["grid"])
                if winner:
                    game_state["status"] = winner
                elif len(game_state["grid"]) == 9:
                    game_state["status"] = "D"
                else:
                    game_state["turn"] = "X" if player == "O" else "O"
    return JsonResponse(game_state)
