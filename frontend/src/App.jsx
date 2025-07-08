import { useEffect, useState } from "react";
import axios from "axios";

function App() {
	const [cards, setCards] = useState([]);

	useEffect(() => {
		axios.get("http://localhost:8000/cards")
			.then(res => setCards(res.data))
			.catch(err => console.error(err));
	}, []);

	return (
		<div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
			<h1>Card Browser</h1>
			<div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
				{cards.map(card => (
					<div key={card.id} style={{ border: "1px solid #ccc", padding: "1rem", width: "200px" }}>
						<h3>{card.name}</h3>
						<p>Type: {card.type}</p>
						{card.hp && <p>HP: {card.hp}</p>}
						{card.attacks?.map((atk, i) => (
							<div key={i}>
								<strong>{atk.name}</strong> - {atk.damage} damage
							</div>
						))}
						<p>{card.description}</p>
					</div>
				))}
			</div>
		</div>
	);
}

export default App;
