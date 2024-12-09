<template>
  <div class="square-container">
    <div class="background" v-if="backgroundProblemId">
      <ProblemDetail :problemId="backgroundProblemId" />
    </div>
    <div class="content">
      <div class="left-sidebar">
        <h2 v-if="!isLoggedIn">欢迎来到OJ平台</h2>
        <div v-if="!isLoggedIn">
          <router-link to="/register">
            <button class="btn">注册</button>
          </router-link>
          <router-link to="/login">
            <button class="btn">登录</button>
          </router-link>
        </div>
        <div v-else>
          <h2>个人主页</h2>
          <p>欢迎，{{ username }}！</p>
          <button @click="logout" class="btn">退出登录</button>
        </div>
      </div>
      <div class="main-content">
        <h1>广场</h1>
        <div class="announcement">
          <h2>中央公告栏</h2>
          <p>欢迎来到OJ平台——Welcome to a world of programming</p>
        </div>
        <div class="links">
          <h3>相关网址链接</h3>
          <ul>
            <li><a href="https://www.luogu.com.cn/" target="_blank">洛谷</a></li>
            <li><a href="https://leetcode.cn/" target="_blank">LeetCode</a></li>
            <!-- 可以在这里添加更多链接 -->
          </ul>
        </div>
        <div class="problems">
          <h3>题目列表</h3>
          <ul>
            <li v-for="problem in problems" :key="problem.id">
              <router-link :to="`/problem/${problem.id}`">{{ problem.title }}</router-link>
            </li>
          </ul>
        </div>
      </div>
      <div class="right-sidebar">
        <div class="search">
          <h3>题目搜索</h3>
          <input type="number" v-model.number="searchProblemId" placeholder="输入题目序号" />
          <button @click="searchProblem" class="btn">搜索</button>
        </div>
        <div class="ranking">
          <h3>比赛排名情况</h3>
          <iframe src="https://www.luogu.com.cn/" width="100%" height="300px"></iframe>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/axios'; // 使用配置好的 Axios 实例
import ProblemDetail from './ProblemDetail.vue';

export default {
  name: 'SquarePage',
  components: {
    ProblemDetail
  },
  data() {
    return {
      isLoggedIn: false,
      username: '',
      searchProblemId: null,
      backgroundProblemId: 1, // 假设背景题目ID为1
      problems: []
    };
  },
  created() {
    this.fetchProblems();
    this.checkLoginStatus();
  },
  methods: {
    fetchProblems() {
      axios.get('/problems')
        .then(response => {
          if (response.data.code === 200) {
            this.problems = response.data.data;
          } else {
            this.$message.error(response.data.msg || '获取题目列表失败');
          }
        })
        .catch(error => {
          console.error('获取题目列表失败:', error);
          this.$message.error('获取题目信息失败，请重试');
        });
    },
    checkLoginStatus() {
      const token = localStorage.getItem('access_token');
      if (token) {
        this.isLoggedIn = true;
        // 获取当前用户信息
        axios.get('/profile/me')
          .then(response => {
            if (response.data.code === 200) {
              this.username = response.data.data.username;
            } else {
              this.isLoggedIn = false;
              this.username = '';
            }
          })
          .catch(error => {
            console.error('获取用户信息失败:', error);
            this.isLoggedIn = false;
            this.username = '';
          });
      }
    },
    logout() {
      axios.post('/logout')
        .then(response => {
          if (response.data.code === 200) {
            localStorage.removeItem('access_token');
            this.isLoggedIn = false;
            this.username = '';
            this.$router.push('/');
            this.$message.success('退出登录成功');
          }
        })
        .catch(error => {
          console.error('退出登录失败:', error);
          this.$message.error('退出登录失败，请重试');
        });
    },
    searchProblem() {
      const id = parseInt(this.searchProblemId, 10);
      if (id && this.problems.some(p => p.id === id)) {
        this.$router.push(`/problem/${id}`);
      } else {
        this.$message.error('请输入有效的题目序号');
      }
    }
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

.square-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  min-height: 100vh;
  background-image: url('@/background.gif'); /* 添加背景图片 */
  background-size: cover; /* 确保背景图片覆盖整个容器 */
  background-position: center; /* 居中背景图片 */
  background-repeat: no-repeat;
}

.background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  opacity: 0.3; /* 设置背景透明度 */
}

.content {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
  flex-wrap: wrap;
}

.left-sidebar, .right-sidebar {
  flex: 1 1 200px;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin: 10px;
  overflow-y: auto;
  color: #333;
}

.main-content {
  flex: 2 1 400px;
  padding: 15px;
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin: 10px;
  overflow-y: auto;
  color: #333;
}

.announcement {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #ffeeba;
  border-left: 5px solid #ffc107;
  border-radius: 4px;
  color: #333;
}

.links ul, .problems ul {
  list-style-type: none;
  padding: 0;
}

.links li, .problems li {
  margin-bottom: 10px;
}

.links a, .problems a {
  color: #007bff;
  text-decoration: none;
  transition: color 0.3s;
}

.links a:hover, .problems a:hover {
  color: #0056b3;
  text-decoration: underline;
}

.search {
  margin-bottom: 20px;
}

.search input {
  width: calc(100% - 80px);
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search button {
  padding: 8px 12px;
  margin-left: 8px;
  border: none;
  background-color: #28a745;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search button:hover {
  background-color: #218838;
}

.btn {
  padding: 10px 15px;
  margin: 5px 0;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #0056b3;
}

.ranking iframe {
  border: none;
  border-radius: 8px;
}
</style>