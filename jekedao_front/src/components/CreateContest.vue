<template>
  <div class="create-contest">
    <canvas id="starfield"></canvas>
    <div class="content">
      <h1>发布比赛</h1>
      <el-form ref="form" :model="form" label-width="100px">
        <el-form-item label="比赛名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="比赛描述">
          <el-input type="textarea" v-model="form.description"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm" class="large-button">提交</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  name: 'CreateContest',
  data() {
    return {
      form: {
        name: '',
        description: ''
      }
    };
  },
  methods: {
    submitForm() {
      if (!this.form.name || !this.form.description) {
        this.$message.error('名称和描述为必填项');
        return;
      }

      axios.post('/contests', this.form)
        .then(response => {
          if (response.data.code === 201) {
            this.$message.success('比赛发布成功');
            this.$router.push('/contest');
          } else {
            this.$message.error(response.data.msg || '比赛发布失败');
          }
        })
        .catch(error => {
          console.error('比赛发布失败:', error);
          this.$message.error('比赛发布失败，请重试');
        });
    },
    drawStars() {
      var canvas = document.getElementById('starfield'),
        context = canvas.getContext('2d'),
        stars = [],
        stars_count = 800;

      function ini() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        stars = [];
        makeStars();
      }

      function makeStars() {
        for (var i = 0; i < stars_count; i++) {
          let x = Math.random() * canvas.offsetWidth;
          let y = Math.random() * canvas.offsetHeight;
          let radius = Math.random() * 0.8;
          let color = "rgba(" + Math.random() * 255 + "," + Math.random() * 255 + "," + Math.random() * 255 + ",0.8)";
          let speed = Math.random() * 0.5;
          stars.push({ x, y, radius, color, speed });
        }
      }

      function drawStars() {
        context.fillStyle = "#0e1729";
        context.fillRect(0, 0, canvas.width, canvas.height);
        for (var i = 0; i < stars.length; i++) {
          var x = stars[i].x - stars[i].speed;
          if (x < -2 * stars[i].radius) x = canvas.width;
          stars[i].x = x;
          var y = stars[i].y;
          var radius = stars[i].radius;
          context.beginPath();
          context.arc(x, y, radius * 2, 0, 2 * Math.PI);
          context.fillStyle = stars[i].color;
          context.fill();
        }
      }

      ini();
      setInterval(drawStars, 50);
      window.onresize = ini;
    }
  },
  mounted() {
    this.drawStars();
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  font-family: 'KaiTi', serif;
}

html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}

canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -6;
  background: #0e1729;
}

.create-contest {
  padding: 20px;
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.content {
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
  color: #333;
  width: 100%;
  max-width: 600px;
}

h1 {
  color: #333;
  text-align: center;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-button.large-button {
  padding: 15px 20px;
  font-size: 18px;
  border-radius: 20px;
  width: 100%;
}
</style>