import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def calc(x):
    return str(math.log(abs(12*math.sin(int(x)))))

try:
    # Инициализация браузера
    browser = webdriver.Chrome()
    browser.get("http://suninjuly.github.io/explicit_wait2.html")
    
    # 1. Ожидаем, когда цена станет $100 (ждём не менее 12 секунд)
    price = WebDriverWait(browser, 12).until(
        EC.text_to_be_present_in_element((By.ID, "price"), "$100")
    )
    
    # 2. Нажимаем на кнопку "Book"
    book_button = browser.find_element(By.ID, "book")
    book_button.click()
    
    # 3. Решаем математическую задачу
    # Получаем значение x
    x_element = browser.find_element(By.ID, "input_value")
    x = x_element.text
    y = calc(x)
    
    # Вводим ответ
    answer_field = browser.find_element(By.ID, "answer")
    answer_field.send_keys(y)
    
    # 4. Отправляем решение
    submit_button = browser.find_element(By.ID, "solve")
    submit_button.click()
    
    # Получаем результат из алерта
    time.sleep(1)
    alert = browser.switch_to.alert
    answer = alert.text.split()[-1]
    print("Полученный код:", answer)
    alert.accept()
    
finally:
    # Задержка для визуальной проверки
    time.sleep(5)
    browser.quit()