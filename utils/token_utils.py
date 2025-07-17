import os
import json
import random
import string
from db import SessionLocal
from models import Game



def generate_token(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def save_token(game_name, token):
    tokens = {}
    if os.path.exists('tokens.json'):
        with open('tokens.json', 'r') as file:
            tokens = json.load(file)
    tokens[game_name] = token
    with open('tokens.json', 'w') as file:
        json.dump(tokens, file)

def get_token(game_name):
    if os.path.exists('tokens.json'):
        with open('tokens.json', 'r') as file:
            tokens = json.load(file)
            return tokens.get(game_name)
    return None
