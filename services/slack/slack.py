import os
from slack_sdk import WebClient

slack_token = os.environ["REhd5OgrmfXssjSB8kP3H6VZ"]
client = WebClient(token=slack_token)

response = client.chat_postEphemeral(
    channel="C0XXXXXX",
    text="Hello silently from your app! :tada:",
    user="U0XXXXXXX"
)