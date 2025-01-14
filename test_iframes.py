# iframe is a technology that enables to make page inside page - this even can be seen when we inspect the page
def test_iframes(page: Page):  # web page - to work with web page (while per browser was opened single web page
    page.goto('https://www.qa-practice.com/')

    time.sleep(3)