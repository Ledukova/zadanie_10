import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

def r(color):
    zpt_pos=0
    c=""
    for i in range(5, len(color)-3):
        if (color[i]==",") and (zpt_pos==0):
            zpt_pos=i
    for i in range(5, zpt_pos):
        c=c+color[i]
    return int(c)

def g(color):
    zpt_start=0
    zpt_end=0
    c=""
    for i in range(6, len(color)-3):
        if (color[i]==",") and (zpt_start==0):
            zpt_start=i
    for i in range(zpt_start+1, len(color)-3):
        if (color[i]==",") and (zpt_end==0):
            zpt_end=i
    for i in range(zpt_start+1, zpt_end):
        c=c+color[i]
    return int(c)

def b(color):
    zpt_1=0
    zpt_2=0
    zpt_3=0
    c=""
    for i in range(6, len(color)-3):
        if (color[i]==",") and (zpt_1==0):
            zpt_1=i
    for i in range(zpt_1+1, len(color)-3):
        if (color[i]==",") and (zpt_2==0):
            zpt_2=i
    for i in range(zpt_2+1, len(color)-2):
        if (color[i]==",") and (zpt_3==0):
            zpt_3=i
    for i in range(zpt_2+1, zpt_3):
        c=c+color[i]
    return int(c)

def test_example(driver):
    driver.get("http://localhost/litecart/")
    my_list=driver.find_elements_by_css_selector("[id$='campaigns'] li")
    color_errors=0
    element_errors=0
    print()
    tovar=list()
    if len(my_list)!=0:
        while len(my_list)!=len(tovar):
            for i in range(0, len(my_list)):
                price_list=my_list[i].find_elements_by_css_selector(".price")
                if len(price_list)==0:
                    name_global=my_list[i].find_element_by_css_selector(".name").get_attribute("textContent")
                    color_global=my_list[i].find_element_by_tag_name("s").value_of_css_property("color") # цвет цены на главной странице
                    if r(color_global)!=g(color_global) or g(color_global)!=b(color_global) or b(color_global)!=r(color_global):
                        color_errors=color_errors+1
                        print("Ошибка: цвет цены товара ", name_global, " на главной странице не серый")
                    strike_global=my_list[i].find_element_by_tag_name("s").value_of_css_property("text-decoration-line") # зачеркнутость цены на главной странице
                    if strike_global!="line-through":
                        color_errors=color_errors+1
                        print("Ошибка: цена товара ", name_global, " на главной странице не зачеркнута")
                    if name_global not in tovar:
                        tovar.append(name_global)
                        my_list[i].find_element_by_css_selector(".name").click() # нажать на товар, для перехода на страницу товара
                        color_local=driver.find_element_by_css_selector(".box .regular-price").value_of_css_property("color") # цвет цены на странице товара
                        if r(color_local)!=g(color_local) or g(color_local)!=b(color_local) or b(color_local)!=r(color_local):
                            color_errors=color_errors+1
                            print("Ошибка: цвет цены товара ", name_global, " на странице товара не серый")
                        strike_local=driver.find_element_by_css_selector(".box .regular-price").value_of_css_property("text-decoration-line") # зачеркнутость цены на странице товара
                        if strike_local!="line-through":
                            color_errors=color_errors+1
                            print("Ошибка: цена товара ", name_global, " на странице товара не зачеркнута")
                        driver.find_element_by_css_selector(".middle a[href='/litecart/']").click()
                        my_list=driver.find_elements_by_css_selector("[id$='campaigns'] li") # обновляем список товара при обновлении страницы
    else:
        element_errors=element_errors+1
        print("Ошибка: в разделе Campaigns нет товаров")
    if (color_errors>0) or (element_errors>0):
        raise Exception(color_errors, " несоответствий начальной цены товара (не зачеркнута либо не серая) на главной странице и на странице товара. Или в разделе Campaigns нет товаров")









