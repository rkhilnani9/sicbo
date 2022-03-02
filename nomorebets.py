import requests, argparse

parser = argparse.ArgumentParser(
    description='Parse timestamp')

parser.add_argument('--ts', type=str)

args = parser.parse_args()


url = 'https://dev-feed.cardcasino.io/api/v1/ai-gaming/events'
myobj_nomorebets = {
"result":  {
 "eventType": "noMoreBets",
 "gameType": "sicbo",
 "tableId":  "sicbo-1",
 "roundId":  "345968",
 "ts": str(args.ts),
 "diceTwo": 5,
"diceOne": 5,
"diceThree": 3
},
"sequenceId": 2341566
}
x = requests.post(url, json = myobj_nomorebets)
