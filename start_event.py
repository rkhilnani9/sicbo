import requests, argparse

parser = argparse.ArgumentParser(
    description='Parse timestamp')

parser.add_argument('--ts', type=str)

args = parser.parse_args()


url = 'https://dev-feed.cardcasino.io/api/v1/ai-gaming/events'
myobj_start = {"result": {
             "eventType":"roundStart",
             "gameType":"sicbo",
             "tableId":"sicbo-1",
             "roundId": str(args.ts),
             "ts":123,
             "betTime":123456
            },"sequenceId":123}

x = requests.post(url, json = myobj_start)

