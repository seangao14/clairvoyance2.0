import pandas as pd
import json
import requests
from clairvoyance.config import patch

champs = requests.get(f'http://ddragon.leagueoflegends.com/cdn/{patch}.1/data/en_US/champion.json').json()

# rid = riot id for the champion

# maps riot id to index
def idx_from_rid():
    df = pd.DataFrame.from_dict(champs['data'], orient='index')

    names = df['key']
    names = pd.Series(dict((v,k) for k,v in names.iteritems()))
    names_dict = names.to_dict()
    
    # maps champion name to index
    # champ_dict = dict((champ, idx) for idx, champ in enumerate(names_dict.values()))

    # maps riot champion id to index
    nums_dict = dict((champ_key, idx) for idx, champ_key in enumerate(names_dict.keys()))
    
    return nums_dict

# maps riot id to champion name
def name_from_rid():
    df = pd.DataFrame.from_dict(champs['data'], orient='index')

    names = df['key']
    names = pd.Series(dict((v,k) for k,v in names.iteritems()))
    names_dict = names.to_dict()
    return names_dict

def idx_from_name():
    df = pd.DataFrame.from_dict(champs['data'], orient='index')

    names = df['key']
    names = pd.Series(dict((v,k) for k,v in names.iteritems()))
    names_dict = names.to_dict()
    
    champ_dict = dict((champ, idx) for idx, champ in enumerate(names_dict.values()))

    return champ_dict


idx_rid_dict = idx_from_rid()

name_rid_dict = name_from_rid()

idx_name_dict = idx_from_name()

num_champs = len(idx_rid_dict.keys())