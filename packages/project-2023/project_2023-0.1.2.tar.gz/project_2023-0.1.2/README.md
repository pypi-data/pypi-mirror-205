# Sending Notifications to Your Smartphone for Specific Keywords in Emails
The project involves creating a program that reads gmail and sends notifications to your smartphone using slack when a specific keyword appears.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![](https://img.shields.io/github/issues/kw9212/project_2023)
[![Build Status](https://github.com/kw9212/project_2023/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/kw9212/project_2023/actions?query=workflow%3A%22Build+Status%22)
![](https://github.com/kw9212/project_2023/actions/workflows/build.yml/badge.svg)
[![codecov](https://codecov.io/github/kw9212/project_2023/branch/main/graph/badge.svg?token=05c337ef-226f-41c3-b136-0fe9842b5192)](https://app.codecov.io/gh/kw9212/project_2023)
[![PyPI](https://img.shields.io/pypi/v/project-2023)](https://pypi.org/project/project-2023/)
[![Documentation Status](https://readthedocs.org/projects/project-2023/badge/?version=latest)](https://project-2023.readthedocs.io/en/latest/?badge=latest)


Overview
--------

This idea came from the challenge of having to sort through many emails every day to find the important ones. Gmail already has a labeling function that classifies emails based on specific email addresses as filters. This project aims to create a function that sends notifications based on keywords using slack and smartphones. There is also potential to expand this project to find information in other ways besides just keywords.


Dependencies
------------

- slack_sdk

Usage
-----

### Quick Start

1. Install the package:

```python

pip install project_progress

```

2. Set up your Slack webhook URL. Follow these [instructions](./documentation.md) to create a Slack webhook URL.

3. Create a Python script and import the required functions:

```python

from project_progress import read_email_titles, sendSlackWebhook

```

4. Use the functions to read email titles and send Slack notifications based on specific keywords:

```python
email_titles = read_email_titles()
keyword = "important"

for title in email_titles:
    if keyword in title:
        sendSlackWebhook("Keyword found in email title: " + title, webhook_url)
```

### Lint/Test
To run linting and tests, you need to have the following tools installed:

Flake8 for linting
pytest for testing
Install them using pip:

```python
pip install flake8 pytest
```

### Linting
To lint your code, run the following command in your project directory:

```python
flake8
```

### Testing
To run tests, execute the following command in your project directory:

```python
pytest
```
For more detailed usage instructions and available options, please refer to the [documentation](./documentation.md).
