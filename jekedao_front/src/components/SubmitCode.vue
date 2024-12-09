<template>
  <div class="submit-code-container">
    <div class="form-section">
      <el-form @submit.native.prevent="submitCode">
        <el-form-item label="编程语言" :label-width="formLabelWidth">
          <el-select v-model="selectedLanguage" placeholder="请选择编程语言">
            <el-option label="Python" value="python"></el-option>
            <el-option label="JavaScript" value="javascript"></el-option>
            <el-option label="C++" value="cpp"></el-option>
            <el-option label="C" value="c"></el-option>
            <el-option label="Java" value="java"></el-option>
            <el-option label="Go" value="go"></el-option>
            <el-option label="Rust" value="rust"></el-option>
            <el-option label="Ruby" value="ruby"></el-option>
            <el-option label="PHP" value="php"></el-option>
            <el-option label="Swift" value="swift"></el-option>
            <el-option label="C#" value="csharp"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="代码" :label-width="formLabelWidth">
          <codemirror
  ref="myCm"
  v-model="code"
  :options="cmOptions"
  @ready="onCmReady"
  @blur="onCmBlur"
  @mousedown.native="onMouseDown">
</codemirror>


        </el-form-item>
        <el-button type="primary" @click="submitCode">提交代码</el-button>
      </el-form>
    </div>
    <div class="info-section">
      <div class="user-info">
        <h3>用户信息</h3>
        <p>用户名: {{ username }}</p>
        <p>用户ID: {{ userId }}</p>
      </div>
      <div class="problem-info">
        <h3>题目信息</h3>
        <p>题目ID: {{ problemId }}</p>
        <p>题目名称: {{ problemTitle }}</p>
      </div>
      <div class="submission-result" v-if="submissionResult">
        <h3>评测结果</h3>
        <p>状态: {{ submissionResult.status }}</p>
        <p>用时: {{ submissionResult.time }} ms</p>
        <p>内存: {{ submissionResult.memory }} KB</p>
      </div>
    </div>
  </div>
</template>

<script>
import { codemirror } from 'vue-codemirror';
import 'codemirror/lib/codemirror.css';
import 'codemirror/mode/python/python.js';
import 'codemirror/mode/javascript/javascript.js';
import 'codemirror/mode/clike/clike.js';
import 'codemirror/mode/go/go.js';
import 'codemirror/mode/rust/rust.js';
import 'codemirror/mode/ruby/ruby.js';
import 'codemirror/mode/php/php.js';
import 'codemirror/mode/swift/swift.js';
import 'codemirror/mode/clojure/clojure.js';

// 引入 CodeMirror 插件
import 'codemirror/addon/edit/matchbrackets.js';
import 'codemirror/addon/edit/closebrackets.js';
import 'codemirror/addon/fold/foldcode.js';
import 'codemirror/addon/fold/foldgutter.js';
import 'codemirror/addon/fold/brace-fold.js';
import 'codemirror/addon/fold/indent-fold.js';
import 'codemirror/addon/fold/comment-fold.js';
import 'codemirror/addon/hint/show-hint.js';
import 'codemirror/addon/hint/show-hint.css';
import 'codemirror/addon/hint/javascript-hint.js';
import 'codemirror/addon/hint/xml-hint.js';
import 'codemirror/addon/hint/html-hint.js';
import 'codemirror/addon/hint/anyword-hint.js';
import 'codemirror/addon/display/placeholder.js';
import 'codemirror/addon/fold/foldgutter.css'
import 'codemirror/addon/fold/foldcode'
import 'codemirror/addon/fold/foldgutter'
import 'codemirror/addon/fold/brace-fold'
import 'codemirror/addon/fold/comment-fold'
import 'codemirror/addon/fold/markdown-fold'
import 'codemirror/addon/fold/xml-fold'
import 'codemirror/addon/fold/indent-fold'
import 'codemirror/addon/hint/javascript-hint'
import 'codemirror/addon/hint/xml-hint'
import 'codemirror/addon/hint/sql-hint'
import 'codemirror/addon/hint/anyword-hint'

import 'codemirror/theme/monokai.css';
import 'codemirror/theme/eclipse.css';
import 'codemirror/theme/neat.css';

export default {
  name: 'SubmitCode',
  components: {
    codemirror
  },
  data() {
    return {
      selectedLanguage: '',
      code: '',
      problemId: this.$route.params.problemId,
      username: '用户', // 需要从后端获取
      userId: 1, // 需要从后端获取
      problemTitle: '题目名称', // 需要从后端获取
      formLabelWidth: '100px',
      submissionResult: null,
      submissionId: null,
      pollingInterval: null,
      cmOptions: {
        theme: 'monokai',
        mode: 'python',
        readOnly: false,
        tabSize: 4, // 制表符
        indentUnit: 4, // 缩进位数
        lineNumbers: true,
        ineWiseCopyCut: true,
        viewportMargin: 1000,
        autofocus: true,
        autocorrect: true,
        spellcheck: true,
       // specialChars: /[\u0000-\u001f\u007f-\u009f\u00ad\u061c\u200b-\u200f\u2028\u2029\ufeff\ufff9-\ufffc]/g,
        specialCharPlaceholder: function (ch) {
          let token = document.createElement("span");
          token.className = "cm-invalidchar";
          token.title = "\\u" + ch.charCodeAt(0).toString(16);
          token.setAttribute("aria-label", token.title);
          return token
        },
        extraKeys: {
          Tab: (cm) => {
            if (cm.somethingSelected()) {
              cm.indentSelection('add');
            } else {
              cm.replaceSelection(Array(cm.getOption("indentUnit") + 1).join(" "), "end", "+input");  // 光标处插入 indentUnit 个空格
            }
          },
        },
        lint: false,
        gutters: [
            "CodeMirror-lint-markers",
          "CodeMirror-linenumbers",
          "CodeMirror-foldgutter"
        ],
        lineWrapping: false,
        foldGutter: true, // 启用行槽中的代码折叠
        autoCloseBrackets: true, // 自动闭合符号
        autoCloseTags: true,
        matchTags: { bothTags: true },
        matchBrackets: true, // 在光标点击紧挨{、]括号左、右侧时，自动突出显示匹配的括号 }、]
        styleSelectedText: true,
        styleActiveLine: true,
        autoRefresh: true,
        highlightSelectionMatches: {
          minChars: 2,
          trim: true,
          style: "matchhighlight",
          showToken: false
        },
        hintOptions: {
          completeSingle: false
        }
}
    };
  },
  watch: {
    selectedLanguage(newVal) {
      switch (newVal) {
        case 'python':
          this.cmOptions.mode = 'text/x-python';
          break;
        case 'javascript':
          this.cmOptions.mode = 'text/javascript';
          break;
        case 'cpp':
          this.cmOptions.mode = 'text/x-c++src';
          break;
        case 'c':
          this.cmOptions.mode = 'text/x-csrc';
          break;
        case 'java':
          this.cmOptions.mode = 'text/x-java';
          break;
        case 'go':
          this.cmOptions.mode = 'text/x-go';
          break;
        case 'rust':
          this.cmOptions.mode = 'text/x-rustsrc';
          break;
        case 'ruby':
          this.cmOptions.mode = 'text/x-ruby';
          break;
        case 'php':
          this.cmOptions.mode = 'text/x-php';
          break;
        case 'swift':
          this.cmOptions.mode = 'text/x-swift';
          break;
        case 'csharp':
          this.cmOptions.mode = 'text/x-csharp';
          break;
        default:
          this.cmOptions.mode = 'text/x-python';
      }
    }
  },
  created() {
    this.fetchProblemDetails();
    this.fetchUserDetails();
  },
  methods: {
    fetchProblemDetails() {
      this.$axios.get(`/problems/${this.problemId}`)
        .then(response => {
          if (response.data.code === 200) {
            this.problemTitle = response.data.data.title;
          } else {
            this.$message.error(response.data.msg || '无法获取题目信息');
          }
        })
        .catch(error => {
          console.error('获取题目信息失败:', error);
          this.$message.error('获取题目信息失败，请重试');
        });
    },
    fetchUserDetails() {
      this.$axios.get('/profile/me')
        .then(response => {
          if (response.data.code === 200) {
            this.username = response.data.data.username;
            this.userId = response.data.data.id;
          } else {
            this.$message.error(response.data.msg || '无法获取用户信息');
          }
        })
        .catch(error => {
          console.error('获取用户信息失败:', error);
          this.$message.error('获取用户信息失败，请重试');
        });
    },
    submitCode() {
      const payload = {
        problem_id: parseInt(this.problemId, 10),  // 确保 problemId 是正整数
        language: this.selectedLanguage,
        code: this.code
      };

      console.log('Sending payload:', payload);  // 调试步骤

      this.$axios.post('/submit', payload)
        .then(response => {
          if (response.data.code === 201) {
            this.submissionId = response.data.submission_id;
            this.startPolling();
            this.$message.success('代码提交成功');
          } else {
            this.$message.error(response.data.msg || '代码提交失败');
          }
        })
        .catch(error => {
          console.error('提交失败:', error);
          this.$message.error('代码提交失败，请重试');
        });
    },
    startPolling() {
      this.pollingInterval = setInterval(() => {
        this.$axios.get(`/submission/${this.submissionId}`)
          .then(response => {
            if (response.data.code === 200) {
              this.submissionResult = response.data.data;
              if (this.submissionResult.status !== 'Pending') {
                clearInterval(this.pollingInterval);
                this.$message.success('评测完成');
              }
            } else {
              this.$message.error(response.data.msg || '获取评测结果失败');
              clearInterval(this.pollingInterval);
            }
          })
          .catch(error => {
            console.error('获取评测结果失败:', error);
            this.$message.error('获取评测结果失败，请重试');
            clearInterval(this.pollingInterval);
          });
      }, 2000); // 每2秒轮询一次
    },
    onCmReady(cm) {
  // 这里的 cm 对象就是 codemirror 对象，等于 this.$refs.myCm.codemirror
  cm.on("inputRead", (cm, obj) => {
    if (obj.text && obj.text.length > 0) {
    let c = obj.text[0].charAt(obj.text[0].length - 1)
      if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
        cm.showHint({ completeSingle:false })
      }
    }
  })
}
  }
};



</script>

<style scoped>

.CodeMirror-hints {
  position: absolute;
  z-index: 10;
  overflow: hidden;
  list-style: none;

  margin: 0;
  padding: 2px;

  -webkit-box-shadow: 2px 3px 5px rgba(0,0,0,.2);
  -moz-box-shadow: 2px 3px 5px rgba(0,0,0,.2);
  box-shadow: 2px 3px 5px rgba(0,0,0,.2);
  border-radius: 3px;
  border: 1px solid silver;

  background: white;
  font-size: 90%;
  font-family: monospace;

  max-height: 20em;
  overflow-y: auto;
}
.submit-code-container {
  display: flex;
  flex-wrap: wrap;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-section {
  flex: 2 1 60%;
  padding: 20px;
}

.info-section {
  flex: 1 1 30%;
  padding: 20px;
  margin-left: 20px;
}

.user-info, .problem-info, .submission-result {
  margin-bottom: 20px;
}

.user-info h3, .problem-info h3, .submission-result h3 {
  margin-bottom: 10px;
  color: #007bff;
}

@media (max-width: 768px) {
  .submit-code-container {
    flex-direction: column;
  }
  .info-section {
    margin-left: 0;
    margin-top: 20px;
  }
}
</style>
