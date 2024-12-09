<template>
  <div class="discussion-detail">
    <canvas id="canvas" class="canvas"></canvas>
    <div class="content">
      <h1>{{ discussion.title }}</h1>
      <p>作者: {{ discussion.author }}</p>
      <p>发布时间: {{ formatDate(discussion.publish_time) }}</p>
      <p>{{ discussion.content }}</p>
      <!-- 添加评论组件 -->
      <CommentComponent :discussionId="discussion.id" />
    </div>
  </div>
</template>

<script>
import axios from '@/axios';
import CommentComponent from './CommentComponent.vue';

export default {
  name: 'DiscussionDetail',
  components: {
    CommentComponent
  },
  data() {
    return {
      discussion: {}
    };
  },
  created() {
    // 获取路由参数中的讨论ID
    const discussionId = this.$route.params.discussionId;
    // 获取讨论详情
    this.fetchDiscussion(discussionId);
  },
  methods: {
    fetchDiscussion(discussionId) {
      axios.get(`/discussions/${discussionId}`)
        .then(response => {
          if (response.data.code === 200) {
            this.discussion = response.data.data;
          } else {
            this.$message.error(response.data.msg || '获取讨论详情失败');
          }
        })
        .catch(error => {
          console.error('获取讨论详情失败:', error);
          this.$message.error('获取讨论详情失败，请重试');
        });
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleString();
    },
    drawStars() {
      var canvas = document.getElementById('canvas'),
        ctx = canvas.getContext('2d'),
        w = canvas.width = window.innerWidth,
        h = canvas.height = window.innerHeight,
        hue = 217,
        stars = [],
        count = 0,
        maxStars = 1300;

      var canvas2 = document.createElement('canvas'),
        ctx2 = canvas2.getContext('2d');
      canvas2.width = 100;
      canvas2.height = 100;
      var half = canvas2.width / 2,
        gradient2 = ctx2.createRadialGradient(half, half, 0, half, half, half);
      gradient2.addColorStop(0.025, '#CCC');
      gradient2.addColorStop(0.1, 'hsl(' + hue + ', 61%, 33%)');
      gradient2.addColorStop(0.25, 'hsl(' + hue + ', 64%, 6%)');
      gradient2.addColorStop(1, 'transparent');

      ctx2.fillStyle = gradient2;
      ctx2.beginPath();
      ctx2.arc(half, half, half, 0, Math.PI * 2);
      ctx2.fill();

      function random(min, max) {
        if (arguments.length < 2) {
          max = min;
          min = 0;
        }

        if (min > max) {
          var hold = max;
          max = min;
          min = hold;
        }

        return Math.floor(Math.random() * (max - min + 1)) + min;
      }

      function maxOrbit(x, y) {
        var max = Math.max(x, y),
          diameter = Math.round(Math.sqrt(max * max + max * max));
        return diameter / 2;
      }

      var Star = function () {
        this.orbitRadius = random(maxOrbit(w, h));
        this.radius = random(60, this.orbitRadius) / 8;
        this.orbitX = w / 2;
        this.orbitY = h / 2;
        this.timePassed = random(0, maxStars);
        this.speed = random(this.orbitRadius) / 500000;
        this.alpha = random(2, 10) / 10;

        count++;
        stars[count] = this;
      }

      Star.prototype.draw = function () {
        var x = Math.sin(this.timePassed) * this.orbitRadius + this.orbitX,
          y = Math.cos(this.timePassed) * this.orbitRadius + this.orbitY,
          twinkle = random(10);

        if (twinkle === 1 && this.alpha > 0) {
          this.alpha -= 0.05;
        } else if (twinkle === 2 && this.alpha < 1) {
          this.alpha += 0.05;
        }

        ctx.globalAlpha = this.alpha;
        ctx.drawImage(canvas2, x - this.radius / 2, y - this.radius / 2, this.radius, this.radius);
        this.timePassed += this.speed;
      }

      for (var i = 0; i < maxStars; i++) {
        new Star();
      }

      function animation() {
        ctx.globalCompositeOperation = 'source-over';
        ctx.globalAlpha = 0.5;
        ctx.fillStyle = 'hsla(' + hue + ', 64%, 6%, 2)';
        ctx.fillRect(0, 0, w, h)

        ctx.globalCompositeOperation = 'lighter';
        for (var i = 1, l = stars.length; i < l; i++) {
          stars[i].draw();
        }

        window.requestAnimationFrame(animation);
      }

      animation();
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
body,
html {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
.canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -6;
  filter: alpha(opacity=20);
}
.discussion-detail {
  padding: 20px;
  position: relative;
  z-index: 1;
}

.content {
  background: rgba(0, 0, 0, 0.8);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
  color: #fff;
}

h1 {
  color: #fff;
}

p {
  color: #ddd;
}
</style>