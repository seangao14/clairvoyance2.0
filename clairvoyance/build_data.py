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

def get_accIds():
    challengers = {
        'na1': None,
        'kr': None,
        'euw1': None
    }
    for i in challengers.keys():
        challengers[i] = get_challengers(key, i).json()


    for i in challengers.keys():
        challengers[i] = [j['summonerName'] for j in challengers[i]['entries']]

    accountIds = {
        'na1': [],
        'kr': [],
        'euw1': []
    }
    for i in tqdm(range(300)): # 300 challengers
        for r in challengers.keys():
            if i < len(challengers[r]):
                summ = get_summoner(key, challengers[r][i], r).json()
                try:
                    idx = summ['accountId']
                    accountIds[r].append(idx)
                except Exception as e:
                    print(f"Message: {summ['status']['message']}")
                    if summ['status']['status_code'] == 429:
                        print('Pausing for 10 seconds...')
                        time.sleep(10)

    return accountIds

def get_gameIds(accountIds):
    gameIds = {
        'na1': [],
        'kr': [],
        'euw1': []
    }
    max_len = max(len(accountIds['na1']), len(accountIds['kr']), len(accountIds['euw1']))

    for i in tqdm(range(max_len)):
        for r in accountIds.keys():
            if i < len(accountIds[r]):
                try:
                    matches = get_matchlist_(key, accountIds[r][i], r).json()
                    for match in matches['matches']:
                        if match['queue'] == 420 and match['gameId'] not in gameIds[r]:
                            gameIds[r].append(match['gameId'])
                except:
                    print(f"Message: {matches['status']['message']}")
                    if matches['status']['status_code'] == 429:
                        print('Pausing for 10 seconds...')
                        time.sleep(10)
    return gameIds


def build_game_data(gameIds):
    chunk_size = 500
    data = {
        'na1X': [],
        'na1Y': [],
        'krX': [],
        'krY': [],
        'euw1X': [],
        'euw1Y': [],
    }
    lengths = {
        'na1': len(gameIds['na1']),
        'kr': len(gameIds['kr']),
        'euw1': len(gameIds['euw1'])
    }
    max_len = max(lengths.values())

    for i in tqdm(range(max_len)):
        for r in gameIds.keys():
            if i < lengths[r]:
                match = get_match(key, gameIds[r][i], r).json()
                timeline = get_timeline(key, gameIds[r][i], r).json()
                try:
                    game, win = parse_game(timeline, match)
                    data[f'{r}X'] = data[f'{r}X'] + game
                    data[f'{r}Y'] = data[f'{r}Y'] + win
                    # time.sleep(1.2)
                except Exception as e:
                    print(f'{e}')
                    # print(f"Message: {match['status']['message']}")
                    # if match['status']['status_code'] == 429:
                    #     print('Pausing for 10 seconds...')
                    #     time.sleep(10)
                if i > 0 and i%chunk_size==0:
                    np.save(f'clairvoyance/data/training/{r}X{i//chunk_size}.npy', data[f'{r}X']) 
                    np.save(f'clairvoyance/data/training/{r}Y{i//chunk_size}.npy', data[f'{r}Y']) 
                    data[f'{r}X'] = []
                    data[f'{r}Y'] = []
                    print(f'Chunk {i//chunk_size} saved!')
                elif i==(lengths[r]-1):
                    np.save(f'clairvoyance/data/training/{r}X0.npy', data[f'{r}X']) 
                    np.save(f'clairvoyance/data/training/{r}Y0.npy', data[f'{r}Y']) 
                    data[f'{r}X'] = []
                    data[f'{r}Y'] = []
                    print(f'Chunk 0 saved!')
        # break