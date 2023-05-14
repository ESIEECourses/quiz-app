<template>
    <div>
      <!-- Affichez les détails de la question en utilisant les données fournies via les props -->
      <h2>{{ question.questionTitle }}</h2>
      <p>{{ question.questionText }}</p>
  
      <!-- Affichez l'image de la question s'il y en a une -->
      <img class="question-image" v-if="question.image" :src="question.image" />
  
      <!-- Affichez les réponses possibles -->
      <div class="radio-group">
        <label v-for="(answer, index) in question.possibleAnswers" :key="index">
          <input type="radio" :value="index" v-model="selectedAnswerId" :name="`question-${question.id}`" @click="selectAnswer(index)" />
          {{ answer.text }}
        </label>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'QuestionDisplay',
    emits: ["answer-selected"],
    props: {
      question: {
        type: Object
      }
    },
    data() {
      return {
        selectedAnswerId: null
      };
    },
    methods: {
      selectAnswer(index) {
        const selectedAnswerId = index+1;
        this.$emit('answer-selected', selectedAnswerId);
      }
    }
};
  </script>
  
  <style scoped>
  .radio-group {
    display: flex;
    flex-direction: column;
  }
  
  .question-image {
    width: 400px; /* Ajustez la taille selon vos besoins */
    height: 400px;
  }
  </style>
  