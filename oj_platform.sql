-- 创建数据库
CREATE DATABASE oj_platform;

-- 使用数据库
USE oj_platform;

-- 创建用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    signature VARCHAR(255),
    blog TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建题目表
CREATE TABLE problems (
    id INT PRIMARY KEY,
    title VARCHAR(200) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    difficulty ENUM('Easy', 'Medium', 'Hard') DEFAULT 'Medium',
    upload_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建比赛表
CREATE TABLE contests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建讨论表
CREATE TABLE discussions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author_id INT NOT NULL,
    problem_id INT NOT NULL,
    publish_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    reply_count INT DEFAULT 0,
    FOREIGN KEY (author_id) REFERENCES users(id),
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);

-- 创建题解表
CREATE TABLE solutions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    problem_id INT NOT NULL,
    solution TEXT NOT NULL,
    author_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (problem_id) REFERENCES problems(id),
    FOREIGN KEY (author_id) REFERENCES users(id)
);

-- 创建题目列表表
CREATE TABLE problem_lists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    creator_id INT NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(id)
);

-- 创建测试用例表
CREATE TABLE test_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    problem_id INT NOT NULL,
    test_cases JSON NOT NULL,
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);

-- 创建题目列表与题目关联表
CREATE TABLE problem_list_problems (
    problem_list_id INT NOT NULL,
    problem_id INT NOT NULL,
    PRIMARY KEY (problem_list_id, problem_id),
    FOREIGN KEY (problem_list_id) REFERENCES problem_lists(id),
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);

-- 创建提交记录表
CREATE TABLE submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    problem_id INT NOT NULL,
    user_id INT NOT NULL,
    code TEXT NOT NULL,
    language VARCHAR(50) NOT NULL,
    status ENUM('Pending', 'Accepted', 'Wrong Answer', 'Runtime Error', 'Compilation Error', 'Time Limit Exceeded', 'Memory Limit Exceeded') DEFAULT 'Pending',
    time INT DEFAULT 0,
    memory INT DEFAULT 0,
    submit_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (problem_id) REFERENCES problems(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建评论表
CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    author_id INT NOT NULL,
    discussion_id INT NOT NULL,
    publish_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id),
    FOREIGN KEY (discussion_id) REFERENCES discussions(id)
);