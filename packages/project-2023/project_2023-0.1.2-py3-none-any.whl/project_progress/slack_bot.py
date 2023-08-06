import requests


def sendSlackWebhook(message, webhook_url):
    """
    Send a message to a Slack channel using a webhook URL.

    :param message: The message to send to the Slack channel (str)
    :param webhook_url: The Slack webhook URL (str)
    :return: None
    """
    if webhook_url == "https://example.com/mock_url":
        print("Mock webhook: " + message)
    else:
        payload = {"text": message}
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
