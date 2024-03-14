import React, { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
	const [inputData, setInputData] = useState("");
	const [prediction, setPrediction] = useState(null);
	const [error, setError] = useState(null);

	const handleSubmit = async () => {
		try {
			const response = await axios.get("http://localhost:8000/predict");
			console.log(response);
			setPrediction(response.data.prediction);
			setError(null);
		} catch (error) {
			console.error(error);
			setError("Error fetching prediction");
		}
	};

	return (
		<div className="App">
			<input
				type="text"
				value={inputData}
				onChange={(e) => setInputData(e.target.value)}
			/>
			<button onClick={handleSubmit}>Predict</button>
			{prediction && <p>Prediction: {prediction}</p>}
			{error && <p style={{ color: "red" }}>{error}</p>}
		</div>
	);
};

export default App;
