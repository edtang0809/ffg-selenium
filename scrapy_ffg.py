from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 初始化 Chrome Driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 無頭模式
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 設定爬取的分類與對應名稱
categories = {
    '130': '公司簡介',
    '139': '集團組織',
    '131': '經營理念',
    '132': '企業沿革',
    '133': '經營團隊',
    '134': '全球佈局',
    '135': '友嘉品牌',
    '136': '未來展望',
    '140': '友嘉亮點',
    '137': '全球合資合作',
    '141': '主要客戶群',
    '138': '全球行銷網',
    '104': '友嘉發言',
    '101': '新聞中心',
    '143': '得獎肯定',
    '102': '社會公益',
    '142': '企業責任報告',
    '103': '活動留影',
    '186': '工具機事業群',
    '187': '產業設備事業群',
    '188': '綠能事業群',
    '106': '員工活動'
}

# 抓取指定分類頁面的內容
def scrape_category_data(category_id, category_name):
    url = f'https://www.ffg-tw.com/category.php?c={category_id}'
    driver.get(url)
    
    # 等待 p.bw_001 和表格元素加載完成
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[starts-with(@class, "bw_")]')))
        
        content = ""

        # 抓取所有以 bw_ 開頭的元素
        elements = driver.find_elements(By.XPATH, '//*[starts-with(@class, "bw_")]')
        for element in elements:
            content += element.text + "\n"
        
        # 抓取表格中的內容
        #rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        #for row in rows:
        #    columns = row.find_elements(By.TAG_NAME, "td")
        #    if len(columns) == 2:
        #        year = columns[0].text.strip()
        #        description = columns[1].text.strip()
        #        if year and description:
        #            content += f"{year} - {description}\n"

        print(f"抓取分類：{category_name}")
        print(content[:200])  # 顯示前200字，檢查是否正確抓取
        return content
    except Exception as e:
        print(f"抓取分類 {category_name} ({category_id}) 時發生錯誤: {e}")
        return None

# 抓取所有分類
def scrape_all_categories():
    all_data = {}
    
    for category_id, category_name in categories.items():
        print(f"開始爬取 {category_name} (ID: {category_id})")
        content = scrape_category_data(category_id, category_name)
        if content:
            all_data[category_name] = content
    
    return all_data

def remove_unwanted_text(content):
    unwanted_phrases = [
        "Copyright © 2024友嘉集團 Tel:886-2-2763-9696 新北市汐止區新台五一段98號8樓",
        "Tel:886-2-2763-9696",
        "新北市汐止區新台五一段98號8樓"
    ]
    
    for phrase in unwanted_phrases:
        content = content.replace(phrase, "")  # 替換為空白，移除指定文字
    
    return content.strip()  # 去除開頭與結尾多餘空白

# 儲存資料為文件
def save_to_file(data):
    for category, content in data.items():
        content = remove_unwanted_text(content)
        filename = f"{category}.txt"  # 根據分類命名文件
        content = content.strip()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"已儲存 {category} 內容到文件 {filename}")

# 主程式執行
if __name__ == "__main__":
    try:
        scraped_data = scrape_all_categories()
        save_to_file(scraped_data)
    finally:
        driver.quit()  # 結束瀏覽器會話
