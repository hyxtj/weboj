// src/main.js

import Vue from 'vue';
import App from './App.vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from './axios'; // 使用自定义的 Axios 实例
import VueRouter from 'vue-router';
import router from './router'; // 从 router.js 导入路由
import NavBar from './components/NavBar.vue'; // 导入导航栏组件

Vue.config.productionTip = false;

Vue.use(ElementUI);
Vue.use(VueRouter);

// 将 Axios 挂载到 Vue 原型上，以便在所有组件中通过 this.$axios 访问
Vue.prototype.$axios = axios;

// 注册 NavBar 组件为全局组件（可选）
Vue.component('NavBar', NavBar);

new Vue({
  render: h => h(App),
  router,
  components: { NavBar },
}).$mount('#app');