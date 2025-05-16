import os
import yaml
from pushups_calculator.io import load_config


config = load_config()

def get_opgg_coefficient(note_opgg, config=config):
    for niveau in config['coefficients_opgg'].values():
        if niveau['min'] <= note_opgg < niveau['max']:
            return niveau['coefficient']
    # Si la note est exactement égale au max (ex: 10)
    return config['coefficients_opgg']['excellente']['coefficient']