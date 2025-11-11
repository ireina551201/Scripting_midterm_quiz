import scraper
import database

choice = '0'
main_str = """
----- 博客來 LLM 書籍管理系統 -----
1. 更新書籍資料庫
2. 查詢書籍
3. 離開系統
----------------------------------"""
search_str = """
--- 查詢書籍 ---
a. 依書名查詢
b. 依作者查詢
c. 返回主選單
---------------"""

if __name__ == '__main__':

    database.db_activate('books.db')

    while True:

        print(main_str)
        
        choice = input('請選擇操作選項 (1/2/3): ').strip()

        if choice == '1': #更新資料

            print('開始從網路爬取最新書籍資料...')

            #儲存到資料庫
            for i ,(title ,author ,link ,price) in enumerate(scraper.get_books_info('LLM')):
                
                database.db_update(title ,author ,price ,link)

                print(f'正在爬取第{i//60+1}頁...\n' if i%60 == 0 else '' ,end='')

            print('爬取完成')

            print(f'資料庫更新完成! 總共爬取{i+1}項資料，加入{database.insert_couunt}本新書資料，另外更新了{database.update_count}筆舊資料。')

            continue
        
        elif choice == '2': #查詢書籍
            
            while True:

                print(search_str)

                select = input('請選擇查詢方式(a-c): ')

                if select == 'a' or select == 'b':
                    
                    key = input('請輸入關鍵字: ')

                    books = database.db_search(key ,select)

                    if books is None:

                        print("查無結果")
                    
                    else:

                        print(f'\n找到{len(books)}筆結果:\n')
                        for row in books:
                            
                            print(f'|書名:{row['title']}')
                            print(f'|作者:{row['author']}')
                            print(f'|價格:{row['price']}')
                            print(f'|連結:{row['link']}\n')

                elif select == 'c':

                    break

                else:
                    
                    print(f'無效選項「{select}」，請重新輸入')

                    continue
                
        elif choice == '3': #結束程式

            database.db_close()
            
        else:         
            
            print(f'無效選項「{choice}」，請重新輸入')
            
            continue
        