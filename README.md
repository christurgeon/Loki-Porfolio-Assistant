# StockBot

## Personal Configuration 
Create a file called ```settings.json``` and place it in the root directory of the application. You will need to initialize it with Alpaca, AlphaVantage, and Slack API keys. 

```
{
    "config": {
        "alpha_vantage_key": "xxx-xxx-xxx",
        "requests_interval_millis": "12000",
        "alpaca_key_id": "xxx-xxx-xxx",
        "alpaca_private_key": "xxx-xxx-xxx"
    },
    "slack": {
        "slack_private_key": "xxx-xxx-xxx",
        "default_channel": "market-watcher"
    },
    "stats": {
        "delta": "5.0"
    }
}
```

Current Features:
1. Periodic polling of market data, sends data to slack channel
2. Alpaca hook up for automated trading

Goals:
1. Provide statistics on certain trades/positions
2. Pull lots of data and run advanced statistics 
3. Parse sites for earnings data / SEC data
