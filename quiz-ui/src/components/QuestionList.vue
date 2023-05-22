<template>
  <div class="question-list-container">
    <table class="question-table">
      <thead>
        <tr>
          <th>Position</th>
          <th>Image</th>
          <th>Titre</th>
          <th>Texte</th>
          <th>Réponses</th>
          <th v-if="selectedQuestionId">Actions</th>
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
          <td v-if="selectedQuestionId">
            <button class="neon edit-button" @click="editQuestion(question.id)">Modifier</button>
            <button class="neon delete-button" @click="deleteQuestion">Supprimer</button>

          </td>
        </tr>
      </tbody>
    </table>
    <button v-if="selectedQuestionId" class="neon return-button" @click="resetSelection">Retour</button>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService.js";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: 'QuestionsList',
  props: {
    questionsData: {
      type: Array,
      required: true,
    },
    displayQuestionId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      selectedQuestionId: null,
    };
  },
  methods: {
    editQuestion(questionId) {
      console.log("Dans QuestionList.vue la fonction editQuestion est appelée :", questionId);
      this.$emit('edit-question', questionId);
    },
    async questions() {
      
      try {
        const quizInfo = await quizApiService.getQuizInfo();
        const numberOfQuestions = quizInfo.data.size;
        for (let position = 1; position <= numberOfQuestions; position++) {
          const question = await quizApiService.getQuestionByPosition(position);
          const existingQuestion = this.questionsData.find(q => q.id === question.data.id);
          if (!existingQuestion) {
            this.questionsData.push(question.data);
            console.log(this.questionsData);
          }
          
          
        }
      } catch (error) {
        console.error('Erreur lors de la récupération des questions', error);
      }
      console.log("Les réponses sont correctement importées et la taille de QuestionsData est ", this.questionsData.length);
      
    },
    handleRowClick(questionId) {
      this.selectedQuestionId = questionId;
      console.log(`La réponse de la question ${questionId} a été sélectionnée.`);
    },
   
    async deleteQuestion() {
  console.log(`Supprimer la question avec l'ID ${this.selectedQuestionId}`);
  try {
    const token = await participationStorageService.getToken();
    const response = await quizApiService.deleteOneQuestionById(this.selectedQuestionId, token);
    if (response.status === 204) {
      console.log(`Question avec l'ID ${this.selectedQuestionId} supprimée.`);
      // Créer une copie modifiable de questionsData
      const index = this.questionsData.findIndex(question => question.position === this.selectedQuestionId);
      if (index !== -1) {
        // Supprimer la question de questionsData à l'index trouvé
        this.questionsData.splice(index, 1);
      }
      this.resetSelection();
      location.reload(); // Appel de la méthode pour réinitialiser la sélection
    }
  } catch (error) {
    console.error('Erreur lors de la requête API', error);
  }
},
    resetSelection() {
      this.selectedQuestionId = null;
    },
  },
  computed: {
    filteredQuestions() {
      if (this.selectedQuestionId) {
        return this.questionsData.filter(question => question.id === this.selectedQuestionId);
      } else {
        return this.questionsData;
      }
    },
  },
  mounted() {
    this.questions();
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
