import yfinance as yf
from datetime import datetime
import numpy as np

# ETFs ( 0DTEs)
daily_expiry_etfs = ['SPY', 'QQQ', 'IWM', 'TLT', 'DIA']

# custom ticker list
ticker_list = ['SPY', 'AAPL', 'QQQ', 'MSFT', 'TSLA', 'TLT']

def get_expected_move_with_iv(ticker):
    stock = yf.Ticker(ticker)
    expirations = stock.options
    results = {'ticker': ticker}

    # Get real-time price
    try:
        current_price = stock.fast_info['last_price']
    except:
        current_price = stock.history(period="1d")['Close'][-1]

    today = datetime.today().date()

    if ticker.upper() in daily_expiry_etfs:
        if expirations and datetime.strptime(expirations[0], "%Y-%m-%d").date() == today:
            exp_date = expirations[0]
            results['daily'] = compute_expected_move_and_iv(stock, exp_date, current_price)

    weekly_exp = None
    monthly_exp = None
    for exp in expirations:
        exp_date = datetime.strptime(exp, "%Y-%m-%d").date()
        if exp_date > today:
            if weekly_exp is None and exp_date.weekday() == 4:
                weekly_exp = exp
            if monthly_exp is None and 14 < exp_date.day < 22 and exp_date.weekday() == 4:
                monthly_exp = exp
        if weekly_exp and monthly_exp:
            break

    if weekly_exp:
        results['weekly'] = compute_expected_move_and_iv(stock, weekly_exp, current_price)
    if monthly_exp:
        results['monthly'] = compute_expected_move_and_iv(stock, monthly_exp, current_price)

    return results

def compute_expected_move_and_iv(stock, expiration_date, current_price):
    try:
        opt_chain = stock.option_chain(expiration_date)
        calls = opt_chain.calls
        puts = opt_chain.puts

        calls['diff'] = abs(calls['strike'] - current_price)
        atm_call = calls.sort_values('diff').iloc[0]

        puts['diff'] = abs(puts['strike'] - current_price)
        atm_put = puts.sort_values('diff').iloc[0]

        expected_move = atm_call['lastPrice'] + atm_put['lastPrice']
        iv = np.mean([atm_call['impliedVolatility'], atm_put['impliedVolatility']]) * 100  # To percent

        return {'expected_move': round(expected_move, 2), 'iv': round(iv, 2)}
    except Exception as e:
        return {'error': str(e)}

# Run and display
if __name__ == "__main__":
    results = []
    for ticker in ticker_list:
        try:
            result = get_expected_move_with_iv(ticker)
            results.append(result)
        except Exception as e:
            results.append({'ticker': ticker, 'error': str(e)})

    for r in results:
        print(r)

import pandas as pd

# Flatten the results for CSV output
flattened = []
for r in results:
    base = {'ticker': r['ticker']}
    for timeframe in ['daily', 'weekly', 'monthly']:
        if timeframe in r:
            base_time = base.copy()
            base_time['timeframe'] = timeframe
            base_time['expected_move'] = r[timeframe].get('expected_move')
            base_time['iv'] = r[timeframe].get('iv')
            flattened.append(base_time)


df = pd.DataFrame(flattened)
df.to_csv("expected_moves.csv", index=False)
print("Saved expected moves to expected_moves.csv")

"""
import matplotlib.pyplot as plt

# Optional: sort for better layout
df = df.sort_values(by='ticker')

plt.figure(figsize=(12, 6))
unique_tickers = df['ticker'].unique()
yticks = []
yticklabels = []

color_map = {'daily': 'red', 'weekly': 'purple', 'monthly': 'orange'}

for i, ticker in enumerate(unique_tickers):
    sub_df = df[df['ticker'] == ticker]
    for _, row in sub_df.iterrows():
        base_price = yf.Ticker(row['ticker']).fast_info['last_price']
        lower = base_price - row['expected_move']
        upper = base_price + row['expected_move']
        color = color_map.get(row['timeframe'], 'black')
        plt.hlines(y=i, xmin=lower, xmax=upper, colors=color, linewidth=2, label=row['timeframe'])

    yticks.append(i)
    yticklabels.append(ticker)

plt.yticks(yticks, yticklabels)
plt.xlabel("Price Range")
plt.title("Expected Move Ranges by Ticker and Timeframe")

# Only show each legend label once
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

plt.grid(True)
plt.tight_layout()
plt.show()

"""
