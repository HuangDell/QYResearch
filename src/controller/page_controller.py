
class PageController:
    def __init__(self,driver):
        self.driver = driver

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")