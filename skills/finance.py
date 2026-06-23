import requests

import time

from config import ALPHA_VANTAGE_API_KEY

# =========================
# CRYPTO (CoinGecko - free, no key)
# =========================

COIN_IDS = {
    "bitcoin": "bitcoin", "btc": "bitcoin",
    "ethereum": "ethereum", "eth": "ethereum",
    "solana": "solana", "sol": "solana",
    "dogecoin": "dogecoin", "doge": "dogecoin",
    "ripple": "ripple", "xrp": "ripple",
    "cardano": "cardano", "ada": "cardano",
    "polkadot": "polkadot", "dot": "polkadot",
    "litecoin": "litecoin", "ltc": "litecoin",
    "shiba inu": "shiba-inu", "shib": "shiba-inu",
    "binance coin": "binancecoin", "bnb": "binancecoin",
    "polygon": "matic-network", "matic": "matic-network",
    "avalanche": "avalanche-2", "avax": "avalanche-2",
}


def get_crypto_price(coin_name):
    try:
        coin_id = COIN_IDS.get(coin_name.lower().strip())
        if not coin_id:
            coin_id = coin_name.lower().strip().replace(" ", "-")

        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&tickers=false&community_data=false&developer_data=false"
        response = requests.get(url, timeout=10)
        data = response.json()

        if "error" in data or "market_data" not in data:
            return None

        market = data["market_data"]
        price = market["current_price"]["usd"]
        change_24h = market["price_change_percentage_24h"]
        change_7d = market.get("price_change_percentage_7d", 0)
        high_24h = market["high_24h"]["usd"]
        low_24h = market["low_24h"]["usd"]
        market_cap = market["market_cap"]["usd"]
        ath = market["ath"]["usd"]
        ath_change = market["ath_change_percentage"]["usd"]

        return {
            "name": data["name"],
            "symbol": data["symbol"].upper(),
            "price": price,
            "change_24h": change_24h,
            "change_7d": change_7d,
            "high_24h": high_24h,
            "low_24h": low_24h,
            "market_cap": market_cap,
            "ath": ath,
            "ath_change": ath_change,
        }
    except Exception as e:
        print(f"Crypto error: {e}")
        return None


def get_crypto_history(coin_name, days=14):
    try:
        coin_id = COIN_IDS.get(coin_name.lower().strip(), coin_name.lower().strip())
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
        response = requests.get(url, timeout=10)
        data = response.json()
        prices = [p[1] for p in data.get("prices", [])]
        return prices
    except Exception as e:
        print(f"Crypto history error: {e}")
        return []


# =========================
# TECHNICAL ANALYSIS
# =========================

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None

    deltas = [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)


def get_trend(prices):
    if len(prices) < 2:
        return "unknown"

    short_avg = sum(prices[-5:]) / min(5, len(prices))
    long_avg = sum(prices) / len(prices)

    if short_avg > long_avg * 1.02:
        return "strong uptrend"
    elif short_avg > long_avg:
        return "uptrend"
    elif short_avg < long_avg * 0.98:
        return "strong downtrend"
    elif short_avg < long_avg:
        return "downtrend"
    else:
        return "sideways"


def get_rsi_signal(rsi):
    if rsi is None:
        return "insufficient data"
    if rsi > 70:
        return "overbought (potential pullback)"
    elif rsi < 30:
        return "oversold (potential bounce)"
    else:
        return "neutral zone"


# =========================
# STOCKS (Alpha Vantage)
# =========================

STOCK_SYMBOLS = {
    "apple": "AAPL", "tesla": "TSLA", "microsoft": "MSFT",
    "google": "GOOGL", "amazon": "AMZN", "meta": "META",
    "nvidia": "NVDA", "netflix": "NFLX",
    "reliance": "RELIANCE.BSE", "tcs": "TCS.BSE",
    "infosys": "INFY.BSE", "hdfc": "HDFCBANK.BSE",
    "tata motors": "TATAMOTORS.BSE", "wipro": "WIPRO.BSE",
    "icici": "ICICIBANK.BSE", "sbi": "SBIN.BSE",
}


def get_stock_price(stock_name):
    try:
        symbol = STOCK_SYMBOLS.get(stock_name.lower().strip(), stock_name.upper())

        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()

        quote = data.get("Global Quote", {})
        if not quote or "05. price" not in quote:
            return None

        return {
            "symbol": quote.get("01. symbol"),
            "price": float(quote.get("05. price", 0)),
            "change": float(quote.get("09. change", 0)),
            "change_percent": quote.get("10. change percent", "0%").replace("%", ""),
            "high": float(quote.get("03. high", 0)),
            "low": float(quote.get("04. low", 0)),
            "volume": quote.get("06. volume"),
            "prev_close": float(quote.get("08. previous close", 0)),
        }
    except Exception as e:
        print(f"Stock error: {e}")
        return None


def get_stock_history(stock_name, days=14):
    try:
        symbol = STOCK_SYMBOLS.get(stock_name.lower().strip(), stock_name.upper())
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()

        time_series = data.get("Time Series (Daily)", {})
        if not time_series:
            return []

        dates = sorted(time_series.keys(), reverse=True)[:days]
        prices = [float(time_series[d]["4. close"]) for d in reversed(dates)]
        return prices
    except Exception as e:
        print(f"Stock history error: {e}")
        return []


# =========================
# FORMATTED REPORTS
# =========================

def format_crypto_report(coin_name):
    data = get_crypto_price(coin_name)
    if not data:
        return f"Couldn't find data for {coin_name}! Try saying the full name like 'bitcoin' or 'ethereum'."

    history = get_crypto_history(coin_name, days=14)
    rsi = calculate_rsi(history) if history else None
    trend = get_trend(history) if history else "unknown"
    rsi_signal = get_rsi_signal(rsi)

    change_word = "up" if data["change_24h"] > 0 else "down"
    change_emoji = "📈" if data["change_24h"] > 0 else "📉"

    report = f"""{data['name']} ({data['symbol']}) is at ${data['price']:,.2f}, {change_word} {abs(data['change_24h']):.2f}% in the last 24 hours {change_emoji}.
Over the past week it's {'up' if data['change_7d'] > 0 else 'down'} {abs(data['change_7d']):.2f}%.
24h range: ${data['low_24h']:,.2f} to ${data['high_24h']:,.2f}.
It's currently {abs(data['ath_change']):.1f}% below its all-time high of ${data['ath']:,.2f}.
Technical outlook: price is in a {trend}, with RSI at {rsi if rsi else 'N/A'} which is {rsi_signal}."""

    return report


def format_stock_report(stock_name):
    data = get_stock_price(stock_name)
    if not data:
        return f"Couldn't find data for {stock_name}! Try the company name or stock symbol."

    history = get_stock_history(stock_name, days=14)
    rsi = calculate_rsi(history) if history else None
    trend = get_trend(history) if history else "unknown"
    rsi_signal = get_rsi_signal(rsi)

    change_word = "up" if data["change"] > 0 else "down"
    change_emoji = "📈" if data["change"] > 0 else "📉"

    report = f"""{data['symbol']} is trading at ${data['price']:,.2f}, {change_word} {abs(float(data['change_percent'])):.2f}% today {change_emoji}.
Today's range: ${data['low']:,.2f} to ${data['high']:,.2f}, previous close was ${data['prev_close']:,.2f}.
Technical outlook: price is in a {trend}, with RSI at {rsi if rsi else 'N/A'} which is {rsi_signal}."""

    return report


def get_market_overview():
    try:
        url = "https://api.coingecko.com/api/v3/global"
        response = requests.get(url, timeout=10)
        data = response.json()["data"]

        total_cap = data["total_market_cap"]["usd"]
        cap_change = data["market_cap_change_percentage_24h_usd"]
        btc_dominance = data["market_cap_percentage"]["btc"]

        return f"""Total crypto market is worth ${total_cap / 1e12:.2f} trillion, {'up' if cap_change > 0 else 'down'} {abs(cap_change):.2f}% today.
Bitcoin dominance is at {btc_dominance:.1f}% of the total market."""
    except Exception as e:
        return "Couldn't fetch market overview right now!"


import requests

import time
from config import ALPHA_VANTAGE_API_KEY

# =========================
# CRYPTO (CoinGecko - free, no key)
# =========================

COIN_IDS = {
    "bitcoin": "bitcoin", "btc": "bitcoin",
    "ethereum": "ethereum", "eth": "ethereum",
    "solana": "solana", "sol": "solana",
    "dogecoin": "dogecoin", "doge": "dogecoin",
    "ripple": "ripple", "xrp": "ripple",
    "cardano": "cardano", "ada": "cardano",
    "polkadot": "polkadot", "dot": "polkadot",
    "litecoin": "litecoin", "ltc": "litecoin",
    "shiba inu": "shiba-inu", "shib": "shiba-inu",
    "binance coin": "binancecoin", "bnb": "binancecoin",
    "polygon": "matic-network", "matic": "matic-network",
    "avalanche": "avalanche-2", "avax": "avalanche-2",
}


def get_crypto_price(coin_name):
    try:
        coin_id = COIN_IDS.get(coin_name.lower().strip())
        if not coin_id:
            coin_id = coin_name.lower().strip().replace(" ", "-")

        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&tickers=false&community_data=false&developer_data=false"
        response = requests.get(url, timeout=10)
        data = response.json()

        if "error" in data or "market_data" not in data:
            return None

        market = data["market_data"]
        price = market["current_price"]["usd"]
        change_24h = market["price_change_percentage_24h"]
        change_7d = market.get("price_change_percentage_7d", 0)
        high_24h = market["high_24h"]["usd"]
        low_24h = market["low_24h"]["usd"]
        market_cap = market["market_cap"]["usd"]
        ath = market["ath"]["usd"]
        ath_change = market["ath_change_percentage"]["usd"]

        return {
            "name": data["name"],
            "symbol": data["symbol"].upper(),
            "price": price,
            "change_24h": change_24h,
            "change_7d": change_7d,
            "high_24h": high_24h,
            "low_24h": low_24h,
            "market_cap": market_cap,
            "ath": ath,
            "ath_change": ath_change,
        }
    except Exception as e:
        print(f"Crypto error: {e}")
        return None


def get_crypto_history(coin_name, days=14):
    try:
        coin_id = COIN_IDS.get(coin_name.lower().strip(), coin_name.lower().strip())
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
        response = requests.get(url, timeout=10)
        data = response.json()
        prices = [p[1] for p in data.get("prices", [])]
        return prices
    except Exception as e:
        print(f"Crypto history error: {e}")
        return []


# =========================
# TECHNICAL ANALYSIS
# =========================
def calculate_rsi(prices, period=14):
    if len(prices) < 2:
        return None

    actual_period = min(period, len(prices) - 1)

    deltas = [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]

    avg_gain = sum(gains[-actual_period:]) / actual_period
    avg_loss = sum(losses[-actual_period:]) / actual_period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

def get_trend(prices):
    if len(prices) < 2:
        return "unknown"

    short_avg = sum(prices[-5:]) / min(5, len(prices))
    long_avg = sum(prices) / len(prices)

    if short_avg > long_avg * 1.02:
        return "strong uptrend"
    elif short_avg > long_avg:
        return "uptrend"
    elif short_avg < long_avg * 0.98:
        return "strong downtrend"
    elif short_avg < long_avg:
        return "downtrend"
    else:
        return "sideways"


def get_rsi_signal(rsi):
    if rsi is None:
        return "insufficient data"
    if rsi > 70:
        return "overbought (potential pullback)"
    elif rsi < 30:
        return "oversold (potential bounce)"
    else:
        return "neutral zone"


# =========================
# STOCKS (Alpha Vantage)
# =========================

STOCK_SYMBOLS = {
    "apple": "AAPL", "tesla": "TSLA", "microsoft": "MSFT",
    "google": "GOOGL", "amazon": "AMZN", "meta": "META",
    "nvidia": "NVDA", "netflix": "NFLX",
    "reliance": "RELIANCE.BSE", "tcs": "TCS.BSE",
    "infosys": "INFY.BSE", "hdfc": "HDFCBANK.BSE",
    "tata motors": "TATAMOTORS.BSE", "wipro": "WIPRO.BSE",
    "icici": "ICICIBANK.BSE", "sbi": "SBIN.BSE",
}


def get_stock_price(stock_name):
    try:
        symbol = STOCK_SYMBOLS.get(stock_name.lower().strip(), stock_name.upper())

        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()

        quote = data.get("Global Quote", {})
        if not quote or "05. price" not in quote:
            return None

        return {
            "symbol": quote.get("01. symbol"),
            "price": float(quote.get("05. price", 0)),
            "change": float(quote.get("09. change", 0)),
            "change_percent": quote.get("10. change percent", "0%").replace("%", ""),
            "high": float(quote.get("03. high", 0)),
            "low": float(quote.get("04. low", 0)),
            "volume": quote.get("06. volume"),
            "prev_close": float(quote.get("08. previous close", 0)),
        }
    except Exception as e:
        print(f"Stock error: {e}")
        return None


def get_stock_history(stock_name, days=14):
    try:
        symbol = STOCK_SYMBOLS.get(stock_name.lower().strip(), stock_name.upper())
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()

        time_series = data.get("Time Series (Daily)", {})
        if not time_series:
            return []

        dates = sorted(time_series.keys(), reverse=True)[:days]
        prices = [float(time_series[d]["4. close"]) for d in reversed(dates)]
        return prices
    except Exception as e:
        print(f"Stock history error: {e}")
        return []


# =========================
# FORMATTED REPORTS
# =========================

def format_crypto_report(coin_name):
    data = get_crypto_price(coin_name)
    if not data:
        return f"Couldn't find data for {coin_name}! Try saying the full name like 'bitcoin' or 'ethereum'."

    history = get_crypto_history(coin_name, days=14)
    rsi = calculate_rsi(history) if history else None
    trend = get_trend(history) if history else "unknown"
    rsi_signal = get_rsi_signal(rsi)

    change_word = "up" if data["change_24h"] > 0 else "down"
    change_emoji = "📈" if data["change_24h"] > 0 else "📉"

    report = f"""{data['name']} ({data['symbol']}) is at ${data['price']:,.2f}, {change_word} {abs(data['change_24h']):.2f}% in the last 24 hours {change_emoji}.
Over the past week it's {'up' if data['change_7d'] > 0 else 'down'} {abs(data['change_7d']):.2f}%.
24h range: ${data['low_24h']:,.2f} to ${data['high_24h']:,.2f}.
It's currently {abs(data['ath_change']):.1f}% below its all-time high of ${data['ath']:,.2f}.
Technical outlook: price is in a {trend}, with RSI at {rsi if rsi else 'N/A'} which is {rsi_signal}."""

    return report


def format_stock_report(stock_name):
    data = get_stock_price(stock_name)
    if not data:
        return f"Couldn't find data for {stock_name}! Try the company name or stock symbol."

    history = get_stock_history(stock_name, days=14)
    rsi = calculate_rsi(history) if history else None
    trend = get_trend(history) if history else "unknown"
    rsi_signal = get_rsi_signal(rsi)

    change_word = "up" if data["change"] > 0 else "down"
    change_emoji = "📈" if data["change"] > 0 else "📉"

    report = f"""{data['symbol']} is trading at ${data['price']:,.2f}, {change_word} {abs(float(data['change_percent'])):.2f}% today {change_emoji}.
Today's range: ${data['low']:,.2f} to ${data['high']:,.2f}, previous close was ${data['prev_close']:,.2f}.
Technical outlook: price is in a {trend}, with RSI at {rsi if rsi else 'N/A'} which is {rsi_signal}."""

    return report


def get_market_overview():
    try:
        url = "https://api.coingecko.com/api/v3/global"
        response = requests.get(url, timeout=10)
        data = response.json()["data"]

        total_cap = data["total_market_cap"]["usd"]
        cap_change = data["market_cap_change_percentage_24h_usd"]
        btc_dominance = data["market_cap_percentage"]["btc"]

        return f"""Total crypto market is worth ${total_cap / 1e12:.2f} trillion, {'up' if cap_change > 0 else 'down'} {abs(cap_change):.2f}% today.
Bitcoin dominance is at {btc_dominance:.1f}% of the total market."""
    except Exception as e:
        return "Couldn't fetch market overview right now!"