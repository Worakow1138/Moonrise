import os
import subprocess
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.service import Service
try:
    import session_info
except ImportError:
    pass



class MoonBrowser:

    def open_browser(self, browser_type, *browser_args):
        """Creates a Smart Browser, a selenium-generated browser session that can be interacted with via Robot Keywords and Python methods, interchangeably. 
           Smart Browsers and the accompanying webdriver exe file (chromedriver.exe, geckodriver.exe, etc.) do not automatically close after a test execution.
           Arguments:
           - url: The starting url for the Smart Browser to navigate to
           - browser: The desired browser to open (currently supports Chrome, Firefox, Edge, and IE)
           - browser_options: Additional arguments for the browser session, e.g. --headless to launch in headless modes
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

        if "persist" in browser_args:
            Service.__del__ = lambda new_del: None

        self.moon_driver = browser_options[browser_type]['webdriver_create'](options=options)

        session_info_file = open(os.path.dirname(os.path.realpath(__file__))+'\\session_info.py', 'w')
        session_info_file.write(f'executor_url="{self.moon_driver.command_executor._url}"\nsession_id="{self.moon_driver.session_id}"')

    def use_current_browser(self):
        """Allows for test executions to begin on the last opened Smart Browser
        """

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
        self.moon_driver.session_id = session_info.session_id

        # Replace the patched function with original function
        RemoteWebDriver.execute = org_command_execute


    def cleanup_browser(self):
        """Attempts to tear down most recent Smart Browser.
           Kills all geckodriver.exe, chromedriver.exe, and msedgedriver.exe processes.
        """
        try:
            self.moon_driver.quit()
        except:
            pass
        subprocess.call('taskkill /f /im geckodriver.exe', stdout=open(os.devnull, "wb"), stderr=open(os.devnull, "wb"))
        subprocess.call('taskkill /f /im chromedriver.exe', stdout=open(os.devnull, "wb"), stderr=open(os.devnull, "wb"))
        subprocess.call('taskkill /f /im msedgedriver.exe', stdout=open(os.devnull, "wb"), stderr=open(os.devnull, "wb"))

    def navigate_to_page(self, url):
        """
        """
        
        if not url.startswith("https") and not url.startswith("http"):
            url = "https://" + url

        self.moon_driver.get(url)
