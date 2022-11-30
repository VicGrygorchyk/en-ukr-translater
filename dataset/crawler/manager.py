from typing import Union

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selen_kaa.webdriver import SeWebDriver


class PWManager:

    def __init__(self):
        self.options = Options()
        self.options.add_argument("user-data-dir=/home/mudro/Documents/Projects/driver_/")
        custom_driver = webdriver.Chrome(
            '/home/mudro/Documents/Projects/en-ukr-translater/venv/bin/chromedriver',
            chrome_options=self.options
        )
        self.browser: Union[SeWebDriver, webdriver.Chrome] = SeWebDriver(custom_driver)

    def close(self):
        self.browser.quit()

    def close_eng_window(self):
        windows = self.browser.window_handles
        for win in windows:
            self.browser.switch_to.window(win)
            title = self.browser.title.lower()
            if 'ukrainian' not in title:
                self.browser.close()
                break

    def switch_to_eng(self):
        windows = self.browser.window_handles
        for win in windows:
            self.browser.switch_to.window(win)
            title = self.browser.title.lower()
            if 'ukrainian' not in title:
                break

    def switch_to_ukr(self):
        windows = self.browser.window_handles
        for win in windows:
            self.browser.switch_to.window(win)
            title = self.browser.title.lower()
            if 'ukrainian' in title:
                break
