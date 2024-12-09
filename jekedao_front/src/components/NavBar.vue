<!-- src/components/NavBar.vue -->
<template>
  <div class="navbar">
    <el-button type="primary" @click="toggleMenu">
      <i :class="menuIcon"></i>
    </el-button>
    <el-drawer
      title="导航菜单"
      :visible.sync="menuVisible"
      direction="ltr"
      size="20%"
      :wrapper-closable="false"
      :modal-append-to-body="false"
      :before-close="handleClose"
    >
      <div class="menu">
        <el-button type="text" @click="navigateTo('/')">首页</el-button>
        <el-button type="text" @click="navigateTo('/square')">广场</el-button>
        <el-button type="text" @click="navigateTo('/problemset')">题库</el-button>
        <el-button type="text" @click="navigateTo('/problemlist')">题单</el-button>
        <el-button type="text" @click="navigateTo('/contest')">比赛</el-button>
        <el-button type="text" @click="navigateTo('/discussion')">讨论</el-button>
        <el-button type="text" @click="navigateTo('/create-contest')">发布比赛</el-button>
        <el-button type="text" @click="navigateTo('/upload')">上传题目</el-button>
        <el-button type="text" @click="navigateTo('/create-problemlist')">设计题单</el-button>
        <el-button y="bottom" type="text" @click="navigateTo('/uploadsolutions')">上传题解</el-button>

        <template v-if="!isLoggedIn">
          <el-divider></el-divider>
          <el-button type="text" @click="navigateTo('/login')">登录</el-button>
          <el-button type="text" @click="navigateTo('/register')">注册</el-button>
        </template>
        <template v-else>
          <el-divider></el-divider>
          <el-button type="text" @click="navigateToProfile">个人主页</el-button>
          <el-button type="text" @click="logout">退出登录</el-button>
        </template>
      </div>
    </el-drawer>
  </div>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      menuVisible: false,
      isLoggedIn: false,
      username: '',
      userId: null
    };
  },
  computed: {
    menuIcon() {
      return this.menuVisible ? 'el-icon-close' : 'el-icon-menu';
    }
  },
  created() {
    this.checkLoginStatus();
    // 监听全局事件，更新登录状态
    window.addEventListener('user-login-status-change', this.checkLoginStatus);
  },
  beforeDestroy() {
    window.removeEventListener('user-login-status-change', this.checkLoginStatus);
  },
  methods: {
    toggleMenu() {
      this.menuVisible = !this.menuVisible;
    },
    navigateTo(route) {
      this.menuVisible = false;
      this.$router.push(route).catch(err => {
        console.error('路由跳转失败:', err);
        this.menuVisible = true;
      });
    },
    // 修改 handleClose 方法，接受 done 回调并正确调用它
    handleClose(done) {
      // 弹出确认对话框
      this.$confirm('确定关闭导航菜单？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(() => {
        done(); // 调用 done 回调以完成关闭
      }).catch(() => {
        // 用户取消关闭，不调用 done()，Drawer 保持开启
      });
    },
    logout() {
      // 删除 Token
      localStorage.removeItem('access_token');
      // 清除 Axios 默认头
      delete this.$axios.defaults.headers.common['Authorization'];
      this.isLoggedIn = false;
      this.username = '';
      this.userId = null;
      this.$message.success('退出登录成功');
      this.navigateTo('/login');
      // 触发全局事件，通知其他组件
      const event = new Event('user-login-status-change');
      window.dispatchEvent(event);
    },
    checkLoginStatus() {
      const token = localStorage.getItem('access_token');
      if (token) {
        this.isLoggedIn = true;
        // 获取用户信息（例如用户名和用户ID）
        this.$axios.get('/profile/me') // 使用 this.$axios
          .then(response => {
            if (response.data.code === 200) {
              this.username = response.data.data.username;
              this.userId = response.data.data.id;
            } else {
              this.isLoggedIn = false;
              this.userId = null;
            }
          })
          .catch(() => {
            this.isLoggedIn = false;
            this.userId = null;
          });
      } else {
        this.isLoggedIn = false;
        this.userId = null;
      }
    },
    navigateToProfile() {
      if (this.userId) {
        this.navigateTo(`/profile/${this.userId}`);
      } else {
        this.$message.error('无法获取用户信息');
      }
    }
  }
};
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 10px;
  left: 10px;
  z-index: 1000; /* 确保按钮置于所有层的上方 */
  font-family: '楷体', 'KaiTi', serif;
}

.menu {
  display: flex;
  flex-direction: column;
  margin-top: 20px;
  font-family: '楷体', 'KaiTi', serif;
  align-items: center; /* 添加此行以居中按钮 */
}

.el-divider {
  margin: 10px 0;
  font-family: '楷体', 'KaiTi', serif;
}

/* 确保所有按钮上的文字均为楷体 */
.el-button {
  font-family: '楷体', 'KaiTi', serif;
}
</style>