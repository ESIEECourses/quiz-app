<template>
  <div>
      <button class='neon' @click="logout">Déconnexion</button>
    </div>
  <div class="form-container">
    
    <p class="title">Edit question</p>
    <form @submit="updateQuestion" class="form">
      <div class="input-group">
        <label for="position">Position</label>
        <input type="number" name="position" id="position" v-model="question.position" placeholder="">
      </div>
      <div class="input-group">
        <label for="titre">Titre</label>
        <input type="text" name="titre" id="titre" v-model="question.title" placeholder="">
      </div>
      <div class="input-group">
        <label for="intitule">Intitulé</label>
        <input name="intitule" id="intitule" v-model="question.text" placeholder="">
      </div>
      <div class="input-group"> 
        <label for="image">Image</label>
        <ImageUpload @file-change="handleImageChange"></ImageUpload>
        <img v-if="question.image" :src="question.image" alt="Preview" class="image-preview">
      </div>
      <div class="input-group">
        <div v-for="(answer, index) in question.possibleAnswers" :key="index">
          
          <label :for="'answer-' + index">Intitulé de la réponse {{ index + 1 }}</label>
          <input
            :name="'answer-text-' + index"
            :id="'answer-text-' + index"
            :value="index"
            type="radio"
            v-model="selectedAnswerIndex"
            :checked="answer.isCorrect"
            @change="updateCorrectAnswer(index)"
            class="answer-radio"
          >
          <input :name="'answer-text-' + index" :id="'answer-text-' + index" v-model="answer.text" placeholder="Intitulé de la réponse" >
        </div>
      </div>
      <div class="button-container">
        <button type="submit" class="neon submit-button">Submit</button>
        <button type="button" class="neon cancel-button" @click="cancelEdit">Annuler</button>
      </div>
    </form>
    
  </div>
  
</template>


<script>
import ImageUpload from "@/components/ImageUpload.vue";
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";
export default {
  data() {
    return {
      question: null,
      selectedAnswerIndex: null
    };
  },
  components: {
      ImageUpload
    },
    mounted() {
    
    const correctAnswerIndex = this.question.possibleAnswers.findIndex(answer => answer.isCorrect);
    if (correctAnswerIndex !== -1) {
      this.selectedAnswerIndex = correctAnswerIndex;
    }
  },
    created() {
      // Récupération des données de la question depuis le stockage local
      const editQuestionData = localStorage.getItem('editQuestionData');
      if (editQuestionData) {
        this.question = JSON.parse(editQuestionData);
        
    }else{
      this.$router.push('/admin/questionlist')
    }
  },
  methods: {
    updateCorrectAnswer(selectedIndex) {
      this.question.possibleAnswers.forEach((answer, index) => {answer.isCorrect = index === selectedIndex;});
  },
    handleImageChange(imageDataUrl) {
            this.question.image = imageDataUrl;
          },
    cancelEdit(){
      localStorage.removeItem('editQuestionData');
      this.$router.push('/admin/questionlist')
    },
    logout(){
      participationStorageService.clear();
      this.$router.push('/admin');
    },
    async updateQuestion(event) {
      event.preventDefault();
      console.log('Mise à jour de la question avec l\'ID', this.question.id);
      console.log('voici ce qu on va envoyer:', this.question)
      const token = participationStorageService.getToken();
      try{
          const response = await quizApiService.updateQuestionById(this.question.id, this.question, token);
          if (response.status === 204){
            console.log('question updated in BD');
            this.$router.push('/admin/questionlist')
          }
      }catch(error){
            console.error('Erreur lors de la requête API', error);
          }
      }
  }
    
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


  .button-container {
      display: flex;
      justify-content: space-between;
      margin-top: 1.5rem;
    }
  
    .submit-button,
    .cancel-button {
      flex-basis: 45%; /* Ajustez la taille selon vos besoins */
      margin-right: 1rem; /* Ajoute une marge entre les boutons */
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
    .image-preview {
    max-width: 200px;
    max-height: 200px;
  }
    .form-container {
      justify-content: center;
      width: 500px;
      border-radius: 0.75rem;
      background-color: rgba(17, 24, 39, 1);
      padding: 2rem;
      color: rgba(243, 244, 246, 1);
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
    
  
    .line {
      height: 1px;
      flex: 1 1 0%;
      background-color: rgba(55, 65, 81, 1);
    }
</style>