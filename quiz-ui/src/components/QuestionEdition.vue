<template>
  <div class="form-container">
    <p class="title">Edit question</p>
    <form @submit="updateQuestion" class="form">
      <div class="input-group">
        <label for="position">Position</label>
        <input type="number" name="position" id="position" v-model="question.position" :min="1" :max="questionsDataLength" placeholder="">
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
      <div v-for="(answer, index) in question.possibleAnswers" :key="index">
        <div class="input-group">
          <label :for="'answer-' + index">Intitulé de la réponse {{ index + 1 }}</label>
          <input
            type="radio"
            :name="'answer-' + index"
            :id="'answer-' + index"
            :value="index"
            v-model="selectedAnswerIndex"
          >
          <input :name="'answer-text-' + index" :id="'answer-text-' + index" v-model="answer.text" placeholder="Intitulé de la réponse">
        </div>
      </div>
      <div class="button-container">
        <button type="submit" class="neon submit-button">Submit</button>
        <button class="neon cancel-button" @click="cancelEdit">Annuler</button>
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
      
      // ...
    };
  },
  name: 'QuestionEdition',
  components: {
    ImageUpload
  },
  props: {
    question: {
      type: Object,
      required: true
    },
    questionsDataLength: {
      type: Number,
      required: true
    }
  },
  computed: {
    getAnswerText: {
      get() {
        return index => this.question.possibleAnswers[index].text;
      },
      set() {
        return (index, value) => {
          this.question.possibleAnswers[index].text = value;
        };
      }
    }
  },
  methods: {
    async updateQuestion(event) {
      event.preventDefault();
      console.log('Mise à jour de la question avec l\'ID', this.question.id);
      const token = participationStorageService.getToken();
      try{
        const response = await quizApiService.updateQuestionById(this.question.id, this.question, token);
        if (response.status === 204){
          console.log('question updated in BD');
          this.updatedQuestion = true;
          setTimeout(() => {
            this.updatedQuestion = false;
          }, 3000); 
        }
      }catch(error){
        console.error('Erreur lors de la requête API', error);
      }

      console.log("on va envoyer cet objet", this.question)
    },
    handleImageChange(imageDataUrl) {
      this.question.image = imageDataUrl;
    },
    imageFileChangedHandler(b64String) {
      this.question.image = b64String;
    },
    cancelEdit() {
      this.$emit('cancel-edit');
    },
    
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
  
  .social-message {
    display: flex;
    align-items: center;
    padding-top: 1rem;
  }
  
  .line {
    height: 1px;
    flex: 1 1 0%;
    background-color: rgba(55, 65, 81, 1);
  }
  
  .social-message .message {
    padding-left: 0.75rem;
    padding-right: 0.75rem;
    font-size: 0.875rem;
    line-height: 1.25rem;
    color: rgba(156, 163, 175, 1);
  }
  
  .social-icons {
    display: flex;
    justify-content: center;
  }
  
  .social-icons .icon {
    border-radius: 0.125rem;
    padding: 0.75rem;
    border: none;
    background-color: transparent;
    margin-left: 8px;
  }
  
  .social-icons .icon svg {
    height: 1.25rem;
    width: 1.25rem;
    fill: #fff;
  }
  
  .signup {
    text-align: center;
    font-size: 0.75rem;
    line-height: 1rem;
    color: rgba(156, 163, 175, 1);
  }
  
  </style>
  