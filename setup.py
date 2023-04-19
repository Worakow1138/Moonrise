#!/usr/bin/env python

from os.path import abspath, join, dirname
from setuptools import find_packages, setup


VERSION = '1.0.0'


setup(
    name         = 'moonrise',
    version      = VERSION,
    author       = 'Christopher Diamond-Jones',
    author_email = 'christopher.jones1138@gmail.com',
    # url          = '',
    # project_urls = {
    #     'Source': '',
    #     'Issue Tracker': '',
    #     'Documentation': '',
    #     'Release Notes': f'',
    #     'Slack': '',
    #     'Twitter': '',
    # },
    # download_url = '',
    license      = 'MIT License',
    # description  = DESCRIPTION,
    # long_description = DESCRIPTION,
    # long_description_content_type = 'text/x-rst',
    # keywords     = KEYWORDS,
    # platforms    = 'any',
    python_requires='>=3.6',
    # classifiers  = CLASSIFIERS,
    package_dir  = {'': 'src'},
    # package_data = {},
    packages     = find_packages('src'),
    install_requires = ["selenium", "colorama"],
    entry_points = {'console_scripts': ['moonrise = Moonrise.__main__:run_cli']}
)
