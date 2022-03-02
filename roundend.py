from loguru import logger
import requests
import argparse
import numpy as np

parser = argparse.ArgumentParser(
    description='Parse timestamp')
parser.add_argument('--ts', type=str)
args = parser.parse_args()

url = 'https://dev-feed.cardcasino.io/api/v1/ai-gaming/events'


def expand_card(card):
    suit = card[1]
    rank = card[0]
    if suit == 's':
        suit = 'spades'
    elif suit == 'c':
        suit = 'clubs'
    elif suit == 'h':
        suit = 'hearts'
    else:
        suit = 'diamonds'
    if rank == 'j':
        rank = 'jack'
    elif rank == 'q':
        rank = 'queen'
    elif rank == 'k':
        rank = 'king'
    elif rank == 'a':
        rank = 'ace'
    elif rank == 'x':
        rank = 10

    return {'suit': suit, 'rank': rank}


dice_numbers = open("sicbo_numbers.txt", "r").read()

myobj_end = {"result": {
             "eventType": "roundEnded",
             "gameType": "sicbo",
             "tableId": "sicbo-1",
             "roundId": str(args.ts),
             "ts": 1234567890,
             "diceNumbers": [{"dice1" : dice_numbers.split(",")[0]}, {"dice2" : dice_numbers.split(",")[1]}, {"dice3" : dice_numbers.split(",")[2]}
             ]}, "sequenceId": 2341566}

logger.info(f'ROUND END: {myobj_end}')

x = requests.post(url, json=myobj_end)
