import { useEffect, useState } from "react";
import axios from "axios";

import PlayerBoard from "./PlayerBoard";
import Hand from "./Hand";
import Controls from "./Controls";

function BattleBoard() {
    const [gameState, setGameState] = useState(null);

    const loadGame = async () => {
        try {
            const res = await axios.get("http://localhost:8000/debug/game");
            setGameState(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        loadGame();

        const interval = setInterval(() => {
            loadGame();
        }, 2000);

        return () => clearInterval(interval);
    }, []);

    if (!gameState) {
        return <div>Loading game...</div>;
    }

    return (
        <div
            style={{
                padding: "20px",
                background: "#1e1e1e",
                color: "white",
                minHeight: "100vh",
            }}
        >
            <h1>Pokemon TCG Pocket Simulator</h1>

            <h2>Current Turn: {gameState.current_player}</h2>

            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    marginBottom: "20px",
                }}
            >
                <div>P1 Points: {gameState.points?.p1 ?? 0}</div>
                <div>P2 Points: {gameState.points?.p2 ?? 0}</div>
            </div>

            {/* OPPONENT */}
            <PlayerBoard
                player={gameState.players.p2}
                isOpponent={true}
                refreshGame={loadGame}
            />

            {/* PLAYER */}
            <PlayerBoard
                player={gameState.players.p1}
                isOpponent={false}
                refreshGame={loadGame}
            />

            {/* HAND */}
            <Hand cards={gameState.players.p1.hand} />

            <Controls refreshGame={loadGame} />
        </div>
    );
}

export default BattleBoard;