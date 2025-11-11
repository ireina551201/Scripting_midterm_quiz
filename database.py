import sqlite3

#全域變數
conn = None
cur = None
over = set()
insert_couunt = 0
update_count = 0

#初始化
def db_activate(file_name):

    global conn
    global cur

    conn = sqlite3.connect(file_name)
    conn.row_factory = sqlite3.Row
    
    cur = conn.cursor()
    cur.execute(
                """
                    CREATE TABLE IF NOT EXISTS llm_books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT UNIQUE,
                        author TEXT,
                        price INTEGER,
                        link TEXT)

                """
                )

#新增/更新書籍資訊
def db_update(title ,author ,price ,link):  

    global insert_couunt
    global update_count
    global over

    #如果書籍存在就新增，否則判斷資料是否需要更新。
    cur.execute('SELECT * FROM llm_books WHERE title = ?' ,(title ,))
    
    db_book = cur.fetchone()

    if db_book is None:

        cur.execute('INSERT INTO llm_books (title ,author ,price ,link) VALUES (? ,? ,? ,?)' ,(title ,author ,price ,link))
        
        insert_couunt += 1
    
    elif db_book["author"] != author or db_book["price"] != price:

        if title not in over:
            
            index +=1

            cur.execute('UPDATE llm_books SET author = ? ,price = ? WHERE title = ?' ,(author, price ,title))

            update_count += 1
    
    over.add(title)
    
    conn.commit()   

#查詢資料
def db_search(key ,flag='title'):

    query = ''

    if flag == 'a':

        query = 'SELECT * FROM llm_books WHERE title LIKE ?'

    elif flag == 'b':

        query = 'SELECT * FROM llm_books WHERE author LIKE ?'

    #使用模糊搜尋
    cur.execute(query ,(f'%{key}%' ,))

    book_list = cur.fetchall()

    if not book_list:
        
        return None
    
    else:

        return book_list
    
def db_close():

    cur.close()
    conn.close()
