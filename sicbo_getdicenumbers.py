import pandas as pd
import pymongo
from pymongo import MongoClient
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
from loguru import logger

dice_numbers_gen_app = FastAPI()
dice_numbers_gen_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = "mongodb+srv://satya:ecYuTiv8tjFsv8Jo@ezugi.mdwax.mongodb.net/GapDev?authSource=admin&replicaSet=atlas-11ti8d-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = MongoClient(CONNECTION_STRING)
db = client.ssgdev
collection = db["bets"]


def get_zerojson():
    return [
        {
            "market_type": "ODD_EVEN",
            "runners": [
                {
                    "runnerType": "ODD",
                    "oddValue": 1.98,
                    "totalStake": 0,
                    "totalBets": 20,
                },
                {
                    "runnerType": "EVEN",
                    "oddValue": 1.98,
                    "totalStake": 0,
                    "totalBets": 4,
                },
            ],
        },
        {
            "market_type": "HIGH_LOW",
            "runners": [
                {
                    "runnerType": "SMALL",
                    "oddValue": 1.98,
                    "totalStake": 0,
                    "totalBets": 20,
                },
                {
                    "runnerType": "BIG",
                    "oddValue": 1.98,
                    "totalStake": 0,
                    "totalBets": 4,
                },
            ],
        },
        {
            "market_type": "ANY_TRIPLE",
            "runners": [
                {
                    "runnerType": "ANY_TRIPLE",
                    "oddValue": 20,
                    "totalStake": 0,
                    "totalBets": 20,
                },
                {
                    "runnerType": "NO_TRIPLE",
                    "oddValue": 0,
                    "totalStake": 0,
                    "totalBets": 4,
                },
            ],
        },
        {
            "market_type": "TRIPLE",
            "runners": [
                {
                    "runnerType": "1+1+1",
                    "oddValue": 80,
                    "totalStake": 0,
                    "totalBets": 20,
                },
                {
                    "runnerType": "2+2+2",
                    "oddValue": 80,
                    "totalStake": 0,
                    "totalBets": 20,
                },
                {
                    "runnerType": "3+3+3",
                    "oddValue": 80,
                    "totalStake": 0,
                    "totalBets": 20,
                },
                {
                    "runnerType": "4+4+4",
                    "oddValue": 80,
                    "totalStake": 0,
                    "totalBets": 20,
                },
                {
                    "runnerType": "5+5+5",
                    "oddValue": 80,
                    "totalStake": 0,
                    "totalBets": 20,
                },
                {
                    "runnerType": "6+6+6",
                    "oddValue": 80,
                    "totalStake": 0,
                    "totalBets": 20,
                },
            ],
        },
        {
            "market_type": "ALL_DICE_TOTAL",
            "runners": [
                {
                    "runnerType": "THREE",
                    "oddValue": 80,
                    "totalStake": 0,
                    "totalBets": 10,
                },
                {
                    "runnerType": "FOUR",
                    "oddValue": 30,
                    "totalStake": 0,
                    "totalBets": 9,
                },
                {
                    "runnerType": "FIVE",
                    "oddValue": 20,
                    "totalStake": 0,
                    "totalBets": 9,
                },
                {"runnerType": "SIX", "oddValue": 16, "totalStake": 0, "totalBets": 1,},
                {
                    "runnerType": "SEVEN",
                    "oddValue": 13,
                    "totalStake": 0,
                    "totalBets": 1,
                },
                {
                    "runnerType": "EIGHT",
                    "oddValue": 9,
                    "totalStake": 0,
                    "totalBets": 1,
                },
                {"runnerType": "NINE", "oddValue": 7, "totalStake": 0, "totalBets": 1,},
                {"runnerType": "TEN", "oddValue": 7, "totalStake": 0, "totalBets": 1,},
                {
                    "runnerType": "ELEVEN",
                    "oddValue": 7,
                    "totalStake": 0,
                    "totalBets": 1,
                },
                {
                    "runnerType": "TWELVE",
                    "oddValue": 7,
                    "totalStake": 0,
                    "totalBets": 1,
                },
                {
                    "runnerType": "THIRTEEN",
                    "oddValue": 9,
                    "totalStake": 0,
                    "totalBets": 1,
                },
                {
                    "runnerType": "FOURTEEN",
                    "oddValue": 13,
                    "totalStake": 0,
                    "totalBets": 1,
                },
                {
                    "runnerType": "FIFTEEN",
                    "oddValue": 16,
                    "totalStake": 0,
                    "totalBets": 1,
                },
                {
                    "runnerType": "SIXTEEN",
                    "oddValue": 20,
                    "totalStake": 0,
                    "totalBets": 1,
                },
                {
                    "runnerType": "SEVENTEEN",
                    "oddValue": 30,
                    "totalStake": 0,
                    "totalBets": 1,
                },
                {
                    "runnerType": "EIGHTEEN",
                    "oddValue": 80,
                    "totalStake": 0,
                    "totalBets": 1,
                },
            ],
        },
    ]


@dice_numbers_gen_app.post("/get_dice_numbers")
async def get_next_card_dt(json_data: Request):
    json_data = await json_data.json()
    ts = json_data["ts"]
    result_1 = collection.find(
        {
            "round_id": {"$eq": str(ts)},
            "provider_id": {"$eq": "AIGAMING"},
            "game_id": {"$eq": "AGSB101"},
            # "bet_req.request_time": {"$lt": str(ts2+20)}
        }
    )

    runner_list = []
    markettype_list = []
    betamount_list = []
    odds_list = []
    for _ in range(1):
        for i in result_1:
            runner_list.append(i["bet_details"]["runnerType"])
            markettype_list.append(i["bet_details"]["marketType"])
            betamount_list.append(i["bet_details"]["stakeAmount"])
            odds_list.append(i["bet_details"]["oddValue"])
    t = pd.DataFrame([runner_list, markettype_list, betamount_list, odds_list]).T
    t.columns = ["runners", "market_type", "betsamount", "odds"]
    t2 = t.groupby(["runners", "market_type", "odds"]).agg({"betsamount": "sum"})
    t2 = t2.reset_index()
    logger.info(t2)
    bets_json = get_zerojson()
    for k in range(t2.shape[0]):
        runner = t2.loc[k]["runners"]
        market = t2.loc[k]["market_type"]
        betsamount = t2.loc[k]["betsamount"]
        for i in range(len(bets_json)):
            if bets_json[i]["market_type"] == market:
                for j in range(len(bets_json[i]["runners"])):
                    if bets_json[i]["runners"][j]["runnerType"] == runner:
                        bets_json[i]["runners"][j]["totalStake"] = betsamount

    logger.info(bets_json)
    resp = requests.post("http://0.0.0.0:8051/rtp/sicbo", data=json.dumps(bets_json))

    return resp.json()
