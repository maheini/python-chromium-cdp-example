import time
from browser import Browser

with Browser() as browser:
    page = browser.new_page()
    page.navigate("https://google.com")
    time.sleep(2)
    page.pdf(".my.pdf")
    page.close()
