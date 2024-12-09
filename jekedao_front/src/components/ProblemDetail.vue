<!-- src/components/ProblemDetail.vue -->
<template>
  <div class="problem-detail-container">
    <canvas id="starry"></canvas>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span class="title">{{ problem.title }}</span>
        <div class="header-buttons" v-if="isAuthor">
          <el-button
            type="primary"
            size="mini"
            icon="el-icon-edit"
            @click="openEditDialog"
          >
            编辑题目
          </el-button>
          <el-button
            type="danger"
            size="mini"
            icon="el-icon-delete"
            @click="deleteProblem"
          >
            删除题目
          </el-button>
        </div>
      </div>
      <div v-if="problem">
        <el-row>
          <el-col :span="4" class="label">描述:</el-col>
          <el-col :span="20" class="content">{{ problem.description }}</el-col>
        </el-row>
        <el-row>
          <el-col :span="4" class="label">难度:</el-col>
          <el-col :span="20" class="content">{{ problem.difficulty }}</el-col>
        </el-row>
        <el-row>
          <el-col :span="4" class="label">上传时间:</el-col>
          <el-col :span="20" class="content">{{ formatDate(problem.upload_time) }}</el-col>
        </el-row>
      </div>
      <div v-else-if="loading" class="loading">
        <el-spinner type="double-bubble"></el-spinner>
        <span>加载中...</span>
      </div>
      <div v-else class="error-message">
        <el-alert title="无效的题目ID" type="error" show-icon></el-alert>
      </div>
    </el-card>

    <!-- 编辑题目弹窗 -->
    <el-dialog title="编辑题目" :visible.sync="editDialogVisible">
      <el-form :model="editForm" :rules="editRules" ref="editForm" label-width="120px">
        <el-form-item label="题目标题" prop="title">
          <el-input v-model="editForm.title"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" v-model="editForm.description"></el-input>
        </el-form-item>
        <el-form-item label="难度" prop="difficulty">
          <el-select v-model="editForm.difficulty" placeholder="请选择难度">
            <el-option label="简单" value="Easy"></el-option>
            <el-option label="中等" value="Medium"></el-option>
            <el-option label="困难" value="Hard"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitEdit">确定</el-button>
      </div>
    </el-dialog>

    <!-- 题解和提交代码标签页 -->
    <el-tabs
      v-if="problem"
      type="card"
      class="tabs-section"
      @tab-click="handleTabClick"
      :value="activeTab"
    >
      <el-tab-pane label="题解" name="solution">
        <SolutionDetail :problemId="problemId" />
      </el-tab-pane>
      <el-tab-pane label="提交代码" name="submit">
        <SubmitCode :problemId="problemId" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import axios from '@/axios';
import SolutionDetail from './SolutionDetail.vue'; // 引入题解详情组件
import SubmitCode from './SubmitCode.vue'; // 引入提交代码组件

export default {
  name: 'ProblemDetail',
  components: {
    SolutionDetail,
    SubmitCode
  },
  props: {
    problemId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      problem: null,
      loading: false,
      isAuthor: false, // 是否为题目作者
      activeTab: 'solution', // 默认激活的标签
      editDialogVisible: false, // 编辑弹窗显示状态
      editForm: {
        title: '',
        description: '',
        difficulty: ''
      },
      editRules: {
        title: [
          { required: true, message: '请输入题目标题', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入题目描述', trigger: 'blur' }
        ],
        difficulty: [
          { required: true, message: '请选择难度', trigger: 'change' }
        ]
      }
    };
  },
  watch: {
    problemId(newId, oldId) {
      if (newId !== oldId) {
        this.fetchProblem();
      }
    }
  },
  created() {
    if (this.problemId) {
      this.fetchProblem();
      // 根据当前路由设置激活的标签
      const currentPath = this.$route.path;
      if (currentPath.includes('/solution')) {
        this.activeTab = 'solution';
      } else if (currentPath.includes('/submit')) {
        this.activeTab = 'submit';
      }
    } else {
      this.$message.error('无效的题目ID');
    }
  },
  methods: {
    fetchProblem() {
      console.log('Fetching problem with ID:', this.problemId);
      if (!this.problemId) {
        this.$message.error('无效的题目ID');
        return;
      }
      this.loading = true;
      axios.get(`/problems/${this.problemId}`)
        .then(response => {
          this.loading = false;
          if (response.data.code === 200) {
            this.problem = response.data.data;
            this.checkAuthor();
          } else {
            this.$message.error(response.data.msg || '获取题目信息失败');
          }
        })
        .catch(error => {
          this.loading = false;
          console.error('获取题目信息失败:', error);
          this.$message.error('获取题目信息失败，请重试');
        });
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleString();
    },
    checkAuthor() {
      // 假设后端返回的题目信息包含作者ID
      const currentUserId = parseInt(localStorage.getItem('user_id'), 10);
      if (this.problem.author_id === currentUserId) {
        this.isAuthor = true;
      }
      // 初始化编辑表单数据
      if (this.isAuthor) {
        this.editForm.title = this.problem.title;
        this.editForm.description = this.problem.description;
        this.editForm.difficulty = this.problem.difficulty;
      }
    },
    deleteProblem() {
      this.$confirm('确定要删除这个题目吗？', '删除题目', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        axios.delete(`/problems/${this.problemId}`)
          .then(response => {
            if (response.data.code === 200) {
              this.$message.success('题目删除成功');
              this.$router.push('/problemset');
            } else {
              this.$message.error(response.data.msg || '删除失败');
            }
          })
          .catch(error => {
            console.error('删除题目失败:', error);
            this.$message.error('删除题目失败，请重试');
          });
      }).catch(() => {
        // 取消删除
      });
    },
    openEditDialog() {
      this.editDialogVisible = true;
    },
    submitEdit() {
      this.$refs.editForm.validate((valid) => {
        if (valid) {
          axios.put(`/problems/${this.problemId}`, this.editForm)
            .then(response => {
              if (response.data.code === 200) {
                this.$message.success('题目编辑成功');
                this.editDialogVisible = false;
                this.fetchProblem(); // 重新获取最新题目信息
              } else {
                this.$message.error(response.data.msg || '编辑失败');
              }
            })
            .catch(error => {
              console.error('编辑题目失败:', error);
              this.$message.error('编辑题目失败，请重试');
            });
        } else {
          console.log('表单验证失败');
          return false;
        }
      });
    },
    handleTabClick(tab) {
      this.activeTab = tab.name;
      if (tab.name === 'solution') {
        this.$router.push(`/problem/${this.problemId}/solution`);
      } else if (tab.name === 'submit') {
        this.$router.push(`/problem/${this.problemId}/submit`);
      }
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
            ctx.strokeStyle = "rgba(0, 0, 0, 0.5)";
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
        return 'rgb(' + randNum(50, 200) + ',' + randNum(50, 200) + ',' + randNum(50, 200) + ')';
      }
    }
  },
  mounted() {
    this.initStarryBackground();
    window.addEventListener('resize', this.initStarryBackground);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.initStarryBackground);
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
  font-family: 'KaiTi', '楷体', serif; /* 设置字体为楷体 */
}
#starry {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #ffffff; /* 设置背景颜色为白色 */
  z-index: -1;
}
.problem-detail-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.9); /* 设置容器背景为白色 */
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}
.box-card {
  margin-bottom: 20px;
  width: 100%;
}
.title {
  font-size: 24px;
  font-weight: bold;
  font-family: 'KaiTi', '楷体', serif; /* 设置字体为楷体 */
}
.header-buttons {
  float: right;
}
.header-buttons .el-button {
  margin-left: 10px;
}
.label {
  font-weight: bold;
  padding: 10px 0;
  font-family: 'KaiTi', '楷体', serif; /* 设置字体为楷体 */
}
.content {
  padding: 10px 0;
  color: #555;
  font-family: 'KaiTi', '楷体', serif; /* 设置字体为楷体 */
}
.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  color: #409EFF;
  font-family: 'KaiTi', '楷体', serif; /* 设置字体为楷体 */
}
.loading span {
  margin-left: 10px;
}
.error-message {
  padding: 20px;
  font-family: 'KaiTi', '楷体', serif; /* 设置字体为楷体 */
}
.tabs-section {
  margin-top: 20px;
  width: 100%;
  font-family: 'KaiTi', '楷体', serif; /* 设置字体为楷体 */
}
</style>