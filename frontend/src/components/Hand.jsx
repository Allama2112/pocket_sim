import axios from "axios";

function Hand({ cards, refreshGame }) {

    const playCard = async (cardId) => {
        try {
            await axios.post(
                "http://localhost:8000/battle/play-card",
                {
                    player_id: "p1",
                    card_id: cardId
                }
            );

            refreshGame();

        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div>
            <h2>Your Hand</h2>

            <div
                style={{
                    display: "flex",
                    gap: "10px",
                    flexWrap: "wrap",
                }}
            >
                {cards.map((card, i) => (
                    <div
                        key={i}
                        onClick={() => playCard(card.id)}
                        style={{
                            border: "1px solid white",
                            padding: "10px",
                            width: "120px",
                            background: "#333",
                            cursor: "pointer"
                        }}
                    >
                        <strong>{card.name}</strong>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Hand;