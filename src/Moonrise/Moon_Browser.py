import os
import subprocess
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.service import Service
try:
    from Moonrise import session_info
except ImportError:
    pass



class MoonBrowser:

    moon_driver = None

    def open_browser(self, browser_type, *browser_args, persist=False):
        """Opens a selenium browser of a specified browser type
           Arguments:
           - browser_type: The desired browser (Chrome, Firefox, Edge, or IE).
           - browser_args: Selenium browser arguments, e.g. --headless.
           - persist: If set to True, will keep the browser open for later use.

           Creates class variable moon_driver for access to selenium webdriver methods.
        """ 

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

        if browser_type.lower() not in browser_options:
            raise KeyError(f"'{browser_type}' not in list of acceptable browsers. Acceptable browsers are chrome, edge, firefox, and ie")

        options = browser_options[browser_type]['options']

        for arg in browser_args:
            options.add_argument(arg)

        # Prevent the default browser cleanup 
        if persist == True:
            Service.__del__ = lambda new_del: None

        # moon_driver not only creates a browser session, but also can be used in higher-order methods to access selenium methods, e.g. refresh(), maximize_window(), etc.
        self.moon_driver = browser_options[browser_type]['webdriver_create'](options=options)

        # write executor_url and session_id to a file named session_info.py for future use
        session_info_file = open(str(os.getcwd())+'\\session_info.py', 'w')
        session_info_file.write(f'executor_url="{self.moon_driver.command_executor._url}"\nsession_id="{self.moon_driver.session_id}"')
        session_info_file.close()

    def use_current_browser(self):
        """Allows for test executions to begin on the last opened browser
           Also creates the moon_driver variable for access to selenium webdriver methods
        """

        # To prevent a new browser session from being created, we need to temporarily overwrite the RemoteWebDriver.execute method
        # Save the original function, so we can revert our patch
        org_command_execute = RemoteWebDriver.execute

        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_info.session_id}
            else:
                return org_command_execute(self, command, params)

        # Patch the function before creating the driver object
        RemoteWebDriver.execute = new_command_execute

        self.moon_driver = webdriver.Remote(command_executor=session_info.executor_url, desired_capabilities={})

        # Replace the patched function with original function
        RemoteWebDriver.execute = org_command_execute


    def cleanup_browser(self):
        """Attempts to tear down most recent browser.
           Kills all geckodriver.exe, chromedriver.exe, and msedgedriver.exe processes.
        """
        try:
            self.moon_driver.quit()
            self.moon_driver = None
        except:
            pass
        subprocess.call('taskkill /f /im geckodriver.exe', stdout=open(os.devnull, "wb"), stderr=open(os.devnull, "wb"))
        subprocess.call('taskkill /f /im chromedriver.exe', stdout=open(os.devnull, "wb"), stderr=open(os.devnull, "wb"))
        subprocess.call('taskkill /f /im msedgedriver.exe', stdout=open(os.devnull, "wb"), stderr=open(os.devnull, "wb"))

    def navigate_to_page(self, url):
        """Attempts to navigate to a web page without first needing https or http prefix
           Arguments:
           - url: The desired url
        """
        
        if not url.startswith("https") and not url.startswith("http"):
            url = "https://" + url

        self.moon_driver.get(url)
