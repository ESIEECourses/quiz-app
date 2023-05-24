<template>

  <div class="row">
    <!-- MODE ADMINISTRATEUR DECONNECTÉ-->
    <div class="column">

      <div class="login-box">
 
        <form @submit='login'>
          <p>Enter the Dark side of the force</p>
          <div class="user-box">
            <input type="password" name="" v-model="password">
            <label>Password</label>
            
          </div>
          <div class="centered-button">
            <button type="submit" class="neon">
              SEND
            </button>
          </div>
        
        
        </form>
        <div v-if="showErrorBubble" class="error-bubble">
          Mot de passe incorrect !
        </div>
      </div>
      
    </div>
    
    <div class="column">
      
      <div class="vader">
        <div class="shadow"></div>
        <div class="head"><div class="helmet"><span class="left"></span><span class="right"></span></div><div class="eyes"><span class="left"></span><span class="right"></span></div><span class="grill"><span class="left"></span><span class="center"></span><span class="right"></span></span><span class="mask"><span class="top"></span><span class="left"></span><span class="center"></span><span class="right"></span></span><span class="line"></span></div>
        <div class="torso"><span class="neck"><span class="left"></span><span class="center"></span><span class="right"></span><span class="bottom"></span></span><span class="belt"><span class="center"></span></span><div class="plate"><span class="red_top"></span><span class="red_center"></span><span class="red_bottom"></span><span class="blue"></span><span class="gray"></span></div></div>
        <div class="hand left"><span class="hand"></span></div>
        <div class="hand right animation-right"><span class="hand"></span></div>
        <div class="legs"><span class="left"></span><span class="right"></span></div>
        <div class="boots"><span class="left"></span><span class="right"></span></div>
        <div class="sword animation-left"><span class="handle"></span><span class="light"></span></div>
        </div>
        
    </div>
    
  </div>
</template>


<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: 'Admin',
  data() {
    return {
      showErrorBubble: false,
      password: '',
    };
  },
  methods: {
    async login(event) {
      event.preventDefault();
      try {
        const response = await quizApiService.getAdminToken({ "password": this.password });
        if (response.status === 200) {
          const adminToken = response.data.token;
          participationStorageService.saveToken(adminToken);
          this.$router.push("/admin/questionlist");
        }
      } catch (error) {
        this.showErrorBubble = true;
        console.error('Erreur lors de la requête API', error);
      }
    }
  }
};
</script>


<style scoped>
.button-margin{
  margin-right: 1rem;
}
.centered-button{
  display: flex;
  justify-content: center;
  align-items: center;
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
.row {
  margin-top:  5%;
  display: flex;
  justify-content: center;
}

.column {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex: 50%;
}

.hidden-button{
  background-color: transparent;
  color: transparent;
  border: none;
}

.error-bubble {
  display: inline-block;
  background-color: #ff0000;
  color: #ffffff;
  padding: 5px 10px;
  border-radius: 5px;
  margin-top: 5px;
}

p{
  font-size: 1rem;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.4rem;
  text-shadow: 0 0 19px rgba(255, 255, 255, 0.695), 0 0 20px rgba(255, 255, 255, 0.568), 0 0 30px #1a0e34, 0 0 40px #03e9f4, 0 0 50px #2c26729f, 0 0 60px #180e5c5c, 0 0 70px #101d3548;
  border-radius: 70%;
  padding: 0.5rem;
  position: relative;
}


.create-block{
  display:flex;
  justify-content: center;
}
.login-box {
  top: 50%;
  left: 25%;
  width: 400px;
  padding: 40px;
  transform: translate(-50%, -50%);
  background: rgba(24, 20, 20, 0.987);
  box-sizing: border-box;
  box-shadow: 0 15px 25px rgba(0,0,0,.6);
  border-radius: 10px;
}

.login-box .user-box {
  position: relative;
}

.login-box .user-box input {
  width: 100%;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  margin-bottom: 30px;
  border: none;
  border-bottom: 1px solid #fff;
  outline: none;
  background: transparent;
}

.login-box .user-box label {
  position: absolute;
  top: 0;
  left: 0;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  pointer-events: none;
  transition: .5s;
}

.login-box .user-box input:focus ~ label,
.login-box .user-box input:valid ~ label {
  top: -20px;
  left: 0;
  color: #bdb8b8;
  font-size: 12px;
}

.login-box form a {
  position: relative;
  display: inline-block;
  padding: 10px 20px;
  color: #ffffff;
  font-size: 16px;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  transition: .5s;
  margin-top: 40px;
  letter-spacing: 4px
}

.login-box a:hover {
  background: #03e9f4;
  color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px #03e9f4,
              0 0 25px #03e9f4,
              0 0 50px #03e9f4,
              0 0 100px #03e9f4;
}

.login-box a span {
  position: absolute;
  display: block;
}

@keyframes btn-anim1 {
  0% {
    left: -100%;
  }

  50%,100% {
    left: 100%;
  }
}

.login-box a span:nth-child(1) {
  bottom: 2px;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #03e9f4);
  animation: btn-anim1 2s linear infinite;
}


@keyframes snow {
  0% {
    opacity: 0;
    transform: translateY(0px);
  }

  20% {
    opacity: 1;
  }

  100% {
    opacity: 1;
    transform: translateY(650px);
  }
}

@keyframes astronaut {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

body,html{height:100%;width:100%;overflow-x:hidden}
body{font:normal normal 14px/19px Arial,sans-serif;letter-spacing:1px;margin:0;background:#666460}
::-moz-selection{background:#2D3363;color:#FAEECF}
::selection{background:#2D3363;color:#FAEECF}
.text{position:absolute;bottom:20px;left:25px;color:#ffffff;font-family:Arial,sans-serif;text-transform:uppercase;font-size:14px;line-height:28px;font-weight:bold;letter-spacing:2px;z-index:99}
a{color:#6172BA;text-decoration:none;cursor:pointer}
a:hover{text-decoration:underline}
.vader{position:absolute;top:50%;left:50%;display:inline-block;-webkit-transform:translate(-50%,-50%);transform:translate(-50%,-50%)}
.vader .head{position:relative;width:100px;height:100px;margin-bottom:-10px;z-index:1}
.vader .helmet{position:absolute;top:0;left:5px;width:90px;height:80px;background:#222222;border-radius:80px 80px 0 0}
.vader .helmet::before{content:'';display:inline-block;position:absolute;top:0;left:50%;width:50px;height:8px;margin-left:-25px;background:#040507;border-radius:25px 25px 0 0 / 8px 8px 0 0}
.vader .helmet::after{content:'';display:inline-block;position:absolute;top:8px;left:50%;margin-left:-25px;height:0;width:0;border-left:25px solid transparent;border-right:25px solid transparent;border-top:24px solid #040507}
.vader .helmet span{position:absolute;top:50%;width:35px;height:55px;background:#040507}
.vader .helmet .left{left:-6px;-webkit-transform:rotate(25deg);transform:rotate(25deg)}
.vader .helmet .right{right:-6px;-webkit-transform:rotate(-25deg);transform:rotate(-25deg)}
.vader .helmet span::before{content:'';position:absolute;top:-5px;width:8px;height:55px;background:#222222}
.vader .helmet .left::before{left:0}
.vader .helmet .right::before{right:0}
.vader .line{position:absolute;top:-3px;left:50%;width:6px;height:38px;margin-left:-3px;background:#343434}
.vader .line::before{content:'';display:inline-block;position:absolute;left:-4px;bottom:0;width:4px;height:12px;background:#040507}
.vader .line::after{content:'';display:inline-block;position:absolute;right:-4px;bottom:0;width:4px;height:12px;background:#040507}
.vader .mask{position:absolute;bottom:19px;left:50%}
.vader .mask span{position:absolute;top:0;width:4px;height:4px;border-radius:1px;background:#C6C6C6}
.vader .mask .top{left:50%;margin-top:-16px;margin-left:-2px}
.vader .mask .top::before{content:'';display:inline-block;position:absolute;left:-7px;top:-2px;width:4px;height:24px;background:#040507;border-radius:4px;-webkit-transform:rotate(40deg);transform:rotate(40deg)}
.vader .mask .top::after{content:'';display:inline-block;position:absolute;right:-7px;top:-2px;width:4px;height:24px;background:#040507;border-radius:4px;-webkit-transform:rotate(-40deg);transform:rotate(-40deg)}
.vader .mask .left{left:12px}
.vader .mask .center{left:50%;margin-top:-16px;margin-left:-2px}
.vader .mask .right{right:12px}
.vader .grill{position:absolute;bottom:20px;left:50%;width:20px;margin-left:-10px}
.vader .grill span{position:absolute;bottom:-5px;width:2px;margin-left:-1px;background:#C6C6C6}
.vader .grill .left{left:4px;height:10px}
.vader .grill .center{left:50%;height:17px}
.vader .grill .right{right:2px;height:10px}
.vader .eyes{position:absolute;top:35px;left:10px;width:80px;height:40px;border-radius:40px;background:#343434}
.vader .eyes::before{content:'';display:inline-block;position:absolute;top:33px;left:5px;height:0;width:0;border-left:35px solid transparent;border-right:35px solid transparent;border-top:30px solid #343434}
.vader .eyes span{position:absolute;top:5px;width:30px;height:30px;border-radius:30px;background:#010000;-webkit-transition:background .3s ease-in-out;transition:background .3s ease-in-out}
.vader .eyes .left{left:7px}
.vader .eyes .right{right:7px}
.vader .torso{position:relative;width:60px;height:80px;border-radius:50px 50px 0 0;margin:0 auto;background:#222222}
.vader .torso::before{content:'';display:inline-block;position:absolute;left:-20px;top:-15px;width:100px;height:115px;border-radius:50px 50px 0 0;margin:0 auto;background:#040507;z-index:-1}
.vader .belt{position:absolute;bottom:0;width:100%;height:10px;background:#040507}
.vader .belt span::before{content:'';position:absolute;top:0;left:50%;width:20px;height:10px;border-radius:10px;margin-left:-10px;background:#C6C6C6}
.vader .neck{position:absolute;left:6px;top:3px;width:48px;height:8px;background:#010000;z-index:5}
.vader .neck::before{content:'';position:absolute;top:-8px;left:8px;width:32px;height:10px;background:#222222;border-radius:0 0 4px 4px}
.vader .neck::after{content:'';position:absolute;top:-8px;left:8px;width:32px;height:1px;background:#666666}
.vader .neck span{position:absolute;top:0;width:6px;height:125%;margin-left:-3px;background:#434343}
.vader .neck .left{left:6px;-webkit-transform:rotate(30deg);transform:rotate(30deg);border-radius:5px 0 0 0}
.vader .neck .center{left:50%;top:2px}
.vader .neck .right{right:3px;-webkit-transform:rotate(-30deg);transform:rotate(-30deg);border-radius:0 5px 0 0}
.vader .neck .bottom{position:absolute;top:8px;left:4px;width:46px;height:5px;background:#222222}
.vader .plate{position:absolute;left:15px;top:25px;width:30px;height:32px;background:#343434}
.vader .plate .red_top{position:absolute;left:2px;top:2px;width:12px;height:18px;background:#d81f27}
.vader .plate .red_top::before{content:'';position:absolute;top:0;left:0;width:100%;height:5px;background:rgba(0,0,0,0.2)}
.vader .plate .red_top::after{content:'';position:absolute;bottom:5px;left:0;width:100%;height:2px;background:#343434}
.vader .plate .red_center{position:absolute;right:2px;top:12px;width:12px;height:8px;background:#d81f27}
.vader .plate .red_center::before{content:'';position:absolute;left:0;top:4px;width:100%;height:4px;background:rgba(0,0,0,0.2)}
.vader .plate .red_center::after{content:'';position:absolute;left:5px;top:0;width:2px;height:100%;background:#343434}
.vader .plate .red_bottom{position:absolute;right:2px;bottom:2px;width:4px;height:8px;background:#d81f27}
.vader .plate .blue{position:absolute;right:2px;top:2px;width:12px;height:8px;background:#455caa}
.vader .plate .blue::before{content:'';position:absolute;top:3px;left:0;width:100%;height:2px;background:#343434}
.vader .plate .gray{position:absolute;left:2px;bottom:2px;width:20px;height:8px;background:#9f9fa1}
.vader .plate .gray::before{content:'';position:absolute;left:5px;top:0;width:2px;height:100%;background:#343434}
.vader .plate .gray::after{content:'';position:absolute;right:0;top:0;width:8px;height:100%;background:rgba(0,0,0,0.2)}
.vader .legs{position:relative;width:50px;height:20px;margin:0 auto;background:#222222}
.vader .legs::before{content:'';position:absolute;bottom:0;left:50%;width:20px;height:100%;margin-left:-10px;background:#040507}
.vader .boots{position:absolute;bottom:0;left:50%}
.vader .boots span{content:'';display:inline-block;position:absolute;top:0;width:30px;height:10px;background:#040507}
.vader .boots .left{left:10px;border-radius:0 15px 0 0}
.vader .boots .right{right:10px;border-radius:15px 0 0 0}
.vader .hand{position:absolute;top:60%;z-index:2}
.vader .hand.left{left:-2px;top:82%}
.vader .hand.right{right:-20px}
.vader .hand .hand{position:absolute;top:0;width:11px;height:22px;margin-top:-12px;margin-left:-12px;background:#040507}
.vader .hand.left .hand{left:0;border-radius:22px 0 0 22px}
.vader .hand.right .hand{right:0;width:22px;border-radius:22px}
.vader .sword{position:absolute;top:50%;left:-20px;z-index:10}
.vader .sword .handle{position:absolute;top:0;left:0;width:6px;height:30px;margin-left:-3px;background:#343434}
.vader .sword .handle::before{content:'';position:absolute;left:0;top:5px;width:100%;height:5px;background:#888888}
.vader .sword .handle::after{content:'';position:absolute;right:4px;top:5px;width:4px;height:5px;background:#343434}
.vader .sword .light{position:absolute;bottom:0;left:0;width:20px;height:120px;margin-left:-10px;background:rgba(248,80,50,0);background:-moz-linear-gradient(left, rgba(248,80,50,0) 10%, rgba(247,67,37,0) 20%, rgba(246,41,12,0.67) 40%, rgba(255,176,166,1) 50%, rgba(246,41,12,0.67) 60%, rgba(236,51,30,0) 80%, rgba(231,56,39,0) 90%);background:-webkit-gradient(left top, right top, color-stop(10%, rgba(248,80,50,0)), color-stop(20%, rgba(247,67,37,0)), color-stop(40%, rgba(246,41,12,0.67)), color-stop(50%, rgba(255,176,166,1)), color-stop(60%, rgba(246,41,12,0.67)), color-stop(80%, rgba(236,51,30,0)), color-stop(90%, rgba(231,56,39,0)));background:-webkit-linear-gradient(left, rgba(248,80,50,0) 10%, rgba(247,67,37,0) 20%, rgba(246,41,12,0.67) 40%, rgba(255,176,166,1) 50%, rgba(246,41,12,0.67) 60%, rgba(236,51,30,0) 80%, rgba(231,56,39,0) 90%);background:-o-linear-gradient(left, rgba(248,80,50,0) 10%, rgba(247,67,37,0) 20%, rgba(246,41,12,0.67) 40%, rgba(255,176,166,1) 50%, rgba(246,41,12,0.67) 60%, rgba(236,51,30,0) 80%, rgba(231,56,39,0) 90%);background:-ms-linear-gradient(left, rgba(248,80,50,0) 10%, rgba(247,67,37,0) 20%, rgba(246,41,12,0.67) 40%, rgba(255,176,166,1) 50%, rgba(246,41,12,0.67) 60%, rgba(236,51,30,0) 80%, rgba(231,56,39,0) 90%);background:linear-gradient(to right, rgba(248,80,50,0) 10%, rgba(247,67,37,0) 20%, rgba(246,41,12,0.67) 40%, rgba(255,176,166,1) 50%, rgba(246,41,12,0.67) 60%, rgba(236,51,30,0) 80%, rgba(231,56,39,0) 90%);}
.vader .sword .light::before{content:'';position:absolute;bottom:0;left:50%;width:3px;height:120px;margin-left:-1px;background:rgba(248,80,50,1);z-index:-1}
.vader .shadow{position:absolute;bottom:-17px;left:-25px;display:block;width:150px;height:14px;background:rgba(0,0,0,0.15);border-radius:50%}
.animation-right{-webkit-animation:animationHandRight 1.5s linear infinite;animation:animationHandRight 1.5s linear infinite}
@-webkit-keyframes animationHandRight{0%{-webkit-transform:rotate(0deg);transform:rotate(0deg)}100%{-webkit-transform:rotate(360deg);transform:rotate(360deg)}}
@keyframes animationHandRight{0%{-webkit-transform:rotate(0deg);transform:rotate(0deg)}100%{-webkit-transform:rotate(360deg);transform:rotate(360deg)}}
.animation-left{-webkit-animation:animationHandLeft 3s ease-in-out infinite;animation:animationHandLeft 3s ease-in-out infinite}
@-webkit-keyframes animationHandLeft{0%, 100%{-webkit-transform:translateX(0) rotate(-25deg);transform:translateX(0) rotate(-25deg)}50%{-webkit-transform:translateX(150px) rotate(25deg);transform:translateX(150px) rotate(25deg)}}
@keyframes animationHandLeft{0%, 100%{-webkit-transform:translateX(0) rotate(-25deg);transform:translateX(0) rotate(-25deg)}50%{-webkit-transform:translateX(150px) rotate(25deg);transform:translateX(150px) rotate(25deg)}}
.vader:hover .eyes .left{background:#d81f27}
.vader:hover .eyes .right{background:#455caa}


</style>