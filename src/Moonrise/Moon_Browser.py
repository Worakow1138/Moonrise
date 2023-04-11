import os
import subprocess
from selenium import webdriver
from robot.api.deco import keyword
from Utility_Webdriver_Setup import UtilityWebdriverSetup as UWS
from selenium.webdriver.common.service import Service
try:
    from session_info import session_info
except ImportError:
    pass



class MoonBrowser:

    @keyword
    def open_browser(self, url, browser, *browser_args):
        """Creates a Smart Browser, a selenium-generated browser session that can be interacted with via Robot Keywords and Python methods, interchangeably. 
           Smart Browsers and the accompanying webdriver exe file (chromedriver.exe, geckodriver.exe, etc.) do not automatically close after a test execution.
           Arguments:
           - url: The starting url for the Smart Browser to navigate to
           - browser: The desired browser to open (currently supports Chrome, Firefox, Edge, and IE)
           - browser_options: Additional arguments for the browser session, e.g. --headless to launch in headless modes
        """ 

        global initial_browser

        browser_options = {
            'edge': {
                'options': webdriver.EdgeOptions(),
                'webdriver_create': webdriver.Edge
            },
            'chrome': {
                'options': webdriver.ChromeOptions(),
                'webdriver_create': webdriver.Chrome
            },
            'firefox': {
                'options': webdriver.FirefoxOptions(),
                'webdriver_create': webdriver.Firefox
            },
            'ie': {
                'options': webdriver.IeOptions(),
                'webdriver_create': webdriver.Ie
            },
        }

        browser = browser.lower()

        if browser not in browser_options:
            raise KeyError(f"'{browser}' not in list of acceptable browsers. Acceptable browsers are chrome, edge, firefox, and ie")

        self.options = browser_options[browser]['options']

        for arg in browser_args:
            self.options.add_argument(arg)

        if "persist" in browser_args:
            Service.__del__ = lambda new_del: None

        initial_browser = browser_options[browser]['webdriver_create'](options=self.options)

        session_info = [initial_browser.command_executor._url, initial_browser.session_id]

        UWS.create_utility_webdrivers(session_info[0], session_info[1])

        UWS.browser.get(url)

        return UWS.browser

    @keyword
    def use_current_browser(self):
        """Allows for test executions to begin on the last opened Smart Browser
        """
        UWS.create_utility_webdrivers(session_info[0], session_info[1])

        return UWS.browser


    @keyword
    def cleanup_browser(self):
        """Attempts to tear down most recent Smart Browser.
           Kills all geckodriver.exe, chromedriver.exe, and msedgedriver.exe processes.
        """
        try:
            UWS.browser.quit()
        except:
            pass
        subprocess.call('taskkill /f /im geckodriver.exe', stdout=open(os.devnull, "wb"), stderr=open(os.devnull, "wb"))
        subprocess.call('taskkill /f /im chromedriver.exe', stdout=open(os.devnull, "wb"), stderr=open(os.devnull, "wb"))
        subprocess.call('taskkill /f /im msedgedriver.exe', stdout=open(os.devnull, "wb"), stderr=open(os.devnull, "wb"))
