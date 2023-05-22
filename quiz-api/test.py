'''from flask import request
from jwt_utils import decode_token
from classQuestions import *
import json
import sqlite3



def update_by_id(request, question_id):
    print("Update data by ID: ", questionId)
    #Récupération du body dans la requête 
    questionJson = request.get_json()
    questionPython = Question.json_to_question(json.dumps(questionJson))
        
    #Ajout de la question en base
    try:
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()
            #Requête pour vérifier l'existence de cet ID 
            #Si la question n'existe pas:
                #return 'Request respond Not Found', 404
            #Sinon: 
                #Stocké la position de la question à l'ID en cours
                #Stocké  la position de l'update (questionPython.position)

                # Si ces deux position sont égales on fait juste un update des deux tables:
                    #update_query = "UPDATE QUESTION SET title = ?, text = ?, image = ?, position = ? WHERE id = ?"
                    #    cursor.execute(update_query, (
                    #        questionPython.title,
                    #        questionPython.text,
                    #        questionPython.image,
                    #        questionPython.position,
                    #        questionId
                    #    ))  
                    #    cursor.execute(f"DELETE FROM REPONSE WHERE positionquestion = {position_source}")
                    #    for answer in questionPython.possible_answers:
                    #        cursor.execute(
                    #            "INSERT INTO REPONSE (reponse, booleen, positionquestion) VALUES (?, ?, ?)",
                    #            (answer['text'], str(answer['isCorrect']), position_destination)
                    #        )
                    #
                    #    print('good execution of update')
                    #
                #Sinon:
                    # Il faut que la question prenne la place de la question à la position de l'update 
                    #Il faut déplacer les autres questions en conséquence et aussi leur réponse 
                    #Concernant les réponses la table contient une colonne positionquestion
                    # Il faut donc que les réponses restent liées à leur question

    except sqlite3.Error as e:
            print("Erreur lors de l'update de la question:", e)
            return 'An error occurred while updating the question', 500
    







    VERSION DANS LE BACKEND

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
                    cursor.execute(f"DELETE FROM REPONSE WHERE positionquestion = {position_source}")
                    for answer in questionPython.possible_answers:
                        cursor.execute(
                            "INSERT INTO REPONSE (reponse, booleen, positionquestion) VALUES (?, ?, ?)",
                            (answer['text'], str(answer['isCorrect']), position_destination)
                        )

                    print('good execution of update')
                    
                else:
                    print("We're switching to another position")
                    # Supprimer la question et ses réponses de la base de données
                    cursor.execute(f"DELETE FROM QUESTION WHERE id = {position_source}")
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
                    cursor.execute("INSERT INTO QUESTION (title, text, image, position) VALUES (?, ?, ?, ?)",
                        (questionPython.title, questionPython.text, questionPython.image, position_destination)
                    )

                # Insérer les nouvelles réponses dans la base de données
                    for answer in questionPython.possible_answers:
                        cursor.execute(
                            "INSERT INTO REPONSE (reponse, booleen, positionquestion) VALUES (?, ?, ?)",
                            (answer['text'], str(answer['isCorrect']), position_destination)
                        )
                
                conn.commit()
    
            return 'Question updated', 204
    except sqlite3.Error as e:
        print("Erreur lors de l'update de la question et ses réponses par ID: ", e)
        return 'An error occurred while fetching the question', 500'''