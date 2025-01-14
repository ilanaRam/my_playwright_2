import re
from heapq import nsmallest
from pydoc import locate

from playwright.sync_api import Page, expect, Route, Dialog
import time

# ============================================================
# Used self learning based on explanation from: www.okulik.com
# ============================================================


# This test will test first (land page) of wiki.org page
# page is object that initialised somewhere inside playwright for us so we dont need to wary about it.
def test_find_elem_by_role_click_elem_expect_for_text(page: Page):
    # go to this page in the internet (to this site)
    page.goto('https://www.wikipedia.org/')

    # we want: change to language: russian
    # how we do it: we're actually looking for a 'role' which is a 'link' that written on it 'Русский' that transfers us to a page in russian language
    # upon .click() the link will be clicked and we will expect to get desired result
    page.get_by_role('link', name='Русский').click()
    # here inside the expect() we must indicate what element we ask to expect - from which element we actually wait for some behaviour
    # element is actually a text that we wish to find on the page we will be transferred by clicking the link
    # we will be waiting till this text element will appear (will become visible) on the page
    expect(page.get_by_text("Добро пожаловать в Википедию,")).to_be_visible()
    time.sleep(3)

def test_find_element_by_different_ways(page: Page):
    # go to this page in the internet (to this site)
    page.goto('https://www.wikipedia.org/')

    # search by role
    # we want: change to language: russian
    # how we do it: we actually looking for a 'role' which is a 'link' that written on it 'Русский' that transfers us to a page in russian language
    # upon .click() the link will be clicked and we will expect to get desired result
    page.get_by_role('link', name='Русский').click()

    # here on russian version page we will look for a link with name "Содержание"
    # will click on it and will look for a 'tab' called "Обсуждение"
    # we will click on it and look for a textual title "Обсуждение Википедии:Содержание"

    # search by role
    # click on link
    page.get_by_role('link', name='Содержание').click()

    # search by locator
    # look for element by its id (while beforehand we checked its #ID by inspecting the page) - for this we use a object 'locator'
    # we simply told the playwright - here this is the locator (ID) we are looking for to click on, on the page
    page.locator('#ca-talk').click()

    # search by locator
    # now will be opened a new page where we 'expect' to find the element that has the next locator (ID) that we found by inspection
    # and we expect that on this element will be a text = "Обсуждение Википедии:Содержание"
    expect(page.locator('#firstHeading')).to_have_text("Обсуждение Википедии:Содержание")

    time.sleep(3)

def test_logine_req_check_FE_decides_logine_correct(page: Page):
    # this test check the login REQUEST - if handled correctly

    # go to this page in the internet (to this site)
    page.goto('https://www.gymlog.ru/profile/login/')

    # search field email: by locator for ID - #email, when locator is found we wish to fill in text (not to click)
    page.locator('#email').fill("User412")
    # search field password: by locator for ID - #password
    page.locator('#password').fill("k9L-hL")

    # now after user name + password are filled in we will click on button
    page.get_by_role(role='button', name='Войти').click()
    time.sleep(3)

def test_replace_REQ_data(page: Page):
    # this test works with 'route()'
    # route catches the REQ the web client sends to the WEB server, gives us the REQ data, we can change it and send it to WEB Server to be handled
    # so lets try it!!
    # playwright recommends using regex when we work  with 'route()'

    # we say by route() that we are looking for any REQ that its url contains 'profile/authenticate/' that is why we need regex
    # but first we define inner function that will get the catched REQ (catched by route method) and will change the internal REQ data
    def handler_change_request_inner_func(route: Route):
        print("hi")
        # the data in the REQ is called 'post data'
        data = route.request.post_data
        print(f"The catched data of the REQ is: {data}")
    # in case we do not change a thing we can use continue_() without any params
    #route.continue_()
        # this way we do make change to the REQ data
        if data:
            # we change the REQ data
            data = data.replace('User412','xaxaxa')
        # we resend the REQ with changed data to WEB SERVER
        route.continue_(post_data=data)
        # if we will not resend the REQ - it will be blocked till we do something with it - so we must resend it
        # here we do nothing with the REQ data, we simply resend it

    page.route(re.compile('profile/authenticate/'), # catch by regex,  we say by regex what REQ we are trying to catch
               handler_change_request_inner_func)   # call the inner func to change the REQ data

    # go to this page in the internet (to this site)
    page.goto('https://www.gymlog.ru/profile/login/')
    # search field email: by locator for ID - #email, when locator is found we wish to fill in text (not to click)
    page.locator('#email').fill("User412")
    # search field password: by locator for ID - #password
    page.locator('#password').fill("k9L-hL")
    # now after user name + password are filled in we will click on button
    page.get_by_role(role='button', name='Войти').click()
    time.sleep(3)

def test_replace_RESP_data(page: Page):
    def handler_change_responded_data_func(route: Route):
        print("hi")
        # to get the data from the server - we do by fetching it from a route
        # fetch is actually send to server and get answer
        response_data = route.fetch()
        # we get a test from the data
        text_from_data = response_data.text()
        # we change the data
        modified_data = text_from_data.replace('old_user_name', 'new_user_name')
        # we send the RESP to WEB Client (browser)
        route.fulfill(response=response_data, # this is the data we fetched and changed
                      body=modified_data)     # this is the data we modified
    # rout enables us to hook into the network requests initiated by the page and take custom actions before the requests are sent,
    # or modify their behavior.
    # route catches the RESP sent as answer for REQ from web server to web client
    page.route(re.compile('/profile/412'), # url or part of url that we wish to catch
               handler_change_responded_data_func) # handler = func that will handle the catched data

    # go to this page in the internet (to this site)
    page.goto('https://www.gymlog.ru/profile/login/')
    # search field email: by locator for ID - #email, when locator is found we wish to fill in text (not to click)
    page.locator('#email').fill("User412")
    # search field password: by locator for ID - #password
    page.locator('#password').fill("k9L-hL")
    # now after user name + password are filled in we will click on button
    page.get_by_role(role='button', name='Войти').click()
    # from some reason I need to make any click on the page to be able to catch RESP data and call handler
    page.get_by_role('link', name='ьвшгк').click()
    time.sleep(3)

def test_alert(page: Page):
    """
    This test checks Ability to work with Allert pop ups messages that pop up and block us from clicking on any other elements in the site
    :param page:
    :return:
    """
    page.goto("https://demoblaze.com/")

    def accept_dialog_alert(alert: Dialog):
        # print the text of the alerted message
        print(f"The alert pop up message is: {alert.message}")

        time.sleep(2)
        # accept - this means click on OK on the alert pop up
        alert.accept()

    # on = WHEN | in case when, 'on' knows to wait for some event and based on occurred event to do things
    # in this case on will wait for Alert and will clic on OK
    # on can get many arguments, one of them is dialog (when dialog, when console, when crash, when pageerror, .....)
    # the second param of the on is what to be done when dialog occurred -> here we will deliver inner function

    page.on('dialog',       # wait when Alert pop up was raised
            accept_dialog_alert)  # call this func that will clic on ok on this pop up message

    page.get_by_role('link',name='Samsung galaxy s6').click() # here will be opened new page
    page.get_by_role('link',name='Add to cart').click() # here will be created a Alert pop up
    page.wait_for_event('dialog') # here we wait till Alert msg will pop up on the screen, we should clic on the OK on the Alert msg, else the next operation will not be executed
                                  # as test stack till the ok is clicked
    # how to clic on the OK on the Alert msg pop up?

    page.locator('#cartur').click() # then we can click on another tab on the screen called 'Cart'

    # upon this click the Alert pop up will be originated
    # but to see it we must wait - without waiting the playwright is running very fast and test will finish even before the alert message will pop up



