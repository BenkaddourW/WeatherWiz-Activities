import requests


api_uri='http://127.0.0.1:5000/v1/activite/statut'

data=requests.get(api_uri)

condition = input('Saisir condition météo: ')
data = {'condition': condition}

response = requests.post(api_uri, json=data)

if response.status_code == 200:
    message = response.json()['message']
    print(f'Réponse : {message}')
else:
    print(f'Erreur: {response.status_code} - {response.text}')