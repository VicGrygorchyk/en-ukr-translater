import time

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    StaleElementReferenceException, TimeoutException
)

from dataset.crawler.manager import PWManager
from dataset.crawler.list_page import DecisionsListPage

pw_manager: PWManager = PWManager()
decisions_list = DecisionsListPage(pw_manager)


def load(idx):
    try:
        decisions_list.wait_animation_to_finish()
        if idx % 8 == 0:
            body = pw_manager.browser.init_web_element('body')
            body.click()
            body.send_keys(Keys.PAGE_DOWN)
        try:
            items = decisions_list.get_results_list()
            time.sleep(1)
            items[idx].should.be_visible()
            items[idx].click()
        except StaleElementReferenceException:
            items = decisions_list.get_results_list()
            time.sleep(1)
            items[idx].should.be_visible()
            items[idx].click()
        decisions_list.wait_animation_to_finish()
        try:
            decisions_list.click_word_btn()
        except TimeoutException:
            print("no word format")
            return
        time.sleep(1.5)
        decisions_list.switch_to_diff_lang()
        time.sleep(1.5)
        try:
            decisions_list.open_eng_version()
        except TimeoutException:
            print("no eng version")
            return
        decisions_list.wait_animation_to_finish()
        time.sleep(1.5)
        pw_manager.switch_to_eng()
        decisions_list.click_word_btn()
        pw_manager.close_eng_window()
    finally:
        pw_manager.switch_to_ukr()
        decisions_list.click_close_btn()
        decisions_list.wait_animation_to_finish()


def main():
    try:
        decisions_list.open_page()
        decisions_list.wait_animation_to_finish()
        counter = 7
        while True:
            counter += 1
            if counter > 200:
                break
            try:
                load(counter)
            except:
                continue
            
    finally:
        pw_manager.close()


main()
