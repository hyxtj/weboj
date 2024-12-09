<template>
  <div class="contest-page">
    <canvas id="starfield"></canvas>
    <div class="content">
      <h1>比赛</h1>
      <el-button type="primary" @click="createContest" class="large-button">发布新比赛</el-button>
      <el-table :data="contests" style="width: 100%">
        <el-table-column prop="name" label="名称" width="300">
          <template slot-scope="scope">
            <router-link :to="`/contest/${scope.row.id}`">{{ scope.row.name }}</router-link>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180"></el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  name: 'ContestPage',
  data() {
    return {
      contests: []
    };
  },
  created() {
    this.fetchContests();
  },
  methods: {
    createContest() {
      this.$router.push('/create-contest');
    },
    fetchContests() {
      axios.get('/contests')
        .then(response => {
          if (response.data.code === 200) {
            this.contests = response.data.data;
          } else {
            this.$message.error(response.data.msg || '获取比赛列表失败');
          }
        })
        .catch(error => {
          console.error('获取比赛列表失败:', error);
          this.$message.error('获取比赛列表失败，请重试');
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

.contest-page {
  padding: 20px;
  position: relative;
  z-index: 1;
  min-height: 100vh;
}

.content {
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
  color: #333;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}

.el-button.large-button {
  margin-bottom: 20px;
  padding: 15px 20px;
  font-size: 18px;
  border-radius: 20px;
}

.el-table {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
}
</style>