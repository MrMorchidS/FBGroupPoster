from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import time
import os


# Retry decorator definition
def retry(max_retries):
    """Decorator to retry a method upon failure (exception or non-200 status)."""

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            last_status = None
            for attempt in range(max_retries + 1):
                try:
                    status = func(self, *args, **kwargs)
                    if status == 200:
                        return status
                    last_status = status
                except:
                    pass
                # Wait before retrying (except on the last attempt)
                if attempt < max_retries:
                    time.sleep(3)
            return last_status

        return wrapper

    return decorator


class BasePoster:
    def __init__(
        self, headless: bool = True, url: str = "", cookie=None, logger=None
    ) -> None:
        self._logger = logger
        self._browser_name = "chromium"
        self._cookie = cookie
        self._scr_width = 1360
        self._scr_height = 768
        self._url = url
        self._headless = headless
        self._wait_until = "networkidle"
        self._timeout = 60000
        self._slow_mo = 100
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None
        self._session = None

    # ------------------------------
    # Playwright Session
    # ------------------------------
    def _start_pw_session(self) -> None:
        """Launch browser session."""
        self._playwright = sync_playwright().start()
        lunch_args = {
            "headless": self._headless,
            "slow_mo": self._slow_mo,
        }
        browser_launcher = {
            "chromium": self._playwright.chromium.launch,
            "firefox": self._playwright.firefox.launch,
            "webkit": self._playwright.webkit.launch,
        }.get(self._browser_name)
        if not browser_launcher:
            os._exit(1)

        self._browser = browser_launcher(**lunch_args)
        self._context = self._browser.new_context(
            extra_http_headers={"Cookie": self._cookie},
            viewport={"width": self._scr_width, "height": self._scr_height},
        )
        self._context.set_default_timeout(self._timeout)
        self._page = self._context.new_page()

    def _stop_pw_session(self) -> None:
        """Close browser session."""
        if self._page:
            self._page.close()
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    # ------------------------------
    # Requests Session
    # ------------------------------
    def _start_rq_session(self) -> None:
        """Start requests session."""
        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": "Mozilla/5.0",
                "Cookie": self._cookie,
            }
        )

    def _stop_rq_session(self) -> None:
        """Close requests session."""
        self._rq_session.close()
        self._rq_session = None

    # ------------------------------
    # Navigation
    # ------------------------------
    @retry(3)
    def _goto_url(self, url: str) -> int:
        """Go to URL."""
        response = self._page.goto(url, wait_until=self._wait_until)
        return response.status

    def __rq_get(self, url: str) -> None:
        """requests get"""
        return self._session.get(url, timeout=60)

    # ------------------------------
    # HTML / Soup
    # ------------------------------
    def _get_html(self, url: str = None) -> str | None:
        """Get page HTML."""
        if not self._session:
            if url:
                status = self._goto_url(url)
                if status != 200:
                    return
            time.sleep(2)
            self._page.wait_for_load_state(self._wait_until)
            return self._page.content()
        else:
            response = self.__rq_get(url)
            return response.content if response.ok else None

    def _get_soup(self, url: str = None) -> BeautifulSoup | None:
        """Get soup from page."""
        html = self._get_html(url)
        if not html:
            return
        return BeautifulSoup(html, "html.parser")

    # ------------------------------
    # Element Interaction
    # ------------------------------
    def _is_visible(self, selector: str, timeout: int = 3000) -> bool:
        """Check if an element is visible on the page."""
        try:
            return self._page.is_visible(selector, timeout=timeout)
        except:
            return False

    def _fill_input(self, selector: str, value: str) -> None:
        """Fill an input field using a CSS selector."""
        self._page.wait_for_selector(selector)
        self._page.locator(selector).fill(value)

    def _click_btn(self, selector: str) -> None:
        """Click a button using a CSS selector."""
        self._page.wait_for_selector(selector)
        self._page.locator(selector).click()
