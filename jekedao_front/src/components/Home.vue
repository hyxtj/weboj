<template>
  <div class="home-container">
    <el-row>
      <el-col :span="12" class="form-container">
        <LoginComponent />
      </el-col>
      <el-col :span="12" class="form-container">
        <RegisterComponent />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import LoginComponent from './Login.vue';
import RegisterComponent from './RegisterComponent.vue';

export default {
  name: 'HomePage',
  components: {
    LoginComponent,
    RegisterComponent
  }
};
</script>

<style>
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f0f2f5;
}

.form-container {
  padding: 20px;
  background: #fff;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin: 10px;
}
</style>