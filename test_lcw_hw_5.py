import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class Locators(object):
    CATEGORY_ERKEK = (By.LINK_TEXT, "ERKEK")
    CATEGORY_KAZAK = (By.LINK_TEXT, "Kazak")
    KAZAK_BREADCRUMB = (By.CLASS_NAME, 'lcw-breadcrumb__item-list')
    QUICK_FILTER_NEW = (By.CLASS_NAME, 'quick-filters__item--newest')
    PRODUCT_IMAGE = (By.CLASS_NAME, 'product-card')
    ADD_TO_CART_ICON = (By.ID, 'pd_add_to_cart')
    BEDEN_SECENEKLERI = (By.CSS_SELECTOR, 'a:not([class="disabledSelected"])[data-tracking-label="BedenSecenekleri"]')
    ADD_TO_CART_BUTTON = (By.ID, 'pd_add_to_cart')
    CART_COUNT = (By.CLASS_NAME, 'badge-circle')
    CART_HEADER = (By.CLASS_NAME, 'cart-header')
    MAIN_HEADER_LOGO = (By.CLASS_NAME, 'main-header-logo')


class TestLcwHw5(unittest.TestCase):
    base_url = 'https://www.lcwaikiki.com/tr-TR/TR'

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(10)

    def test_lcw_hw_5(self):
        self.assertEqual(self.base_url, self.driver.current_url, "Lcw Anasayfa Açılmadı")
        erkek = self.driver.find_element(*Locators.CATEGORY_ERKEK)
        hover = ActionChains(self.driver).move_to_element(erkek)
        hover.perform()
        self.driver.find_element(*Locators.CATEGORY_KAZAK).click()
        kazak = self.driver.find_element(*Locators.KAZAK_BREADCRUMB).text
        self.assertIn('Kazak', kazak, "Kazak kategorisinde degilsin")
        self.driver.find_element(*Locators.QUICK_FILTER_NEW).click()
        self.driver.find_element(*Locators.PRODUCT_IMAGE).click()
        self.assertTrue(self.driver.find_element(*Locators.ADD_TO_CART_ICON), "Product sayfasında degilsin")
        self.driver.find_element(*Locators.BEDEN_SECENEKLERI).click()
        self.driver.find_element(*Locators.ADD_TO_CART_BUTTON).click()
        self.assertEqual('1', self.driver.find_element(*Locators.CART_COUNT).text,
                         "Sepete urun eksik ya da yanlıs eklendi")
        self.driver.find_element(*Locators.CART_COUNT).click()
        self.assertIn('Sepetim', self.driver.find_element(*Locators.CART_HEADER).text,
                      "Cart sayfasinda degilsin")
        self.driver.find_element(*Locators.MAIN_HEADER_LOGO).click()
        self.assertEqual(self.base_url, self.driver.current_url, "Lcw Anasayfa Açılmadı")

    def tearDown(self):
        self.driver.quit()
