import json
import sqlite3

#Création de la class question
class Question:
    def __init__(self, title, text, image, position, possible_answers):
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.possible_answers = possible_answers


def question_to_json(question):
    return json.dumps({
        'title': question.title,
        'text': question.text,
        'image': question.image,
        'position': question.position,
        'possibleAnswers': question.possible_answers
    })

def json_to_question(json_data):
    json_databis = json.dumps(json_data)
    data = json.loads(json_databis)
    return Question(
        title=data['title'],
        text=data['text'],
        image=data['image'],
        position=data['position'],
        possible_answers=data['possibleAnswers']
    )




# Fonction pour insérer une question en base de données
def insert_question(question):
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()

        #Puisque le stockage d'une liste est impossible on remet en forme la liste des réponses
        possible_answers_json = json.dumps(question.possible_answers)
        
        # Exécution de la requête d'insertion
        cursor.execute(
            "INSERT INTO QUESTION (title, text, image, position, possibleAnswers) "
            "VALUES (?, ?, ?, ?, ?)",
            (question.title, question.text, question.image, question.position, possible_answers_json)
        )
        
        # Validation de la transaction
        conn.commit()
        
        # Fermeture de la connexion à la base de données
        conn.close()
        
        return True  # Indique que l'insertion a réussi
        
    except sqlite3.Error as e:
        print("Erreur lors de l'insertion de la question en base de données:", e)
        return False  # Indique que l'insertion a échoué
