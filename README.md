# Moonrise

- [Moonrise](#moonrise)
  - [Introduction](#introduction)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Usage](#usage)
    - [CLI Commands](#cli-commands)
    - [Example Test Suite](#example-test-suite)
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
            print("this is a test")

### CLI Commands
lorem ipsum

### Example Test Suite
lorem ipsum

## Why the Name "Moonrise"?
Since [selenium](https://www.selenium.dev/) is named after the element [Selenium](https://en.wikipedia.org/wiki/Selenium), which is named after [Selene](https://en.wikipedia.org/wiki/Selene), the ancient Greek goddess of the Moon, it only seemed fitting to have a name that incorporated a lunar theme!