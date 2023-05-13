
#EndPoint pour supprimer toutes les questions si on est connecté 
@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions():
	token = request.headers.get('Authorization')
	if token:
		try:
			# Connexion à la base de données
			conn = sqlite3.connect('quiz.db')
			cursor = conn.cursor()
			
			# Exécution de la requête de suppression
			cursor.execute("DELETE FROM QUESTION")
			cursor.execute("DELETE FROM REPONSE")
			
			# Validation de la transaction
			conn.commit()
			
			# Fermeture de la connexion à la base de données
			cursor.close()
			conn.close()
			
			return 'All questions have been deleted', 204
			
		except sqlite3.Error as e:
			print("Erreur lors de la suppression des questions en base de données:", e)
			return 'An error occurred while deleting the questions', 500
	else:
		return 'Unauthorized', 401
	



'''FIN PARTIE 1'''

#************************************************************************#

'''Début PARTIE 2'''
# EndPoint pour récupérer une question par ID
@app.route('/questions/id/<questionId>', methods=['GET'])
def get_question_by_id(questionId):
	return getById(questionId)

# EndPoint pour UPDATE une question par ID
@app.route('/questions/id/<questionId>', methods=['PUT'])
def update_question(questionId):
    token = request.headers.get('Authorization')
    if token:
        return updateById(questionId)
    else:
        return 'Unauthorized', 401

#EndPoint pour supprimer une question et ses réponses en fonction de son ID
@app.route('/questions/id/<questionId>', methods=['DELETE'])
def delete_question(questionId):
	token = request.headers.get('Authorization')
	if token:
		return deleteById(questionId)
	else:
		return 'Unauthorized', 401


#EndPoint pour réordonner une question et ses réponses en fonction de son ID
@app.route('/questions/id/<questionId>/<positionDest>', methods=['PUT'])
def reoder_question(questionId, positionDest):
	token = request.headers.get('Authorization')
	if token:
		return reoderById(questionId, positionDest)
	else:
		return 'Unauthorized', 401

'''FIN PARTIE 2'''

#************************************************************************#

'''Début PARTIE 3'''
# EndPoint pour récupérer une question par Position
@app.route('/questions/position/<questionPosition>', methods=['GET'])	
def get_question_by_position(questionPosition):
	return getByPosition(questionPosition)

'''FIN PARTIE 3'''







def updateById(questionId):
    try:
        # Récupérer les données de la question depuis le corps de la requête
        question_data = request.get_json()
        questionPy = Question.json_to_question(json.dumps(question_data))

        # Vérifier si la question existe dans la base de données
        with sqlite3.connect('quiz.db') as conn:
            cursor = conn.cursor()

            # Exécuter une requête SELECT pour vérifier l'existence de la question
            cursor.execute(f"SELECT * FROM QUESTION WHERE id = {questionId}")
            existing_question = cursor.fetchone()
            if existing_question is None:
                return 'Request respond Not Found', 404
            else:
                # PositionSource = position de la question qui est en base
                position_source = existing_question[4]  # 4 correspond à l'index de la colonne "position" dans le résultat
                # PositionDestination = question_data['position']
                position_destination = question_data['position']
                if position_destination == position_source:
                    # Mettre à jour les données de la question dans la base de données
                    cursor.execute(f"UPDATE QUESTION SET title = {question_data['title']}, text = {question_data['text']}, image = {question_data['image']}, position = {question_data['position']} WHERE id = {questionId}")

                    # Supprimer les anciennes réponses associées à la question
                    cursor.execute(f"DELETE FROM REPONSE WHERE positionquestion = {question_data['position']}")
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




    


