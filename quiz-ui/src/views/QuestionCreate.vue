<template>
  <div class="form-container">
    <p class="title">Create question</p>
    <form @submit="createQuestion" class="form">
      <div class="input-group">
        <label for="position">Position</label>
        <input type="number" name="position" id="position" v-model="question.position" :min=1 :max="numberOfQuestions+1"  placeholder="" required>
      </div>
      <div class="input-group">
        <label for="titre">Titre</label>
        <input type="text" name="titre" id="titre" v-model="question.title" placeholder="" required>
      </div>
      <div class="input-group">
        <label for="intitule">Intitulé</label>
        <input name="intitule" id="intitule" v-model="question.text" placeholder="" required>
      </div>
      <div class="input-group">
        <label for="image">Image</label>
        <ImageUpload @file-change="handleImageChange"></ImageUpload>
        <img v-if="question.image" :src="question.image" alt="Preview" class="image-preview" >
      </div>
      <div v-for="(answer, index) in question.possibleAnswers" :key="index" class="input-group">
        <label :for="'answer-' + index">Réponse {{ index + 1 }}</label>
        <input type="radio" :name="'answer'" :id="'answer-' + index" :value="index" v-model="selectedAnswerIndex" required>
        <input name="intitule" :id="'answer-text-' + index" v-model="answer.text" placeholder="Intitulé de la réponse" required>
      </div>
      <div class="button-container">
        <button type="submit" class="neon submit-button">Submit</button>
        <button type="button" class="neon cancel-button" @click="cancelCreate">Annuler</button>
      </div>
    </form>
  </div>
</template>
  
  <script>
  import quizApiService from "@/services/QuizApiService";
  import participationStorageService from "@/services/ParticipationStorageService";
  import ImageUpload from "@/components/ImageUpload.vue";
  
  export default {
    data() {
      return {
        selectedAnswerIndex: null,
        numberOfQuestions: 0,
        question: {
          position: null,
          title: '',
          text: '',
          image: null,
          possibleAnswers: [
            { text: "", isCorrect: false },
            { text: "", isCorrect: false },
            { text: "", isCorrect: false },
            { text: "", isCorrect: false }
          ]
        }
      };
    },
    name: 'QuestionCreate',
    components: {
      ImageUpload
    },
    created() {
    this.getNumberOfQuestions(); 
    this.checkAdminLogin();
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
      async createQuestion(event) {
        event.preventDefault();
        console.log('Création de la question');
        this.question.possibleAnswers.forEach((answer, index) => {
          answer.isCorrect = (index === this.selectedAnswerIndex);
        });
        const token = participationStorageService.getToken();
        console.log("La nouvelle question: ", this.question)
        try {
          const response = await quizApiService.addNewQuestion(this.question, token);
          if (response.status === 200) {
            console.log('Question created in BD');
            this.$router.push('/admin/questionlist');
          }
        } catch (error) {
          console.error('Erreur lors de la requête API', error);
        }
      },
      handleImageChange(imageDataUrl) {
        this.question.image = imageDataUrl;
      },
      cancelCreate() {
        this.$router.push('/admin/questionlist');
      },
      async getNumberOfQuestions(){
        const quizInfo = await quizApiService.getQuizInfo();
        this.numberOfQuestions = quizInfo.data.size;
        

      }

    }
  };
  </script>
  
  <style scoped>
 .form-container {
    justify-content: center;
    width: 500px;
    border-radius: 0.75rem;
    background-color: rgba(17, 24, 39, 1);
    margin-top: 50px;
    padding: 2rem;
    color: rgba(243, 244, 246, 1);
  }

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
  .title {
    text-align: center;
    font-size: 1.5rem;
    line-height: 2rem;
    font-weight: 700;
  }
  
  .form {
    margin-top: 1.5rem;
  }
  
  .input-group {
    margin-top: 0.25rem;
    font-size: 0.875rem;
    line-height: 1.25rem;
  }
  
  .input-group label {
    display: block;
    color: rgba(156, 163, 175, 1);
    margin-bottom: 4px;
  }
  
  .input-group input {
    width: 100%;
    border-radius: 0.375rem;
    border: 1px solid rgba(55, 65, 81, 1);
    outline: 0;
    background-color: rgba(17, 24, 39, 1);
    padding: 0.75rem 1rem;
    color: rgba(243, 244, 246, 1);
  }
  
  .input-group input:focus {
    border-color: #03e9f4;
  }
  
  
  
  
  
  .submit {
    margin-top:1%;
    display: block;
    width: 100%;
    background-color: #03e9f4;
    padding: 0.75rem;
    text-align: center;
    color: rgba(17, 24, 39, 1);
    border: none;
    border-radius: 0.375rem;
    font-weight: 600;
  }
  
  </style>
  