import time
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Конфигурация теста
LOGIN = ""  # замените на ваш реальный логин
PASSWORD = ""        # замените на ваш реальный пароль
LESSON_URLS = [
    "https://stepik.org/lesson/236895/step/1",
    "https://stepik.org/lesson/236896/step/1",
    "https://stepik.org/lesson/236897/step/1",
    "https://stepik.org/lesson/236898/step/1",
    "https://stepik.org/lesson/236899/step/1",
    "https://stepik.org/lesson/236903/step/1",
    "https://stepik.org/lesson/236904/step/1",
    "https://stepik.org/lesson/236905/step/1"
]
WAIT_TIME = 10  # время ожидания после открытия страницы урока
CORRECT_ANSWER = str(math.log(int(time.time())))  # Правильный ответ для заданий

def authorize(driver):
    """Функция для выполнения авторизации"""
    print("Выполнение авторизации...")
    try:
        # Переход на главную страницу для авторизации
        driver.get("https://stepik.org")
        
        # Нажатие кнопки входа
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.navbar__auth_login")))
        login_button.click()
        
        # Заполнение формы
        email_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.NAME, "login")))
        email_field.send_keys(LOGIN)
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(PASSWORD)
        
        # Отправка формы
        submit_button = driver.find_element(By.CSS_SELECTOR, "button.sign-form__btn")
        submit_button.click()
        
        # Ожидание завершения авторизации
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.modal-dialog")))
        print("Авторизация успешна")
        return True
    except Exception as e:
        print(f"Ошибка авторизации: {str(e)}")
        driver.save_screenshot('auth_error.png')
        return False

def test_lesson(driver, lesson_url, lesson_num):
    """Функция для тестирования одного урока"""
    try:
        print(f"\nТестирование урока {lesson_num} из {len(LESSON_URLS)}: {lesson_url}")
        
        # 1. Открываем страницу урока
        driver.get(lesson_url)
        print(f"Ожидание {WAIT_TIME} секунд после загрузки...")
        time.sleep(WAIT_TIME)
        
        # 2. Авторизация перед каждым уроком
        if not authorize(driver):
            return False
        
        # Возвращаемся на страницу урока после авторизации
        driver.get(lesson_url)
        time.sleep(3)  # Небольшая задержка после перезагрузки
        
        # 3. Ввод ответа
        answer_field = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.textarea")))
        
        # Проверяем, что поле пустое
        answer_field.clear()
        assert answer_field.get_attribute("value") == "", "Поле ответа не пустое перед вводом"
        answer_field.send_keys(CORRECT_ANSWER)
        
        # 4. Отправка ответа
        submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.submit-submission")))
        submit_button.click()
        
        # 5. Проверка фидбека
        feedback = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.smart-hints__hint")))
        
        assert feedback.text == "Correct!", f"Ожидался текст 'Correct!', получено: '{feedback.text}'"
        
        print(f"УСПЕХ: Урок {lesson_num} пройден успешно")
        return True
        
    except Exception as e:
        print(f"ОШИБКА в уроке {lesson_num}: {str(e)}")
        driver.save_screenshot(f'error_lesson_{lesson_num}.png')
        print(f"Скриншот сохранён как 'error_lesson_{lesson_num}.png'")
        return False

def test_lessons():
    # Настройка ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        # Инициализация драйвера Chrome
        driver = webdriver.Chrome()
        driver.maximize_window()
        
        # Проход по всем урокам
        results = []
        for i, lesson_url in enumerate(LESSON_URLS, 1):
            results.append(test_lesson(driver, lesson_url, i))
            
        # Вывод итогов
        success_count = sum(results)
        print(f"\nИтоги тестирования:")
        print(f"Успешно пройдено: {success_count} из {len(LESSON_URLS)}")
        print(f"Неудачных тестов: {len(LESSON_URLS) - success_count}")
        
    except Exception as e:
        print(f"ОШИБКА ИНИЦИАЛИЗАЦИИ ДРАЙВЕРА: {str(e)}")
    finally:
        if 'driver' in locals():
            time.sleep(3)
            driver.quit()
        print("\nТестирование всех уроков завершено")

if __name__ == "__main__":
    test_lessons()