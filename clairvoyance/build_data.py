import requests
import json
import numpy as np
import pandas as pd
import time
import pickle

from tqdm import tqdm
from clairvoyance.riot_api_helpers import *
from clairvoyance.game_parser import *
from clairvoyance.config import key

'''
routing values:
na1
kr
euw1
'''

def get_challengers(region):
    challengers = get_challengers(key, region).json()
    challenger_names = [i['summonerName'] for i in challengers['entries']]

    accountIds = []
    for name in tqdm(challenger_names):
        try:
            time.sleep(1.21)
            id = get_summoner(key, name).json()['accountId']
            accountIds.append(id)
        except Exception as e:
            time.sleep(10)
            print(f'Error: {e}')
    return accountIds

def get_gameIds(accountIds):
    gameIds = []
    for idx in tqdm(accountIds):
        try:
            time.sleep(1.21)
            matches = get_matchlist(key, idx).json()
            for match in matches['matches']:
                if match['queue'] == 420 and match['gameId'] not in gameIds:
                    gameIds.append(match['gameId'])
        except:
            time.sleep(10)
            print(f'Error: {e}')
    return gameIds


def get_game_data():
    X, y = [], []
    for ids in tqdm(gameIds):
        try:
            match = get_match(key, f'{ids}').json()
            timeline = get_timeline(key, f'{ids}').json()
            game, win = parse_game(timeline, match)
            X = X + game
            y = y + win
            time.sleep(0.5)
        except Exception as e:
            print(f'Error: {e}')
            time.sleep(2)

    X = np.array(X)
    y = np.array(y)

    with open('data/training/X.npy', 'wb') as f:
        np.save(f, X)
    with open('data/training/y.npy', 'wb') as f:
        np.save(f, y)
    return X, y