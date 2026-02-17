import requests

# ################# insertion##########33/
api_uri = 'http://127.0.0.1:5000/v1/activite/insertion'

condition = input('Saisir condition : ')
reponse = input('Saisir reponse : ')

demande = {'condition': condition, 'reponse': reponse}

# Utiliser POST au lieu de GET pour l'insertion
response = requests.post(api_uri, json=demande)

if response.status_code == 200:
    message = response.json()['message']
    print(f'Réponse : {message}')
else:
    print(f'Erreur: {response.status_code} - {response.text}')


# #########suppression#################
api_uri = 'http://127.0.0.1:5000/v1/activite/suppression'

condition = input('Saisir condition à supprimer (ex: "Il pleut."): ')
data = {'condition': condition}

response = requests.post(api_uri, json=data)

if response.status_code == 200:
    message = response.json()['message']
    print(f'Réponse : {message}')
else:
    print(f'Erreur: {response.status_code} - {response.text}')

# ######## recuperer tous les conditions#############

api_uri = 'http://127.0.0.1:5000/v1/activite/conditions'

try:

    response = requests.get(api_uri)

    if response.status_code == 200:
        data = response.json()
        conditions = data.get('conditions', [])

        print("Liste de toutes les conditions:")
        for i, condition in enumerate(conditions, 1):
            print(f"{i}. {condition}")
    else:
        print(f"Erreur: {response.status_code}", response.json().get('error', ''))

except requests.exceptions.RequestException as e:
    print(f"Erreur de connexion: {str(e)}")


# ######Lister de toutes les conditions et réponses######
api_uri = 'http://127.0.0.1:5000/v1/activite/alldata'

try:
    response = requests.get(api_uri)

    if response.status_code == 200:
        data = response.json()
        donnees = data.get('donnees', [])

        print("Liste de toutes les conditions et réponses:")
        for i, item in enumerate(donnees, 1):
            condition = item.get('condition')
            reponse = item.get('reponse')
            print(f"{i}. Condition: {condition}, Réponse: {reponse}")
    else:
        print(f"Erreur: {response.status_code}", response.json().get('error', ''))

except requests.exceptions.RequestException as e:
    print(f"Erreur de connexion: {str(e)}")


# #######mise a jour ########## erreur
api_uri = 'http://127.0.0.1:5000/v1/activite/update'

# Données à mettre à jour
data = {
    "id": 29,  # remplace par l’id réel que tu veux modifier
    "condition": "Nouvelle condition 2",
    "reponse": "Nouvelle réponse 2"
}

try:
    response = requests.post(api_uri, json=data)

    if response.status_code == 200:
        print(" Mise à jour réussie :", response.json())
    else:
        print("Erreur lors de la mise à jour :", response.status_code)
        print(response.json())

except Exception as e:
    print("Exception levée :", str(e))


# # # URL de l'API
api_uri = 'http://127.0.0.1:5000/v1/activite/select_activites_byid/2'

# Envoi de la requête GET (corrigé, car votre endpoint attend GET et non POST)

response = requests.get(api_uri)

if response.status_code == 200:
    print(" Succès - Recherche par ID :", response.json())
else:
    print(" Échec - Code statut :", response.status_code, "| Réponse :", response.json())