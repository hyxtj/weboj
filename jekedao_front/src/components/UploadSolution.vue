<template>
  <div class="upload-solution">
    <canvas id="starfield"></canvas>
    <div class="content">
      <h1>上传题解</h1>
      <el-form
        ref="form"
        :model="form"
        :rules="rules"
        label-width="80px"
        @submit.native.prevent="submitForm"
      >
        <el-form-item label="题目ID" prop="problemId">
          <el-input
            v-model.number="form.problemId"
            placeholder="请输入题目ID"
            type="number"
          ></el-input>
        </el-form-item>

        <el-form-item label="题解内容" prop="solution">
          <el-input
            type="textarea"
            v-model="form.solution"
            placeholder="请输入题解内容"
            :rows="5"
          ></el-input>
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
  name: "UploadSolution",
  data() {
    return {
      form: {
        problemId: null,
        solution: "",
      },
      loading: false,
      rules: {
        problemId: [
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
        solution: [
          { required: true, message: "请输入题解内容", trigger: "blur" },
          { min: 10, message: "题解内容长度至少10个字符", trigger: "blur" },
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
            .post("/uploadsolutions", {
              problemId: this.form.problemId,
              solution: this.form.solution,
            })
            .then((response) => {
              this.loading = false;
              if (response.data.code === 201) {
                this.$message.success("题解上传成功！");
                this.resetForm();
                this.$router.push("/problemset"); // 确保跳转路径正确
              } else {
                this.$message.error(response.data.msg || "题解上传失败");
              }
            })
            .catch((error) => {
              this.loading = false;
              console.error("题解上传失败:", error);
              if (error.response) {
                console.error("响应数据:", error.response.data);
                console.error("响应状态:", error.response.status);
                console.error("响应头:", error.response.headers);
                this.$message.error(
                  error.response.data.msg || "题解上传失败"
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

.upload-solution {
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