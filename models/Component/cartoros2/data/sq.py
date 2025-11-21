import sqlite3

# 创建一个连接到xgo数据库的连接对象
conn = sqlite3.connect('xgo.db')

# 创建一个游标对象，用于执行SQL语句
c = conn.cursor()

# 执行SQL语句，创建xgo_mapping表
c.execute('''CREATE TABLE xgo_mapping
             (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              task_id TEXT NOT NULL,
              task_name TEXT NOT NULL,
              task_status TEXT NOT NULL,
              create_time DATETIME DEFAULT CURRENT_TIMESTAMP)''')
              
c.execute('''CREATE TABLE xgo_map
             (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              map_id TEXT NOT NULL,
              map_name TEXT NOT NULL UNIQUE,
              map_path TEXT NOT NULL,
              create_time DATETIME DEFAULT CURRENT_TIMESTAMP)''')

# 提交更改
conn.commit()

# 关闭连接
conn.close()

