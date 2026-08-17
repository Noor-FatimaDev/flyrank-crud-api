import sqlite3

data_base= "tasks.db"

def get_connection():
    
   conn = sqlite3.connect(data_base)
   conn.row_factory = sqlite3.Row
   return conn

def init_db():
   conn = get_connection()
   conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                     (id INTEGER PRIMARY KEY ,
                      title TEXT NOT NULL,
                      done INTEGER default 0)''')
   
   cursor = conn.execute("SELECT COUNT(*) FROM tasks")
   count = cursor.fetchone()[0]
   
   if count == 0:
      conn.executemany('''INSERT INTO tasks (title, done) VALUES (?,?)''',
                       [
         ("Buy milk", 0),
        ("Walk dog", 0),
        ("Finish assignment", 1)
                       ]
                         )
   conn.commit()
   conn.close()