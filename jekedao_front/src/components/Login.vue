<template>
  <div id="app" class="login-container">
    <canvas id="starry"></canvas>
    <el-form :model="loginForm" ref="loginForm" class="login-form" @submit.native.prevent="handleLogin">
      <h2 class="form-title">欢迎登录</h2>
      <el-form-item prop="username" :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]">
        <el-input v-model="loginForm.username" placeholder="用户名" prefix-icon="el-icon-user"></el-input>
      </el-form-item>
      <el-form-item prop="password" :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]">
        <el-input type="password" v-model="loginForm.password" placeholder="密码" show-password prefix-icon="el-icon-lock"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleLogin" :loading="loading" class="login-button">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from '@/axios'; // 使用自定义的 Axios 实例

export default {
  name: 'LoginComponent',
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loading: false
    };
  },
  methods: {
    handleLogin() {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          this.loading = true;
          axios.post('/login', this.loginForm)
            .then(response => {
              this.loading = false;
              if (response.data.code === 200) {
                this.$message.success('登录成功');
                // 存储 Token
                localStorage.setItem('access_token', response.data.access_token);
                // 跳转到用户仪表盘
                this.$router.push('/dashboard');
                // 触发全局事件，通知其他组件更新登录状态
                const event = new Event('user-login-status-change');
                window.dispatchEvent(event);
              } else {
                this.$message.error(response.data.msg || '登录失败');
              }
            })
            .catch((error) => {
              this.loading = false;
              console.error('登录失败:', error);
              this.$message.error('登录失败，请重试');
            });
        } else {
          this.$message.error('请完成表单字段的填写');
          return false;
        }
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

<style scoped>
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
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.login-form {
  width: 350px;
  padding: 30px;
  background: rgba(0, 0, 0, 0.8);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  border-radius: 12px;
  z-index: 1;
  color: #fff;
  text-align: center;
}

.form-title {
  font-size: 28px;
  margin-bottom: 20px;
  color: #fff;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
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

.login-button {
  width: 100%;
  padding: 15px;
  font-size: 18px;
  border-radius: 25px;
  background: linear-gradient(45deg, #6b8cff, #a3a8ff);
  color: #fff;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: background 0.3s ease, transform 0.3s ease;
}

.login-button:hover {
  background: linear-gradient(45deg, #5a7bff, #9298ff);
  transform: translateY(-2px);
}

.login-button:active {
  transform: translateY(1px);
}
</style>