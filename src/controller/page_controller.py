
class PageController:
    def __init__(self,driver):
        self.driver = driver

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def open_url_in_new_tab(self, url):
        # Store the original window handle
        original_window = self.driver.current_window_handle

        # Open a new tab
        self.driver.execute_script("window.open('');")

        # Switch to the new tab (it's the last one in the list)
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # Navigate to the URL in the new tab
        self.driver.get(url)

        return original_window

    def close_current_tab_and_switch_back(self, original_window):
        # Close the current tab
        self.driver.close()

        # Switch back to the original tab
        self.driver.switch_to.window(original_window)

    def fullscreen(self):
        self.driver.maximize_window()

    def scroll_by_pixel(self, pixel=300):
        """通过JavaScript滚动指定像素"""
        self.driver.execute_script(f"window.scrollBy(0, {pixel});")
