<template>
  <div class="problem-list-page">
    <canvas id="cvs"></canvas>
    <div class="content">
      <h1>题单</h1>
      <el-collapse v-model="activeNames" accordion>
        <el-collapse-item
          v-for="list in problemLists"
          :key="list.id"
          :name="list.id.toString()"
        >
          <template #title>
            <div class="list-header">
              <span class="list-name">{{ list.name }}</span>
              <span class="list-meta">
                创建者: {{ list.creator }} | 创建时间: {{ list.createTime }} | 题目数量: {{ list.problems.length }}
              </span>
            </div>
          </template>
          <el-table :data="list.problems" style="width: 100%">
            <el-table-column prop="id" label="题目ID" width="100">
              <template #default="scope">
                <router-link :to="`/problem/${scope.row.id}`">{{ scope.row.id }}</router-link>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="题目名称" width="180">
              <template #default="scope">
                <router-link :to="`/problem/${scope.row.id}`">{{ scope.row.name }}</router-link>
              </template>
            </el-table-column>
            <el-table-column prop="difficulty" label="难度" width="100">
              <template #default="scope">
                <el-tag :type="getTagType(scope.row.difficulty)">{{ scope.row.difficulty }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="uploadTime" label="上传时间" width="180"></el-table-column>
          </el-table>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProblemList",
  data() {
    return {
      activeNames: [],
      problemLists: [
        {
          id: 1,
          name: "题单1",
          creator: "用户1",
          createTime: "2023-10-01",
          problems: [
            { id: 1, name: "题目1", difficulty: "简单", uploadTime: "2023-10-01" },
            { id: 2, name: "题目2", difficulty: "中等", uploadTime: "2023-10-02" },
            { id: 3, name: "题目3", difficulty: "困难", uploadTime: "2023-10-03" },
          ],
        },
        {
          id: 2,
          name: "题单2",
          creator: "用户2",
          createTime: "2023-10-02",
          problems: [
            { id: 4, name: "题目4", difficulty: "简单", uploadTime: "2023-10-04" },
            { id: 5, name: "题目5", difficulty: "中等", uploadTime: "2023-10-05" },
          ],
        },
        // 可以添加更多题单
      ],
    };
  },
  methods: {
    getTagType(difficulty) {
      switch (difficulty) {
        case "简单":
          return "success";
        case "中等":
          return "warning";
        case "困难":
          return "danger";
        default:
          return "";
      }
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
      // 重新设置画布大小后，可能需要重新初始化背景
      // 如果动画不继续，可以在这里调用 initDynamicBackground() 或其他恢复动画的逻辑
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

.problem-list-page {
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

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
}

.list-name {
  font-weight: bold;
  font-size: 20px;
}

.list-meta {
  color: #666;
  font-size: 14px;
}

.el-collapse-item__content {
  padding: 20px 0;
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
}

@media (max-width: 768px) {
  .content {
    padding: 20px;
  }

  h1 {
    font-size: 24px;
  }

  .list-name {
    font-size: 18px;
  }

  .list-meta {
    font-size: 12px;
  }

  .el-table-column {
    font-size: 14px;
  }
}
</style>