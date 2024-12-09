<template>
  <div id="app" class="dashboard-container">
    <canvas id="starry"></canvas>
    <div class="dashboard">
      <h1>欢迎，{{ username }}！</h1>
      <p>这是您的仪表盘。</p>

      <!-- 个人签名 -->
      <div class="section">
        <h2>个人签名</h2>
        <p v-if="!isEditingSignature">{{ signature || '您还没有设置签名。' }}</p>
        <el-button v-else type="primary" @click="saveSignature" class="large-button">保存</el-button>
        <el-button v-if="!isEditingSignature" type="primary" @click="editSignature" class="large-button">编辑签名</el-button>
        <el-button v-else @click="cancelEditSignature" class="large-button">取消</el-button>
        <el-input
          v-if="isEditingSignature"
          v-model="editSignatureText"
          placeholder="请输入您的签名"
          clearable
        ></el-input>
      </div>

      <!-- 个人博客 -->
      <div class="section">
        <h2>个人博客</h2>
        <p v-if="!isEditingBlog">{{ blog || '您还没有撰写博客。' }}</p>
        <el-button v-else type="primary" @click="saveBlog" class="large-button">保存</el-button>
        <el-button v-if="!isEditingBlog" type="primary" @click="editBlog" class="large-button">编辑博客</el-button>
        <el-button v-else @click="cancelEditBlog" class="large-button">取消</el-button>
        <el-input
          type="textarea"
          v-if="isEditingBlog"
          v-model="editBlogText"
          placeholder="请输入您的博客内容"
          clearable
          rows="6"
        ></el-input>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  name: 'UserDashboard',
  data() {
    return {
      username: '',
      signature: '',
      blog: '',
      isEditingSignature: false,
      editSignatureText: '',
      isEditingBlog: false,
      editBlogText: ''
    };
  },
  created() {
    this.fetchUserInfo();
  },
  methods: {
    fetchUserInfo() {
      axios.get('/profile/me')
        .then(response => {
          if (response.data.code === 200) {
            this.username = response.data.data.username;
            this.signature = response.data.data.signature;
            this.blog = response.data.data.blog;
          } else {
            this.$message.error(response.data.message || '无法获取用户信息');
          }
        })
        .catch(() => {
          this.$message.error('无法获取用户信息');
        });
    },
    editSignature() {
      this.isEditingSignature = true;
      this.editSignatureText = this.signature;
    },
    saveSignature() {
      if (this.editSignatureText.trim() === '') {
        this.$message.error('签名不能为空');
        return;
      }
      axios.put('/profile/me', { signature: this.editSignatureText })
        .then(response => {
          if (response.data.code === 200) {
            this.signature = response.data.data.signature;
            this.isEditingSignature = false;
            this.$message.success('签名更新成功');
          } else {
            this.$message.error(response.data.message || '更新签名失败');
          }
        })
        .catch(() => {
          this.$message.error('更新签名失败');
        });
    },
    cancelEditSignature() {
      this.isEditingSignature = false;
      this.editSignatureText = '';
    },
    editBlog() {
      this.isEditingBlog = true;
      this.editBlogText = this.blog;
    },
    saveBlog() {
      if (this.editBlogText.trim() === '') {
        this.$message.error('博客内容不能为空');
        return;
      }
      axios.put('/profile/me', { blog: this.editBlogText })
        .then(response => {
          if (response.data.code === 200) {
            this.blog = response.data.data.blog;
            this.isEditingBlog = false;
            this.$message.success('博客更新成功');
          } else {
            this.$message.error(response.data.message || '更新博客失败');
          }
        })
        .catch(() => {
          this.$message.error('更新博客失败');
        });
    },
    cancelEditBlog() {
      this.isEditingBlog = false;
      this.editBlogText = '';
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
      for (let i = 0; i < 150; i++) {
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
  font-family: 'KaiTi', serif;
}
body,
html {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
#starry {
  position: absolute;
  background-color: #000000;
}
.dashboard-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.dashboard {
  width: 800px;
  padding: 30px;
  background: rgba(0, 0, 0, 0.8);
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  z-index: 1;
  color: #fff;
}

.section {
  margin-bottom: 40px;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.section h2 {
  margin-bottom: 10px;
  color: #fff;
}

.section p {
  font-size: 16px;
  margin-bottom: 10px;
  color: #fff;
}

.section .el-button {
  margin-right: 10px;
  padding: 15px 20px;
  font-size: 16px;
  border-radius: 20px;
}

.el-input {
  margin-top: 10px;
  width: 100%;
}
</style>