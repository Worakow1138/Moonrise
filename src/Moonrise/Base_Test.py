import os
import traceback
from colorama import Fore, Style, init
init(convert=True)

class BaseTest:
    """Creates the structure for test suites written using the Moonrise framework
    """

    # The dictionary to be referenced when evaluating what tests to run
    tests = {}


    def __init__(self, test_cases=()):
        """Executes all test cases that either fall under the `tests` dictionary, or are specified by `test_cases`.

           Arguments:
           - `test_cases`: Test Case names to be executed. If none specified, will execute all test cases under the given test suite.
        """

        self.passes = 0
        self.failures = 0
        self.totals = 0

        self.colors = {
        "pass": Fore.LIGHTGREEN_EX,
        "fail": Fore.LIGHTRED_EX,
        "header": Fore.LIGHTCYAN_EX,
        "info": ""
        }

        self.run_tests(test_cases)


    def run_tests(self, test_cases):

        suite_tests = self.tests.get(f"{self.__module__}.{self.__class__.__name__}")

        if suite_tests is None or (test_cases != () and len(set(test_cases).intersection(suite_tests)) == 0):
            if test_cases and suite_tests:
                print(f'Skipping test suite "{self.__class__.__name__}" because no tests matching {test_cases} were found.')
            return
        
        if not os.path.exists(str(os.getcwd() + "\\reports")):
            os.makedirs(str(os.getcwd()) + "\\reports")
        self.reports_folder = str(os.getcwd() + "\\reports")
        self.report_file = open(f"{self.reports_folder}\\{self.__class__.__name__}.log", "w")
        
        if test_cases:
            test_cases = set(test_cases).intersection(suite_tests)
        else:
            test_cases = suite_tests
        
        self.suite_setup()

        self.totals += len(test_cases)
        
        for tc in test_cases:
            suite_tests.get(tc)(self)

        self.suite_teardown()

    def log_to_report(cls, message, log_type = "info"):
        print(f"\n{cls.colors.get(log_type)}{message}{Style.RESET_ALL}")
        for color in cls.colors.values():
            message = message.replace(color, "")
        cls.report_file.write("\n\n" + message)

    def suite_setup(self):
        self.log_to_report(f"----------------- Beginning Suite: {self.__class__.__name__} -----------------", log_type="header")

    def suite_teardown(self):
        self.log_to_report(f"----------------- Ending Suite: {self.__class__.__name__} -----------------", log_type="header")
        if self.failures > 0:
            end_string = f"{self.colors.get('pass')}{self.passes} tests passing, {self.colors.get('fail')}{self.failures} tests failing, {self.colors.get('header')}{self.totals} tests total"
        else:
            end_string = f"{self.colors.get('pass')}{self.passes} tests passing, {self.colors.get('header')}{self.totals} tests total"
        self.log_to_report(end_string)

    def test_teardown(self):
        pass

    def test_setup(self, tc_name):
        self.log_to_report(f"--- Starting test: {tc_name} ---", log_type="header")
        pass

    @classmethod
    def test(cls, test_case):
        def test_wrapper(self):
            self.test_setup(test_case.__name__)
            try:
                test_case(self)
                self.log_to_report(f"{test_case.__name__} PASS", log_type = "pass")
                self.passes += 1
            except Exception:
                self.log_to_report(f"{traceback.format_exc()}")
                if self.moon_driver:
                    self.moon_driver.save_screenshot(f"{self.reports_folder}\\{test_case.__name__}.png")
                self.log_to_report(f"{test_case.__name__} FAIL", log_type = "fail")
                self.failures += 1
            finally:
                self.test_teardown()
        mod_and_suite = f"{test_case.__module__}.{test_case.__qualname__.split('.')[0]}"
        cls.tests.setdefault(mod_and_suite, {})
        cls.tests[mod_and_suite][test_case.__name__] = test_wrapper
        return test_wrapper