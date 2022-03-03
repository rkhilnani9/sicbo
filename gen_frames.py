import argparse
import shutil
import random
import os
import json
import requests
from loguru import logger
import numpy as np

parser = argparse.ArgumentParser(description="Parse timestamp")

parser.add_argument("--ts", type=str)

args = parser.parse_args()


json_time = {"ts": str(args.ts)}
resp = requests.post("http://0.0.0.0:8008/get_dice_numbers", data=json.dumps(json_time))
dice_numbers = resp.json()

f = open("sicbo_dice_numbers.txt", "w")
logger.info("File opened!")
f.write(f"{dice_numbers['dice1']}, {dice_numbers['dice2']}, {dice_numbers['dice3']}")
f.close()
