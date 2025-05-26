import time
from browser import Browser

content = ""
with open("print.html") as my_file:
    content = my_file.read()

now = time.time()

with Browser() as browser:
    page = browser.new_page(mock_domain="https://mydomain.com/")

    page.set_content(content)
    js = """
        new Promise(resolve => {
            const checkInterval = setInterval(() => {
                if (window.myEventFired) {
                    clearInterval(checkInterval);
                    resolve();
                }
            }, 100);
        });
    """
    page.exec_js(js)

    page.pdf("myfile.pdf")
    page.close()


print(time.time() - now)
