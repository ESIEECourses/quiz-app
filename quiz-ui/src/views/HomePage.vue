<template>
  <div>
    <h1>Home page</h1>
    <div>
      <router-link to="/start-new-quiz-page">Démarrer le quiz !</router-link>
    </div>
    <h2>Meilleurs scores</h2>
    <div v-if="registeredScores.length === 0">Aucun score enregistré.</div>
    <ol v-else>
      <li v-for="(scoreEntry, index) in registeredScores" :key="index">
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </li>
    </ol>
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
        this.registeredScores.sort((a, b) => b.score - a.score);
      } else {
        console.error("Erreur lors de la récupération des scores du quiz");
      }
    } catch (error) {
      console.error("Erreur lors de la requête API", error);
    }
  }
};
</script>
