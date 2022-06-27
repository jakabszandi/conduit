from test_data import test_user
import time


def login(self):
    main_sign_in_btn = self.browser.find_element_by_xpath('//a[@href="#/login"]')
    main_sign_in_btn.click()
    email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"]')
    password_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"]')
    sign_in_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    email_input.send_keys(test_user["email"])
    password_input.send_keys(test_user["password"])
    sign_in_btn.click()
    time.sleep(2)