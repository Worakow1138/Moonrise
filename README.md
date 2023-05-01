# Moonrise

- [Moonrise](#moonrise)
  - [Introduction](#introduction)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Example Test Suites](#example-test-suites)
    - [CLI Commands](#cli-commands)
  - [Why the Name "Moonrise"?](#why-the-name-moonrise)

## Introduction
Moonrise is a test suite creation toolset with additional quality of life upgrades for using the [selenium](https://www.selenium.dev/) test framework.

Notable features:
- Test Suite and Test Case organization
- Browser session generation with selenium
- Web element lookup methods with built-in dynamic waits for elements to become available
- Test report generation

## Dependencies
Moonrise only has two dependencies: [selenium](https://pypi.org/project/selenium/) and [colorama](https://pypi.org/project/colorama/). Both of these dependencies are automatically installed with moonrise.

## Installation
Recommend using pypi to install moonrise, `pip install moonrise`. You may also retrieve the latest version from [github](https://github.com/Worakow1138/Moonrise).

## Usage
Moonrise is designed for ultimate ease of use while still giving access to the power of the selenium framework. By simply extending the Moonrise class, any Python class becomes a test suite, capable of executing automated test cases and generating test reports.

    from moonrise import Moonrise

    class ExampleSuite(Moonrise):
        
        @Moonrise.test
        def example_test(self):
            self.log_to_report("this is a test")

### Example Test Suites
Below are two example test suites created to be used with Moonrise. Copy this example code into a python module to get started.

    from moonrise import Moonrise

    class ExampleSuite(Moonrise):

        def suite_setup(self):
            self.log_to_report("this is the beginning of the test suite.")
        
        def suite_teardown(self):
            self.log_to_report("this is the end of the test suite.")
        
        def test_setup(self):
            self.log_to_report("this is the beginning of the test case.")
        
        def test_teardown(self):
            self.log_to_report("this is the end of the test case.")
        
        @Moonrise.test
        def example_test(self):
            self.log_to_report("this is a test")
        
        @Moonrise.test
        def test_failure(self):
            self.log_to_report("this test should fail")
            assert 1 == 2, "this failure is intentional"

    class SeleniumExamples(Moonrise):
        
        Moonrise.default_timeout = 10
        
        def test_setup(self):
            self.open_browser("chrome", persist=True)
            self.moon_driver.maximize_window()
        
        def test_teardown(self):
            self.cleanup_browser()

        @Moonrise.test
        def retrieve_hello_world(self):
            self.navigate_to_page("the-internet.herokuapp.com/dynamic_loading/2")
            self.click_element("#start button")
            self.log_to_report(self.get_text("#finish"))

        @Moonrise.test
        def fail_to_retrieve_hello_world_in_time(self):
            self.navigate_to_page("the-internet.herokuapp.com/dynamic_loading/2")
            self.click_element("#start button")
            self.log_to_report(self.get_text("#finish", timeout=2))

### CLI Commands
The easiest way to use Moonrise is through the command line.

## Why the Name "Moonrise"?
Since [selenium](https://www.selenium.dev/) is named after the element [Selenium](https://en.wikipedia.org/wiki/Selenium), which is named after [Selene](https://en.wikipedia.org/wiki/Selene), the ancient Greek goddess of the Moon, it only seemed fitting to have a name that incorporated a lunar theme!