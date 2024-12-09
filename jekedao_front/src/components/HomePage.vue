<template>
  <div class="home-container">
    <h1 class="dynamic-text" ref="dynamicText">欢迎来到OJ平台</h1>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  mounted() {
    this.renderDynamicText();
  },
  methods: {
    renderDynamicText() {
      const text = this.$refs.dynamicText.innerText;
      this.$refs.dynamicText.innerText = '';
      let index = 0;
      const interval = setInterval(() => {
        if (index < text.length) {
          this.$refs.dynamicText.innerHTML += `<span style="color: ${this.getRandomColor()}">${text[index]}</span>`;
          index++;
        } else {
          clearInterval(interval);
        }
      }, 200); // 每个字符显示的间隔时间
    },
    getRandomColor() {
      const letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=KaiTi&display=swap'); /* 引入楷体字体 */

.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: url('../background.gif') no-repeat center center;
  background-size: cover; /* 确保背景图片覆盖整个容器 */
  flex-direction: column;
}

.dynamic-text {
  font-size: 3em; /* 放大字体 */
  font-weight: bold;
  font-family: 'KaiTi', sans-serif; /* 改变字体为楷体 */
  animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>