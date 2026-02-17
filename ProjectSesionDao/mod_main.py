from doctest import debug

from mod_classe import Activite
from mod_dao import creer_table, inserer_data, selectionner_data

# from flask import Flask
# app=Flask(__name__)

def creer_activite():

    condition= input('Saisir la condition:')
    reponse = input('Saisir la reponse:')

    return Activite(condition,reponse)

def afficher_data(registre):
    for tmp in registre:
        print(tmp)

def main():
    cde_ddl = '''create table if not exists activite(
            id integer primary key autoincrement,
            condition text,
            reponse text
            )
            '''

    # creer table
    creer_table(cde_ddl)

    # creer un objet
    activite=creer_activite()
    #inserer
    inserer_data(activite)

    #selectionner
    registre = selectionner_data()
    # Afficher le contenu qui est dans la table selon condition
    afficher_data(registre)

# if __name__ == '__main__':
#     app.run(debug=True,port=5600)



# ### Route : Récupérer un projet par ID ###
# @app.route('/v1/dao/projet/<int:code_projet>', methods=['GET'])
# def get_projet(code_projet):
#     conn = creer_connexion()
#     curseur = conn.cursor()
#     curseur.execute('SELECT Code_projet, Description FROM projets WHERE Code_projet = ?', (code_projet,))
#     projet = curseur.fetchone()
#     fermer_connexion(conn)
#
#     if projet:
#         return jsonify({'Code_projet': projet[0], 'Description': projet[1]})
#     else:
#         return jsonify({'erreur': 'Projet non trouvé'}), 404
#
# ### Route : Lister tous les projets ###
# @app.route('/v1/dao/projet', methods=['GET'])
# def get_all_projets():
#     conn = creer_connexion()
#     curseur = conn.cursor()
#     curseur.execute('SELECT Code_projet, Description FROM projets')
#     projets = curseur.fetchall()
#     fermer_connexion(conn)
#
#     liste = [{'Code_projet': p[0], 'Description': p[1]} for p in projets]
#     return jsonify(liste)
#
# ## Lancement ###
