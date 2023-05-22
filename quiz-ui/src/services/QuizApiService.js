import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getQuestion(id) {
    return this.call("get", `questions/${id}`);
  },
  async postparticipations(data){
    return this.call("post", `participations`, data);
  },
  getAnswers(){
    return this.call("get", '/answers');
  },

  getAdminToken(password){
    return this.call("post", "/login", password);
  },
  deleteAllQuestion(token){
    return this.call("delete", "/questions/all",null, token)
  },
  deleteAllParticipation(token){
    return this.call("delete", "/participations/all",null, token)
  },
  addNewQuestion(question, token){
    return this.call("post", '/questions', question, token)
  },
  deleteOneQuestionById(questionId, token) {
    return this.call("delete", `/questions/${questionId}`, null, token);
  },
  getQuestionByPosition(position) {
    return this.call("get", `/questions?position=${position}`);
  },
  updateQuestionById(questionId, updatedQuestion, token) {
    return this.call("put", `/questions/${questionId}`, updatedQuestion, token);
  },
  getAllParticipations(){
    return this.call("get", "/classement")
  }
};