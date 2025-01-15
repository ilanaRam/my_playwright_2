# iframe is a technology that enables to make page inside page - this even can be seen when we inspect the page
import time

from playwright.sync_api import Page


def test_iframes(page: Page):  # web page - to work with web page (while per browser was opened single web page
    page.goto('https://www.qa-practice.com/elements/iframe/iframe_page')
    # inside iframe, I wish to click on button on the right (with multiple lines) , its name is: <span class="navbar-toggler-icon"></span>
    # lets find it by class - when we look by class we dont need #, we do need <.><tag name>

    # just by locating a button in the frame and clicking on it - it will not work, without a hint to playwright they will not know to find something in the iframe
    #page.locator(".navbar-toggler-icon").click()

    # 1. find iframe in the page
    # 2. after frame was found, locate button by locator and click on button
    page.frame_locator('iframe').locator(".navbar-toggler-icon").click()
    time.sleep(3)


def test_select_from_browser_default_drop_down_list(page: Page):
    # what is select - it is ability to choose option from drop down list
    # there are few types of the select:
    # default selector - belongs to browser - this means it is impossible to communicate with and for this playwright prepared some help
    # selector created as page - it looks much nicer - we find it by locator

    # here I show how to communicate with default selector
    page.goto("https://magento.softwaretestingboard.com/men/tops-men/jackets-men.html")

    # we look for id sorter
    # we can find 2 selectors on the page, if we do not define which one to work with - the playwright will not work with anyone so we can say - play with first
    # then we make action: select option from the list and define what is written on this option
    page.locator('#sorter').first.select_option('Price')
    time.sleep(3)