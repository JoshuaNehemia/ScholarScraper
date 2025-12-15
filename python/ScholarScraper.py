# Project models
from scholarScraperConfig import ScholarScraperConfig

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScholarScraper:
    __BASE_URL = "https://scholar.google.com/scholar?hl=en"

    def __init__(self, query: str = "", config: ScholarScraperConfig = None):
        self.config = config or ScholarScraperConfig()
        
        if self.config._is_verbose:
            print("Initializing ScholarScraper...")

        # Internal state
        self.__query = None
        self.__query_array = []
        self.__query_url = ""
        self.__search_url = ""

        # Init webdriver (ALWAYS)
        self.__webdriver = self._init_webdriver(headless=False)

        if query:
            self.set_query(query)

    # -------------------- Getters --------------------
    def get_query(self):
        return self.__query

    def get_query_array(self):
        return self.__query_array

    def get_query_url(self):
        return self.__query_url

    def get_search_url(self):
        return self.__search_url

    # -------------------- Setters --------------------
    def set_query(self, query: str):
        if not query:
            raise ValueError("Query cannot be empty or None.")
        if not isinstance(query, str):
            raise TypeError("Query must be a string.")

        self.__query = query
        self.__query_array = query.split()
        self.__query_url = "+".join(self.__query_array)
        self._build_search_url()

    def _build_search_url(self):
        self.__search_url = f"{self.__BASE_URL}&q={self.__query_url}"

        if self.config._is_verbose:
            print("Search URL built:")
            print(self.__search_url)

    # -------------------- WebDriver --------------------
    def _init_webdriver(
        self,
        headless=True,
        proxy=None,
        no_sandbox=True,
        disable_dev_shm=True,
        disable_gpu=True,
        disable_software_rasterizer=True,
        remote_allow_origins=True,
        extra_args=None,
    ):
        if self.config._is_verbose:
            print("Initializing Selenium WebDriver...")

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        
        if headless:
            chrome_options.add_argument("--headless=new")
        if no_sandbox:
            chrome_options.add_argument("--no-sandbox")
        if disable_dev_shm:
            chrome_options.add_argument("--disable-dev-shm-usage")
        if disable_gpu:
            chrome_options.add_argument("--disable-gpu")
        if disable_software_rasterizer:
            chrome_options.add_argument("--disable-software-rasterizer")
        if remote_allow_origins:
            chrome_options.add_argument("--remote-allow-origins=*")
        if proxy:
            chrome_options.add_argument(f"--proxy-server={proxy}")
        if extra_args:
            for arg in extra_args:
                chrome_options.add_argument(arg)

        return webdriver.Chrome(options=chrome_options)

    def _close_webdriver(self):
        if self.config._is_verbose:
            print("Closing Selenium WebDriver...")
        if self.__webdriver:
            self.__webdriver.quit()

    # -------------------- Status Check --------------------
    def check_request_status(self):
        if self.config._is_verbose:
            print("Checking request status...")

        if not self.__webdriver.title:
            return False

        if "scholar.google.com" not in self.__webdriver.current_url:
            return False

        return True

    # -------------------- Scraping Logic --------------------
    def request_scholar(self, query: str):
        if self.config._is_verbose:
            print(f"Scraping Google Scholar for query: {query}")

        self.set_query(query)
        self.__webdriver.get(self.get_search_url())

        if not self.check_request_status():
            raise RuntimeError("Failed to access Google Scholar.")

        if self.config._is_verbose:
            print("Page loaded successfully.")
            print("Title:", self.__webdriver.title)

    def scrape_scholar_papers(self, count=10):
        papers = []

        WebDriverWait(self.__webdriver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.gs_r"))
        )

        results = self.__webdriver.find_elements(By.CSS_SELECTOR, "div.gs_r")

        for node in results[:count]:
            title = node.find_element(By.CSS_SELECTOR, "a")
            title_result = title.text
            link_result = title.get_attribute("href")

            papers.append({
                "title": title_result,
                "link": link_result
            })

        return papers

# Test
if __name__ == "__main__":
    config = ScholarScraperConfig(is_verbose=True)
    scraper = ScholarScraper(config=config)
    scraper.request_scholar("machine learning")
    papers = scraper.scrape_scholar_papers(5)
    print(papers)