from selenium import webdriver


def open_search(site):
    chrome_brw = webdriver.Chrome('.\\chromedriver')
    chrome_brw.get('https://www.google.com.ua')
    user_mess = chrome_brw.find_element_by_name("q")
    user_mess.send_keys(site)
    user_mess.submit()