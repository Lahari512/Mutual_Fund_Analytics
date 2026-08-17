import json
from pathlib import Path

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Performance Analytics — Mutual Fund Analysis\n",
                "\n",
                "This notebook evaluates 40 mutual fund schemes using return, risk, performance, and benchmark metrics.\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Daily Returns\n",
                "\n",
                "Daily return is calculated as NAV(t) / NAV(t-1) − 1 for all 40 schemes. Extreme-return and missing-value checks were performed."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "\n",
                "daily = pd.read_csv('../data/processed/daily_returns.csv')\n",
                "daily.head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. CAGR Analysis\n",
                "\n",
                "CAGR was calculated for 1-year, 3-year and 5-year periods where sufficient history was available."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "cagr = pd.read_csv('../data/processed/cagr_analysis.csv')\n",
                "cagr.head(10)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Sharpe Ratio\n",
                "\n",
                "Sharpe ratio uses a 6.5% annual risk-free rate proxy and annualizes daily excess returns using √252."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "sharpe = pd.read_csv('../data/processed/sharpe_ratio.csv')\n",
                "sharpe.sort_values('sharpe_rank').head(10)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Sortino Ratio\n",
                "\n",
                "Sortino ratio measures risk-adjusted performance using downside deviation instead of total volatility."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "sortino = pd.read_csv('../data/processed/sortino_ratio.csv')\n",
                "sortino.sort_values('sortino_rank').head(10)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Alpha and Beta\n",
                "\n",
                "Fund returns were regressed against NIFTY 100 returns using OLS. Annualized alpha is the regression intercept multiplied by 252."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "alpha_beta = pd.read_csv('../data/processed/alpha_beta.csv')\n",
                "alpha_beta.head(10)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Maximum Drawdown\n",
                "\n",
                "Maximum drawdown measures the largest decline from a previous NAV peak."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "drawdown = pd.read_csv('../data/processed/max_drawdown.csv')\n",
                "drawdown.head(10)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7. Fund Scorecard\n",
                "\n",
                "The score combines 3-year return, Sharpe ratio, alpha, expense ratio and maximum drawdown using the specified weighted ranking methodology."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "scorecard = pd.read_csv('../data/processed/fund_scorecard.csv')\n",
                "scorecard.sort_values('overall_rank').head(10)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Top 5 Funds\n",
                "\n",
                "1. ICICI Pru Midcap Fund — Regular — Growth: 84.50\n",
                "2. Axis Midcap Fund — Regular — Growth: 80.75\n",
                "3. HDFC Mid-Cap Opportunities Fund — Regular — Growth: 80.50\n",
                "4. Mirae Asset Large Cap Fund — Regular — Growth: 80.00\n",
                "5. Kotak Flexicap Fund — Regular — Growth: 78.25"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 8. Benchmark Comparison and Tracking Error\n",
                "\n",
                "The top five funds were compared against NIFTY 50 and NIFTY 100 over the latest available three-year period. Tracking error is the annualized standard deviation of fund return minus benchmark return."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "tracking = pd.read_csv('../data/processed/tracking_error.csv')\n",
                "tracking"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Benchmark Comparison Chart\n",
                "\n",
                "The final benchmark comparison visualization is available at `dashboard/benchmark_comparison.png`."
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

output = Path("notebooks/Performance_Analytics.ipynb")
output.write_text(
    json.dumps(notebook, indent=2),
    encoding="utf-8"
)

print("Performance_Analytics.ipynb created successfully.")