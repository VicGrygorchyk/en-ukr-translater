from typing import TYPE_CHECKING
import time
if TYPE_CHECKING:
    from dataset.crawler.manager import PWManager
    from selen_kaa.webdriver import SeElementsArray

URL = 'https://hudoc.echr.coe.int/eng#{%22languageisocode%22:[%22UKR%22],%22documentcollectionid2%22:[%22GRANDCHAMBER%22,%22CHAMBER%22]}'
RESULT_HEADER_CSS = '.result-item .headlineContaniner'
DOWNLOAD_WORD_BTN = '#wordbutton'
DIFF_LANG_TAB = '.tabscontainer #translation .center'
ENG_LINK = 'a.language[href*="ENG"]'
CLOSE_BTN = '#closebutton[title="Close Navigator"]'
LOADING_IMG = '.loadingimage'


class DecisionsListPage:

    def __init__(self, pw_mng: 'PWManager'):
        self.pw_mng = pw_mng

    def open_page(self):
        self.pw_mng.browser.get(URL)

    def wait_animation_to_finish(self):
        anim = self.pw_mng.browser.init_web_element(LOADING_IMG)
        anim.expect.be_visible(2)
        anim.expect.be_invisible(15)

    def get_results_list(self) -> 'SeElementsArray':
        results = self.pw_mng.browser.init_all_web_elements(RESULT_HEADER_CSS)
        return results

    def click_word_btn(self):
        btn = self.pw_mng.browser.init_web_element(DOWNLOAD_WORD_BTN)
        btn.should.be_visible(10)
        btn.click()
        time.sleep(1)

    def click_close_btn(self):
        btn = self.pw_mng.browser.init_web_element(CLOSE_BTN)
        btn.should.be_visible()
        btn.click()

    def switch_to_diff_lang(self):
        tab = self.pw_mng.browser.init_web_element(DIFF_LANG_TAB)
        tab.should.be_visible(10)
        tab.click()

    def open_eng_version(self):
        link = self.pw_mng.browser.init_web_element(ENG_LINK)
        link.should.be_visible(5)
        link.click()
