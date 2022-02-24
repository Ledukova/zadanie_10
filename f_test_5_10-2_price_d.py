import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver(request):
    wd = webdriver.Firefox()
    request.addfinalizer(wd.quit)
    return wd

def size (text):
    c=""
    for i in range(0, len(text)-2):
        c=c+text[i]
    return float(c)

def test_example(driver):
    driver.get("http://localhost/litecart/")
    color_errors=0
    my_list=driver.find_elements_by_css_selector("[id$='campaigns'] li")
    print()
    tovar=list()
    element_errors=0
    if len(my_list)!=0:
        while len(my_list)!=len(tovar):
            for i in range(0, len(my_list)):
                name_global=my_list[i].find_element_by_css_selector(".name").get_attribute("textContent")
                prise_obichnay_global=my_list[i].find_element_by_tag_name("s").value_of_css_property("font-size") # размер цены начальной на главной странице
                prise_akzionay_global=my_list[i].find_element_by_tag_name("strong").value_of_css_property("font-size") # размер цены акционной на главной странице
                #print(prise_akzionay_global, prise_obichnay_global)
                #print("главная страница: цена акционная - ", size(prise_akzionay_global), "цена начальная - ", size(prise_obichnay_global))
                if size(prise_akzionay_global) <= size(prise_obichnay_global):
                    color_errors=color_errors+1
                    print("Ошибка: размер обычной цены товара ", name_global, " на главной странице меньше или равнен размеру цены акционной")
                if name_global not in tovar:
                    tovar.append(name_global)
                    my_list[i].find_element_by_css_selector(".name").click() # нажать на товар, для перехода на страницу товара
                    prise_obichnay_local=driver.find_element_by_css_selector(".box .regular-price").value_of_css_property("font-size") # размер цены начальная на странице товара
                    prise_akzionay_local=driver.find_element_by_css_selector(".box .campaign-price").value_of_css_property("font-size") # размен цены акционной  на странице товара
                    #print("страница товара акционная -", size(prise_akzionay_local), "начальная цена", size(prise_obichnay_local))
                    if size(prise_akzionay_local) <= size(prise_obichnay_local):
                        color_errors=color_errors+1
                        print("Ошибка: размер обычной цены товара ", name_global, " на странице товара меньше или равнен размеру цены акционной")
                    driver.find_element_by_css_selector(".middle a[href='/litecart/']").click()
                    my_list=driver.find_elements_by_css_selector("[id$='campaigns'] li") # обновляем список товара при обновлении страницы
    else:
        element_errors=element_errors+1
        print("Ошибка: в разделе Campaigns нет товаров")
    if (color_errors>0) or (element_errors>0):
        raise Exception(color_errors, " ошибок размера цены товара. Или в разделе Campaigns нет товаров")









