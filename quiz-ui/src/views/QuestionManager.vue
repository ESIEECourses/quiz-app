<template>
      <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" v-if="currentQuestion" />
  </template>
  
  <script>
  import QuestionDisplay from "@/components/QuestionDisplay.vue";
  import quizApiService from "@/services/QuizApiService.js";
  import participationStorageService from "@/services/ParticipationStorageService.js"
  export default {
    components: {
        QuestionDisplay,
    },
    data() {
      return {
        score: 0,
        
        player:{
            playerName:"",
            answers:[]
        },
        currentQuestionPosition: 1,
        totalNumberOfQuestions: 0,
        goodAnswers: [],
        currentQuestion: {
            questionTitle:"",
            questionText:"",
            possibleAnswers:[],
            image:""
        },
        isQuizFinished: false,
      };
    },
    async created() {
      // Appel API pour récupérer les questions et le nombre total de questions
      try {
        const response = await quizApiService.getQuizInfo();
        if (response.status === 200) {
          this.totalNumberOfQuestions = response.data.size;
          this.loadQuestionByPosition(this.currentQuestionPosition);
        } else {
          console.error("Erreur lors de la récupération des informations du quiz");
        }
      } catch (error) {
        console.error("Erreur lors de la requête API ", error);
      }
      try {
        const response = await quizApiService.getAnswers();
        console.log(response);
        if (response.status === 200) {
          this.goodAnswers = response.data;
          console.log(this.goodAnswers);
        } else {
          console.error("Erreur lors de la récupération des bonnes réponses");
        }
      } catch (error) {
        console.error("Erreur lors de la requête API ", error);
      }
    },
    methods: {
      async loadQuestionByPosition(position) {
        try {
            console.log(position)
            const response = await quizApiService.getQuestionByPosition(position);
            console.log("loadQuestionByPosition:", response.data)
            if (response.status === 200) {
                this.currentQuestion.questionTitle = response.data.title;
                this.currentQuestion.questionText = response.data.text;
                this.currentQuestion.possibleAnswers = response.data.possibleAnswers;
                this.currentQuestion.image = response.data.image;
                console.log("Question en cours", this.currentQuestion)
            } else {
                console.error("Erreur lors du chargement de la question");
            }
        } catch (error) {
            console.error("Erreur lors de la requête API", error);
        }
      },
      answerClickedHandler(selectedAnswerId) {

        // Vérifiez si la réponse sélectionnée correspond à la réponse correcte
        const currentQuestion = this.currentQuestion;
        const correctAnswerId = currentQuestion.correctAnswerId;
        const isCorrectAnswer = selectedAnswerId === correctAnswerId;

        if (isCorrectAnswer) {
          // Augmentez le score
          this.score++;
        }

        // Utilisez l'ID de la réponse sélectionnée
        console.log("ID de la réponse sélectionnée :", selectedAnswerId);
        this.player.answers.push(selectedAnswerId)
        console.log("Pour l'instant, voici tes réponses:", this.player.answers)
        this.selectedAnswerId = selectedAnswerId;


        
        // Passez à la question suivante ou terminez le quiz si toutes les questions ont été répondues
        this.currentQuestionPosition++;
        if (this.currentQuestionPosition <= this.totalNumberOfQuestions) {
            this.loadQuestionByPosition(this.currentQuestionPosition);
        } else {
          
          console.log("Pour l'instant, voici tes réponses:", this.player.answers)
          this.selectedAnswerId = selectedAnswerId;
          for (let i = 0; i < this.player.answers.length; i++) {
            if (this.player.answers[i] === this.goodAnswers[i]) {
              this.score++;
            }
          }
            console.log(this.score);
            this.endQuiz();
        }
        },
      async endQuiz() {
        // Effectuer les opérations de fin de quiz, par exemple, afficher les résultats
        // Vous pouvez également rediriger l'utilisateur vers une autre page à ce stade
        //const answersArray = Object.values(this.player.answers);
        this.player.playerName = participationStorageService.getPlayerName();
        
        participationStorageService.saveParticipationScore(this.score);
        
;        //console.log(this.player)
        //console.log("Valeur du playername", this.player.playerName);
        //console.log("Type du playerName:", typeof this.player.playerName);
        //console.log("Valeur des réponses", answersArray);
        //console.log("Type des réponses:", typeof answersArray);
        //this.player.answers = answersArray;
        //console.log({"playerName": this.player.playerName, "answers": this.player.answers })
        const postResult = await quizApiService.postparticipations(this.player);
        
        // Construire l'URL avec les paramètres du score
        const scorePageURL = `/score?score=${this.score}`;

        // Redirigez l'utilisateur vers la page de score en utilisant l'URL avec les paramètres
        this.$router.push(scorePageURL);

        console.log("Quiz terminé !");
      },
    },
  };
  </script>
  


<style>


  .centered-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}
</style>