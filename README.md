# Online Judge Platform
这是一个在线评测平台（Online Judge Platform）项目，采取前后端分离开发的思想，前端使用Vue.js框架开发，后端使用Flask框架开发，Mysql数据库维护。项目支持用户注册、登录、题目管理、代码提交评测、讨论区等功能。

## 项目结构

```
oj_platform/
├── app.py 
├── judger2.py
├── requirements.txt
├── Introduction.md
├── oj_platform.sql
└── jekedao_front/
    ├── node_modules/
    ├── package.json
    ├── package-lock.json
    ├── public/
    ├── src/
        ├── App.vue
        ├── main.js
        ├── router.js
        ├── assets/
        ├── components/
            ├── CommentComponent.vue
            ├── Contest.vue
            ├── ContestDetail.vue
            ├── CreateContest.vue
            ├── CreateDiscussion.vue
            ├── CreateProblemList.vue
            ├── Dashboard.vue
            ├── Discussion.vue
            ├── DiscussionDetail.vue
            ├── Home.vue
            ├── HomePage.vue
            ├── Login.vue
            ├── NavBar.vue
            ├── ProblemDetail.vue
            ├── ProblemList.vue
            ├── ProblemSet.vue
            ├── Register.vue
            ├── SolutionDetail.vue
            ├── Square.vue
            ├── SubmitCode.vue
            ├── UploadProblem.vue
            ├── UploadSolution.vue
            └──  UserProfile.vue
```

## 依赖项

项目所需的依赖项已列在`requirements.txt`文件中。请确保在部署前安装所有依赖项。

### 安装依赖项

```bash
pip install -r requirements.txt
```

## 系统要求

- Python 3.7 或更高版本
- MySQL 5.7 或更高版本
- GCC 和 G++ 编译器（用于代码评测）
- Windows SDK（用于资源限制）

## 安装步骤

### 1. 安装Python

确保机器上安装了Python 3.7或更高版本。可以从[Python官网](https://www.python.org/downloads/)下载并安装。

### 2. 安装MySQL

确保机器上安装了MySQL数据库。可以从[MySQL官网](https://dev.mysql.com/downloads/installer/)下载并安装。

### 3. 安装GCC和G++编译器

评测机需要使用GCC和G++编译器来编译用户提交的代码。可以从[MinGW](https://sourceforge.net/projects/mingw/)下载并安装MinGW，确保安装了GCC和G++编译器。

#### 配置环境变量：

将MinGW的`bin`目录添加到系统的`PATH`环境变量中，以便在命令行中可以直接调用`gcc`和`g++`命令。

### 4. 安装Windows SDK

为了在Windows上限制进程的资源使用，需要安装Windows SDK。可以从[Windows SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/)下载并安装。

### 5. 配置数据库

在MySQL中创建一个新的数据库，并在项目中配置数据库连接。

#### 创建数据库：

```sql
CREATE DATABASE oj_platform;
```

#### 配置数据库连接：

在`app.py`中配置数据库连接URI：

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/oj_platform'
```

### 6. 初始化数据库

使用Flask-Migrate初始化数据库并创建表结构。

#### 初始化迁移环境：

```bash
flask db init
```

#### 生成迁移脚本：

```bash
flask db migrate -m "Initial migration"
```

#### 应用迁移：

```bash
flask db upgrade
```

### 7. 启动项目

在项目根目录下运行以下命令启动Flask应用：

```bash
python app.py
```

### 8. 配置评测机

确保评测机代码（`judger2.py`）能够正确运行。可以在本地测试评测机的功能，确保编译和运行用户代码的逻辑正确。

### 9. 配置日志和监控（可选）

如果需要日志和监控功能，可以配置ELK堆栈或Prometheus和Grafana。

#### 安装ELK堆栈：

- Elasticsearch: [下载](https://www.elastic.co/downloads/elasticsearch)
- Logstash: [下载](https://www.elastic.co/downloads/logstash)
- Kibana: [下载](https://www.elastic.co/downloads/kibana)

#### 安装Prometheus和Grafana：

- Prometheus: [下载](https://prometheus.io/download/)
- Grafana: [下载](https://grafana.com/grafana/download)

## 前端部分

### 技术栈

- **框架**: Vue.js 3.x
- **UI 组件库**: Element UI
- **HTTP 请求**: Axios
- **路由管理**: Vue Router
- **动画**: Canvas
- **代码分割**: 动态导入（`import()`）
- **打包工具**: Webpack

### 依赖安装

#### 1. 安装 Node.js 和 npm

确保你已经安装了 Node.js 和 npm。你可以通过以下命令检查是否已安装：

```bash
node -v
npm -v
```

如果没有安装，请访问 [Node.js 官网](https://nodejs.org/) 下载并安装。

#### 2. 克隆项目

克隆项目到本地：

```bash
git clone https://github.com/your-repo/your-project.git
cd your-project
```

#### 3. 安装项目依赖

在项目根目录下运行以下命令，安装项目所需的所有依赖：

```bash
npm install
```

#### 4. 开发环境运行

在开发环境下启动项目：

```bash
npm run serve
```

项目将在本地启动，默认地址为 `http://localhost:8080`。

#### 5. 生产环境构建

构建生产环境的代码：

```bash
npm run build
```

构建后的代码将生成在 `dist` 目录下。

### 项目结构

```
jekedao_front/
├── node_modules/
├── package.json
├── package-lock.json
├── public/
├── src/
    ├── App.vue
    ├── main.js
    ├── router.js
    ├── assets/
    ├── components/
        ├── CommentComponent.vue
        ├── Contest.vue
        ├── ContestDetail.vue
        ├── CreateContest.vue
        ├── CreateDiscussion.vue
        ├── CreateProblemList.vue
        ├── Dashboard.vue
        ├── Discussion.vue
        ├── DiscussionDetail.vue
        ├── Home.vue
        ├── HomePage.vue
        ├── Login.vue
        ├── NavBar.vue
        ├── ProblemDetail.vue
        ├── ProblemList.vue
        ├── ProblemSet.vue
        ├── Register.vue
        ├── SolutionDetail.vue
        ├── Square.vue
        ├── SubmitCode.vue
        ├── UploadProblem.vue
        ├── UploadSolution.vue
        └──  UserProfile.vue
```

### 开发指南

#### 1. 启动开发服务器

在开发环境下启动项目：

```bash
npm run serve
```

#### 2. 代码规范

项目使用 ESLint 进行代码规范检查，确保代码风格一致。在提交代码前，请运行以下命令进行检查：

```bash
npm run lint
```

#### 3. 构建生产环境代码

构建生产环境的代码：

```bash
npm run build
```

#### 4. 单元测试

项目中包含单元测试（如果使用），运行以下命令执行测试：

```bash
npm run test:unit
```

## API文档

### 用户管理

- **注册用户**
  - **URL**: `/register`
  - **Method**: `POST`
  - **Body**:
    ```json
    {
      "username": "example",
      "email": "example@example.com",
      "password": "password"
    }
    ```
  - **Response**:
    ```json
    {
      "code": 200,
      "msg": "注册成功"
    }
    ```

- **用户登录**
  - **URL**: `/login`
  - **Method**: `POST`
  - **Body**:
    ```json
    {
      "username": "example",
      "password": "password"
    }
    ```
  - **Response**:
    ```json
    {
      "code": 200,
      "msg": "登录成功",
      "access_token": "your_jwt_token"
    }
    ```

### 题目管理

- **获取题目列表**
  - **URL**: `/problems`
  - **Method**: `GET`
  - **Response**:
    ```json
    {
      "code": 200,
      "data": [
        {
          "id": 1,
          "title": "Example Problem",
          "description": "This is an example problem.",
          "difficulty": "Medium",
          "upload_time": "2023-10-01T12:00:00Z"
        }
      ]
    }
    ```

- **提交题目**
  - **URL**: `/problems`
  - **Method**: `POST`
  - **Body**:
    ```json
    {
      "id": 1,
      "title": "Example Problem",
      "description": "This is an example problem.",
      "difficulty": "Medium",
      "testCases": [
        {
          "input": "1 2",
          "output": "3"
        }
      ]
    }
    ```
  - **Response**:
    ```json
    {
      "code": 201,
      "msg": "题目上传成功",
      "data": {
        "id": 1,
        "title": "Example Problem",
        "description": "This is an example problem.",
        "difficulty": "Medium",
        "upload_time": "2023-10-01T12:00:00Z"
      }
    }
    ```

### 代码提交与评测

- **提交代码**
  - **URL**: `/submit`
  - **Method**: `POST`
  - **Body**:
    ```json
    {
      "problem_id": 1,
      "code": "int main() { return 0; }",
      "language": "c"
    }
    ```
  - **Response**:
    ```json
    {
      "code": 201,
      "msg": "代码提交成功",
      "submission_id": 1
    }
    ```

- **获取评测结果**
  - **URL**: `/submission/<int:submission_id>`
  - **Method**: `GET`
  - **Response**:
    ```json
    {
      "code": 200,
      "data": {
        "id": 1,
        "problem_id": 1,
        "user_id": 1,
        "code": "int main() { return 0; }",
        "language": "c",
        "status": "Accepted",
        "time": 0.01,
        "memory": 1.2,
        "submit_time": "2023-10-01T12:00:00Z"
      }
    }
    ```

## 许可证

本项目采用MIT许可证。详细信息请参阅[LICENSE](LICENSE)文件。