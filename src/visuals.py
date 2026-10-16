
import calendar
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

# Consistent theme for all charts
BLUE = "#3B82F6"
ORANGE = "#F97316"
TEAL = "#14B8A6"


def money_format(value, _):
    if abs(value) >= 1000:
        return f"${value / 1000:,.0f}k"
    return f"${value:,.0f}"


def revenue_trend_fig(monthly_df):
    fig = Figure(figsize=(10, 4), layout="tight")
    ax = fig.subplots()

    ax.plot(
        monthly_df["month_start"],
        monthly_df["revenue"],
        color=BLUE,
        marker="o",
        linewidth=2.5
    )
    ax.fill_between(
        monthly_df["month_start"],
        monthly_df["revenue"],
        color=BLUE,
        alpha=0.12
    )

    ax.set_title("Monthly Revenue Trend", fontsize=14, pad=12)
    ax.set_xlabel("Month")
    ax.yaxis.set_major_formatter(FuncFormatter(money_format))
    ax.grid(axis="y", alpha=0.25)
    return fig


def top_products_fig(top_df):
    fig = Figure(figsize=(8, 4.5), layout="tight")
    ax = fig.subplots()

    bars = ax.barh(
        top_df["product"][::-1],
        top_df["revenue"][::-1],
        color=BLUE
    )

    ax.set_title("Top Products by Revenue", fontsize=14)
    ax.xaxis.set_major_formatter(FuncFormatter(money_format))
    ax.grid(axis="x", alpha=0.2)

    for bar in bars:
        ax.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f" ${bar.get_width():,.0f}",
            va="center",
            fontsize=8
        )

    return fig


def share_donut_fig(share_df, label_col, title):
    fig = Figure(figsize=(6, 4.5), layout="tight")
    ax = fig.subplots()

    ax.pie(
        share_df["revenue"],
        labels=share_df[label_col],
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"width": 0.42, "edgecolor": "white"}
    )

    ax.set_title(title, fontsize=14)
    return fig


def heatmap_fig(matrix):
    fig = Figure(figsize=(10, 4.5), layout="tight")
    ax = fig.subplots()

    image = ax.imshow(
        matrix.values,
        aspect="auto",
        cmap="Blues"
    )

    ax.set_xticks(
        range(12),
        [calendar.month_abbr[m] for m in range(1, 13)]
    )
    ax.set_yticks(range(len(matrix.index)), matrix.index)
    ax.set_title("Sales Activity: Weekday vs Month", fontsize=14)

    fig.colorbar(image, ax=ax, label="Revenue")
    return fig


def forecast_fig(series, forecast_df, model_name):
    fig = Figure(figsize=(10, 4.5), layout="tight")
    ax = fig.subplots()

    ax.plot(
        series.index,
        series.values,
        color=BLUE,
        linewidth=2.5,
        label="Actual Revenue"
    )

    ax.plot(
        forecast_df.index,
        forecast_df["forecast"],
        color=ORANGE,
        linestyle="--",
        marker="o",
        linewidth=2.5,
        label=f"Forecast ({model_name})"
    )

    ax.fill_between(
        forecast_df.index,
        forecast_df["lower"],
        forecast_df["upper"],
        color=ORANGE,
        alpha=0.18,
        label="95% Forecast Range"
    )

    ax.set_title("Future Sales Forecast", fontsize=14)
    ax.yaxis.set_major_formatter(FuncFormatter(money_format))
    ax.grid(axis="y", alpha=0.25)
    ax.legend()

    return fig
