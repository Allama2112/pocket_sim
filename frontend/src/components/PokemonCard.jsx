import axios from "axios";

function PokemonCard({ pokemon, isOpponent, refreshGame, playerId }) {
    if (!pokemon) return null;

    const card = pokemon.card;
    const energy = pokemon.energy || 0;

    const attack = async (attackIndex) => {
        if (isOpponent) return;

        try {
            await axios.post("http://localhost:8000/battle/attack", {
                player_id: playerId,
                attack_index: attackIndex,
            });

            refreshGame();
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div
            style={{
                border: "1px solid white",
                padding: "10px",
                marginBottom: "10px",
                background: "#2a2a2a",
                minWidth: "160px",
            }}
        >
            <h4>{card.name}</h4>

            <p>HP: {card.health}</p>
            <p>Damage: {pokemon.damage}</p>
            <p>Energy: {energy}</p>

            {/* ATTACKS ONLY FOR PLAYER */}
            {!isOpponent && card.attacks && (
                <div>
                    <h5>Attacks</h5>

                    {card.attacks.map((atk, i) => {
                        const cost = atk.cost?.length || 0;
                        const canUse = energy >= cost;

                        return (
                            <button
                                key={i}
                                onClick={() => attack(i)}
                                disabled={!canUse}
                                style={{
                                    display: "block",
                                    margin: "5px 0",
                                    padding: "5px",
                                    opacity: canUse ? 1 : 0.4,
                                    cursor: canUse ? "pointer" : "not-allowed",
                                }}
                            >
                                {atk.name} ({atk.damage}) — Cost: {cost}
                            </button>
                        );
                    })}
                </div>
            )}
        </div>
    );
}

export default PokemonCard;