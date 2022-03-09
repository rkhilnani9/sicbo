from loguru import logger
import requests
import argparse
import numpy as np

parser = argparse.ArgumentParser(description="Parse timestamp")
parser.add_argument("--ts", type=str)
args = parser.parse_args()

url = "https://dev-feed.cardcasino.io/api/v1/ai-gaming/events"


dice_numbers = open("sicbo_dice_numbers.txt", "r").read()

myobj_end = {
    "result": {
        "eventType": "roundEnded",
        "gameType": "sicbo",
        "tableId": "Sicbo-1",
        "roundId": str(args.ts),
        "ts": 1234567890,
        "diceOne":int(dice_numbers.split(",")[0].strip()),
        "diceTwo": int(dice_numbers.split(",")[1].strip()),
        "diceThree": int(dice_numbers.split(",")[2].strip()),
    },
    "sequenceId": 2341566,
}

logger.info(f"ROUND END: {myobj_end}")

x = requests.post(url, json=myobj_end)
