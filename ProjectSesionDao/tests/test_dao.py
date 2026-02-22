import pytest
import sys
import os

# --- CONFIGURATION CHEMINS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from mod_dao import app, creer_table

# Solution anti-bug Windows : On force un chemin ABSOLU pour la base de test
TEST_DB = os.path.join(current_dir, 'test_bd.dbf')


@pytest.fixture
def client():
    """
    Simulation du client et création d'une base de données DE TEST isolée.
    """
    app.config['TESTING'] = True
    app.config['DATABASE'] = TEST_DB

    # Nettoyage avant test (avec try/except pour contourner les verrouillages Windows)
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except PermissionError:
            pass

    # Création de la table
    cde_ddl = '''create table if not exists activite(
            id integer primary key autoincrement,
            condition text,
            reponse text
            )'''
    creer_table(cde_ddl)

    with app.test_client() as client:
        yield client

    # Nettoyage après test
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except PermissionError:
            pass

        # --- LES TESTS RENFORCÉS ---


def test_insertion_activite_valide(client):
    payload = {'condition': 'Tempete', 'reponse': 'Rester a la maison'}
    response = client.post('/v1/dao/ins_activite', json=payload)
    assert response.status_code == 201, f"Erreur d'insertion: {response.get_data(as_text=True)}"


def test_selection_activite_existante(client):
    # 1. On insère ET ON VÉRIFIE que l'insertion a marché
    res_ins = client.post('/v1/dao/ins_activite', json={'condition': 'Neige', 'reponse': 'Ski'})
    assert res_ins.status_code == 201, f"L'insertion a échoué: {res_ins.get_data(as_text=True)}"

    # 2. On sélectionne ET ON VÉRIFIE
    response = client.post('/v1/dao/select_activites', json={'condition': 'Neige'})
    assert response.status_code == 200, f"La sélection a échoué: {response.get_data(as_text=True)}"
    assert response.get_json()['reponse'] == 'Ski'


def test_selection_activite_inexistante(client):
    response = client.post('/v1/dao/select_activites', json={'condition': 'Volcan'})
    assert response.status_code == 404


def test_suppression_activite(client):
    res_ins = client.post('/v1/dao/ins_activite', json={'condition': 'Vent', 'reponse': 'Cerf-volant'})
    assert res_ins.status_code == 201

    resp_all = client.get('/v1/dao/select_data')
    assert resp_all.status_code == 200

    donnees = resp_all.get_json().get('donnees', [])
    assert len(donnees) > 0, "La base de données est vide !"
    target_id = donnees[0]['id']

    response_del = client.delete('/v1/activities', json={'id': target_id})
    assert response_del.status_code == 200
    assert response_del.get_json()['deleted'] is True


def test_modification_activite(client):
    res_ins = client.post('/v1/dao/ins_activite', json={'condition': 'Froid', 'reponse': 'Manteau'})
    assert res_ins.status_code == 201

    resp_all = client.get('/v1/dao/select_data')
    target_id = resp_all.get_json()['donnees'][0]['id']

    payload_modif = {'id': target_id, 'condition': 'Très Froid', 'reponse': 'Deux manteaux'}
    response_put = client.put('/v1/dao/modifie_data', json=payload_modif)
    assert response_put.status_code == 200

    resp_check = client.get(f'/v1/activite/select_activites_byid/{target_id}')
    assert resp_check.get_json()['reponse'] == 'Deux manteaux'


def test_selection_activite_par_id(client):
    res_ins = client.post('/v1/dao/ins_activite', json={'condition': 'Canicule', 'reponse': 'Boire de l eau'})
    assert res_ins.status_code == 201

    resp_all = client.get('/v1/dao/select_data')
    target_id = resp_all.get_json()['donnees'][0]['id']

    response_get = client.get(f'/v1/activite/select_activites_byid/{target_id}')
    assert response_get.status_code == 200
    assert response_get.get_json()['condition'] == 'Canicule'


def test_selection_toutes_conditions(client):
    client.post('/v1/dao/ins_activite', json={'condition': 'Pluie', 'reponse': 'Parapluie'})
    client.post('/v1/dao/ins_activite', json={'condition': 'Pluie', 'reponse': 'Imperméable'})
    client.post('/v1/dao/ins_activite', json={'condition': 'Soleil', 'reponse': 'Lunettes'})

    response = client.get('/v1/dao/select_conditions')
    assert response.status_code == 200

    conditions = response.get_json()['conditions']
    assert len(conditions) == 2
    assert 'Pluie' in conditions
    assert 'Soleil' in conditions