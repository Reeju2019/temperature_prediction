from fastapi import FastAPI, Body, HTTPException

# Import the WeatherPredictor class from model.py
from Model import predict_temperature

app = FastAPI()

# CORS configuration (adjust origins and methods as needed)
# origins = ["http://localhost:3000"]

# app.add_middleware(
#     FastAPI.middleware.CorsMiddleware,
#     allow_origins=origins,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/predict")
async def get_temperature_prediction():
    """
    API endpoint to predict tomorrow's temperature for a given city.

    Args:
        city (str): The city name for which to make the prediction.

    Returns:
        dict: A dictionary containing the predicted temperature and execution time (if successful).
              str: An error message if an error occurs.
    """
    city = "Kolkata"
    try:
        # Make prediction and capture the response
        prediction = predict_temperature(city_name=city)

        # Extract predicted temperature and execution time (assuming specific format)
        predicted_temp, execution_time = (
            prediction["predicted_temperature"],
            prediction["execution_time"],
        )

        # Convert execution time to a float
        # execution_time = float(execution_time_str.split(": ")[-1])

        # Return prediction as a dictionary
        return {
            "predicted_temperature": predicted_temp,
            "execution_time": execution_time,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error making prediction: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    # Use default port 8000 or any preferred port
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
