from datetime import date, timedelta
import requests
from sklearn.linear_model import LinearRegression
import time


def fetch_weather_data(api_key="SFLVGCZGLDA62448TE2AKSHTJ", city_name="Kolkata"):
    """
    Fetches weather data from the Visual Crossing API for the specified city.

    Args:
        api_key (str, optional): The API key for Visual Crossing. Defaults to "SFLVGCZGLDA62448TE2AKSHTJ".
        city_name (str, optional): The name of the city to fetch data for. Defaults to "Kolkata".

    Returns:
        dict: The parsed JSON response containing weather data (if successful).
            None: If an error occurs or data is not found.
    """
    today = date.today()

    # Get the date for 7 days ago
    last_week = today - timedelta(days=30)
    print(last_week)

    # Format the dates as YYYY-MM-DD
    date_string = f"{last_week:%Y-%m-%d}/{today:%Y-%m-%d}"
    start_time = time.time()  # Record start time
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_name}/{date_string}?unitGroup=metric&key={api_key}&contentType=json"
    response = requests.get(url)

    if response.status_code == 200:
        end_time = time.time()  # Record end time
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.4f} seconds")
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


def prepare_data(data):
    """
    Extracts and prepares temperature data from the weather response.

    Args:
        data (dict): The parsed JSON response containing weather data.

    Returns:
        tuple: A tuple containing lists of days and corresponding temperatures (if sufficient data exists).
            None: If insufficient data is found.
    """

    days, temperatures = [], []
    if "days" in data:
        for day in data["days"]:
            if "temp" in day:
                days.append(data["days"].index(day))
                temperatures.append(day["temp"])
            elif "high" in day and "low" in day:
                average_temp = (day["high"] + day["low"]) / 2
                days.append(data["days"].index(day))
                temperatures.append(average_temp)

    if len(days) > 1:
        return days, temperatures
    else:
        return None


def create_or_load_model():
    """
    Creates a new linear regression model.

    Returns:
        sklearn.linear_model.LinearRegression: The linear regression model object.
    """

    model = LinearRegression()
    return model


def predict_temperature(api_key="SFLVGCZGLDA62448TE2AKSHTJ", city_name="Kolkata"):
    """
    Predicts tomorrow's temperature for the specified city and returns it as a dictionary.

    Args:
        api_key (str, optional): The API key for Visual Crossing. Defaults to "SFLVGCZGLDA62448TE2AKSHTJ".
        city_name (str, optional): The name of the city to fetch data for. Defaults to "Kolkata".

    Returns:
        dict: A dictionary containing the predicted temperature, execution time (if successful),
            or an error message.
    """

    weather_data = fetch_weather_data(api_key, city_name)
    if weather_data is None:
        return {"error": f"Error fetching weather data for {city_name}"}

    days, temperatures = prepare_data(weather_data)
    if days is None:
        return {
            "error": f"Insufficient temperature data to perform prediction for {city_name}"
        }

    model = create_or_load_model()

    start_time = time.time()
    print(f"Start time: {start_time:.4f} seconds")
    X = [[day] for day in days]  # Feature (day) as 2D array
    y = temperatures  # Target (temperature)
    print("X: ", len(X))
    print("y: ", len(y))
    model.fit(X, y)
    predicted_temp = model.predict([[days[-1] + 1]])[0]
    end_time = time.time()
    print(f"End time: {end_time:.4f} seconds")
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.4f} seconds")

    return {
        "predicted_temperature": f"{predicted_temp:.2f}°C",
        "execution_time": execution_time,
    }


if __name__ == "__main__":
    prediction = predict_temperature()
    print(prediction)  # Only used for testing in this context, remove in production
