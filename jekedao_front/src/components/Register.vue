<template>
  <div id="app" class="register-container">
    <canvas id="starry"></canvas>
    <el-form :model="registerForm" ref="registerForm" class="register-form">
      <el-form-item prop="username">
        <el-input v-model="registerForm.username" placeholder="用户名"></el-input>
      </el-form-item>
      <el-form-item prop="email">
        <el-input v-model="registerForm.email" placeholder="邮箱"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input type="password" v-model="registerForm.password" placeholder="密码"></el-input>
      </el-form-item>
      <el-form-item prop="confirmPassword">
        <el-input type="password" v-model="registerForm.confirmPassword" placeholder="确认密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleRegister">注册</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
//import axios from '@/axios'; // 使用实例化的 Axios

export default {
  name: 'RegisterComponent',
  data() {
    return {
      registerForm: {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      }
    };
  },
  methods: {
    handleRegister() {
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        this.$message.error('密码和确认密码不一致');
        return;
      }
      this.$axios.post('/register', this.registerForm)
        .then(response => {
          if (response.data.code === 200) {
            this.$message.success(response.data.message);
            this.$router.push('/login');
          } else {
            this.$message.error(response.data.message);
          }
        })
        .catch(() => {
          this.$message.error('注册失败');
        });
    },
    initStarryBackground() {
      let canvas = document.getElementById('starry');
      canvas.width = document.documentElement.clientWidth;
      canvas.height = document.documentElement.clientHeight;
      let ctx = canvas.getContext('2d');

      class Star {
        constructor() {
          this.x = randNum(3, canvas.width - 3);
          this.y = randNum(3, canvas.height - 3);
          this.r = randNum(1, 3);
          this.color = randColor();
          this.speedX = randNum(-2, 2) * 0.2;
          this.speedY = randNum(-3, 3) * 0.2;
        }
        draw() {
          ctx.beginPath();
          ctx.globalAlpha = 1;
          ctx.fillStyle = this.color;
          ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
          ctx.fill();
        }
        move() {
          this.x += this.speedX;
          this.y += this.speedY;
          if (this.x <= 3 || this.x >= canvas.width - 3) this.speedX *= -1;
          if (this.y <= 3 || this.y >= canvas.height - 3) this.speedY *= -1;
        }
      }

      let stars = [];
      for (let i = 0; i < 200; i++) {
        let star = new Star();
        stars.push(star);
      }

      let mouseX, mouseY;
      canvas.onmousemove = function (event) {
        mouseX = event.offsetX;
        mouseY = event.offsetY;
      }

      function mouseLine() {
        for (var i = 0; i < stars.length; i++) {
          if (Math.sqrt(Math.pow((stars[i].x - mouseX), 2) + Math.pow((stars[i].y - mouseY), 2)) < 120) {
            ctx.beginPath();
            ctx.moveTo(stars[i].x, stars[i].y);
            ctx.lineTo(mouseX, mouseY);
            ctx.strokeStyle = "white";
            ctx.globalAlpha = 0.8;
            ctx.stroke();
          }
        }
      }

      function drawLine() {
        for (var i = 0; i < stars.length; i++) {
          stars[i].draw();
          stars[i].move();
        }
      }

      function main() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        mouseLine();
        drawLine();
        window.requestAnimationFrame(main);
      }

      main();

      function randNum(m, n) {
        return Math.floor(Math.random() * (n - m + 1) + m);
      }

      function randColor() {
        return 'rgb(' + randNum(0, 255) + ',' + randNum(0, 255) + ',' + randNum(0, 255) + ')';
      }
    }
  },
  mounted() {
    this.initStarryBackground();
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
}
body,
html {
  width: 100%;
  height: 100%;
  overflow: hidden;
  font-family: 'Arial', sans-serif;
}
#starry {
  position: absolute;
  background-color: #000000;
}
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.register-form {
  width: 300px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.8);
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  z-index: 1;
  color: #fff;
  text-align: center;
}

.el-input {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 16px;
}

.el-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.el-button {
  width: 100%;
  padding: 15px;
  font-size: 18px;
  border-radius: 25px;
  background: linear-gradient(45deg, #6b8cff, #a3a8ff);
  color: #fff;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: background 0.3s ease, transform 0.3s ease;
}

.el-button:hover {
  background: linear-gradient(45deg, #5a7bff, #9298ff);
  transform: translateY(-2px);
}

.el-button:active {
  transform: translateY(1px);
}
</style>