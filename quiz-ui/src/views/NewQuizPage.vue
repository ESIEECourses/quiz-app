<template>
    <div>
      <h1>New Quiz Page</h1>
      <form @submit="startQuiz" class="my-4">
        <div class="mb-3">
          <label for="playerName" class="form-label">Nom du joueur :</label>
          <input type="text" id="playerName" v-model="username" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary" @click="launchNewQuiz">Commencer le quiz</button>
      </form>
    </div>
  </template>
  
  <script>
  import participationStorageService from "@/services/ParticipationStorageService";
  import QuestionManager from "../views/QuestionManager.vue";
  export default {
  name: "NewQuizPage",
  data() {
    return {
      username: "", // Variable pour stocker le nom du joueur
    };
  },
  methods: {
  launchNewQuiz() {
    console.log("Launch new quiz with", this.username);
    // Stockage du nom du joueur
    participationStorageService.savePlayerName(this.username);
    // Redirection vers la route '/questions'
    this.$router.push('/questions');
  },
},
};
  </script>
  