import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_connection():
    return sqlite3.connect('todolist.db')

def query(sql):
    conn = create_connection()
    conn.row_factory = dict_factory
    c = conn.cursor()
    result = c.execute(sql).fetchall()
    conn.close()    
    return result    

def insert_task(title, description):
    conn = create_connection()
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(f"INSERT INTO tasks (title, description) VALUES ('{title}', '{description}')")
    conn.commit()
    conn.close()


def update_task(id, title, description):
    conn = create_connection()
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(f"UPDATE tasks SET title='{title}', description='{description}' where id = '{id}'")
    conn.commit()
    conn.close()


def task_done(id):
    conn = create_connection()
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(f"UPDATE tasks SET status='Done' where id = '{id}'")
    conn.commit()
    conn.close()


def get_tasks_all():
    return query('select * from tasks order by created_at desc ')


def get_tasks_by_status(status, order = 'desc'):
    return query(f"select * from tasks where status = '{status}' order by created_at {order} ")


def get_task_by_id(id):
    return query(f"select * from tasks where id = '{id}'")

