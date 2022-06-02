import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common import exceptions

driver_path = "geckodriver.exe"
f_options = Options()
f_options.add_argument('--no-sandbox')
f_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Firefox(executable_path=driver_path, options=f_options)


genisTabloXpath = '//*[@id="genisbultencheck"]' # genis istatistikleri gosteren checkbox xpathi
futbolXpath = '/html/body/div[5]/div[1]/div/div[3]/div/div/table/tbody/tr[2]/td/label[3]' # futbol istatistiklerini gosteren checkbox xpathi

browser.get("http://www.spordb.com/iddaa-programi/") # verilerin cekildigi site

browser.find_element_by_xpath(genisTabloXpath).click()
browser.find_element_by_xpath(futbolXpath).click()

time.sleep(5)

# mac oynanan haftalar
daterangeList = '//*[@id="iddaa_daterange"]/option['

data_file = open("scraped_data.txt", "w", encoding="utf-8")
for i in range(2, 26):
    dateRangeXpath = daterangeList + str(i) + ']'
    browser.find_element_by_xpath(dateRangeXpath).click()
    time.sleep(5)
    print(i)
    try:
        # tablodaki rowlarin cekilmesi
        rows = browser.find_elements_by_css_selector("tr")
        for row in rows:
            line = row.text.replace("\n", " ")
            # alt alta yazilan bozuk stringlerin tek satira cevrilmesi
            # bos satirlarin gecilmesi
            if len(line) != 0:
                splitted_line = line.split(" ") # satir verilerinin tokenlara ayrilmasi
                is_hour = splitted_line[0]
                if ":" in is_hour: # bozuk satirlarin alinmamasi
                    data_of_row = []
                    for token in splitted_line:
                        temp_token = token 
                        temp_token_lower = temp_token.lower()
                        contains_letter = temp_token_lower.islower() # sadece numerik verilerin kontrolu
                        # skor / oran tespiti
                        if (len(token) == 3 and "-" in token) or (len(token) >= 4 and "." in token and contains_letter is False):
                            data_of_row.append(token)
                    # skor ve iddia oranlarini eksiksiz iceren satirlarin cekilmesi ve dosyaya yazilmasi
                    if len(data_of_row) == 26:
                        data_file.write(" ".join(data_of_row) + "\n")
    except exceptions.StaleElementReferenceException:
        pass
data_file.close()