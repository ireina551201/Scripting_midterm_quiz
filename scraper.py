from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import re ,time

# repuirement
# 1. 在博客來網頁開啟
# 2. 查詢「LLM」圖書資訊
# 3. 限定在「圖書」的範圍內
# 4. 爬取書籍資料:
#       -> 書名 title
#       -> 作者 author
#       -> 價格 price
#       -> 書籍鏈結 link
# 5. 抓取完後，跳轉至下一頁，重複第四點，直到尾端。

def get_books_info(search):
    """
    每次yield回傳一本書的資訊(title ,author ,link ,price)
    """

    #初始化
    url = 'https://www.books.com.tw/?loc=tw_logo_001'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options)
    browser.get(url)

    #進入搜尋結果頁面
    search_box = browser.find_element(By.NAME ,'key')
    search_box.send_keys(search)
    search_box.submit()

    time.sleep(2)

    #選擇「圖書」類別
    type_list = browser.find_elements(By.CLASS_NAME ,'container2')
    for cls in type_list:
        if '圖書' in cls.text:
            cls.click()
            break
    
    #獲取總頁數
    total_page = browser.find_element(By.CSS_SELECTOR ,'select#page_select option[selected]')
    total_page = re.search(r'.* ([0-9]*) .*' ,total_page.text).group(1)

    time.sleep(2)

    #爬取並回傳訊息
    for _ in range(int(total_page)):

        book_list = []

        #獲取書籍容器，使用WebDroverWait等待頁面完整載入
        table = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-searchbox.clearfix")))

        #獲取書籍項目容器清單
        for item in table.find_elements(By.CLASS_NAME ,'table-td'):
    
            id = item.get_attribute('id')

            if id is None:
                continue

            if  re.match('prod-itemlist-.*' ,id):
                
                book_list.append(item)

        #爬取書籍資料並回傳
        for book in book_list:

            #獲取書名
            title  = book.find_element(By.TAG_NAME ,'h4').find_element(By.TAG_NAME ,'a').get_attribute('title')

            #獲取作者資訊
            author = ''
            inital = True
            for element in book.find_elements(By.CSS_SELECTOR ,'p.author a[rel=go_author]'):
                if inital:
                    author += f'{element.get_attribute('title')}'
                else: author += f' ,{element.get_attribute('title')}'
                inital = False

            #獲取鏈結
            link   = book.find_element(By.CSS_SELECTOR ,f'a[title="{title}"]').get_attribute('href')

            #獲取價格
            price  = book.find_element(By.CSS_SELECTOR ,'.price.clearfix').find_element(By.TAG_NAME ,'li').text
            price = re.search(r'([0-9]*)\s?元' ,price)
            if price:          
                price = int(price.group(1))           
            else:           
                print(f'無法搜尋到「{title}」書本的價格')
                exit(1)
            
            yield title ,author ,link ,price
        
        #下一頁
        next_button = browser.find_element(By.CLASS_NAME ,'next')
        next_button.click()