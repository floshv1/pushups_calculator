import sys
import os
import pytest
import yaml

# Ajoute le dossier pompes_calculator au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pompes_calculator')))
from calcul import calculate_pushups

@pytest.fixture
def config():
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)
    


def test_calculate_pushups_example(config):
    performance = {
        'kills': 2,
        'morts': 10,
        'assists': 6,
        'bottes_triompantes': False
    }

    objectives = {
        'baron': 1,
        'herald': 1,
        'dragons': 1,
        'grubs': 1,
        'tour': 4
    }

    note_opgg = 6.5  # Cela correspond à un coefficient 1.25 (moyenne)

    result = calculate_pushups(performance, objectives, note_opgg, config, debug=True)

    # Calcul attendu :
    # (10 * 5) = 50
    # - (2 + 6) = -8
    # objectifs :
    # baron: -6
    # herald: -4
    # dragons: -3
    # grubs: -2
    # tour: 4 * -2 = -8
    # total objectifs = -6 -4 -3 -2 -8 = -23
    # total avant coef = 50 - 8 - 23 = 19
    # coeff = 1.25 → 19 * 1.25 = 23.75 → arrondi = 24

    assert result == 24
