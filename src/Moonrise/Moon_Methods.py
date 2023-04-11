from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class MoonMethods:
    """This class mostly houses calls to SeleniumLibrary Keywords that also behave in a "Smart" fashion, meaning these Keywords will:
       1. Confirm that the element is visible before attempting to interact with the element
       2. Confirm that any "loading elements" have ceased to be visible before attempting to search for the given elements
       3. Fail the Keyword if any of the above actions are not correctly performed within a time limit given at call of the Keyword
       4. Be accessible from a Python file as well as in Robot Framework
    """
    
    # Default time to wait for a desired condition in the Smart Keywords
    default_timeout = 60

    def get_web_element(self, locator, timeout=None, get_multiples = False):
        """Performs a SeleniumLibrary ``robot_keyword`` while ensuring that the element represented by ``locator`` is first visible within 
        the time limit in seconds, given by ``timeout``.

        ``args`` represents any information necessary to the SeleniumLibrary keyword, e.g. Input Text requires an element locator and args="Text to Enter"

        Waiting for the element to become visible is not performed if the keyword is defined as one of the ``wait_until`` SeleniumLibrary keywords
        """

        # Timeout for element to be found may come from the timeout given to this method, the smart_timeout set when instantiating the RobotOil class,
        # or the default_timeout.
        if timeout:
            time_to_wait = timeout
        else:
            time_to_wait = self.default_timeout
        time_to_wait = int(time_to_wait)

        location_methods = {
            "name": By.NAME,
            "id": By.ID,
            "link": By.LINK_TEXT,
            "xpath": By.XPATH,
            "partial link text": By.PARTIAL_LINK_TEXT,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME,
            "css": By.CSS_SELECTOR,
        }

        multi_element_return = {
            False: EC.visibility_of_element_located,
            True: EC.visibility_of_all_elements_located
        }

        wait = WebDriverWait(self.moon_driver, time_to_wait)
        if type(locator) is WebElement:
            return locator
        if locator.startswith("/"):
            return wait.until(multi_element_return.get(get_multiples)((By.XPATH, locator)))
        elif locator.split(":")[0] in location_methods:
            return wait.until(multi_element_return.get(get_multiples)((location_methods[locator.split(":")[0]], locator.split(":")[1])))
        else:
            return wait.until(multi_element_return.get(get_multiples)((By.CSS_SELECTOR, locator)))

    def click_element(self, locator, timeout=None):
        """Click the element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        The ``modifier`` argument can be used to pass
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html#selenium.webdriver.common.keys.Keys|Selenium Keys]
        when clicking the element. The `+` can be used as a separator
        for different Selenium Keys. The `CTRL` is internally translated to
        the `CONTROL` key. The ``modifier`` is space and case insensitive, example
        "alt" and " aLt " are supported formats to
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html#selenium.webdriver.common.keys.Keys.ALT|ALT key]
        . If ``modifier`` does not match to Selenium Keys, keyword fails.

        If ``action_chain`` argument is true, see `Boolean arguments` for more
        details on how to set boolean argument, then keyword uses ActionChain
        based click instead of the <web_element>.click() function. If both
        ``action_chain`` and ``modifier`` are defined, the click will be
        performed using ``modifier`` and ``action_chain`` will be ignored.

        Example:
        | Click Element | id:button |                   | # Would click element without any modifiers.               |
        | Click Element | id:button | CTRL              | # Would click element with CTLR key pressed down.          |
        | Click Element | id:button | CTRL+ALT          | # Would click element with CTLR and ALT keys pressed down. |
        | Click Element | id:button | action_chain=True | # Clicks the button using an Selenium  ActionChains        |

        The ``modifier`` argument is new in SeleniumLibrary 3.2
        The ``action_chain`` argument is new in SeleniumLibrary 4.1
        """
        self.get_web_element(locator=locator, timeout=timeout).click()


    def input_text(self, locator, text, timeout=None):
        """Types the given ``text`` into the text field identified by ``locator``.

        When ``clear`` is true, the input element is cleared before
        the text is typed into the element. When false, the previous text
        is not cleared from the element. Use `Input Password` if you
        do not want the given ``text`` to be logged.

        If [https://github.com/SeleniumHQ/selenium/wiki/Grid2|Selenium Grid]
        is used and the ``text`` argument points to a file in the file system,
        then this keyword prevents the Selenium to transfer the file to the
        Selenium Grid hub. Instead, this keyword will send the ``text`` string
        as is to the element. If a file should be transferred to the hub and
        upload should be performed, please use `Choose File` keyword.

        See the `Locating elements` section for details about the locator
        syntax. See the `Boolean arguments` section how Boolean values are
        handled.

        Disabling the file upload the Selenium Grid node and the `clear`
        argument are new in SeleniumLibrary 4.0
        """
        self.get_web_element(locator=locator, timeout=timeout).send_keys(text)

    # def get_web_element(self, locator, timeout=None):
    #     """Returns the first WebElement matching the given ``locator``.

    #     See the `Locating elements` section for details about the locator
    #     syntax.
    #     """
    #     return self.get_web_element(locator=locator, timeout=timeout)

    def get_web_elements(self, locator, timeout=None):
        """Returns a list of WebElement objects matching the ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        Starting from SeleniumLibrary 3.0, the keyword returns an empty
        list if there are no matching elements. In previous releases, the
        keyword failed in this case.
        """
        return self.get_web_element(locator=locator, timeout=timeout, get_multiples=True)

    def select_from_list_by_value(self, locator, values, timeout=None):
        """Selects options from selection list ``locator`` by ``values``.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        Select(self.get_web_element(locator=locator, timeout=timeout)).select_by_value(values)
        
    def select_from_list_by_label(self, locator, labels, timeout=None):
        """Selects options from selection list ``locator`` by ``labels``.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        Select(self.get_web_element(locator=locator, timeout=timeout)).select_by_visible_text(labels)

    def select_from_list_by_index(self, locator, indexes, timeout=None):
        """Selects options from selection list ``locator`` by ``indexes``.

        Indexes of list options start from 0.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        dd = self.get_web_element(locator=locator, timeout=timeout)
        Select(dd).select_by_index(indexes) 

    def get_text(self, locator, timeout=None):
        """Returns the text value of the element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        return self.get_web_element(locator=locator, timeout=timeout).text