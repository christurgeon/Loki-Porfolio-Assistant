# StockBot

## Personal Configuration 
Create a file called ```settings.json``` and place it in the root directory of the application. You will need to initialize it with API keys and your personal phone number. Follow the example below.

```
{
    "number": "11234567890",
    "alpha_vantage_key": "XXX",
    "alpaca_key_id": "XXX",
    "alpaca_private_key": "XXX"
}
```

Goals:
1. Provide statistics on certain trades/positions
2. Pull lots of data and run advanced statistics 
3. Implement a DB to store relevant data
4. Create a texting/messaging feature to interact with you
5. Parse sites for earnings data / SEC data
