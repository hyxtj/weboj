<template>
  <div class="create-problemlist">
    <h1>设计题单</h1>
    <el-form ref="form" :model="form" label-width="100px">
      <el-form-item label="题单名称">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item label="题单描述">
        <el-input type="textarea" v-model="form.description"></el-input>
      </el-form-item>
      <el-form-item label="选择题目">
        <el-select v-model="form.selectedProblems" multiple placeholder="请选择题目">
          <el-option
            v-for="problem in problems"
            :key="problem.id"
            :label="problem.name"
            :value="problem.id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'CreateProblemList',
  data() {
    return {
      form: {
        name: '',
        description: '',
        selectedProblems: []
      },
      problems: [
        { id: 1, name: '题目1' },
        { id: 2, name: '题目2' },
        { id: 3, name: '题目3' }
        // 可以添加更多题目
      ]
    };
  },
  methods: {
    submitForm() {
      // 提交表单逻辑
      console.log('提交题单:', this.form);
      // 可以在这里添加提交到服务器的逻辑
    }
  }
};
</script>

<style>
.create-problemlist {
  padding: 20px;
}

h1 {
  color: #333;
}

.el-form-item {
  margin-bottom: 20px;
}
</style>