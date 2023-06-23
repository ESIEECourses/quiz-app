from flask import Flask, request
from flask_cors import CORS
from jwt_utils import build_token, decode_token, JwtError
from questions import *
import hashlib
import sqlite3


#HELLO WORLD

app = Flask(__name__)
CORS(app)


#Endpoint Racine
@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}, it's rayen"

#EndPoint rebuild-bd
@app.route('/rebuild-db', methods=['POST'])
def rebuild_bd():
	token = request.headers.get('Authorization')
	if(goodToken(token)):
		return retrieveBD()
	else:
		return 'Unauthorized', 401

#EndPoint pour récupérer les informations sur le quizz
@app.route('/quiz-info', methods=['GET'])
def get_quizz_info():
	return getQuizInfo()

# EndPoint delete all questions
@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions():
	token = request.headers.get('Authorization')
	if(goodToken(token)):
		return deleteall()
	else:
		return 'Unauthorized', 401

# EndPoint delete all participations 
@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations():
	token = request.headers.get('Authorization')
	if(goodToken(token)):
		return deleteallparticipations()
	else:
		return 'Unauthorized', 401
	

#Endpoint login 
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


#Endpoint ajout question
@app.route('/questions', methods=['POST'])
def PostQuestion():
	token = request.headers.get('Authorization')
	if(goodToken(token)):
		return insert_question_reponses(request)
	else:
		return 'Unauthorized', 401
	
#Endpoint récupération d'une question et ses réponses par position
@app.route('/questions', methods=['GET'])
def get_question_at_position():
	position = request.args.get('position')
	return getQuestionByPosition(position)

#Endpoint get d'une question et ses réponses par ID
@app.route('/questions/<questionId>', methods=['GET'])
def get_question_by_id(questionId):
	return getById(questionId)

#Endpoint update d'une question et ses réponses par ID
@app.route('/questions/<questionId>', methods=['PUT'])
def update_question_by_id(questionId):
	token = request.headers.get('Authorization')
	if(goodToken(token)):
		return updateById(request, questionId)
	else:
		return 'Unauthorized', 401
	

#Endpoint delete d'une question et ses réponses par ID
@app.route('/questions/<questionId>', methods=['DELETE'])
def delete_question_by_id(questionId):
	token = request.headers.get('Authorization')
	if(goodToken(token)):
		return deleteById(request, questionId)
	else:
		return 'Unauthorized', 401


#Endpoint participations 
@app.route('/participations', methods=['POST'])
def post_participation():
	return postParticpation(request)
	

@app.route('/answers', methods=['GET'])
def getAnswers():
	return getGoodAnswers()

@app.route('/classement', methods=['GET'])
def get_scores():
	return getScores()



if __name__ == "__main__":
    app.run()