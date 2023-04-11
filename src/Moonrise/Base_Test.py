

class BaseTest:
    def __init__(self, *test_cases):
        suite_tests = self.tests.get(self.__class__.__name__)
        if suite_tests is None:
            return
        if set(test_cases).intersection(suite_tests) != set(test_cases):
            mismatched_tcs = []
            for tc in test_cases:
                if tc not in suite_tests:
                    mismatched_tcs.append(tc)
            raise Exception(f"'Test Case(s) {mismatched_tcs} not in not found in Test Suite '{self.__class__.__name__}'")
        self.suite_setup()
        for tc in test_cases or suite_tests:
            suite_tests.get(tc)(self)

    def __del__(self):
        self.suite_teardown()

    def suite_setup(self):
        pass

    def suite_teardown(self):
        pass

    def test_teardown(self):
        pass

    def test_setup(self):
        pass

    tests = {}

    @classmethod
    def test(cls, test_case):
        def test_wrapper(self):
            self.test_setup()
            try:
                test_case(self)
            except Exception as err:
                print("Error: ", err)
                self.moon_driver.save_screenshot(test_case.__name__ + ".png")
            finally:
                self.test_teardown()
        suite_name = test_case.__qualname__.split(".")[0]
        cls.tests.setdefault(suite_name, {})
        cls.tests[suite_name][test_case.__name__] = test_wrapper
        return test_wrapper