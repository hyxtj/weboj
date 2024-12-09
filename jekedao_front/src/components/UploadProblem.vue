<template>
  <div class="upload-problem">
    <canvas id="starfield"></canvas>
    <div class="content">
      <h1>上传题目</h1>
      <el-form
        ref="form"
        :model="form"
        :rules="rules"
        label-width="80px"
        @submit.native.prevent="submitForm"
      >
        <el-form-item label="题目ID" prop="id">
          <el-input
            v-model.number="form.id"
            placeholder="请输入题目ID"
            type="number"
          ></el-input>
        </el-form-item>

        <el-form-item label="题目标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入题目标题"></el-input>
        </el-form-item>

        <el-form-item label="题目描述" prop="description">
          <el-input
            type="textarea"
            v-model="form.description"
            placeholder="请输入题目描述"
            :rows="5"
          ></el-input>
        </el-form-item>

        <el-form-item label="难度" prop="difficulty">
          <el-select v-model="form.difficulty" placeholder="请选择难度">
            <el-option label="Easy" value="Easy"></el-option>
            <el-option label="Medium" value="Medium"></el-option>
            <el-option label="Hard" value="Hard"></el-option>
          </el-select>
        </el-form-item>

        <!-- 测试用例输入和输出 -->
        <el-form-item label="测试用例">
          <div
            v-for="(testCase, index) in form.testCases"
            :key="index"
            class="test-case"
          >
            <el-form-item
              label="输入"
              :prop="'testCases.' + index + '.input'"
              :rules="rules.testCaseInput"
              class="inline-form-item"
            >
              <el-input
                type="textarea"
                v-model="testCase.input"
                placeholder="请输入测试用例输入"
                :rows="3"
              ></el-input>
            </el-form-item>
            <el-form-item
              label="输出"
              :prop="'testCases.' + index + '.output'"
              :rules="rules.testCaseOutput"
              class="inline-form-item"
            >
              <el-input
                type="textarea"
                v-model="testCase.output"
                placeholder="请输入测试用例输出"
                :rows="3"
              ></el-input>
            </el-form-item>
            <el-button
              type="danger"
              @click="removeTestCase(index)"
              class="delete-button"
            >
              删除
            </el-button>
          </div>
          <el-button type="primary" @click="addTestCase" class="add-button">
            添加测试用例
          </el-button>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            @click="submitForm"
            :loading="loading"
            class="submit-button"
          >
            提交
          </el-button>
          <el-button @click="resetForm" class="reset-button">
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import axios from "@/axios"; // 使用配置好的 Axios 实例

export default {
  name: "UploadProblem",
  data() {
    return {
      form: {
        id: null, // 添加 ID 字段
        title: "",
        description: "",
        difficulty: "Medium",
        testCases: [{ input: "", output: "" }], // 初始化至少一个测试用例
      },
      loading: false,
      rules: {
        id: [
          { required: true, message: "请输入题目ID", trigger: "blur" },
          { type: "number", message: "题目ID必须是数字", trigger: "blur" },
          {
            validator: (rule, value, callback) => {
              if (value === null || value === undefined) {
                callback(new Error("题目ID为必填项"));
              } else if (typeof value !== "number") {
                callback(new Error("题目ID必须是数字"));
              } else if (value <= 0) {
                callback(new Error("题目ID必须大于0"));
              } else {
                callback();
              }
            },
            trigger: "blur",
          },
        ],
        title: [
          { required: true, message: "请输入题目标题", trigger: "blur" },
          {
            min: 5,
            max: 100,
            message: "标题长度在5到100个字符",
            trigger: "blur",
          },
        ],
        description: [
          { required: true, message: "请输入题目描述", trigger: "blur" },
          { min: 10, message: "描述长度至少10个字符", trigger: "blur" },
        ],
        difficulty: [
          { required: true, message: "请选择难度", trigger: "change" },
        ],
        testCaseInput: [
          { required: true, message: "请输入测试用例输入", trigger: "blur" },
        ],
        testCaseOutput: [
          { required: true, message: "请输入测试用例输出", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    submitForm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loading = true;
          axios
            .post("/problems", {
              id: this.form.id,
              title: this.form.title,
              description: this.form.description,
              difficulty: this.form.difficulty,
              testCases: this.form.testCases,
            })
            .then((response) => {
              this.loading = false;
              if (response.data.code === 201) {
                this.$message.success("题目上传成功！");
                this.resetForm();
                this.$router.push("/problemset"); // 确保跳转路径正确
              } else {
                this.$message.error(response.data.msg || "题目上传失败");
              }
            })
            .catch((error) => {
              this.loading = false;
              console.error("题目上传失败:", error);
              if (error.response) {
                console.error("响应数据:", error.response.data);
                console.error("响应状态:", error.response.status);
                console.error("响应头:", error.response.headers);
                this.$message.error(
                  error.response.data.msg || "题目上传失败"
                );
              } else if (error.request) {
                console.error("请求数据:", error.request);
                this.$message.error("未收到服务器响应，请检查网络连接");
              } else {
                console.error("错误信息:", error.message);
                this.$message.error("发生错误，请重试");
              }
            });
        } else {
          this.$message.error("请完成表单字段的填写");
          return false;
        }
      });
    },
    resetForm() {
      this.$refs.form.resetFields();
    },
    addTestCase() {
      this.form.testCases.push({ input: "", output: "" });
    },
    removeTestCase(index) {
      if (this.form.testCases.length > 1) {
        this.form.testCases.splice(index, 1);
      } else {
        this.$message.error("至少需要一个测试用例");
      }
    },
    drawStars() {
      const canvas = document.getElementById("starfield");
      const context = canvas.getContext("2d");
      let stars = [];
      const starsCount = 300;

      function init() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        stars = [];
        createStars();
      }

      function createStars() {
        for (let i = 0; i < starsCount; i++) {
          const x = Math.random() * canvas.width;
          const y = Math.random() * canvas.height;
          const radius = Math.random() * 1.5;
          const color = `rgba(${Math.floor(
            Math.random() * 255
          )}, ${Math.floor(Math.random() * 255)}, ${Math.floor(
            Math.random() * 255
          )}, 0.8)`;
          const speed = Math.random() * 0.5;
          stars.push({ x, y, radius, color, speed });
        }
      }

      function animate() {
        context.fillStyle = "#0e1729";
        context.fillRect(0, 0, canvas.width, canvas.height);
        stars.forEach((star) => {
          star.x -= star.speed;
          if (star.x < -star.radius) star.x = canvas.width + star.radius;
          context.beginPath();
          context.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
          context.fillStyle = star.color;
          context.fill();
        });
        requestAnimationFrame(animate);
      }

      window.addEventListener("resize", init);
      init();
      animate();
    },
  },
  mounted() {
    this.drawStars();
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'KaiTi', serif;
}

html,
body,
#app {
  height: 100%;
  margin: 0;
  padding: 0;
}

canvas#starfield {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -6;
  background: #0e1729;
}

.upload-problem {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  position: relative;
  padding: 20px;
}

.content {
  background: rgba(255, 255, 255, 0.95);
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  color: #333;
  width: 100%;
  max-width: 700px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.el-form-item {
  margin-bottom: 25px;
}

.inline-form-item {
  display: inline-block;
  width: 45%;
  margin-right: 5%;
}

.inline-form-item:last-child {
  margin-right: 0;
}

.test-case {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
}

.test-case .el-form-item {
  flex: 1;
  margin-right: 10px;
}

.test-case .el-form-item:last-child {
  margin-right: 0;
}

.delete-button {
  height: 40px;
  align-self: center;
}

.add-button {
  width: 100%;
  height: 45px;
  font-size: 16px;
  border-radius: 8px;
}

.submit-button,
.reset-button {
  height: 50px;
  font-size: 18px;
  border-radius: 8px;
  width: 48%;
}

.reset-button {
  margin-left: 4%;
  background-color: #f5f5f5;
  color: #333;
}

.submit-button {
  background-color: #409eff;
  color: #fff;
}

.submit-button:hover {
  background-color: #66b1ff;
}

.reset-button:hover {
  background-color: #e6e6e6;
}
</style>