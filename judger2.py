# import subprocess
# import time
# import psutil
# import os
# from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum, JSON, func
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime
# import win32job
# import win32api
# import win32con

# # 配置
# DATABASE_URI = 'mysql+pymysql://root:123456@localhost/oj_platform'  # 数据库连接URI
# COMPILE_TIMEOUT = 5  # 编译超时时间
# RUN_TIMEOUT = 2  # 运行超时时间
# MAX_MEMORY = 4 * 1024 * 1024 * 1024  # 最大内存限制 4GB

# # 创建数据库引擎和会话
# engine = create_engine(DATABASE_URI)
# Session = sessionmaker(bind=engine)
# session = Session()

# # 定义数据库模型
# Base = declarative_base()

# class Problem(Base):
#     __tablename__ = 'problems'
#     id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
#     title = Column(String(200), unique=True, nullable=False)
#     description = Column(Text, nullable=False)
#     difficulty = Column(Enum('Easy', 'Medium', 'Hard'), nullable=False, default='Medium')
#     upload_time = Column(DateTime, server_default=func.current_timestamp())

# class TestCase(Base):
#     __tablename__ = 'test_cases'
#     id = Column(Integer, primary_key=True)
#     problem_id = Column(Integer, nullable=False)
#     test_cases = Column(JSON, nullable=False)

# # 限制资源
# def limit_resources(pid):
#     hJob = win32job.CreateJobObject(None, "")
#     basic_limit_info = win32job.QueryInformationJobObject(hJob, win32job.JobObjectBasicLimitInformation)
#     basic_limit_info['LimitFlags'] = win32job.JOB_OBJECT_LIMIT_PROCESS_MEMORY | win32job.JOB_OBJECT_LIMIT_JOB_TIME

#     extended_limit_info = win32job.QueryInformationJobObject(hJob, win32job.JobObjectExtendedLimitInformation)
#     extended_limit_info['BasicLimitInformation'] = basic_limit_info
#     extended_limit_info['ProcessMemoryLimit'] = MAX_MEMORY
#     extended_limit_info['JobMemoryLimit'] = MAX_MEMORY
#     extended_limit_info['JobTimeLimit'] = RUN_TIMEOUT * 1000  # 转换为毫秒

#     win32job.SetInformationJobObject(hJob, win32job.JobObjectExtendedLimitInformation, extended_limit_info)
#     win32job.AssignProcessToJobObject(hJob, win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid))


# def evaluate_submission(submission_id, language, code, problem_id):
#     # 获取题目数据
#     problem = session.query(Problem).filter_by(id=problem_id).first()
#     if not problem:
#         return {'status': 'Error', 'message': '题目未找到'}

#     # 获取测试用例
#     test_cases = session.query(TestCase).filter_by(problem_id=problem_id).first()
#     if not test_cases:
#         return {'status': 'Error', 'message': '测试用例未找到'}

#     # 编译代码
#     source_file = f"submission.{language}"
#     with open(source_file, 'w') as f:
#         f.write(code)

#     executable = "submission.out"
#     if language == 'c':
#         compile_cmd = ['gcc', source_file, '-o', executable]
#     elif language == 'cpp':
#         compile_cmd = ['g++', source_file, '-o', executable]
#     else:
#         return {'status': 'Error', 'message': '不支持的编程语言'}

#     # 删除可能存在的旧文件
#     if os.path.exists(executable):
#         try:
#             os.remove(executable)
#         except PermissionError:
#             print(f"PermissionError: 无法删除文件 {executable}，文件可能正在被使用")
#             return {'status': 'Error', 'message': '无法删除旧的可执行文件'}

#     try:
#         compile_proc = subprocess.run(compile_cmd, timeout=COMPILE_TIMEOUT)
#     except subprocess.TimeoutExpired:
#         return {'status': 'Compilation Error', 'message': '编译超时'}
#     if compile_proc.returncode != 0:
#         return {'status': 'Compilation Error', 'message': '编译失败'}

#     # 评测每个测试点
#     results = []
#     maxTime = 0
#     maxMemory = 0
#     RUN_TIMEOUT = 2  # 假设运行超时时间为2秒
#     for test_case in test_cases.test_cases:
#         input_data = test_case['input']
#         expected_output = test_case['output']

#         with open('input.txt', 'w') as fin:
#             fin.write(input_data)

#         with open('input.txt', 'r') as fin, open('output.tmp', 'w') as fout:
#             start_time = time.time()
#             end_time = time.time()
#             try:
#                 proc = subprocess.Popen([executable], stdin=fin, stdout=fout)
#                 limit_resources(proc.pid)
#                 proc.wait(timeout=RUN_TIMEOUT)
#             except subprocess.TimeoutExpired:
#                 proc.kill()
#                 results.append('TLE')
#                 maxTime = max(maxTime, RUN_TIMEOUT)
#                 maxMemory = max(maxMemory, MAX_MEMORY)
#                 end_time = time.time()
#                 continue
#             except Exception as e:
#                 print(f"Error during evaluation: {e}")
#                 continue
#             end_time = time.time()

#         if proc.returncode != 0:
#             results.append('RE')
#             continue

#         # 计算用时和占用空间
#         used_time = end_time - start_time
#         process = psutil.Process(proc.pid)
#         used_memory = process.memory_info().rss

#         if used_time > RUN_TIMEOUT:
#             maxTime = max(maxTime, used_time)
#             maxMemory = max(maxMemory, used_memory)
#             results.append('TLE')
#             continue
#         if used_memory > MAX_MEMORY:
#             maxTime = max(maxTime, used_time)
#             maxMemory = max(maxMemory, used_memory)
#             results.append('MLE')
#             continue

#         maxTime = max(maxTime, used_time)
#         maxMemory = max(maxMemory, used_memory)

#         # 检查输出正确性
#         with open('output.tmp', 'r') as user_output:
#             actual_output = user_output.read().strip()
#             print(f"Expected Output: {expected_output}")
#             print(f"Actual Output: {actual_output}")
#             if actual_output == expected_output.strip():
#                 results.append('AC')
#             else:
#                 results.append('WA')

#     final_result = 'Accepted' if all(r == 'AC' for r in results) else ' '.join(results)
#     return {
#         'status': final_result,
#         'time': maxTime,
#         'memory': maxMemory
#     }

# if __name__ == "__main__":
#     # 这里可以添加一些测试代码，用于测试 evaluate_submission 函数
#     pass

import subprocess
import time
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum, JSON, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 配置
DATABASE_URI = 'mysql+pymysql://root:123456@localhost/oj_platform'  # 数据库连接URI
COMPILE_TIMEOUT = 5  # 编译超时时间
RUN_TIMEOUT = 2  # 运行超时时间

# 创建数据库引擎和会话
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# 定义数据库模型
Base = declarative_base()

class Problem(Base):
    __tablename__ = 'problems'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    title = Column(String(200), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(Enum('Easy', 'Medium', 'Hard'), nullable=False, default='Medium')
    upload_time = Column(DateTime, server_default=func.current_timestamp())

class TestCase(Base):
    __tablename__ = 'test_cases'
    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, nullable=False)
    test_cases = Column(JSON, nullable=False)

def evaluate_submission(submission_id, language, code, problem_id):
    # 获取题目数据
    problem = session.query(Problem).filter_by(id=problem_id).first()
    if not problem:
        return {'status': 'Error', 'message': '题目未找到'}

    # 获取测试用例
    test_cases = session.query(TestCase).filter_by(problem_id=problem_id).first()
    if not test_cases:
        return {'status': 'Error', 'message': '测试用例未找到'}

    # 编译代码
    source_file = f"submission.{language}"
    with open(source_file, 'w') as f:
        f.write(code)

    executable = "submission.out"
    if language == 'c':
        compile_cmd = ['gcc', source_file, '-o', executable]
    elif language == 'cpp':
        compile_cmd = ['g++', source_file, '-o', executable]
    else:
        return {'status': 'Error', 'message': '不支持的编程语言'}

    # 删除可能存在的旧文件
    if os.path.exists(executable):
        try:
            os.remove(executable)
        except PermissionError:
            print(f"PermissionError: 无法删除文件 {executable}，文件可能正在被使用")
            return {'status': 'Error', 'message': '无法删除旧的可执行文件'}

    try:
        compile_proc = subprocess.run(compile_cmd, timeout=COMPILE_TIMEOUT)
    except subprocess.TimeoutExpired:
        return {'status': 'Compilation Error', 'message': '编译超时'}
    if compile_proc.returncode != 0:
        return {'status': 'Compilation Error', 'message': '编译失败'}

    # 评测每个测试点
    results = []
    for test_case in test_cases.test_cases:
        input_data = test_case['input']
        expected_output = test_case['output']

        with open('input.txt', 'w') as fin:
            fin.write(input_data)

        with open('input.txt', 'r') as fin, open('output.tmp', 'w') as fout:
            try:
                proc = subprocess.Popen([executable], stdin=fin, stdout=fout)
                proc.wait(timeout=RUN_TIMEOUT)
            except subprocess.TimeoutExpired:
                proc.kill()
                results.append('Time Limit Exceeded')
                continue
            except Exception as e:
                print(f"Error during evaluation: {e}")
                results.append('Runtime Error')
                continue

        if proc.returncode != 0:
            results.append('Runtime Error')
            continue

        # 检查输出正确性
        with open('output.tmp', 'r') as user_output:
            actual_output = user_output.read().strip()
            print(f"Expected Output: {expected_output}")
            print(f"Actual Output: {actual_output}")
            if actual_output == expected_output.strip():
                results.append('Accepted')
            else:
                results.append('Wrong Answer')

    final_result = 'Accepted' if all(r == 'Accepted' for r in results) else 'Wrong Answer'
    if any(r == 'Time Limit Exceeded' for r in results):
        final_result = 'Time Limit Exceeded'
    elif any(r == 'Runtime Error' for r in results):
        final_result = 'Runtime Error'

    return {
        'status': final_result,
        'time': 0,
        'memory': 0
    }

if __name__ == "__main__":
    # 这里可以添加一些测试代码，用于测试 evaluate_submission 函数
    pass