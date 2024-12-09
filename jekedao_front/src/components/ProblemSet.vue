<template>
  <div class="problem-set">
    <canvas id="cvs"></canvas>
    <div class="content">
      <h1>题库</h1>
      <div v-if="problems.length === 0" class="no-problems">没有题目</div>
      <el-row v-else>
        <el-col :span="24">
          <el-table
            :data="displayedProblems"
            border
            style="width: 100%">
            <el-table-column prop="id" label="题目ID" width="100">
              <template #default="scope">
                <router-link :to="`/problem/${scope.row.id}`">{{ scope.row.id }}</router-link>
              </template>
            </el-table-column>
            <el-table-column prop="title" label="题目名称" width="200">
              <template #default="scope">
                <router-link :to="`/problem/${scope.row.id}`">{{ scope.row.title }}</router-link>
              </template>
            </el-table-column>
            <el-table-column prop="difficulty" label="难度" width="120">
              <template #default="scope">
                <el-tag :color="getTagColor(scope.row.difficulty)">{{ scope.row.difficulty }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="upload_time" label="上传时间" width="180"></el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button @click="viewProblem(scope.row.id)" type="primary" size="medium">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="pagination">
            <el-pagination
              @current-change="handleCurrentChange"
              :current-page="currentPage"
              :page-size="pageSize"
              layout="prev, pager, next"
              :total="problems.length">
            </el-pagination>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import axios from '@/axios'; // 使用实例化的 Axios

export default {
  name: 'ProblemSet',
  data() {
    return {
      problems: [],
      currentPage: 1,
      pageSize: 10,
    };
  },
  computed: {
    displayedProblems() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = this.currentPage * this.pageSize;
      return this.problems.slice(start, end);
    },
  },
  created() {
    this.fetchProblems();
  },
  methods: {
    getTagColor(difficulty) {
      switch (difficulty) {
        case 'Easy':
          return '#67C23A'; // 绿色
        case 'Medium':
          return '#E6A23C'; // 橙色
        case 'Hard':
          return '#F56C6C'; // 红色
        default:
          return '#909399'; // 灰色
      }
    },
    viewProblem(id) {
      this.$router.push(`/problem/${id}`);
    },
    handleCurrentChange(page) {
      this.currentPage = page;
    },
    fetchProblems() {
      axios.get('/problems') // 使用 axios 实例
        .then(response => {
          if (response.data.code === 200) {
            this.problems = response.data.data.map(problem => ({
              id: problem.id,
              title: problem.title,
              difficulty: problem.difficulty,
              upload_time: problem.upload_time.split('T')[0] // 格式化日期
            }));
          } else {
            this.$message.error(response.data.msg || '获取题目失败');
          }
        })
        .catch(error => {
          console.error('获取题目失败:', error);
          this.$message.error('获取题目失败，请重试');
        });
    },
    initDynamicBackground() {
      const cvs = document.getElementById("cvs");
      const ctx = cvs.getContext("2d");
      const { clientWidth: width, clientHeight: height } = document.documentElement;
      cvs.width = width;
      cvs.height = height;
      ctx.fillStyle = "#ffffff"; // 小点的颜色

      // 生成小点，400是小点的数量
      const bgColors = Array.from(new Array(400)).map(() => ({
        x: Math.random() * width,
        y: Math.random() * height,
        step: Math.random() * 0.1 + 0.5,
      }));

      // 渲染函数
      const render = () => {
        ctx.clearRect(0, 0, width, height);
        ctx.beginPath();
        bgColors.forEach((v) => {
          v.y = v.y > height ? 0 : v.y + v.step;
          ctx.rect(v.x, v.y, 3, 3);
        });
        ctx.fill();
        requestAnimationFrame(render);
      };
      render();

      // 禁止用户缩放浏览器
      const keyCodeMap = {
        61: true,
        107: true, // 数字键盘 +
        109: true, // 数字键盘 -
        173: true, // 火狐 - 号
        187: true, // +
        189: true, // -
      };
      // 覆盖ctrl||command + ‘+’/‘-’
      document.onkeydown = function (event) {
        const e = event || window.event;
        const ctrlKey = e.ctrlKey || e.metaKey;
        if (ctrlKey && keyCodeMap[e.keyCode]) {
          e.preventDefault();
        } else if (e.detail) {
          // Firefox
          event.returnValue = false;
        }
      };
      // 覆盖鼠标滑动
      document.body.addEventListener(
        "wheel",
        (e) => {
          if (e.ctrlKey) {
            e.preventDefault();
            return false;
          }
        },
        { passive: false }
      );
    },
  },
  mounted() {
    this.initDynamicBackground();
    window.addEventListener("resize", () => {
      const cvs = document.getElementById("cvs");
      const { clientWidth: width, clientHeight: height } = document.documentElement;
      cvs.width = width;
      cvs.height = height;
      // 重新初始化背景以适应新的尺寸
      this.initDynamicBackground();
    });
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "KaiTi", serif;
}

html,
body,
#app {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

canvas#cvs {
  position: absolute;
  top: 0;
  left: 0;
  z-index: -6;
  background-color: #000;
}

.problem-set {
  position: relative;
  padding: 20px;
  height: 100vh;
  overflow: auto;
}

.content {
  background: rgba(255, 255, 255, 0.95);
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  color: #333;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 32px;
}

.no-problems {
  text-align: center;
  font-size: 18px;
  color: #999;
  margin-top: 50px;
}

.el-table {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.el-table th {
  background-color: #f5f5f5;
  color: #333;
}

.el-tag {
  border-radius: 4px;
  padding: 5px 10px;
  color: #fff;
  font-weight: bold;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.el-button {
  min-width: 80px;
  height: 40px;
  font-size: 16px;
  border-radius: 8px;
}

.el-button.primary {
  background-color: #409eff;
  color: #fff;
}

.el-button.primary:hover {
  background-color: #66b1ff;
}

.el-button.default {
  background-color: #f5f5f5;
  color: #333;
}

.el-button.default:hover {
  background-color: #e6e6e6;
}

@media (max-width: 768px) {
  .content {
    padding: 20px;
  }

  h1 {
    font-size: 24px;
  }

  .no-problems {
    font-size: 16px;
  }

  .el-tag {
    font-size: 14px;
    padding: 4px 8px;
  }

  .el-button {
    min-width: 70px;
    height: 35px;
    font-size: 14px;
  }
}
</style>