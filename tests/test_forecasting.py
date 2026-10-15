
import sys
import os
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.forecasting import (
    create_features,
    build_data,
    predict_future,
    calculate_errors,
    evaluate_models,
    forecast_future
)


# Create sample monthly revenue data
dates = pd.date_range(
    start="2023-01-01",
    periods=36,
    freq="MS"
)

revenue = pd.Series(
    np.arange(1000, 37000, 1000),
    index=dates
)


# Test 1: Check feature creation
def test_create_features():

    features = create_features(revenue, pd.Timestamp("2026-01-01"))

    assert "lag_1" in features
    assert "lag_6" in features
    assert "roll_3" in features
    assert "month_sin" in features
    assert "month_cos" in features

    print("Test 1 passed: Features created successfully")


# Test 2: Check training data
def test_build_data():

    X, y = build_data(revenue)

    assert len(X) == len(revenue) - 6
    assert len(y) == len(revenue) - 6
    assert len(X) == len(y)

    print("Test 2 passed: Training data created successfully")


# Test 3: Check error calculation
def test_calculate_errors():

    actual = [100, 200, 300]
    predicted = [110, 190, 310]

    errors = calculate_errors(actual, predicted)

    assert errors["mae"] > 0
    assert errors["rmse"] > 0
    assert errors["mape_pct"] >= 0

    print("Test 3 passed: Errors calculated successfully")


# Test 4: Check future predictions
def test_predict_future():

    X, y = build_data(revenue)

    from sklearn.linear_model import Ridge
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    model = make_pipeline(
        StandardScaler(),
        Ridge()
    )

    model.fit(X, y)

    predictions = predict_future(model, revenue, periods=3)

    assert len(predictions) == 3
    assert (predictions >= 0).all()

    print("Test 4 passed: Future predictions created successfully")


# Test 5: Check model comparison
def test_evaluate_models():

    table, forecasts, actual = evaluate_models(
        revenue,
        test_months=6
    )

    assert len(table) > 0
    assert "model" in table.columns
    assert "mae" in table.columns
    assert "rmse" in table.columns

    print("Test 5 passed: Models compared successfully")


# Test 6: Check final forecast
def test_forecast_future():

    result, model_name = forecast_future(
        revenue,
        periods=6,
        test_months=6
    )

    assert len(result) == 6
    assert "forecast" in result.columns
    assert "lower" in result.columns
    assert "upper" in result.columns

    assert (result["forecast"] >= 0).all()
    assert (result["lower"] <= result["upper"]).all()

    print("Test 6 passed: Final forecast created successfully")


# Run all tests
if __name__ == "__main__":

    test_create_features()
    test_build_data()
    test_calculate_errors()
    test_predict_future()
    test_evaluate_models()
    test_forecast_future()

    print("\nAll tests passed successfully!")
