// src/router.js

import Vue from 'vue';
import VueRouter from 'vue-router';
import HomePage from './components/HomePage.vue';
import Login from './components/Login.vue';
import Register from './components/Register.vue';
import ProblemSet from './components/ProblemSet.vue';
import ProblemList from './components/ProblemList.vue';
import ContestPage from './components/Contest.vue';
import ContestDetail from './components/ContestDetail.vue';
import CreateContest from './components/CreateContest.vue';
import DiscussionPage from './components/Discussion.vue';
import CreateDiscussion from './components/CreateDiscussion.vue';
import SquarePage from './components/Square.vue';
import UserProfile from './components/UserProfile.vue';
import ProblemDetail from './components/ProblemDetail.vue';
import UploadProblem from './components/UploadProblem.vue';
import SolutionDetail from './components/SolutionDetail.vue';
import CreateProblemList from './components/CreateProblemList.vue';
import SubmitCode from './components/SubmitCode.vue';
import Dashboard from './components/Dashboard.vue';
import UploadSolution from "@/components/UploadSolution.vue";
import DiscussionDetail from './components/DiscussionDetail.vue'; // 添加讨论详情页面

Vue.use(VueRouter);

const routes = [
  { path: '/', component: HomePage },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/problemset', component: ProblemSet, meta: { requiresAuth: true } },
  { path: '/problemlist', component: ProblemList, meta: { requiresAuth: true } },
  { path: '/contest', component: ContestPage, meta: { requiresAuth: true } },
  {
    path: '/contest/:id',
    component: ContestDetail,
    meta: { requiresAuth: true },
    props: true
  },
  { path: '/create-contest', component: CreateContest, meta: { requiresAuth: true } },
  { path: '/discussion', component: DiscussionPage, meta: { requiresAuth: true } },
  { path: '/create-discussion', component: CreateDiscussion, meta: { requiresAuth: true } }, // 添加发布讨论页面
  { path: '/discussion/:discussionId', component: DiscussionDetail, meta: { requiresAuth: true }, props: true }, // 添加讨论详情页面
  { path: '/square', component: SquarePage, meta: { requiresAuth: true } },
  {
    path: '/profile/:userId',
    component: UserProfile,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/problem/:problemId',
    component: ProblemDetail,
    meta: { requiresAuth: true },
    props: route => ({ problemId: parseInt(route.params.problemId, 10) }),
    children: [
      {
        path: 'solution',
        name: 'SolutionDetail',
        component: SolutionDetail,
        meta: { requiresAuth: true },
        props: route => ({ problemId: parseInt(route.params.problemId, 10) })
      },
      {
        path: 'submit',
        name: 'SubmitCode',
        component: SubmitCode,
        meta: { requiresAuth: true },
        props: route => ({ problemId: parseInt(route.params.problemId, 10) })
      },
    ]
  },
  { path: '/upload', component: UploadProblem, meta: { requiresAuth: true } },
  { path: '/uploadsolutions', component: UploadSolution, meta: { requiresAuth: true } }, // 上传题解
  { path: '/create-problemlist', component: CreateProblemList, meta: { requiresAuth: true } },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '*', redirect: '/login' },
];

const router = new VueRouter({
  mode: 'history',
  routes
});

// 路由守卫
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const token = localStorage.getItem('access_token');

  if (requiresAuth && !token) {
    next('/login');
  } else {
    next();
  }
});

// 全局导航守卫，触发全局事件以更新组件状态
router.afterEach(() => {
  const event = new Event('user-login-status-change');
  window.dispatchEvent(event);
});

export default router;