from flask import Flask, request
from flask_cors import CORS
from jwt_utils import build_token, decode_token, JwtError
from questions import *
import hashlib
import sqlite3





app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}, it's rayen"

'''
# Début de la créations des différents EndPoints 
# 1ère Partie: info score +connexion+ ajout des questions et réponses en BD + suppression data de la bdd
# 2ème Partie: endpoints liés à l'ID des questions 
# 3ème Partie: endpoints liés à la POSITION des questions 
'''

'''Début PARTIE 1'''
#EndPoint pour récupérer les scores
@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

#EndPoint pour récupérer les scores
@app.route('/rebuild-db', methods=['POST'])
def rebuild_bd():
	return retrieveBD()
	'''token = request.headers.get('Authorization')
	if token:
		return retrieveBD()
	else:
		return 'Unauthorized', 401'''
	
	

#EndPoint pour se connecter en tant qu'admin avec MDP haché 
@app.route('/login', methods=['POST'])
def PostLogin():
	payload = request.get_json()
	password =payload['password'].encode('UTF-8')
	hashedPassword = hashlib.md5(password).digest()
	if hashedPassword == b"\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@":
		token = build_token()
		return {"token": token},200
	else:
		return 'Unauthorized', 401

#EndPoint pour ajouter une question dans la BDD  TEST OK
@app.route('/questions', methods=['POST'])
def PostQuestion():
	token = request.headers.get('Authorization')
	if token:
		# Récupérer la question depuis le corps de la requête
		question_data = request.get_json()
		# Convertir la question JSON en objet Question
		question = Question.json_to_question(json.dumps(question_data))
		
		if insert_question_reponse(question):
			return {"id": question.position}, 200
		else:
			return {"error": "Failed to create question"}, 500
	else:
		return 'Unauthorized', 401
	


'''
10/05/2023

MAJ RESPECT DES TESTS DE LA COLLECTION POSTMAN
'''

# EndPoint delete question - unauthorized  TEST OK
'''@app.route('/questions/1', methods=['DELETE'])
def delete_first_question():
	token = request.headers.get('Authorization')
	if token:
		return deleteq1()
	else:
		return 'Unauthorized', 401'''


# EndPoint delete all question - unauthorized  TEST OK
@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions():
	token = request.headers.get('Authorization')
	if token:
		return deleteallq()
	else:
		return 'Unauthorized', 401



# EndPoint Delete all participations TEST OK
@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations():
	token = request.headers.get('Authorization')
	if token:
		return deleteallp()
	else:
		return 'Unauthorized', 401


# EndPoint Get question by id TEST OK
@app.route('/questions/<questionId>', methods=['GET'])
def get_question_by_id(questionId):
	return getById(questionId)
	

# EndPoint Update question TEST OK
@app.route('/questions/<questionId>', methods=['PUT'])
def update_question(questionId):
	token = request.headers.get('Authorization')
	if token:
		return updateById(questionId)
	else:
		return 'Unauthorized', 401


    
# EndPoint Get question by position TEST OK
@app.route('/questions', methods=['GET'])
def get_question_at_position_2():
	position = request.args.get('position')
	return getquestionposition(position)
	

    


# EndPoint Delete question TEST OK
@app.route('/questions/<questionId>', methods=['DELETE'])
def delete_question_by_id(questionId):
	token = request.headers.get('Authorization')
	if token:
		return deleteById(questionId)
	else:
		return 'Unauthorized', 401

if __name__ == "__main__":
    app.run()