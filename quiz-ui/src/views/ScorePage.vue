<template>
    <div class="score-page">
      
      <h1 class="texto">{{ playername }}</h1>
      <h1> Vous avez terminé le quiz bravo </h1>
      <p>Votre score : {{ score }}</p>
      <p>Classement : {{ ranking }}</p>
      <p>Meilleurs scores :</p>
      <ul>
        <li v-for="topScore in topScores" :key="topScore.id">
          {{ topScore[2] }}
        </li>
      </ul>
      <button @click="goToHomePage">Retour à la Home page</button>
    </div>
  </template>
  
  <script>
   import quizApiService from "@/services/QuizApiService.js";
   import participationStorageService from "@/services/ParticipationStorageService.js"
  export default {
    name: 'ScorePage',
    data() {
      return {
        playername: "",
        ranking: 0, 
        topScores: [],
        registeredScores: [] 
      };
    },
    async created() {
        this.getClassement();
        this.playername = participationStorageService.getPlayerName();
    },
    methods: {
        goToHomePage() {
            // Redirigez l'utilisateur vers la Home page
            participationStorageService.clear();
            this.$router.push('/');
        },
        async getClassement(){
          /*try {
                const response = await quizApiService.getQuizInfo();
                if (response.status === 200) {

                    this.registeredScores = response.data.scores;
                    const userScoreIndex = this.registeredScores.findIndex(score => score.playerName === participationStorageService.getPlayerName());
                    console.log("Position Score", userScoreIndex);
                    if (userScoreIndex !== -1) {
                        this.ranking = userScoreIndex + 1; // La position est indexée à partir de 0, donc ajoutez 1 pour obtenir la position réelle
                    }
                } else {
                    console.error("Erreur lors de la récupération des scores du quiz");
                }
            } catch (error) {
                console.error("Erreur lors de la requête API", error);
            }*/
          try {
                const response = await quizApiService.getAllParticipations();
                if (response.status === 200) {
                  console.log("les participations", response);
                  const scores = response.data.scores;
                  const lastIndex = scores.length;
                  let classement = 0;
                  let idCursor =0;
                  for(let i=0; i<lastIndex; i++){
                    if(scores[i][1] === this.playername && scores[i][0] >idCursor){
                      this.topScores.push(scores[i]);
                      classement = i+1;
                      idCursor = scores[i][0];                    
                    }
                    
                  }
                  console.log("classement:", classement, "id", idCursor);
                  console.log("TOP SCORES", this.topScores);
                  this.ranking = classement;

                  /*const scores = response.data.scores;
                  const lastIndex = scores.length - 1;
                  const classement = scores[lastIndex][2];
                  console.log("Troisième valeur :", classement);
                  this.ranking = classement;*/
                }
                else {
                    console.error("Erreur lors de la récupération des scores du quiz");
                }
            } catch (error) {
                console.error("Erreur lors de la requête API", error);
            }



        }
    },
    computed: {
        score() {
            const scoreParam = this.$route.query.score;
            return parseInt(scoreParam) || 0;
        },
    },
  };
  </script>
  
  <style scoped>
  .score-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }

  .texto{
    color: #03e9f4;
    font-weight: bold;
    justify-content: center;
  }
  
  .score-page h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .score-page p {
    margin-bottom: 10px;
  }
  
  .score-page button {
    padding: 10px 20px;
    background-color: #333;
    color: #03e9f4;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .score-page button:hover {
    background-color: #03e9f4;
    color: #050801;
  }
  </style>
  