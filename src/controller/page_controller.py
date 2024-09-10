
class PageController:
    def __init__(self):
        pass

    def scroll_to_bottom(self,driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_top(self,driver):
        driver.execute_script("window.scrollTo(0, 0);")

    def open_url_in_new_tab(self, driver,url):
        # Store the original window handle
        original_window = self.driver.current_window_handle

        # Open a new tab
        driver.execute_script("window.open('');")

        # Switch to the new tab (it's the last one in the list)
        driver.switch_to.window(self.driver.window_handles[-1])

        # Navigate to the URL in the new tab
        driver.get(url)

        return original_window

    def close_current_tab_and_switch_back(self,driver, original_window):
        # Close the current tab
        driver.close()

        # Switch back to the original tab
        driver.switch_to.window(original_window)

    def fullscreen(self,driver):
        driver.maximize_window()

    def scroll_by_pixel(self,driver, pixel=300):
        """通过JavaScript滚动指定像素"""
        driver.execute_script(f"window.scrollBy(0, {pixel});")
