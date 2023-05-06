from flask import Flask, request
from flask_cors import CORS
from jwt_utils import build_token, decode_token, JwtError
from questions import json_to_question, insert_question
import hashlib
import sqlite3





app = Flask(__name__)
CORS(app)




@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}, it's rayen"



@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def PostLogin():
	payload = request.get_json()
	password =payload['password'].encode('UTF-8')
	hashedPassword = hashlib.md5(password).digest()
	if hashedPassword == b"\x1d\xec\x84\xba\x18f[\xde\xd8\x84\xe3'r\xe9\x8bq":
		token = build_token()
		return {"token": token},200
	else:
		return 'Unauthorized', 401


@app.route('/questions', methods=['POST'])
def PostQuestion():
	token = request.headers.get('Authorization')
	if token:
		#Récupérer la question depuis le corps de la requête
		question_data = request.get_json()
		
		# Convertir la question JSON en objet Question
		
		question = json_to_question(question_data)
		
		# Insérer la question en base de données
		if insert_question(question):
			return {"id": question.position}, 200
		else:
			return {"error": "Failed to create question"}, 500
	else:
		return 'Unauthorized', 401
	
		

@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions():
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()
        
        # Exécution de la requête de suppression
        cursor.execute("DELETE FROM QUESTION")
        
        # Validation de la transaction
        conn.commit()
        
        # Fermeture de la connexion à la base de données
        cursor.close()
        conn.close()
        
        return 'All questions have been deleted'
        
    except sqlite3.Error as e:
        print("Erreur lors de la suppression des questions en base de données:", e)
        return 'An error occurred while deleting the questions', 500



if __name__ == "__main__":
    app.run()