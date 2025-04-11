# VolatilityHorizons
Automated generation of TradingView Pine Script overlays for option chain expected moves, combining fundamental data analysis with technical chart visualization
![Example Overlay](https://via.placeholder.com/800x400.png?text=Screenshot+Coming+Soon) *Example visualization placeholder*

## ✨ Features
- Multi-timeframe support (Daily/Weekly/Monthly)
- Automatic price synchronization via Yahoo Finance
- Customizable color schemes
- Dynamic ticker filtering
- CSV-based move configuration

## 🚀 Quick Start
```bash
# Clone repository
git clone https://github.com/YOURNAME/REPO_NAME.git

# Install dependencies
pip install -r requirements.txt

# Add your expected moves to CSV format:
# ticker,timeframe,expected_move
AAPL,daily,2.5
TSLA,weekly,15.3
```

## ⚙️ Configuration
1. Edit `expected_moves.csv`:
```csv
ticker,timeframe,expected_move
NVDA,weekly,25.4
SPY,monthly,8.2
```

2. Run generation script:
```bash
python main.py
```

3. Import `expected_moves.pine` to TradingView:
- Open Chart → Pine Editor → Add new script
- Copy/paste generated code
- Add to chart from 'Indicators' list

## 🎨 Customization
**Color Schemes:**
```python
# In main.py, modify the color_map:
color_map = {
    'daily': 'color.rgb(255, 0, 0)',    # Red
    'weekly': 'color.rgb(148, 0, 211)', # Purple
    'monthly': 'color.rgb(255, 165, 0)' # Orange
}
```

**Timeframe Support:**
Add new timeframes by including them in both CSV and color mapping.
