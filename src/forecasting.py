
import numpy as np
import pandas as pd

from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# Number of previous months used for prediction
N_LAGS = 6


# 1. Create input features for prediction
def create_features(history, next_date):

    features = {}

    # Take revenue from the previous 6 months
    for i in range(1, N_LAGS + 1):
        features["lag_" + str(i)] = history.iloc[-i]

    # Calculate average revenue of the last 3 months
    features["roll_3"] = history.iloc[-3:].mean()

    # Get month number
    month = next_date.month

    # Represent the month using sine and cosine
    features["month_sin"] = np.sin(2 * np.pi * month / 12)
    features["month_cos"] = np.cos(2 * np.pi * month / 12)

    return features


# 2. Prepare training data
def build_data(monthly):

    X = []
    y = []

    # Start after the first 6 months
    for i in range(N_LAGS, len(monthly)):

        history = monthly.iloc[:i]
        next_date = monthly.index[i]

        features = create_features(history, next_date)

        X.append(features)
        y.append(monthly.iloc[i])

    # Convert data into a DataFrame
    X = pd.DataFrame(X)
    y = np.array(y)

    return X, y


# 3. Predict future months
def predict_future(model, history, periods=6):

    history = history.copy()
    predictions = []

    for i in range(periods):

        # Find the next month
        next_date = history.index[-1] + pd.offsets.MonthBegin(1)

        # Create input features
        features = create_features(history, next_date)

        # Convert features into DataFrame
        input_data = pd.DataFrame([features])

        # Predict revenue
        prediction = model.predict(input_data)[0]

        # Do not allow negative revenue
        prediction = max(0, float(prediction))

        predictions.append(prediction)

        # Add prediction to history for the next month
        history.loc[next_date] = prediction

    # Create a Series of predictions
    forecast_dates = history.index[-periods:]

    result = pd.Series(predictions, index=forecast_dates)

    return result


# 4. Calculate model errors
def calculate_errors(actual, predicted):

    mae = mean_absolute_error(actual, predicted)

    mse = mean_squared_error(actual, predicted)
    rmse = np.sqrt(mse)

    # Avoid division by zero in percentage error
    actual_values = np.array(actual)
    predicted_values = np.array(predicted)

    non_zero = actual_values != 0

    if non_zero.any():
        percentage_error = (
            np.abs(
                (actual_values[non_zero] - predicted_values[non_zero])
                / actual_values[non_zero]
            ) * 100
        )

        mape = percentage_error.mean()
    else:
        mape = 0

    result = {
        "mae": round(float(mae), 1),
        "rmse": round(float(rmse), 1),
        "mape_pct": round(float(mape), 1)
    }

    return result


# 5. Compare different prediction models
def evaluate_models(monthly, test_months=6):

    # Split data into training and testing
    train = monthly.iloc[:-test_months]
    test = monthly.iloc[-test_months:]

    forecasts = {}

    # Model 1: Average of the last 3 months
    average_revenue = train.iloc[-3:].mean()

    forecasts["Moving average (3)"] = pd.Series(
        average_revenue,
        index=test.index
    )

    # Model 2: Revenue from the same month last year
    seasonal = monthly.shift(12).iloc[-test_months:]

    if not seasonal.isna().any():

        forecasts["Seasonal naive"] = pd.Series(
            seasonal.values,
            index=test.index
        )

    # Prepare data for machine-learning models
    X, y = build_data(train)

    # Model 3: Ridge regression
    ridge_model = make_pipeline(
        StandardScaler(),
        Ridge(alpha=1.0)
    )

    ridge_model.fit(X, y)

    ridge_prediction = predict_future(
        ridge_model,
        train,
        test_months
    )

    forecasts["Ridge"] = ridge_prediction

    # Model 4: Random Forest
    forest_model = RandomForestRegressor(
        n_estimators=300,
        random_state=42
    )

    forest_model.fit(X, y)

    forest_prediction = predict_future(
        forest_model,
        train,
        test_months
    )

    forecasts["RandomForest"] = forest_prediction

    # Calculate errors for every model
    results = []

    for name in forecasts:

        prediction = forecasts[name]

        errors = calculate_errors(test, prediction)

        row = {
            "model": name,
            "mae": errors["mae"],
            "rmse": errors["rmse"],
            "mape_pct": errors["mape_pct"]
        }

        results.append(row)

    # Create comparison table
    table = pd.DataFrame(results)

    # Best model comes first
    table = table.sort_values("mae")

    table = table.reset_index(drop=True)

    return table, forecasts, test


# 6. Forecast future revenue
def forecast_future(monthly, periods=6, model_name=None,
                    test_months=6):

    # Compare models
    table, forecasts, test = evaluate_models(
        monthly,
        test_months
    )

    # Select the best machine-learning model
    if model_name is None:

        machine_learning_models = table[
            table["model"].isin(["Ridge", "RandomForest"])
        ]

        model_name = machine_learning_models.iloc[0]["model"]

    # Get the error of the selected model
    model_errors = table[table["model"] == model_name]

    rmse = model_errors.iloc[0]["rmse"]

    # Train the selected model using all available data
    X, y = build_data(monthly)

    if model_name == "Ridge":

        model = make_pipeline(
            StandardScaler(),
            Ridge(alpha=1.0)
        )

    elif model_name == "RandomForest":

        model = RandomForestRegressor(
            n_estimators=300,
            random_state=42
        )

    else:
        raise ValueError("Choose Ridge or RandomForest")

    model.fit(X, y)

    # Predict future revenue
    predicted = predict_future(
        model,
        monthly,
        periods
    )

    # Create forecast table
    result = pd.DataFrame({
        "forecast": predicted
    })

    # Calculate lower and upper estimates
    result["lower"] = (
        result["forecast"] - 1.96 * rmse
    ).clip(lower=0)

    result["upper"] = result["forecast"] + 1.96 * rmse

    return result, model_name
