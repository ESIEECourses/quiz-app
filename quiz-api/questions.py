from flask import request
from jwt_utils import decode_token
from classQuestions import *
import json
import sqlite3






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

def goodToken(token):
    if (token):
        try : 
            decode_token(token.replace("Bearer ", ""))
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False


def getQuizInfo():
    try:
        with sqlite3.connect('quiz.db') as conn:
            #On récupère le nombre de questions
            cursor = conn.cursor()
            query = cursor.execute("SELECT COUNT(*) FROM QUESTION")
            
            last_id = query.fetchall()[0][0]
            
            #On récupère les joueurs et leur score du meilleur au moins bon 
            cursor.execute("SELECT * FROM PARTICIPATION ORDER BY score DESC")
            participations = cursor.fetchall()
            listeScores = []
            for part in participations:
                listeScores.append({'playerName': part[1], 'score': part[2]})
            return {'size': last_id, 'scores': listeScores }, 200
    except sqlite3.Error as e:
        
        return {"Erreur lors de la récupération des informations du quizz": e}, 500
    



#Insertion d'une nouvelle question
def insert_question_reponses(request):
    #Récupération du body dans la requête 
    questionJson = request.get_json()
    #Passage d'un JSON à un objet Question en Python
    questionPython = Question.json_to_question(json.dumps(questionJson))
    #Ajout de la question en base
    try:
        with sqlite3.connect('quiz.db') as conn:
            
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM QUESTION WHERE position = {questionPython.position}")
            count = cursor.fetchone()[0]

            if count>0:
                cursor.execute(f"UPDATE QUESTION SET position = position + 1 WHERE position >= {questionPython.position}")
                cursor.execute(f"UPDATE REPONSE SET positionquestion = positionquestion + 1 WHERE positionquestion >= {questionPython.position}")
            
            cursor.execute(
                "INSERT INTO QUESTION (title, text, image, position) VALUES (?, ?, ?, ?)",
                (questionPython.title, questionPython.text, questionPython.image, questionPython.position)
            )
            #Récupération de l'ID de la question insérée
            query = cursor.execute(f"SELECT seq FROM sqlite_sequence WHERE name=\"QUESTION\"")
            last_id = query.fetchall()[0][0]



            # Insérer les réponses possibles dans la table REPONSE
            for rep in questionPython.possible_answers:
                cursor.execute(
                    "INSERT INTO REPONSE (reponse, booleen, positionquestion) VALUES (?, ?, ?)",
                    (rep['text'], str(rep['isCorrect']), questionPython.position)
                )
            conn.commit()
            
            return {'id': last_id}, 200
    except sqlite3.Error as e:
        print("Erreur lors de l'insertion de la question en base de données:", e)
        return "Une erreur s'est produite lors de l'insertion de la question", 500



# Suppression de toutes les questions/réponses 
def deleteall():
    try:
        # Vérifier si la question existe dans la base de données
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM QUESTION")
            cursor.execute("DELETE FROM REPONSE")
            cursor.execute("DELETE FROM PARTICIPATION")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name=\"PARTICIPATION\"")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name=\"REPONSE\"")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name=\"QUESTION\"")


            conn.commit()

            return 'Ok',204
    except sqlite3.Error as e:
        print("Erreur :", e)
        return 'An error occurred while getting deleting all questions and answers', 500
    

def deleteallparticipations():
    try:
        # Vérifier si la question existe dans la base de données
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM PARTICIPATION")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name=\"PARTICIPATION\"")
            


            conn.commit()

            return 'Ok',204
    except sqlite3.Error as e:
        print("Erreur :", e)
        return 'An error occurred while getting deleting all participations', 500


def getById(questionId):
    print("Récupération d'une question par ID: ", questionId)
    try:
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()

            # Récupération des données de la question depuis la table QUESTION
            cursor.execute(f"SELECT * FROM QUESTION WHERE id = {questionId}")
            questionDB= cursor.fetchone()
            if questionDB is None:
                return 'Request respond Not Found', 404


            # Création de l'objet Question avec les données récupérées
            question = Question(
                id=questionDB[0],
                title=questionDB[2],
                text=questionDB[1],
                image=questionDB[3],
                position=questionDB[4],
                possible_answers=[]
            )
            print("Question ", question.title," and ", question.position)
            # Récupération de la valeur de la colonne "position" de la table QUESTION
            position = questionDB[4]
            print("Position =", position)
            # Récupération des données des réponses depuis la table REPONSE en utilisant la valeur de "position"
            cursor.execute(f"SELECT * FROM REPONSE WHERE positionquestion = {position}")
            reponse_data = cursor.fetchall()
            print(reponse_data)
            for rep in reponse_data:
                # Construction de l'objet réponse en fonction du champ "booleen" dans la base de données
                reponse = {
                    'text': rep[1],
                    'isCorrect': bool(rep[2] == 'True') # Convertir 'True' en True et 'False' en False
                }
                question.possible_answers.append(reponse)

            conn.commit()
            # Conversion de l'objet Question en JSON
            json_data = question.question_to_json()

            return json_data, 200
    except sqlite3.Error as e:
        print("Erreur lors de la récupération de la question en base de données:", e)
        return 'An error occurred while fetching the question', 500
    



def getQuestionByPosition(position):
    print("Récupération d'une question par position: ", position)
    try:
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM QUESTION WHERE position = {position}")
            questionDB= cursor.fetchone()
            if questionDB is None:
                return 'Request respond Not Found', 404


            # Création de l'objet Question avec les données récupérées
            question = Question(
                id=questionDB[0],
                title=questionDB[2],
                text=questionDB[1],
                image=questionDB[3],
                position=questionDB[4],
                possible_answers=[]
            )
            
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
    

import sqlite3
import json

def updateById(request, questionId):
    print("Update data by ID: ", questionId)
    #Récupération du body dans la requête 
    questionJson = request.get_json()
    questionPython = Question.json_to_question(json.dumps(questionJson))
        
    #Ajout de la question en base
    try:
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()
            # Exécuter une requête SELECT pour vérifier l'existence de la question
            cursor.execute(f"SELECT * FROM QUESTION WHERE id = {questionId}")
            existing_question = cursor.fetchone()
            
            if existing_question is None:
                return 'Request respond Not Found', 404
            else:
                print("One question exist at the position")
                # PositionSource = position de la question qui est en base
                position_source = existing_question[4]  # 4 correspond à l'index de la colonne "position" dans le résultat
                # PositionDestination = question_data['position']
                position_destination = questionPython.position

                #On test si la position est la même 
                if position_destination == position_source:
                    
                    update_query = "UPDATE QUESTION SET title = ?, text = ?, image = ?, position = ? WHERE id = ?"
                    cursor.execute(update_query, (
                        questionPython.title,
                        questionPython.text,
                        questionPython.image,
                        questionPython.position,
                        questionId
                ))

                    print('good execution of update')
                    # Supprimer les anciennes réponses associées à la question
                    cursor.execute(f"DELETE FROM REPONSE WHERE positionquestion = {position_source}")
                    for answer in questionPython.possible_answers:
                        cursor.execute(
                            "INSERT INTO REPONSE (reponse, booleen, positionquestion) VALUES (?, ?, ?)",
                            (answer['text'], str(answer['isCorrect']), position_source)
                        )

                    return 'Question updated (same position)',204
                else:
                    print("We're switching to another position")
                    # Supprimer la question et ses réponses de la base de données
                    cursor.execute(f"DELETE FROM QUESTION WHERE position = {position_source}")
                    cursor.execute(f"DELETE FROM REPONSE WHERE positionquestion = {position_source}")
                    if position_source > position_destination:
                        print("Question go up")
                        # Ajouter +1 à toutes les questions et réponses ayant une position en base
                        # >= PositionDestination ET < PositionSource
                        cursor.execute(f"UPDATE QUESTION SET position = position + 1 WHERE position >= {position_destination} AND position < {position_source}")
                        cursor.execute(f"UPDATE REPONSE SET positionquestion = positionquestion + 1 WHERE positionquestion >= {position_destination} AND positionquestion < {position_source}")
                    elif position_source < position_destination:
                        print("QUestion go down")
                        # Ajouter -1 à toutes les questions et réponses ayant une position en base
                        # > PositionSource ET <= PositionSource
                        cursor.execute(f"UPDATE QUESTION SET position = position - 1 WHERE position > {position_source} AND position <= {position_destination}")
                        cursor.execute(f"UPDATE REPONSE SET positionquestion = positionquestion - 1 WHERE positionquestion > {position_source} AND positionquestion <= {position_destination}")

                    # Insérer la question mise à jour dans la base de données avec la nouvelle position
                    cursor.execute("INSERT INTO QUESTION (id, title, text, image, position) VALUES (?, ?, ?, ?, ?)",
                        (questionId, questionPython.title, questionPython.text, questionPython.image, questionPython.position)
                    )

                    # Insérer les nouvelles réponses dans la base de données
                    for answer in questionPython.possible_answers:
                        cursor.execute(
                            "INSERT INTO REPONSE (reponse, booleen, positionquestion) VALUES (?, ?, ?)",
                            (answer['text'], str(answer['isCorrect']), position_destination)
                        )
                
                conn.commit()
    
            return 'Question updated (other position)', 204
    except sqlite3.Error as e:
        print("Erreur lors de l'update de la question et ses réponses par ID: ", e)
        return 'An error occurred while fetching the question', 500
    



def deleteById(request, questionId):
    print("Delete question by ID:", questionId)
    try:
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM QUESTION WHERE id = {questionId}")
            question_data = cursor.fetchone()
            if question_data is None:
                return 'Request respond Not Found', 404
            # Suppression des réponses associées à la question
            else:
                # PositionSource = position de la question qui est en base
                position_source = question_data[4]  # 4 correspond à l'index de la colonne "position" dans le résultat
                cursor.execute(f"DELETE FROM REPONSE WHERE positionquestion = (SELECT position FROM QUESTION WHERE id = {questionId})")
                # Suppression de la question
                cursor.execute(f"DELETE FROM QUESTION WHERE id = {questionId}")
                cursor.execute(f"UPDATE QUESTION SET position = position - 1 WHERE position > {position_source} ")
                cursor.execute(f"UPDATE REPONSE SET positionquestion = positionquestion - 1 WHERE positionquestion > {position_source}")

                # Valider la transaction et fermer la connexion à la base de données
                conn.commit()
            return 'Question and its answers deleted successfully', 204
        
    except sqlite3.Error as e:
        print("Erreur lors de la suppression de la question en base de données:", e)
        return 'An error occurred while deleting the question', 500
    

def postParticpation(request):
    print("Adding participation")
    participationJson = request.get_json()
    goodAnswers = getGoodAnswers()[0]
    print(goodAnswers)
    player_name = str(participationJson["playerName"])
    score = 0
    if len(participationJson["answers"]) != len(goodAnswers):
        return "Bad request", 400
    else:
        print("len okay")
        for i in range(len(participationJson["answers"])):
            if goodAnswers[i] == participationJson["answers"][i]:
                score+=1
        try:
            with sqlite3.connect('quiz.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO PARTICIPATION (playername, score) VALUES (?, ?)", (player_name, score))
                
                conn.commit()
                return {"playerName": participationJson["playerName"], "score": score},200
        except sqlite3.Error as e:
            print("Erreur lors de l'insertion de la participation en base de données:", e)
            return 'An error occurred while inserting the participation', 500
        



def getGoodAnswers():
    with sqlite3.connect('quiz.db') as conn:
        cursor = conn.cursor()
        #Récupération du nombre de questions
        query = cursor.execute("SELECT seq FROM sqlite_sequence WHERE name=\"QUESTION\"")
        last_id = query.fetchall()[0][0]
        goodAnswers =[]
        for i in range(1,last_id+1):
            cursor.execute(f"SELECT reponse, booleen FROM REPONSE WHERE positionquestion = {i}")
            reponses_data = cursor.fetchall()
            reponses = [{'text': row[0], 'isCorrect': (row[1] == 'True')} for row in reponses_data]
            # Récupérer la position de la bonne réponse
            for index,reponse in enumerate(reponses): 
                if reponse['isCorrect']:
                    goodAnswers.append(index + 1)

        

        return goodAnswers,200
    


def getScores():
    try:
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PARTICIPATION ORDER BY score DESC")
            scores = cursor.fetchall()
            return {'scores': scores}, 200
        
    except sqlite3.Error as e:
            print("Erreur lors de a récupération des scores:", e)
            return 'An error occurred while getting participations', 500


