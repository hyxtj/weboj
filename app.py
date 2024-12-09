# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_cors import CORS
from datetime import datetime, timedelta
from sqlalchemy import Enum as SAEnum
from flask_migrate import Migrate
from logging.handlers import RotatingFileHandler
import logging
import json
import subprocess

app = Flask(__name__)


# 配置 CORS
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:8080"}})

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/oj_platform'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # 请替换为一个强密码
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# 集成 Flask-Migrate
migrate = Migrate(app, db)

# 日志配置
if not app.debug:
    handler = RotatingFileHandler('error.log', maxBytes=100000, backupCount=3)
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


# 数据库模型
#用户模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    signature = db.Column(db.String(255), nullable=True)  # 新增签名字段
    blog = db.Column(db.Text, nullable=True)  # 新增博客字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'signature': self.signature,
            'blog': self.blog,
            'created_at': self.created_at.isoformat()
        }

#题目模型
class Problem(db.Model):
    __tablename__ = 'problems'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=False)
    title = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(SAEnum('Easy', 'Medium', 'Hard'), nullable=False, default='Medium')
    upload_time = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'difficulty': self.difficulty,
            'upload_time': self.upload_time.isoformat()
        }

#比赛模型
class Contest(db.Model):
    __tablename__ = 'contests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }

#讨论模型
class Discussion(db.Model):
    __tablename__ = 'discussions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    publish_time = db.Column(db.DateTime, default=datetime.utcnow)
    reply_count = db.Column(db.Integer, default=0)

    author = db.relationship('User', backref=db.backref('discussions', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'author': self.author.username,  # 确保返回作者的用户名
            'publish_time': self.publish_time.isoformat(),
            'reply_count': self.reply_count
        }

#题解模型
class Solution(db.Model):
    __tablename__ = 'solutions'
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    solution = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    problem = db.relationship('Problem', backref=db.backref('solutions', lazy=True))
    author = db.relationship('User', backref=db.backref('solutions', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'problem_id': self.problem_id,
            'solution': self.solution,
            'author_id': self.author_id,
            'created_at': self.created_at.isoformat()
        }

#题目列表模型
class ProblemList(db.Model):
    __tablename__ = 'problem_lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('problem_lists', lazy=True))
    problems = db.relationship('Problem', secondary='problem_list_problems', backref='problem_lists')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'creator_id': self.creator_id,
            'create_time': self.create_time.isoformat(),
            'problems': [problem.to_dict() for problem in self.problems]
        }
    
#测试用例模型
class TestCase(db.Model):
    __tablename__ = 'test_cases'
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    test_cases = db.Column(db.JSON, nullable=False)

    problem = db.relationship('Problem', backref=db.backref('test_cases', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'problem_id': self.problem_id,
            'test_cases': self.test_cases
        }

problem_list_problems = db.Table('problem_list_problems',
                                 db.Column('problem_list_id', db.Integer, db.ForeignKey('problem_lists.id'),
                                           primary_key=True),
                                 db.Column('problem_id', db.Integer, db.ForeignKey('problems.id'), primary_key=True)
                                 )

#提交模型
class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    status = db.Column(SAEnum('Pending', 'Accepted', 'Wrong Answer', 'Runtime Error', 'Compilation Error', 'Time Limit Exceeded', 'Memory Limit Exceeded'), default='Pending')
    time = db.Column(db.Integer, default=0)  # 用时，单位为秒
    memory = db.Column(db.Integer, default=0)  # 内存占用，单位为MB
    submit_time = db.Column(db.DateTime, default=datetime.utcnow)

    problem = db.relationship('Problem', backref=db.backref('submissions', lazy=True))
    user = db.relationship('User', backref=db.backref('submissions', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'problem_id': self.problem_id,
            'user_id': self.user_id,
            'code': self.code,
            'language': self.language,
            'status': self.status,
            'time': self.time,
            'memory': self.memory,
            'submit_time': self.submit_time.isoformat()
        }
    
#评论模型
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    discussion_id = db.Column(db.Integer, db.ForeignKey('discussions.id'), nullable=False)
    publish_time = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship('User', backref=db.backref('comments', lazy=True))
    discussion = db.relationship('Discussion', backref=db.backref('comments', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'author_id': self.author_id,
            'author': self.author.username,  # 确保返回作者的用户名
            'discussion_id': self.discussion_id,
            'publish_time': self.publish_time.isoformat()
        }

#获取当前用户
@app.route('/profile/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user:
        return jsonify({'code': 200, 'data': user.to_dict()}), 200
    return jsonify({'code': 404, 'msg': '用户未找到'}), 404

#从数据库中获取用户信息
@app.route('/profile/<int:user_id>', methods=['GET'])
@jwt_required(optional=True)
def get_user_profile(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'code': 200, 'data': user.to_dict()}), 200
    return jsonify({'code': 404, 'msg': '用户未找到'}), 404

#注册新用户
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'code': 400, 'msg': '请提供完整的注册信息'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'code': 400, 'msg': '用户名或邮箱已存在'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '注册成功'}), 200

#用户登录
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'code': 400, 'msg': '请提供用户名和密码'}), 400

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'code': 200, 'msg': '登录成功', 'access_token': access_token}), 200
    return jsonify({'code': 401, 'msg': '用户名或密码错误'}), 401

#用户注销
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # JWT 不支持注销，所以前端需要删除 Token
    return jsonify({'code': 200, 'msg': '登出成功'}), 200

#获取题目列表
@app.route('/problems', methods=['GET', 'POST'])
@jwt_required()
def handle_problems():
    if request.method == 'GET':
        problems = Problem.query.all()
        return jsonify({'code': 200, 'data': [problem.to_dict() for problem in problems]}), 200
    elif request.method == 'POST':
        data = request.get_json()
        problem_id = data.get('id')
        title = data.get('title')
        description = data.get('description')
        difficulty = data.get('difficulty', 'Medium')
        test_cases = data.get('testCases')

        # 验证 ID 是否存在
        if problem_id is None:
            return jsonify({'code': 400, 'msg': '题目ID为必填项'}), 400

        # 确保 ID 为正整数
        if not isinstance(problem_id, int) or problem_id <= 0:
            return jsonify({'code': 400, 'msg': '题目ID必须是正整数'}), 400

        if not title or not description:
            return jsonify({'code': 400, 'msg': '标题和描述为必填项'}), 400

        if difficulty not in ['Easy', 'Medium', 'Hard']:
            return jsonify({'code': 400, 'msg': '无效的难度级别'}), 400

        if not test_cases or len(test_cases) == 0:
            return jsonify({'code': 400, 'msg': '至少需要一个测试用例'}), 400

        existing_problem = Problem.query.filter_by(id=problem_id).first()
        if existing_problem:
            return jsonify({'code': 400, 'msg': '题目ID已存在'}), 400

        existing_title = Problem.query.filter_by(title=title).first()
        if existing_title:
            return jsonify({'code': 400, 'msg': '题目标题已存在'}), 400

        new_problem = Problem(id=problem_id, title=title, description=description, difficulty=difficulty)
        db.session.add(new_problem)
        db.session.commit()

        # 创建测试用例
        new_test_cases = []
        for test_case in test_cases:
            if not test_case.get('input') or not test_case.get('output'):
                return jsonify({'code': 400, 'msg': '每个测试用例的输入和输出为必填项'}), 400
            new_test_cases.append({
                'input': test_case.get('input'),
                'output': test_case.get('output')
            })

        new_test_case = TestCase(problem_id=problem_id, test_cases=new_test_cases)
        db.session.add(new_test_case)
        db.session.commit()

        return jsonify({'code': 201, 'msg': '题目上传成功', 'data': new_problem.to_dict()}), 201

#获取题目详情
@app.route('/problems/<int:problem_id>', methods=['GET'])
@jwt_required(optional=True)
def get_problem(problem_id):
    problem = Problem.query.get(problem_id)
    if problem:
        return jsonify({'code': 200, 'data': problem.to_dict()}), 200
    else:
        return jsonify({'code': 404, 'msg': '题目未找到'}), 404
#获取题解
@app.route('/solutions/<int:problem_id>', methods=['GET'])
@jwt_required(optional=True)
def get_solution(problem_id):
    solution = Solution.query.filter_by(problem_id=problem_id).first()
    if solution:
        return jsonify({'code': 200, 'data': solution.to_dict()}), 200
    else:
        return jsonify({'code': 404, 'msg': '题解未找到'}), 404


# 错误处理路由
@app.errorhandler(404)
def not_found(e):
    response = jsonify({'code': 404, 'msg': '资源未找到'})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:8080")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 404

# 服务器内部错误处理
@app.errorhandler(500)
def internal_error(e):
    response = jsonify({'code': 500, 'msg': '服务器内部错误'})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:8080")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 500

#提交题解
@app.route('/uploadsolutions', methods=['POST'])
@jwt_required()
def submit_solution():
    data = request.get_json()
    problem_id = data.get('problemId')
    solution = data.get('solution')

    if not problem_id or not solution:
        return jsonify({'code': 400, 'msg': '题目ID和题解内容为必填项'}), 400

    # 确保 problem_id 为正整数
    if not isinstance(problem_id, int) or problem_id <= 0:
        return jsonify({'code': 400, 'msg': '题目ID必须是正整数'}), 400

    # 验证题目是否存在
    problem = Problem.query.get(problem_id)
    if not problem:
        return jsonify({'code': 404, 'msg': '题目未找到'}), 404

    # 获取当前用户
    user_id = get_jwt_identity()

    # 创建新的题解
    new_solution = Solution(problem_id=problem_id, solution=solution, author_id=user_id)
    db.session.add(new_solution)
    db.session.commit()

    return jsonify({'code': 201, 'msg': '题解上传成功', 'data': new_solution.to_dict()}), 201

#修改用户信息
@app.route('/profile/me', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'msg': '用户未找到'}), 404

    data = request.get_json()
    signature = data.get('signature')
    blog = data.get('blog')

    if signature is not None:
        user.signature = signature
    if blog is not None:
        user.blog = blog

    db.session.commit()

    return jsonify({'code': 200, 'msg': '用户信息更新成功', 'data': user.to_dict()}), 200

#创建讨论
@app.route('/discussions', methods=['POST'])
@jwt_required()
def create_discussion():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    problem_id = data.get('problem_id')

    if not title or not content or not problem_id:
        return jsonify({'code': 400, 'msg': '标题、内容和题目ID为必填项'}), 400

    user_id = get_jwt_identity()
    new_discussion = Discussion(title=title, content=content, author_id=user_id, problem_id=problem_id)
    db.session.add(new_discussion)
    db.session.commit()

    return jsonify({'code': 201, 'msg': '讨论发布成功', 'data': new_discussion.to_dict()}), 201

#获取讨论列表
@app.route('/discussions', methods=['GET'])
@jwt_required(optional=True)
def get_discussions():
    discussions = Discussion.query.all()
    return jsonify({'code': 200, 'data': [discussion.to_dict() for discussion in discussions]}), 200

#获取单个讨论详情
@app.route('/discussions/<int:discussion_id>', methods=['GET'])
@jwt_required(optional=True)
def get_discussion(discussion_id):
    discussion = Discussion.query.get(discussion_id)
    if discussion:
        return jsonify({'code': 200, 'data': discussion.to_dict()}), 200
    return jsonify({'code': 404, 'msg': '讨论未找到'}), 404

#创建评论
@app.route('/discussions/<int:discussion_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(discussion_id):
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'code': 400, 'msg': '评论内容为必填项'}), 400

    user_id = get_jwt_identity()
    new_comment = Comment(content=content, author_id=user_id, discussion_id=discussion_id)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({'code': 201, 'msg': '评论发布成功', 'data': new_comment.to_dict()}), 201

#获取评论列表
@app.route('/discussions/<int:discussion_id>/comments', methods=['GET'])
@jwt_required(optional=True)
def get_comments(discussion_id):
    comments = Comment.query.filter_by(discussion_id=discussion_id).all()
    if not comments:
        return jsonify({'code': 404, 'msg': '没有找到评论'}), 404
    return jsonify({'code': 200, 'data': [comment.to_dict() for comment in comments]}), 200

#提交代码
@app.route('/submit', methods=['POST'])
@jwt_required()
def submit_code():
    data = request.get_json()
    print('Received data:', data)  # 调试步骤

    problem_id = data.get('problem_id')
    code = data.get('code')
    language = data.get('language')

    if not problem_id or not code or not language:
        return jsonify({'code': 400, 'msg': '题目ID、代码和编程语言为必填项'}), 400

    # 确保 problem_id 为正整数
    try:
        problem_id = int(problem_id)
        if problem_id <= 0:
            return jsonify({'code': 400, 'msg': '题目ID必须是正整数'}), 400
    except ValueError:
        return jsonify({'code': 400, 'msg': '题目ID必须是正整数'}), 400

    # 验证题目是否存在
    problem = Problem.query.get(problem_id)
    if not problem:
        return jsonify({'code': 404, 'msg': '题目未找到'}), 404

    # 获取当前用户
    user_id = get_jwt_identity()

    # 创建新的提交
    new_submission = Submission(problem_id=problem_id, user_id=user_id, code=code, language=language)
    db.session.add(new_submission)
    db.session.commit()

    # 调用评测函数
    result = judge_code(new_submission)

    # 更新提交记录的状态、用时和内存占用
    new_submission.status = result['status']
    new_submission.time = result['time']
    new_submission.memory = result['memory']
    db.session.commit()

    return jsonify({'code': 201, 'msg': '代码提交成功', 'submission_id': new_submission.id}), 201

#获取评测结果
@app.route('/submission/<int:submission_id>', methods=['GET'])
@jwt_required(optional=True)
def get_submission_result(submission_id):
    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({'code': 404, 'msg': '提交未找到'}), 404

    return jsonify({'code': 200, 'data': submission.to_dict()}), 200

#提交代码
@app.route('/post_result', methods=['POST'])
def post_result():
    data = request.get_json()
    submission_id = data.get('id')
    result = data.get('result')
    used_time = data.get('time')
    used_memory = data.get('memory')

    if not submission_id or not result:
        return jsonify({'code': 400, 'msg': '提交ID和评测结果为必填项'}), 400

    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({'code': 404, 'msg': '提交未找到'}), 404

    submission.status = result
    submission.time = used_time
    submission.memory = used_memory
    db.session.commit()

    return jsonify({'code': 200, 'msg': '评测结果更新成功'}), 200

from judger2 import evaluate_submission
#评测模型调用
def judge_code(submission):
    problem_id = submission.problem_id
    language = submission.language
    code = submission.code

    # 调用 judger2.py 中的评测函数
    result = evaluate_submission(submission.id, language, code, problem_id)

    # 确保结果包含 status、time 和 memory 字段
    if 'status' not in result:
        result['status'] = 'Error'
    if 'time' not in result:
        result['time'] = 0
    if 'memory' not in result:
        result['memory'] = 0

    # 确保 status 字段在 ENUM 定义的范围内
    if result['status'] not in ['Pending', 'Accepted', 'Wrong Answer', 'Runtime Error', 'Compilation Error', 'Time Limit Exceeded', 'Memory Limit Exceeded']:
        result['status'] = 'Error'

    return result

# 发布比赛
@app.route('/contests', methods=['POST'])
@jwt_required()
def create_contest():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({'code': 400, 'msg': '名称和描述为必填项'}), 400

    new_contest = Contest(name=name, description=description)
    db.session.add(new_contest)
    db.session.commit()

    return jsonify({'code': 201, 'msg': '比赛创建成功', 'data': new_contest.to_dict()}), 201

# 查看所有比赛
@app.route('/contests', methods=['GET'])
@jwt_required(optional=True)
def get_contests():
    contests = Contest.query.all()
    return jsonify({'code': 200, 'data': [contest.to_dict() for contest in contests]}), 200

# 查看单个比赛详情
@app.route('/contests/<int:contest_id>', methods=['GET'])
@jwt_required(optional=True)
def get_contest(contest_id):
    contest = Contest.query.get(contest_id)
    if contest:
        return jsonify({'code': 200, 'data': contest.to_dict()}), 200
    return jsonify({'code': 404, 'msg': '比赛未找到'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')