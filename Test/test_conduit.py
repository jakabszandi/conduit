import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from test_data import test_user
from test_functions import login


class TestConduit(object):
    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        URL = "http://localhost:1667/"
        self.browser.get(URL)

    def teardown(self):
        self.browser.quit()

    # 01 Cookie nyilatkozat használatának tesztelése
    def test_cookie_accept(self):
        cookie_panel = self.browser.find_element_by_id('cookie-policy-panel')
        decline_btn = self.browser.find_element_by_xpath(
            '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--decline"]')
        accept_btn = self.browser.find_element_by_xpath(
            '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        # Elemek megjelenésének ellenőrzése
        assert cookie_panel.is_displayed()
        assert decline_btn.is_displayed()
        assert accept_btn.is_displayed()
        # Gomb megnyomása
        accept_btn.click()
        time.sleep(2)
        # Ellenőrizzük, hogy a panel eltűnik
        cookie_panel = self.browser.find_elements_by_id('cookie-policy-panel')
        assert len(cookie_panel) == 0

    # 02 Regisztráció tesztelése negatív ágon, üresen hagyott mezőkkel
    def test_registration(self):
        main_sign_up_btn = self.browser.find_element_by_xpath('//a[@href="#/register"]')
        main_sign_up_btn.click()
        # Űrlap elemeinek azonosítása
        username_input = self.browser.find_element_by_xpath('//input[@placeholder="Username"]')
        email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"]')
        password_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"]')
        sign_up_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        # Tabulátor megnyomása mezőkben
        username_input.send_keys(Keys.TAB)
        email_input.send_keys(Keys.TAB)
        password_input.send_keys(Keys.TAB)
        sign_up_btn.click()
        time.sleep(1)
        # Sikertelen regisztráció ellenőrzés
        failed_sign = self.browser.find_element_by_xpath('//div[@class="swal-title"]')
        failed_message = self.browser.find_element_by_xpath('//div[@class="swal-text"]')
        failed_btn = self.browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
        # Sikertelen regisztrációs szöveg megjelenése
        assert failed_sign.text == "Registration failed!"
        assert failed_message.text == "Username field required."
        failed_btn.click()

    # 03 Bejelentkezés tesztelése pozitív ágon
    def test_login(self):
        # Regisztráció pozitív ágon
        try:
            main_sign_up_btn = self.browser.find_element_by_xpath('//a[@href="#/register"]')
            main_sign_up_btn.click()
            # Űrlap elemeinek azonosítása
            username_input = self.browser.find_element_by_xpath('//input[@placeholder="Username"]')
            email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"]')
            password_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"]')
            sign_up_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
            # Adatok megadása
            username_input.send_keys(test_user["username"])
            email_input.send_keys(test_user["email"])
            password_input.send_keys(test_user["password"])
            sign_up_btn.click()
            time.sleep(2)
            success_sign = self.browser.find_element_by_xpath('//div[@class="swal-text"]')
            assert success_sign.is_displayed()
        except NoSuchElementException:
            success_btn = self.browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
            success_btn.click()
            time.sleep(1)
            # Bejelentkezés
            main_sign_in_btn = self.browser.find_element_by_xpath('//a[@href="#/login"]')
            main_sign_in_btn.click()
            # Űrlap elemeinek azonosítása
            email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"]')
            password_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"]')
            sign_in_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
            # Adatok megadása
            email_input.send_keys(test_user["email"])
            password_input.send_keys(test_user["password"])
            sign_in_btn.click()
            time.sleep(2)
            # Username megjelenésének ellenőrzése
            nav_bar = self.browser.find_element_by_xpath('//nav')
            assert test_user["username"] in nav_bar.text

    # 04 Adatok listázása
    def test_listing(self):
        login(self)
        # Article címek azonosítása
        article_titles = self.browser.find_elements_by_xpath('//h1')
        page_title = self.browser.find_element_by_xpath('//h1[@class="logo-font"]')
        # Üres lista létrehozása
        article_list = []
        for title in article_titles:
            if title.text != page_title.text:
                article_list.append(title.text)
        # Ellenőrizzük, hogy a lista nem üres
        assert len(article_list) > 0

    # 05 Több oldalas lista bejárása
    def test_paginator(self):
        login(self)
        # Lapozó gombok azonosítása
        page_html = self.browser.find_element_by_xpath('//html')
        page_html.send_keys(Keys.END)
        page_list = self.browser.find_elements_by_xpath('//a[@class="page-link"]')
        # Gombok bejárása for ciklussal
        for page in page_list:
            page.click()
            opened_page = self.browser.find_element_by_xpath('//li[@class="page-item active"]')
            # Ellenőrzés
            assert page.text == opened_page.text

    # 06 Új adat bevitele
    def test_new_article(self):
        login(self)
        # Elemek azonosítása
        new_article_btn = self.browser.find_element_by_xpath('//a[@href="#/editor"]')
        new_article_btn.click()
        time.sleep(1)
        title_input = self.browser.find_element_by_xpath('//input[@placeholder="Article Title"]')
        about_input = self.browser.find_element_by_xpath('//input[@class="form-control"]')
        text_input = self.browser.find_element_by_xpath('//textarea[@placeholder="Write your article (in markdown)"]')
        tag_input = self.browser.find_element_by_xpath('//input[@placeholder="Enter tags"]')
        publish_btn = self.browser.find_element_by_xpath('//button[@type="submit"]')
        # Create_article_data.txt beolvasása
        with open('Test/create_article_data.txt', 'r', encoding='UTF8') as article_data:
            article_content = article_data.readlines()
        # Űrlap kitöltése
        title_input.send_keys(article_content[1].rstrip())
        about_input.send_keys(article_content[3].rstrip())
        text_input.send_keys(article_content[5].rstrip())
        tag_input.send_keys(article_content[7])
        tag_input.send_keys(article_content[8])
        tag_input.send_keys(article_content[9])
        publish_btn.click()
        time.sleep(1)
        # Ellenőrzés
        new_title = self.browser.find_element_by_xpath('//h1')
        assert new_title.text == article_content[1].rstrip()

    # 07 Ismételt és sorozatos adatbevitel forrásból
    def test_write_comment(self):
        login(self)
        selected_article = self.browser.find_element_by_xpath('//a[@href="#/articles/lorem-ipsum-dolor-sit-amet"]/h1')
        selected_article.click()
        time.sleep(1)
        comment_area = self.browser.find_element_by_xpath('//textarea[@placeholder="Write a comment..."]')
        post_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-sm btn-primary"]')
        with open('Test/comments.csv', 'r', encoding='UTF8') as comments:
            table = csv.reader(comments)
            for row in table:
                comment_area.send_keys(row)
                post_btn.click()
                time.sleep(1)
        posted_comment = self.browser.find_elements_by_xpath('//p[@class="card-text"]')
        posted_comm_list = []
        for comment in posted_comment:
            posted_comm_list.append(comment.text)
        assert posted_comm_list[2] == "This is a test comment."

    # 08 Meglévő adat módosítása
    def test_modifying(self):
        login(self)
        settings_page = self.browser.find_element_by_xpath('//a[@href="#/settings"]')
        settings_page.click()
        time.sleep(2)
        picture_area = self.browser.find_element_by_xpath('//input[@placeholder="URL of profile picture"]')
        update_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        # Új kép URL megadása
        picture_area.clear()
        picture_area.send_keys(
            "https://www.testing-whiz.com/media/2943/test-automation-accelerating-towards-the-nextgen-software-testing.jpg")
        update_btn.click()
        time.sleep(2)
        # Módosítás sikerességének ellenőrzése
        success_sign = self.browser.find_element_by_xpath('//div[@class="swal-title"]')
        success_btn = self.browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
        assert success_sign.is_displayed
        success_btn.click()

    # 09 Adatok lementése felületről
    def test_save_data(self):
        login(self)
        # Profil megnyitása
        user_profile_page = self.browser.find_element_by_xpath('//li[@class="nav-item"]/a[@href="#/@testUser0327/"]')
        user_profile_page.click()
        time.sleep(2)
        article_title = self.browser.find_elements_by_xpath('//a[@href="#/articles/this-is-a-test-article"]/h1')
        article_about = self.browser.find_elements_by_xpath('//a[@href="#/articles/this-is-a-test-article"]/p')
        # collected_articles.txt beolvasása és írása
        with open('Test/collected_articles.txt', 'w', encoding='UTF8') as article_data:
            article_data.write('Posted article title: \n')
            for title in article_title:
                article_data.write('-' + title.text + '\n')
            article_data.write('Posted article about: \n')
            for about in article_about:
                article_data.write('-' + about.text + '\n')
        # Ellenőrzés
        with open('Test/collected_articles.txt', 'r', encoding='UTF8') as collected_data:
            data_content = collected_data.readlines()
        assert data_content[1].rstrip() == "-This is a test article."

    # 10 Adat törlése
    def test_delete_data(self):
        login(self)
        user_profile_page = self.browser.find_element_by_xpath('//li[@class="nav-item"]/a[@href="#/@testUser0327/"]')
        user_profile_page.click()
        time.sleep(2)
        articles_list = self.browser.find_element_by_xpath(
            '//a[@href="#/articles/this-is-a-test-article"]/h1[text()="This is a test article."]')
        articles_list.click()
        time.sleep(2)
        delete_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-outline-danger btn-sm"]')
        delete_btn.click()
        time.sleep(2)
        assert self.browser.current_url == "http://localhost:1667/#/"

    # 11 Kijelentkezés
    def test_logout(self):
        login(self)
        profile_sign = self.browser.find_element_by_xpath('//a[@href="#/@testUser0327/"]')
        assert profile_sign.text == test_user["username"]
        logout_btn = self.browser.find_element_by_xpath('//a[@active-class="active"]')
        logout_btn.click()
        time.sleep(2)
        main_sign_in_btn = self.browser.find_element_by_xpath('//a[@href="#/login"]')
        assert main_sign_in_btn.is_displayed()
