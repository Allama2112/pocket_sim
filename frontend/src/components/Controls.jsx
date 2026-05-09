import axios from "axios";

function Controls({ refreshGame }) {

    const attack = async () => {
        await axios.post("http://localhost:8000/battle/attack", {
            player_id: "p1",
            attack_index: 0
        });

        refreshGame();
    };

    const endTurn = async () => {
        await axios.post("http://localhost:8000/battle/end-turn", {
            player_id: "p1"
        });

        refreshGame();
    };

    return (
        <div style={{ marginTop: "20px" }}>
            <button onClick={attack}>⚔️ Attack</button>
            <button onClick={endTurn}>➡️ End Turn</button>
        </div>
    );
}

export default Controls;