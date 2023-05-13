<template>
  <div>
    <h1>Home page</h1>
    <div v-for="score in registeredScores" :key="score.id">
      {{ score.playerName }} - {{ score.score }}
    </div>
    <div>
      <router-link to="/start-new-quiz-page">Démarrer le quiz !</router-link>
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
  }
};
</script>
