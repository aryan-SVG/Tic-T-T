$(document).ready(function() {
    let player = document.title.includes("X") ? "X" : "O";
    let myTurn = player === "X";
    let gameStateUrl = "/game/";

    function updateBoard(gameState) {
        for (let cell in gameState.grid) {
            let row = cell[1];
            let col = cell[2];
            $(`td[data-row="${row}"][data-col="${col}"]`).text(gameState.grid[cell]);
        }
    }

    function checkGameState() {
        $.getJSON(gameStateUrl, function(gameState) {
            updateBoard(gameState);
            if (gameState.status !== "P") {
                $("#game-message").text(`${gameState.status} wins!`).show();
            } else {
                myTurn = gameState.turn === player;
            }
        });
    }

    $("#game-board").on("click", "td", function() {
        if (!myTurn) return;
        let row = $(this).data("row");
        let col = $(this).data("col");
        $.post(gameStateUrl, { "move": [row, col], "player": player }, function(gameState) {
            updateBoard(gameState);
            if (gameState.status !== "P") {
                $("#game-message").text(`${gameState.status} wins!`).show();
            } else {
                myTurn = false;
            }
        }, "json");
    });

    $("#game-message").on("click", function() {
        $.post(gameStateUrl, { "reset": true }, function() {
            $("td").text("");
            $("#game-message").hide();
            myTurn = player === "X";
        });
    });

    setInterval(checkGameState, 1000);
});
