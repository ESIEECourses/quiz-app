<template>
  <div class="question-list-container">
    <div>
      <button class='neon button-margin' @click="logout">Déconnexion</button>
      <button class='neon button-margin' @click="deleteAllQuestions">Supprimer toutes les questions</button>
      <button class='neon button-margin' @click="deleteAllParticipations">Supprimer toutes les participations</button>
      <button class='neon button-margin' @click="addQuestion">Ajouter une question</button>
    </div>

    <table class="question-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>Image</th>
          <th>Titre</th>
          <th>Texte</th>
          <th>Réponses</th>
          <th v-if="selectedQuestion !=null">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="question in filteredQuestions"
          :key="question.id"
          class="question-item"
          @click="handleRowClick(question.id)"
        >
          <td>{{ question.position }}</td>
          <td>
            <img :src="question.image" alt="Image de la question" class="image" />
          </td>
          <td>{{ question.title }}</td>
          <td>{{ question.text }}</td>
          <td>
            <ul>
              <li v-for="answer in question.possibleAnswers" :key="answer.id" :class="{ 'correct-answer': answer.isCorrect }">
                {{ answer.text }}
              </li>
            </ul>
          </td>
          <td v-if="selectedQuestion !=null">
            <button class="neon edit-button" @click="editQuestion(question.id)">Modifier</button>
            <button class="neon delete-button" @click="deleteQuestion(question.id)">Supprimer</button>

          </td>
        </tr>
      </tbody>
    </table>
    <button v-if="selectedQuestion !=null" class="neon return-button" @click="resetSelection">Retour</button>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService.js";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: 'QuestionList',
  data() {
    return {
      selectedQuestion: null,
      selectedQuestionId: null,
      isAdminLoggedIn: false, 
      questionsData: [],
    };
  },
  computed: {
    filteredQuestions() {
      return this.selectedQuestion ? [this.selectedQuestion] : this.questionsData;
    },
  },

  methods: {
   
    checkAdminLogin() {
      this.isAdminLoggedIn = participationStorageService.getToken();
      if(this.isAdminLoggedIn == null){
        this.$router.push('/admin');
      }else{
        console.log('token:', this.isAdminLoggedIn)
      }
     
    },
    logout(){
      participationStorageService.clear();
      this.$router.push('/admin');
    },
    async getQuestions() {
      const quizInfo = await quizApiService.getQuizInfo();
      const numberOfQuestions = quizInfo.data.size;

      for (let position = 1; position <= numberOfQuestions; position++) {
            const question = await quizApiService.getQuestionByPosition(position);
            const existingQuestion = this.questionsData.find(q => q.id === question.data.id);
            if (!existingQuestion) {
              console.log(question.data)
              this.questionsData.push(question.data);
            }
          }
    },
    handleRowClick(questionId) {
      this.selectedQuestion = this.questionsData.find(question => question.id === questionId);
      console.log('question selected:', this.selectedQuestion )
    },
    editQuestion(questionId) {
      localStorage.setItem('editQuestionData', JSON.stringify(this.selectedQuestion));
      this.$router.push(`/admin/question/edit/${questionId}`);
    },
    async deleteAllQuestions(){
        const token = participationStorageService.getToken();
        console.log(token);
        try {
          const response = await quizApiService.deleteAllQuestion(token);
          if (response.status === 204){
            console.log('deleted questions all');
            this.questionsData = []; 
            this.selectedQuestion = null; 
            this.getQuestions();
          }
        }catch (error) {
        console.error('Erreur lors de la requête API', error);
      }
    },
    async deleteAllParticipations(){
        const token = participationStorageService.getToken();
        try {
          const response = await quizApiService.deleteAllParticipation(token);
          if (response.status === 204){
            console.log('deleted participations all')
            
          }
        }catch(error) {
            console.error('Erreur lors de la requête API', error);
  
        }
      },
      addQuestion(){
        this.$router.push('/admin/question/add');
      },
      async deleteQuestion(questionId){
        const token = await participationStorageService.getToken();
        try{
          const response = await quizApiService.deleteOneQuestionById(questionId, token);
          if (response.status === 204) {
            console.log(`Question avec l'ID ${questionId} supprimée.`);
            this.questionsData = this.questionsData.filter(question => question.id !== questionId);
            this.selectedQuestion = null;
          }
        }catch (error) {
          console.error('Erreur lors de la requête API', error);
        }
      },

    resetSelection() {
      this.selectedQuestion = null;
    },
    // Redirection vers la liste des questions si l'administrateur est connecté
    redirectToQuestionList() {
      if (this.isAdminLoggedIn) {
        this.$router.push('/admin/questionlist');
      }
    },
  },
  created() {
    // Vérification de la connexion de l'administrateur lors de la création du composant
        this.checkAdminLogin();
      // Redirection vers la liste des questions si l'administrateur est connecté
      this.redirectToQuestionList();
      // Récupération des questions
      this.getQuestions();
  },
};
</script>

<style scoped>

.neon{

padding: 25px 30px;
background-color: #333;
color: #03e9f4;
font-weight: bold;
border: none;
border-radius: 5px;
letter-spacing: 4px;
overflow: hidden;
transition: 0.5s;
cursor: pointer;
}


button:hover{
  background: #03e9f4;
  color: #050801;
  box-shadow: 0 0 5px #03e9f4,
              0 0 25px #03e9f4,
              0 0 50px #03e9f4,
              0 0 200px #03e9f4;
   -webkit-box-reflect:below 1px linear-gradient(transparent, #0005);
}
.question-list-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.question-table {
  border-collapse: collapse;
  width: 100%;
}

.question-table th,
.question-table td {
  text-align: center;
  border: 1px solid black;
  padding: 10px;
}

.question-item .image {
  max-width: 200px;
  max-height: 200px;
}

.question-list-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.question-table ul {
  padding-left: 0;
  margin: 0;
}

.question-table li {
  list-style: none;
  margin-bottom: 5px;
}

.question-table li:before {
  content: '';
  display: inline-block;
  width: 10px;
  height: 10px;
  background-color: black;
  margin-right: 5px;
  vertical-align: middle;
}

.correct-answer {
  font-weight: bold;
  color: #03e9f4;
}
.edit-button,
.delete-button {
  padding: 10px 15px; 
  margin-right: 10px; 
}

.return-button{
  margin-top: 5%
}
</style>
