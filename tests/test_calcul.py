import sys
import os
import pytest
import yaml

# Ajoute le dossier pompes_calculator au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pompes_calculator')))
from pushups_calculator.calcul import calculate_pushups

@pytest.fixture
def config():
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)
    


def test_calculate_pushups_example(config):
    performance = {
        'kills': 4,
        'morts': 8,
        'assists': 9,
        'bottes_triompantes': False
    }

    objectives = {
        'baron': 0,
        'herald': 0,
        'dragons': 0,
        'grubs': 0,
        'tour': 1
    }

    note_opgg = 4.7  # Cela correspond à un coefficient 1.25 (moyenne)

    result = calculate_pushups(performance, objectives, note_opgg, config, debug=True)

    assert result == 24
