import re
from playwright.sync_api import Page, expect, Route, Dialog, BrowserContext
import time

# tab is new web page that will be opened by clicking a link
# for exp: if on this site you click on link: 'Get Insured' will be opened new web page with name 'Nomad Insurance' while the previous page is also opened
# on new page we will click on link 'Sign me up'

def test_tabs(page: Page,                         # web page - to work with web page (while per browser was opened single web page
              context: BrowserContext):   # web browser - to work with browser when we have few web pages in same browser instance
    page.goto('https://www.nomadlist.com/')
    time.sleep(3)
    # upon a click on this button we see that is opened a 'new' page in the same browser (in same context).
    # if we do nothing with it the playwright still thinks that we are on the previous page and will not be able to locate item on the new page
    # so we need to tell playwright to wait for a new page to be opened - we do it by context manager !!
    # page is a way to work with page and not a browser - page knows only this  site we opened !! To get to new page we must apply browser object and not page object

    # we tell playwright to wait for a new event - event of opening new browser object (not the new browser object itself but only the event of opening)

    # first of all we start waiting for event
    # then we click on button that will generate event (button called - 'Get insured')
    # method that will expect for the event - browser_context.expect_page()
    # event will be stored in - new_page_event
    with context.expect_page() as new_page_event:
        page.get_by_alt_text('Get insured').click() # click will create event of opening new page, with will wait for this event
        time.sleep(3)
        new_page = new_page_event.value # event will be stored in new_page, then we will take a .value of the event which is a new page itself

    # on the new page, find item by role (it is button, where written 'Sign me up'), click on it
    new_page.get_by_role('link', name='sign me up').click()
    time.sleep(3)





