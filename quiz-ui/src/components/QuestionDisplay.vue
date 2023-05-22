<template>
   <div class="heading"><span>{{ question.questionTitle }}</span></div>

   <div class="row">
    <div class="column">
      <img class="question-image" v-if="question.image" :src="question.image" />
    </div>
    <div class="column">
      <div>
        <p> {{question.questionText }}</p>
      </div>
      <div>
        <div class="radio-group">
          <div class="answer-item" v-for="(answer, index) in question.possibleAnswers" :key="index" @click="selectAnswer(index)">
            <a>{{ answer.text }}</a>
          </div>
        </div>
      </div>
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

.heading {
  display: flex;
  flex-direction: column;
  font-size: 1.3rem;
  justify-content: center;
  align-items: center;
  user-select: none;
  padding-top: 100px;
}
  .centered-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
}

.question-image {
  width: 200px; /* Ajustez la taille selon vos besoins */
  height: 200px;
}

.radio-group {
  display: grid;
  grid-template-columns: repeat(2, 1fr);

}

.answer-item {
  margin-bottom: 10px;
  width: 300px;
  height: 150px;
  background-color: #3a3a3a;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: bold;
  font-size: 18px;
  margin: 10px;
  cursor: pointer;
  text-align: center; /* Alignement du texte au centre */
}

.answer-item a {
  text-decoration: none; /* Supprimer la décoration du lien */
  color: #fff; /* Couleur du texte */
}

.answer-item:hover {
  background-color: #555555; /* Couleur de fond au survol */
}

.answer-item input[type="radio"] {
  margin-right: 5px;
}

.questions-block{
  display: flex;
  justify-content: center;
  text-align: center;
}

.row {
  margin-top:  5%;
  display: flex;
}

.column {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex: 50%;
}
.answers{
  font-size: 1.1rem;
    background: #fff;
    border-radius: 4px;
    transition: .3s;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    color: #000;
    width: 100%;
    cursor: default;
    box-shadow: 0 0 4px #2e2e4a;
}

span {
  font-size: 3rem;
  text-transform: uppercase;
  letter-spacing: 0.4rem;
  text-shadow: 0 0 19px rgba(255, 255, 255, 0.695), 0 0 20px rgba(255, 255, 255, 0.568), 0 0 30px #1a0e34, 0 0 40px #03e9f4, 0 0 50px #2c26729f, 0 0 60px #180e5c5c, 0 0 70px #101d3548;
  border-radius: 70%;
  padding: 0.5rem;
  position: relative;
}

  
</style>

<!--<div class="questions-block">
      <p><p>{{this.selectedAnswerId}}</p> {{question.questionText }}</p>
      <img class="question-image" v-if="question.image" :src="question.image" />
  
     
      <div class="radio-group">
        <label v-for="(answer, index) in question.possibleAnswers" :key="index" class="answer-item">
          <input type="radio" :value="index" v-model="selectedAnswerId" :name="`question-${question.id}`" @click="selectAnswer(index)" />
          {{ answer.text }}
        </label>
      </div>-->
