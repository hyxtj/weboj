
<template>
  <div class="solution">
    <h1>题解</h1>
    <p>题目ID: {{ problemId }}</p>
    <p>题解内容: {{ solution.solution }}</p>
    <!-- 可以在这里添加更多题解信息 -->
  </div>
</template>

<script>
import axios from '@/axios';
export default {
  name: 'SolutionDetail',
  data() {
    return {
      problemId: '',
      solution: ''
    };
  },
  created() {
    // 获取路由参数中的题目ID
    this.problemId = this.$route.params.problemId;
    // 获取题解信息
    this.fetchSolution(this.problemId);
  },
  methods: {
    fetchSolution() {
  this.loading = true;
  axios.get(`/solutions/${this.problemId}`)
    .then(response => {
      console.log('Response data:', response.data); // 添加调试信息
      this.loading = false;
      if (response.data.code === 200) {
        this.solution = response.data.data;
      } else {
        this.$message.error(response.data.msg || '获取题解失败');
      }
    })
    .catch(error => {
      this.loading = false;
      console.error('获取题解失败:', error);
      this.$message.error('获取题解失败，请重试');
    });
}
  }
};
</script>