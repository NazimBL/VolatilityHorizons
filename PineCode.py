import pandas as pd
import yfinance as yf

# Load your expected moves CSV
df = pd.read_csv("expected_moves.csv")

# Get live prices for each unique ticker
base_prices = {}
for ticker in df['ticker'].unique():
    try:
        base_prices[ticker] = yf.Ticker(ticker).fast_info['last_price']
    except:
        base_prices[ticker] = None

# Start building the Pine Script
pine_lines = [
    "//@version=5",
    'indicator("Expected Moves Overlay (Auto)", overlay=true)',
    ""
]

# Define color map for timeframes
color_map = {'daily': 'color.red', 'weekly': 'color.purple', 'monthly': 'color.orange'}

# Generate dynamic plot() lines
for idx, row in df.iterrows():
    ticker = row['ticker'].upper()
    timeframe = row['timeframe']
    move = row['expected_move']
    price = base_prices.get(ticker)

    if pd.isna(move) or price is None:
        continue

    upper = round(price + move, 2)
    lower = round(price - move, 2)
    color = color_map.get(timeframe, 'color.gray')
    label = f"{ticker}_{timeframe}"

    # Use conditional ternary operator for syminfo.ticker match
    pine_lines.append(f'plot(syminfo.ticker == "{ticker}" ? {upper} : na, title="{label}_upper", color={color}, linewidth=1)')
    pine_lines.append(f'plot(syminfo.ticker == "{ticker}" ? {lower} : na, title="{label}_lower", color={color}, linewidth=1)')
    pine_lines.append("")

# Save Pine Script to file
pine_script = "\n".join(pine_lines)
with open("expected_moves.pine", "w") as f:
    f.write(pine_script)

print("✅ Pine Script saved to expected_moves.pine")
