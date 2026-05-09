import PokemonCard from "./PokemonCard";

function PlayerBoard({ player, isOpponent, refreshGame }) {
    return (
        <div
            style={{
                marginBottom: "40px",
                border: "1px solid gray",
                padding: "20px",
            }}
        >
            <h2>{isOpponent ? "Opponent" : "You"}</h2>

            {/* ACTIVE */}
            <div style={{ marginBottom: "20px" }}>
                <h3>Active Pokémon</h3>

                <PokemonCard
                    pokemon={player.active}
                    isOpponent={isOpponent}
                    refreshGame={refreshGame}
                    playerId={isOpponent ? "p2" : "p1"}
                />
            </div>

            {/* BENCH */}
            <div>
                <h3>Bench</h3>

                <div style={{ display: "flex", gap: "10px" }}>
                    {player.bench.map((pokemon, i) => (
                        <PokemonCard
                            key={i}
                            pokemon={pokemon}
                            isOpponent={isOpponent}
                            refreshGame={refreshGame}
                            playerId={isOpponent ? "p2" : "p1"}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}

export default PlayerBoard;