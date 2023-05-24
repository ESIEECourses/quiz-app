<template>
    
      <div class="heading"><span>Experience the Future Today</span></div>
      <!---->
      <div class="start-quiz">
        <router-link to="/start-new-quiz-page">
          <button class="neon">
            START QUIZ
          </button>
        </router-link>
      </div>
      
      <div v-if="registeredScores.length === 0" class="no-score">
        <span class="text">No one in the matrice </span>
      </div>
      <div class="score-grid" v-else>
        <div class=" first-score" :key="0">
          <img src="/src/assets/gold-cup.png" alt="Gold Trophy" class="trophy-image"/>
          {{ topScores[0].playerName }} - {{ topScores[0].score }}
        </div>
        <div class="second-third-score">
        <div v-for="(scoreEntry, index) in topScores.slice(1)" :key="index + 1" class="score-item">
          <img v-if="index === 0" src="/src/assets/silver-cup.png" alt="Silver Trophy" class="trophy-image" />
          <img v-else-if="index === 1" src="/src/assets/bronze-cup.png" alt="Bronze Trophy" class="trophy-image"/>
          {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
        </div>
        </div>
      </div>
    
</template>


<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: []
    };
  },
  
  async created() {
    console.log("Composant Home page 'created'");
    try {
      const response = await quizApiService.getQuizInfo();
      if (response.status === 200) {
        this.registeredScores = response.data.scores;

      } else {
        console.error("Erreur lors de la récupération des scores du quiz");
      }
    } catch (error) {
      console.error("Erreur lors de la requête API", error);
    }
  },
  computed: {
    topScores() {
      return this.registeredScores.slice(0, 3); // Récupérer uniquement les trois premiers scores
    }
  },
};
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;700&display=swap');

.start-quiz{
  margin-top: 5%;
  display: flex;
  justify-content: center;
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

button:hover{
    background: #03e9f4;
    color: #050801;
    box-shadow: 0 0 5px #03e9f4,
                0 0 25px #03e9f4,
                0 0 50px #03e9f4,
                0 0 200px #03e9f4;
     -webkit-box-reflect:below 1px linear-gradient(transparent, #0005);
}
.trophy-image {
  max-width: 50px; /* Ajustez la largeur maximale selon vos besoins */
}

li {
    list-style-type: none;
  }
.score-grid {
  align-items: center;
  padding-top: 50px;
  padding-bottom: 50px;
}


.score-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 25px;
  padding-left: 25px;
  padding-right: 25px;
  margin-bottom: 25px;
}

.first-score{
  display: flex;
  flex-direction: column;
  align-items: center;
}
.second-third-score{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.heading {
  display: flex;
  flex-direction: column;
  font-size: 1.3rem;
  justify-content: center;
  align-items: center;
  user-select: none;
  padding-top: 100px;
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

.text{
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.4rem;
  text-shadow: 0 0 19px rgba(255, 255, 255, 0.695), 0 0 20px rgba(255, 255, 255, 0.568), 0 0 30px #1a0e34, 0 0 40px #03e9f4, 0 0 50px #2c26729f, 0 0 60px #180e5c5c, 0 0 70px #101d3548;
  border-radius: 70%;
  padding: 0.5rem;
  position: relative;
}
.no-score{
  margin-top:5%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

</style>