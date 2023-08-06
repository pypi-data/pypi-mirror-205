import asyncio

from config import config

from rum_with_telegram import DataExchanger

asyncio.run(DataExchanger(config).handle_rum())

    

