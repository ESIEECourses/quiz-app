import json
import sqlite3
from flask import request

#Création de la class question
class Question:
    def __init__(self, title, text, image, position, possible_answers):
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.possible_answers = possible_answers

    #Conversion Python vers JSON
    def question_to_json(self):
        return json.dumps({
            'title': self.title,
            'text': self.text,
            'image': self.image,
            'position': self.position,
            'possibleAnswers': self.possible_answers
        })

    @staticmethod
    #Conversion JSON vers Python 
    def json_to_question(json_data):
        data = json.loads(json_data)

        possible_answers = []
        for rep in data['possibleAnswers']:
            dict_reponse = {
                'text': str(rep['text']),
                'isCorrect': bool(rep['isCorrect'])
            }
            possible_answers.append(dict_reponse)
        return Question(
            title=data['title'],
            text=data['text'],
            image=data['image'],
            position=data['position'],
            possible_answers=possible_answers
        )





#OKKKKKKK
# Fonction pour insérer une question en base de données
def insert_question_reponse(question):
    try:
        # Établir une connexion à la base de données
        with sqlite3.connect('quiz.db') as conn:
            
            cursor = conn.cursor()

            # Récupérer le nombre total de questions existantes
            cursor.execute("SELECT COUNT(*) FROM QUESTION")
            total_questions = cursor.fetchone()[0]

            # Vérifier si une question existe déjà à la position spécifiée
            cursor.execute(f"SELECT COUNT(*) FROM QUESTION WHERE position = {question.position}")
            existing_question_count = cursor.fetchone()[0]

            if existing_question_count > 0:
                # Décaler les questions existantes à partir de la position spécifiée
                cursor.execute(f"UPDATE QUESTION SET position = position + 1 WHERE position >= {question.position}")
                cursor.execute(f"UPDATE REPONSE SET positionquestion = positionquestion + 1 WHERE positionquestion >= {question.position}")


            # Insérer la question dans la table QUESTION
            cursor.execute(
                "INSERT INTO QUESTION (title, text, image, position) VALUES (?, ?, ?, ?)",
                (question.title, question.text, question.image, question.position)
            )

            # Insérer les réponses possibles dans la table REPONSE
            for rep in question.possible_answers:
                cursor.execute(
                    "INSERT INTO REPONSE (reponse, booleen, positionquestion) VALUES (?, ?, ?)",
                    (rep['text'], str(rep['isCorrect']), question.position)
                )

            # Valider les modifications dans la base de données
            conn.commit()

        # Retourner True pour indiquer que l'insertion s'est bien déroulée
        return True
    except sqlite3.Error as e:
        print("Erreur lors de l'insertion de la question en base de données:", e)
        return "Une erreur s'est produite lors de l'insertion de la question", 500




# Récupération d'une question par ID avec ses réponses
def getById(id):
    try:
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()

            # Récupération des données de la question depuis la table QUESTION
            cursor.execute(f"SELECT * FROM QUESTION WHERE id = {id}")
            question_data = cursor.fetchone()
            if question_data is None:
                return 'Request respond Not Found', 404


            # Création de l'objet Question avec les données récupérées
            question = Question(
                title=question_data[2],
                text=question_data[1],
                image=question_data[3],
                position=question_data[4],
                possible_answers=[]
            )

            # Récupération de la valeur de la colonne "position" de la table QUESTION
            position = question_data[4]

            # Récupération des données des réponses depuis la table REPONSE en utilisant la valeur de "position"
            cursor.execute(f"SELECT * FROM REPONSE WHERE positionquestion = {position}")
            reponse_data = cursor.fetchall()

            for rep in reponse_data:
                # Construction de l'objet réponse en fonction du champ "booleen" dans la base de données
                reponse = {
                    'text': rep[1],
                    'isCorrect': bool(rep[2] == 'True') # Convertir 'True' en True et 'False' en False
                }
                question.possible_answers.append(reponse)

            # Conversion de l'objet Question en JSON
            json_data = question.question_to_json()

            return json_data, 200
    except sqlite3.Error as e:
        print("Erreur lors de la récupération de la question en base de données:", e)
        return 'An error occurred while fetching the question', 500


    

# Récupération d'une question par Position avec ses réponses
def getByPosition(position):
    try:
        # Connexion à la base de données
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()

            # Exécution de la requête de sélection des questions par position
            cursor.execute(f"SELECT * FROM QUESTION WHERE position = {position}")
            question_data = cursor.fetchone()
            if question_data is None:
                return 'Request respond Not Found', 404

            # Création de l'objet Question avec les données récupérées
            question = Question(
                title=question_data[2],
                text=question_data[1],
                image=question_data[3],
                position=question_data[4],
                possible_answers=[]
            )

            # Récupération des réponses associées à la question depuis la table REPONSE
            cursor.execute(f"SELECT * FROM REPONSE WHERE positionquestion = {position}")
            reponse_data = cursor.fetchall()

            answers = []
            for rep in reponse_data:
                # Construction de l'objet réponse en fonction du champ "booleen" dans la base de données
                reponse = {
                    'text': rep[1],
                    'isCorrect': bool(rep[2] == 'True') # Convertir 'True' en True et 'False' en False
                }
                answers.append(reponse)

            question.possible_answers = answers

            # Fermeture de la connexion à la base de données
            

            # Conversion de l'objet Question en JSON
            json_data = question.question_to_json()

            return json_data, 200

    except sqlite3.Error as e:
        print("Erreur lors de la récupération de la question en base de données:", e)
        return 'An error occurred while fetching the question', 500



def updateById(questionId):
    try:
        # Récupérer les données de la question depuis le corps de la requête
        question_data = request.get_json()
        print(question_data)
        questionPy = Question.json_to_question(json.dumps(question_data))

        # Vérifier si la question existe dans la base de données
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()

            # Exécuter une requête SELECT pour vérifier l'existence de la question
            cursor.execute(f"SELECT * FROM QUESTION WHERE id = {questionId}")
            existing_question = cursor.fetchone()
            print(existing_question)
            if existing_question is None:
                return 'Request respond Not Found', 404
            else:
                # PositionSource = position de la question qui est en base
                position_source = existing_question[4]  # 4 correspond à l'index de la colonne "position" dans le résultat
                # PositionDestination = question_data['position']
                position_destination = question_data['position']
                if position_destination == position_source:
                    print("inside")
                    print(type(question_data['title']),"=",type(questionPy.title))
                    print(questionId)
                    # Mettre à jour les données de la question dans la base de données
                    update_query = "UPDATE QUESTION SET title = ?, text = ?, image = ?, position = ? WHERE id = ?"
                    cursor.execute(update_query, (
                        question_data['title'],
                        question_data['text'],
                        question_data['image'],
                        question_data['position'],
                        questionId
                ))

                    print('good execution of update')
                    # Supprimer les anciennes réponses associées à la question
                    cursor.execute(f"DELETE FROM REPONSE WHERE positionquestion = {position_source}")
                else:
                    # Supprimer la question et ses réponses de la base de données
                    cursor.execute(f"DELETE FROM QUESTION WHERE id = {questionId}")
                    cursor.execute(f"DELETE FROM REPONSE WHERE positionquestion = {position_source}")
                    if position_source > position_destination:
                        # Ajouter +1 à toutes les questions et réponses ayant une position en base
                        # >= PositionDestination ET < PositionSource
                        cursor.execute(f"UPDATE QUESTION SET position = position + 1 WHERE position >= {position_destination} AND position < {position_source}")
                        cursor.execute(f"UPDATE REPONSE SET positionquestion = positionquestion + 1 WHERE positionquestion >= {position_destination} AND positionquestion < {position_source}")
                    elif position_source < position_destination:
                        # Ajouter -1 à toutes les questions et réponses ayant une position en base
                        # > PositionSource ET <= PositionSource
                        cursor.execute(f"UPDATE QUESTION SET position = position - 1 WHERE position > {position_source} AND position <= {position_destination}")
                        cursor.execute(f"UPDATE REPONSE SET positionquestion = positionquestion - 1 WHERE positionquestion > {position_source} AND positionquestion <= {position_destination}")

                    # Insérer la question mise à jour dans la base de données avec la nouvelle position
                    cursor.execute("INSERT INTO QUESTION (id, title, text, image, position) VALUES (?, ?, ?, ?, ?)",
                        (questionId, question_data['title'], question_data['text'], question_data['image'], question_data['position'])
                    )

                # Insérer les nouvelles réponses dans la base de données
                    for answer in question_data['possibleAnswers']:
                        cursor.execute(
                            "INSERT INTO REPONSE (reponse, booleen, positionquestion) VALUES (?, ?, ?)",
                            (answer['text'], str(answer['isCorrect']), question_data['position'])
                        )
                
                conn.commit()
        

                return 'Question updated successfully', 204

    except sqlite3.Error as e:
        print("Erreur lors de la mise à jour de la question en base de données:", e)
        return 'An error occurred while updating the question', 500
    



#Suppression d'une question par ID avec ses réponses
def deleteById(id):
    try:
        # Vérifier si la question existe dans la base de données
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM QUESTION WHERE id = {id}")
            question_data = cursor.fetchone()
            if question_data is None:
                return 'Request respond Not Found', 404
            # Suppression des réponses associées à la question
            else:
                # PositionSource = position de la question qui est en base
                position_source = question_data[4]  # 4 correspond à l'index de la colonne "position" dans le résultat
                cursor.execute(f"DELETE FROM REPONSE WHERE positionquestion = (SELECT position FROM QUESTION WHERE id = {id})")
                # Suppression de la question
                cursor.execute(f"DELETE FROM QUESTION WHERE id = {id}")
                cursor.execute(f"UPDATE QUESTION SET position = position - 1 WHERE position > {position_source} ")
                cursor.execute(f"UPDATE REPONSE SET positionquestion = positionquestion - 1 WHERE positionquestion > {position_source}")

                # Valider la transaction et fermer la connexion à la base de données
                conn.commit()
            return 'Question and its answers deleted successfully', 204
        
    except sqlite3.Error as e:
        print("Erreur lors de la suppression de la question en base de données:", e)
        return 'An error occurred while deleting the question', 500
    





def reoderById(questionId, positionDest):
    try:
        # Vérifier si la question existe dans la base de données
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM QUESTION WHERE id = {questionId}")
            question_data = cursor.fetchone()
            if question_data is None:
                return 'Request respond Not Found', 404

            # Récupérer la position actuelle de la question
            current_position = question_data[4]

            # Vérifier si la position de destination est valide
            positionDest = int(positionDest)
            if positionDest <= 0:
                return 'Invalid destination position', 400

            # Vérifier si la position de destination est différente de la position actuelle
            if positionDest == current_position:
                return 'Destination position is the same as the current position', 400

            # Mettre à jour la position de la question actuelle
            cursor.execute(f"UPDATE QUESTION SET position = {positionDest} WHERE id = {questionId}")

            # Réordonner les questions entre la position actuelle et la position de destination
            if positionDest < current_position:
                # Décrémenter les positions des questions entre la position de destination et la position actuelle
                cursor.execute(f"UPDATE QUESTION SET position = position + 1 WHERE position >= {positionDest} AND position < {current_position} AND id != {questionId}")
                
            else:
                # Incrémenter les positions des questions entre la position actuelle et la position de destination
                cursor.execute(f"UPDATE QUESTION SET position = position - 1 WHERE position > {current_position} AND position <= {positionDest} AND id != {questionId}")

            # Mettre à jour les positions des réponses associées à la question
            cursor.execute(f"UPDATE REPONSE SET positionquestion = {positionDest} WHERE positionquestion = {current_position}")

            conn.commit()
            return 'Question reordered successfully', 204

    except sqlite3.Error as e:
        print("Erreur :", e)
        return 'An error occurred while reordering the question', 500



'''
10/05/2023

MAJ RESPECT DES TESTS DE LA COLLECTION POSTMAN
'''

#def deleteq1():
 #   return 'ok', 204


def deleteallq():
    try:
        # Vérifier si la question existe dans la base de données
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()
            # Exécution de la requête de suppression
            cursor.execute("DELETE FROM QUESTION")
            cursor.execute("DELETE FROM REPONSE")
			
			# Validation de la transaction
            conn.commit()
            
            return 'All questions have been deleted', 204 
    except sqlite3.Error as e:
        print("Erreur lors de la suppression des questions en base de données:", e)
        return 'An error occurred while deleting the questions', 500
    


def deleteallp():
    try:
        # Vérifier si la question existe dans la base de données
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM PARTICIPATION")
            conn.commit()
            return 'All participation are deleted', 204
    except sqlite3.Error as e:
        print("Erreur :", e)
        return 'An error occurred while deleting all participation', 500
    


def getquestionposition(position):
    try:
        # Vérifier si la question existe dans la base de données
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM QUESTION WHERE position = {position}")
            question_data = cursor.fetchone()
            if question_data is None:
                return 'Request respond Not Found', 404
            
            # Création de l'objet Question avec les données récupérées
            question = Question(
                title=question_data[2],
                text=question_data[1],
                image=question_data[3],
                position=question_data[4],
                possible_answers=[]
            )

            # Récupération des réponses associées à la question depuis la table REPONSE
            cursor.execute(f"SELECT * FROM REPONSE WHERE positionquestion = {position}")
            reponse_data = cursor.fetchall()

            answers = []
            for rep in reponse_data:
                # Construction de l'objet réponse en fonction du champ "booleen" dans la base de données
                reponse = {
                    'text': rep[1],
                    'isCorrect': bool(rep[2] == 'True') # Convertir 'True' en True et 'False' en False
                }
                answers.append(reponse)

            question.possible_answers = answers
            # Conversion de l'objet Question en JSON
            json_data = question.question_to_json()

            return json_data, 200

    except sqlite3.Error as e:
        print("Erreur :", e)
        return 'An error occurred while getting the question at position 2', 500
    



def retrieveBD():
    try:
        # Vérifier si la question existe dans la base de données
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM QUESTION")
            cursor.execute("DELETE FROM REPONSE")
            cursor.execute("DELETE FROM PARTICIPATION")
            cursor.execute("DELETE FROM sqlite_sequence")


            conn.commit()

            return 'Ok',200
    except sqlite3.Error as e:
        print("Erreur :", e)
        return 'An error occurred while getting deleting all infos', 500
    