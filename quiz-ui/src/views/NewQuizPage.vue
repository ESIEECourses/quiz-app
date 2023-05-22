<template>
  
  <div class="centered-container">
    <form @submit="launchNewQuiz" class="mb-3">
      <span>Pseudo</span>
      <div class="pseudoform">
        <label for="playerName" class="form-label">
          
        </label>
        <input type="text" id="playerName" v-model="username" class="input">
      </div>
      <button type="submit" class="neon smaller-button" @mouseover="checkPseudo">Commencer le quiz</button>
    </form>
    <div v-if="showErrorBubble" class="error-bubble">
      Veuillez entrer un pseudo
    </div>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "NewQuizPage",
  data() {
    return {
      username: "", // Variable pour stocker le nom du joueur
      showErrorBubble: false, // Nouvelle donnée pour afficher la bulle d'erreur
    };
  },
  methods: {
    launchNewQuiz(event) {
      event.preventDefault(); // Empêche le rechargement de la page

      console.log("Launch new quiz with", this.username);
      if (this.username !== "") {
        // Stockage du nom du joueur
        participationStorageService.savePlayerName(this.username);
        // Redirection vers la route '/questions'
        this.$router.push("/questions");
      } else {
        this.showErrorBubble = true; // Afficher la bulle d'erreur
      }
    },
  },
};
</script>


<style scoped>
.centered-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
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
.texto {
  color: #03e9f4;
  font-weight: bold;
}
.pseudoform{
  margin-bottom: 10px;
}
.mb-3 { 
  text-align: center;
}

.neon {
  padding: 15px 25px;
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
.form-control{
  margin-bottom: 0px;
}
.neon:hover {
  background: #03e9f4;
  color: #050801;
  box-shadow: 0 0 5px #03e9f4,
              0 0 25px #03e9f4,
              0 0 50px #03e9f4,
              0 0 200px #03e9f4;
  -webkit-box-reflect: below 1px linear-gradient(transparent, #0005);
}

.smaller-button {

  font-size: 14px;
  padding: 10px 20px;
}

.error-bubble {
  display: inline-block;
  background-color: #ff0000;
  color: #ffffff;
  padding: 5px 10px;
  border-radius: 5px;
  margin-top: 5px;
}

.input {
  background-color: #212121;
  max-width: 190px;
  height: 40px;
  padding: 10px;
  /* text-align: center; */
  border: 2px solid white;
  border-radius: 5px;
  /* box-shadow: 3px 3px 2px rgb(249, 255, 85); */
}

.input:focus {
  color: rgb(0, 255, 255);
  background-color: #212121;
  outline-color: rgb(0, 255, 255);
  box-shadow: -3px -3px 15px rgb(0, 255, 255);
  transition: .1s;
  transition-property: box-shadow;
}
</style>
