
import pandas as pd
from matplotlib.figure import Figure

from src import visuals


def test_revenue_chart():
    data = pd.DataFrame({
        "month_start": pd.date_range(
            "2024-01-01", periods=3, freq="MS"
        ),
        "revenue": [1000, 2000, 3000]
    })

    assert isinstance(visuals.revenue_trend_fig(data), Figure)


def test_top_products_chart():
    data = pd.DataFrame({
        "product": ["Laptop", "Phone"],
        "revenue": [5000, 3000]
    })

    assert isinstance(visuals.top_products_fig(data), Figure)


def test_donut_chart():
    data = pd.DataFrame({
        "region": ["North", "South"],
        "revenue": [6000, 4000]
    })

    fig = visuals.share_donut_fig(
        data, "region", "Regional Sales"
    )
    assert isinstance(fig, Figure)


def test_heatmap_chart():
    matrix = pd.DataFrame(
        [[100] * 12 for _ in range(7)],
        index=[
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"
        ],
        columns=range(1, 13)
    )

    assert isinstance(visuals.heatmap_fig(matrix), Figure)


def test_forecast_chart():
    history = pd.Series(
        [1000, 1200, 1400],
        index=pd.date_range("2024-01-01", periods=3, freq="MS")
    )

    forecast = pd.DataFrame(
        {
            "forecast": [1500, 1600],
            "lower": [1300, 1400],
            "upper": [1700, 1800]
        },
        index=pd.date_range("2024-04-01", periods=2, freq="MS")
    )

    fig = visuals.forecast_fig(history, forecast, "Test model")
    assert isinstance(fig, Figure)
