---
name: toobit-cex-market
description: "This skill should be used when the user asks for 'price of BTC', 'ETH ticker', 'show me the orderbook', 'market depth', 'BTC candles', 'OHLCV chart data', 'funding rate', 'open interest', 'mark price', 'index price', 'recent trades', 'book ticker', 'best bid ask', 'long short ratio', 'contract ticker', 'insurance fund', 'risk limits', 'exchange info', 'list instruments', 'what symbols are available', 'klines', 'server time', or any request to query public market data on Toobit CEX. All commands are read-only and do NOT require API credentials. Do NOT use for account balance/positions (use toobit-cex-portfolio), placing/cancelling orders (use toobit-cex-trade)."
license: MIT
metadata:
  author: toobit
  version: "1.0.0"
  homepage: "https://www.toobit.com"
  agent:
    requires:
      bins: ["toobit"]
    install:
      - id: npm
        kind: node
        package: "toobit-trade-cli"
        bins: ["toobit"]
        label: "Install toobit CLI (npm)"
---

# Toobit CEX Market Data CLI

Public market data for Toobit exchange: prices, order books, candles, funding rates, open interest, mark price, index price, long/short ratio, and instrument info. All commands are **read-only** and do **not require API credentials**.

## Prerequisites

1. Install `toobit` CLI:
   ```bash
   npm install -g toobit-trade-cli
   ```
2. No credentials needed for market data — all commands are public.
3. Verify install:
   ```bash
   toobit market ticker --symbol BTCUSDT
   ```

## Skill Routing

- For market data (prices, charts, depth, funding rates) → use `toobit-cex-market` (this skill)
- For account balance, sub-accounts, deposits, withdrawals → use `toobit-cex-portfolio`
- For spot/futures orders, leverage, margin, flash close → use `toobit-cex-trade`

## Quickstart

```bash
# Current BTC spot price
toobit market ticker --symbol BTCUSDT

# BTC 24h ticker (high/low/vol/change)
toobit market ticker-24hr --symbol BTCUSDT

# BTC spot order book (default depth)
toobit market depth --symbol BTCUSDT --limit 20

# BTC hourly klines (last 20)
toobit market klines --symbol BTCUSDT --interval 1h --limit 20

# BTC futures current funding rate
toobit market funding-rate --symbol BTC-SWAP-USDT

# BTC futures funding rate history
toobit market funding-rate-history --symbol BTC-SWAP-USDT --limit 20

# BTC futures open interest
toobit market open-interest --symbol BTC-SWAP-USDT

# BTC futures mark price
toobit market mark-price --symbol BTC-SWAP-USDT

# Exchange info (list all tradeable symbols)
toobit market info

# Server time
toobit market time
```

## Command Index

| # | Command | Type | Description |
|---|---|---|---|
| 1 | `toobit market time` | READ | Server time |
| 2 | `toobit market info` | READ | Exchange info: all tradeable symbols and rules |
| 3 | `toobit market ticker --symbol <sym>` | READ | Last price for a single symbol |
| 4 | `toobit market ticker-24hr --symbol <sym>` | READ | 24h ticker: open, high, low, close, vol, change |
| 5 | `toobit market depth --symbol <sym> [--limit <n>]` | READ | Order book depth (asks + bids) |
| 6 | `toobit market trades --symbol <sym> [--limit <n>]` | READ | Recent public trades |
| 7 | `toobit market klines --symbol <sym> [--interval <i>] [--limit <n>]` | READ | OHLCV candlestick data |
| 8 | `toobit market book-ticker --symbol <sym>` | READ | Best bid/ask price and quantity |
| 9 | `toobit market mark-price --symbol <sym>` | READ | Mark price for futures contracts |
| 10 | `toobit market funding-rate --symbol <sym>` | READ | Current funding rate for futures |
| 11 | `toobit market funding-rate-history --symbol <sym> [--limit <n>]` | READ | Historical funding rates |
| 12 | `toobit market open-interest --symbol <sym>` | READ | Open interest for futures |
| 13 | `toobit market index --symbol <sym>` | READ | Index price for futures |
| 14 | `toobit market contract-ticker --symbol <sym>` | READ | Futures 24h ticker stats |
| 15 | `toobit market contract-ticker-price --symbol <sym>` | READ | Futures last price |
| 16 | `toobit market long-short-ratio --symbol <sym> [--period <p>]` | READ | Long/short account ratio |
| 17 | `toobit market insurance-fund --symbol <sym>` | READ | Insurance fund balance |
| 18 | `toobit market risk-limits --symbol <sym>` | READ | Risk limits and leverage tiers |

## Cross-Skill Workflows

### Check price before placing an order
> User: "What's the current BTC price? I want to place a limit buy."

```
1. toobit-cex-market    toobit market ticker --symbol BTCUSDT          → check last price
2. toobit-cex-market    toobit market depth --symbol BTCUSDT --limit 5 → check bid/ask spread
3. toobit-cex-portfolio toobit account info                            → confirm available USDT
        ↓ user decides price
4. toobit-cex-trade     toobit spot place --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price <px>
```

### Check funding rate before holding a futures position
> User: "Is the BTC futures funding rate high right now?"

```
1. toobit-cex-market    toobit market funding-rate --symbol BTC-SWAP-USDT           → current rate
2. toobit-cex-market    toobit market funding-rate-history --symbol BTC-SWAP-USDT --limit 20 → trend
        ↓ decide whether to hold position
3. toobit-cex-trade     toobit futures positions --symbol BTC-SWAP-USDT → check existing exposure
```

### Compare spot vs futures premium
> User: "Is there a premium between BTC spot and BTC futures?"

```
1. toobit-cex-market    toobit market ticker --symbol BTCUSDT           → spot last price
2. toobit-cex-market    toobit market mark-price --symbol BTC-SWAP-USDT → futures mark price
3. toobit-cex-market    toobit market index --symbol BTCUSDT             → index price
```

### Research market for strategy planning
> User: "What's the BTC market activity like?"

```
1. toobit-cex-market    toobit market klines --symbol BTCUSDT --interval 4h --limit 50 → recent OHLCV
2. toobit-cex-market    toobit market ticker-24hr --symbol BTCUSDT                      → 24h stats
3. toobit-cex-market    toobit market depth --symbol BTCUSDT --limit 20                 → liquidity
4. toobit-cex-market    toobit market open-interest --symbol BTC-SWAP-USDT              → OI for sentiment
5. toobit-cex-market    toobit market long-short-ratio --symbol BTC-SWAP-USDT           → bias check
```

## Operation Flow

### Step 1: Identify the data needed

- Current price → `toobit market ticker`
- 24h stats (high/low/vol/change) → `toobit market ticker-24hr`
- Best bid/ask → `toobit market book-ticker`
- Order book depth → `toobit market depth`
- Price history/chart → `toobit market klines`
- Funding cost → `toobit market funding-rate` / `funding-rate-history`
- Contract mark price → `toobit market mark-price`
- Index price → `toobit market index`
- Futures 24h stats → `toobit market contract-ticker`
- Open interest → `toobit market open-interest`
- Market sentiment → `toobit market long-short-ratio`
- Available instruments → `toobit market info`
- Server health → `toobit market time`

### Step 2: Run commands immediately

All market data commands are read-only — no confirmation needed.

- `--symbol`: spot uses `BTCUSDT` format; futures uses `BTC-SWAP-USDT` format
- `--interval` values: `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1M`
- `--limit`: number of results (default varies per endpoint)
- `--period` (long-short-ratio): `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `12h`, `1d`

### Step 3: No writes — no verification needed

All commands in this skill are read-only. No post-execution verification required.

## CLI Command Reference

### Server Time

```bash
toobit market time [--json]
```

Returns: `serverTime` (Unix timestamp in milliseconds).

---

### Exchange Info

```bash
toobit market info [--json]
```

Returns: all tradeable symbol configurations including `symbol`, `baseAsset`, `quoteAsset`, `minQty`, `maxQty`, `tickSize`, `minNotional`, `status`.

---

### Ticker — Last Price

```bash
toobit market ticker --symbol <sym> [--json]
```

Returns: `symbol`, `price` (last traded price).

---

### 24h Ticker

```bash
toobit market ticker-24hr --symbol <sym> [--json]
```

| Param | Required | Description |
|---|---|---|
| `--symbol` | Yes | Symbol (e.g., `BTCUSDT`, `BTC-SWAP-USDT`) |

Returns: `symbol`, `open`, `high`, `low`, `close`, `volume`, `quoteVolume`, `priceChange`, `priceChangePercent`.

---

### Order Book (Depth)

```bash
toobit market depth --symbol <sym> [--limit <n>] [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--symbol` | Yes | - | Symbol |
| `--limit` | No | 100 | Depth levels (5, 10, 20, 50, 100, 500, 1000) |

Displays asks (ascending) and bids (descending) with price and quantity.

---

### Merged Depth

Use MCP tool `market_get_merged_depth` for merged (aggregated) order book with price precision control.

---

### Recent Trades

```bash
toobit market trades --symbol <sym> [--limit <n>] [--json]
```

Returns: `id`, `price`, `qty`, `isBuyerMaker`, `time`.

---

### Klines / Candles

```bash
toobit market klines --symbol <sym> [--interval <i>] [--limit <n>] [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--symbol` | Yes | - | Symbol |
| `--interval` | No | `1h` | `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1M` |
| `--limit` | No | 500 | Number of candles (max 1000) |
| `--startTime` | No | - | Start time in milliseconds |
| `--endTime` | No | - | End time in milliseconds |

Returns: `time`, `open`, `high`, `low`, `close`, `volume`.

---

### Book Ticker — Best Bid/Ask

```bash
toobit market book-ticker --symbol <sym> [--json]
```

Returns: `symbol`, `bidPrice`, `bidQty`, `askPrice`, `askQty`.

---

### Mark Price (Futures)

```bash
toobit market mark-price --symbol <sym> [--json]
```

Returns: `symbol`, `markPrice`, `time`. Used for unrealized PnL and liquidation calculations.

---

### Mark Price Klines (Futures)

Use MCP tool `market_get_mark_price_klines` for historical mark price candlestick data.

---

### Index Klines

Use MCP tool `market_get_index_klines` for historical index price candlestick data.

---

### Funding Rate (Futures)

```bash
toobit market funding-rate --symbol <sym> [--json]
```

Returns: `symbol`, `fundingRate`, `fundingTime` (next settlement time).

---

### Funding Rate History (Futures)

```bash
toobit market funding-rate-history --symbol <sym> [--limit <n>] [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--symbol` | Yes | - | Futures symbol (e.g., `BTC-SWAP-USDT`) |
| `--limit` | No | 100 | Number of historical records |

Returns: table of `symbol`, `fundingRate`, `fundingTime`.

---

### Open Interest (Futures)

```bash
toobit market open-interest --symbol <sym> [--json]
```

Returns: `symbol`, `openInterest`, `time`.

---

### Index Price (Futures)

```bash
toobit market index --symbol <sym> [--json]
```

Returns: `symbol`, `indexPrice`, `time`.

---

### Contract 24h Ticker (Futures)

```bash
toobit market contract-ticker --symbol <sym> [--json]
```

Returns: 24h statistics for a futures contract including `lastPrice`, `highPrice`, `lowPrice`, `volume`, `turnover`.

---

### Long/Short Ratio (Futures)

```bash
toobit market long-short-ratio --symbol <sym> [--period <p>] [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--symbol` | Yes | - | Futures symbol |
| `--period` | No | `1h` | `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `12h`, `1d` |

Returns: `longShortRatio`, `longAccount`, `shortAccount`, `time`.

---

### Insurance Fund (Futures)

```bash
toobit market insurance-fund --symbol <sym> [--json]
```

Returns: insurance fund balance history for a futures symbol. Symbol must use contract format (e.g., `BTC-SWAP-USDT`).

---

### Risk Limits (Futures)

```bash
toobit market risk-limits --symbol <sym> [--json]
```

Returns: risk limit tiers with `level`, `maxLeverage`, `initialMargin`, `maintainMargin`, `value`. Symbol must use contract format (e.g., `BTC-SWAP-USDT`).

---

## MCP Tool Reference

| Tool | Description |
|---|---|
| `market_get_server_time` | Server time |
| `market_get_exchange_info` | Exchange info (symbols, rules) |
| `market_get_ticker_price` | Single symbol last price |
| `market_get_ticker_24hr` | 24h ticker stats |
| `market_get_depth` | Order book depth |
| `market_get_merged_depth` | Aggregated order book with price precision |
| `market_get_trades` | Recent public trades |
| `market_get_klines` | OHLCV candles |
| `market_get_book_ticker` | Best bid/ask price and quantity |
| `market_get_mark_price` | Mark price for futures |
| `market_get_mark_price_klines` | Mark price klines for futures |
| `market_get_index_klines` | Index price klines |
| `market_get_funding_rate` | Current funding rate |
| `market_get_funding_rate_history` | Historical funding rates |
| `market_get_open_interest` | Open interest |
| `market_get_index_price` | Index price for futures |
| `market_get_contract_ticker_24hr` | Futures 24h ticker |
| `market_get_contract_ticker_price` | Futures last price |
| `market_get_long_short_ratio` | Long/short account ratio |
| `market_get_insurance_fund` | Insurance fund balance |
| `market_get_risk_limits` | Risk limits and leverage tiers |

---

## Input / Output Examples

**"What's the price of BTC?"**
```bash
toobit market ticker --symbol BTCUSDT
# → symbol: BTCUSDT | price: 95000.50
```

**"Show me BTC 24h stats"**
```bash
toobit market ticker-24hr --symbol BTCUSDT
# → symbol: BTCUSDT | high: 96000 | low: 93000 | vol: 12345.6 | change: +1.2%
```

**"What's the BTC/USDT order book look like?"**
```bash
toobit market depth --symbol BTCUSDT --limit 5
# Asks (price / qty):
#          95100.0  2.5
#          95050.0  1.2
# Bids (price / qty):
#          95000.0  3.1
#          94950.0  0.8
```

**"Show me BTC 4H candles for the last 30 periods"**
```bash
toobit market klines --symbol BTCUSDT --interval 4h --limit 30
# → table: time, open, high, low, close, vol
```

**"What's the current funding rate for BTC futures?"**
```bash
toobit market funding-rate --symbol BTC-SWAP-USDT
# → symbol: BTC-SWAP-USDT | fundingRate: 0.0001 | fundingTime: ...
```

**"Show historical funding rates for ETH futures"**
```bash
toobit market funding-rate-history --symbol ETH-SWAP-USDT --limit 20
# → table: fundingRate, fundingTime
```

**"What's the open interest on BTC futures?"**
```bash
toobit market open-interest --symbol BTC-SWAP-USDT
# → symbol: BTC-SWAP-USDT | openInterest: 125000 | time: ...
```

**"What's the best bid/ask for BTC?"**
```bash
toobit market book-ticker --symbol BTCUSDT
# → bidPrice: 95000.0 | bidQty: 3.1 | askPrice: 95001.0 | askQty: 2.5
```

**"What's the BTC long/short ratio?"**
```bash
toobit market long-short-ratio --symbol BTC-SWAP-USDT --period 1h
# → longAccount: 52.3% | shortAccount: 47.7% | ratio: 1.10
```

**"List all available trading pairs"**
```bash
toobit market info
# → table: symbol, baseAsset, quoteAsset, status, minQty, tickSize (up to 50 rows)
```

## Edge Cases

- **Symbol format**: Spot uses `BTCUSDT` (no separator); Futures uses `BTC-SWAP-USDT` (dash-separated with SWAP)
- **Funding rate**: only applies to SWAP (perpetual futures) symbols; returns error for spot symbols
- **Mark price / index price**: only available for futures contracts, not spot
- **Open interest**: only for futures contracts
- **Long/short ratio**: only for futures; `--period` controls the time granularity
- **Klines interval**: use lowercase `h`, `d`, `w`, `M` (e.g., `1h` not `1H`, `1d` not `1D`; exception: `1M` for monthly)
- **No data returned**: symbol may be delisted or format is wrong — verify with `toobit market info`
- **Depth limit**: valid values are 5, 10, 20, 50, 100, 500, 1000; other values will be rounded to the nearest valid value
- **Rate limits**: public endpoints have higher rate limits than private endpoints; typically 10–20 requests per second per IP

## Global Notes

- All market data commands are public — no API key required
- `--json` returns raw Toobit API response for programmatic use
- Candle data is sorted newest-first by default
- All timestamps are in milliseconds (Unix epoch)
- Volume in tickers is in base currency (e.g., BTC for BTCUSDT)
