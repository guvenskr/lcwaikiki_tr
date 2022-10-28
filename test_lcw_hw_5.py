import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


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
        erkek = self.driver.find_element(By.LINK_TEXT, "ERKEK")
        hover = ActionChains(self.driver).move_to_element(erkek)
        hover.perform()
        self.driver.find_element(By.LINK_TEXT, "Kazak").click()
        kazak = self.driver.find_element(By.CLASS_NAME, 'lcw-breadcrumb__item-list').text
        self.assertIn('Kazak', kazak, "Kazak kategorisinde degilsin")
        self.driver.find_element(By.CLASS_NAME, 'quick-filters__item--newest').click()
        self.driver.find_element(By.CLASS_NAME, 'product-card').click()
        self.assertTrue(self.driver.find_element(By.ID, 'pd_add_to_cart'), "Product sayfasında degilsin")
        self.driver.find_element(By.TAG_NAME, 'body').click()
        self.driver.find_element(By.CSS_SELECTOR,
                                 'a:not([class="disabledSelected"])[data-tracking-label="BedenSecenekleri"]').click()
        self.driver.find_element(By.ID, 'pd_add_to_cart').click()
        self.assertEqual('1', self.driver.find_element(By.CLASS_NAME, 'badge-circle').text,
                         "Sepete urun eksik ya da yanlıs eklendi")
        self.driver.find_element(By.CLASS_NAME, 'badge-circle').click()
        self.assertIn('Sepetim', self.driver.find_element(By.CLASS_NAME, 'cart-header').text,
                      "Cart sayfasinda degilsin")
        self.driver.find_element(By.CLASS_NAME, 'main-header-logo').click()
        self.assertEqual(self.base_url, self.driver.current_url, "Lcw Anasayfa Açılmadı")

    def tearDown(self):
        self.driver.quit()
