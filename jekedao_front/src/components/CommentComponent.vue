<template>
    <div class="comment-component">
      <h3>评论区</h3>
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <p>{{ comment.author }}: {{ comment.content }}</p>
        <p class="comment-time">{{ formatDate(comment.publish_time) }}</p>
      </div>
      <el-form @submit.native.prevent="submitComment">
        <el-form-item label="评论内容">
          <el-input type="textarea" v-model="newComment" placeholder="请输入评论内容"></el-input>
        </el-form-item>
        <el-button type="primary" @click="submitComment">发布评论</el-button>
      </el-form>
    </div>
  </template>
  
  <script>
  import axios from '@/axios';
  
  export default {
    name: 'CommentComponent',
    props: {
      discussionId: {
        type: Number,
        required: true
      }
    },
    data() {
      return {
        comments: [],
        newComment: ''
      };
    },
    created() {
      this.fetchComments();
    },
    methods: {
      fetchComments() {
        axios.get(`/discussions/${this.discussionId}/comments`)
          .then(response => {
            if (response.data.code === 200) {
              this.comments = response.data.data;
            } else {
              this.$message.error(response.data.msg || '获取评论列表失败');
            }
          })
          .catch(error => {
            console.error('获取评论列表失败:', error);
            this.$message.error('获取评论列表失败，请重试');
          });
      },
      submitComment() {
        if (!this.newComment) {
          this.$message.error('评论内容为必填项');
          return;
        }
  
        axios.post(`/discussions/${this.discussionId}/comments`, { content: this.newComment })
          .then(response => {
            if (response.data.code === 201) {
              this.$message.success('评论发布成功');
              this.newComment = '';
              this.fetchComments();
            } else {
              this.$message.error(response.data.msg || '评论发布失败');
            }
          })
          .catch(error => {
            console.error('评论发布失败:', error);
            this.$message.error('评论发布失败，请重试');
          });
      },
      formatDate(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleString();
      }
    }
  };
  </script>
  
  <style scoped>
  .comment-component {
    padding: 20px;
  }
  
  .comment {
    margin-bottom: 10px;
    padding: 10px;
    background-color: #f9f9f9;
    border-radius: 4px;
  }
  
  .comment-time {
    font-size: 12px;
    color: #999;
  }
  </style>