import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver(request):
    wd = webdriver.Edge()
    request.addfinalizer(wd.quit)
    return wd

def price (text):
    c=""
    for i in range(1, len(text)):
        c=c+text[i]
    return float(c)

def test_example(driver):
    driver.get("http://localhost/litecart/")
    my_list=driver.find_elements_by_css_selector("[id$='campaigns'] li")
    price_errors=0
    element_errors=0
    print()
    tovar=list()
    if len(my_list)!=0:
        while len(my_list)!=len(tovar):
            for i in range(0, len(my_list)):
                name_global=my_list[i].find_element_by_css_selector(".name").get_attribute("textContent")
                prise1_global=my_list[i].find_element_by_tag_name("s").get_attribute("textContent") # цена начальная на главной странице
                prise2_global=my_list[i].find_element_by_tag_name("strong").get_attribute("textContent") # цена со скидкой на главной странице
                if name_global not in tovar:
                    tovar.append(name_global)
                    my_list[i].find_element_by_css_selector(".name").click() # нажать на товар, для перехода на страницу товара
                    prise1_local=driver.find_element_by_css_selector(".box .regular-price").get_attribute("textContent") # цена начальная на странице товара
                    #print(price(prise1_global), price(prise1_local))
                    if price(prise1_global)!=price(prise1_local):
                        price_errors=price_errors+1
                        print("Ошибка: начальная цена товара ", name_global, " на главной странице - ", prise1_global, " не совпадает с начальной ценой на странице товара - ", prise1_local)
                    prise2_local=driver.find_element_by_css_selector(".box .campaign-price").get_attribute("textContent") # цена начальная на странице товара
                    if price(prise2_global)!=price(prise2_local):
                        price_errors=price_errors+1
                        print("Ошибка: акционная цена товара ", name_global, " на главной странице - ", prise2_global, " не совпадает с акционной ценой на странице товара - ", prise2_local)
                    driver.find_element_by_css_selector(".middle a[href='/litecart/']").click()
                my_list=driver.find_elements_by_css_selector("[id$='campaigns'] li") # обновляем список товара при обновлении страницы
    else:
        element_errors=element_errors+1
        print("Ошибка: в разделе Campaigns нет товаров")
    if (price_errors>0) or (element_errors>0):
        raise Exception(price_errors, " несоответствий цены товара на главной странице и странице товара. Или в разделе Campaigns нет товаров" )









