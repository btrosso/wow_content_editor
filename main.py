import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log_file = None
log_to_console = True
class DataScraper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()  # You can use any other webdriver here
        self.logger = self.create_logger(log_file, log_to_console)

    def create_logger(self, _log_file=None, _log_to_console=True):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        if _log_file:
            file_handler = logging.FileHandler(_log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

    def navigate_to_page(self):
        self.driver.get(self.url)

    def close_browser(self):
        self.driver.quit()

    def scrape_info(self):
        wait = WebDriverWait(self.driver, 10)
        loot_tracker = {}
        try:
            table = wait.until(EC.visibility_of_element_located((By.XPATH, "//table[@class='listview-mode-default']")))
            self.logger.info("Got the table")
            # print(table.get_attribute("outerHTML"))
            all_rows = table.find_elements(By.XPATH, "./tbody/tr")
            x = 0
            for row in all_rows:
                self.logger.info(f"Row {x} begin processing...")
                item_num = None
                cells = row.find_elements(By.XPATH, "./td")
                y = 0
                for c in cells:
                    print(y, repr(c.text))
                    if y == 2:
                        anchor = c.find_element(By.XPATH, "./div/a")
                        if anchor:
                            anchor_string = anchor.get_attribute("href")
                            # print(anchor_string)
                            # Define a regular expression pattern to match the item number
                            pattern = r'item=(\d+)'

                            # Use re.search to find the match in the URL
                            match = re.search(pattern, anchor_string)

                            if match:
                                item_number = match.group(1)
                                item_num = item_number
                                print("Item Number:", item_number)
                                loot_tracker[item_number] = {
                                    "item_name": anchor.text
                                }
                            else:
                                print("Item number not found in the URL.")
                    if y == 12:
                        loot_tracker[item_num]["percent"] = c.text
                    y += 1
                self.logger.info(f"Row {x} finished processing...\n")
                x += 1
        except Exception:
            self.logger.exception("SCRAPE INFO FAILURE", exc_info=True)
        else:
            print(loot_tracker)

# Example usage:
if __name__ == "__main__":
    given_npc_num = "151881"
    url_to_visit = f"https://www.wowhead.com/npc={given_npc_num}"
    scraper = DataScraper(url_to_visit)
    scraper.navigate_to_page()
    scraper.scrape_info()
    # Do something on the webpage (e.g., interact with elements, scrape data)
    time.sleep(10000)
    scraper.close_browser()

