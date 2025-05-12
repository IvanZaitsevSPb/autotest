import time

def test_add_to_basket_button_is_present(browser):
    # Открываем страницу товара
    link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
    browser.get(link)
    
    # Добавляем задержку для визуальной проверки языка
    time.sleep(10)
    
    # Проверяем наличие кнопки добавления в корзину
    add_to_basket_button = browser.find_element_by_css_selector(
        "button.btn-add-to-basket")
    
    # Проверяем, что кнопка действительно присутствует на странице
    assert add_to_basket_button is not None, "Add to basket button is not found"