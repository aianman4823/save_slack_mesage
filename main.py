import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from slack_sdk import WebClient
from gss import import_to_gss


def convert_unixtime_to_datetime(unixtime: str):
    dt_object = datetime.fromtimestamp(float(unixtime))
    formatted_date = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date


load_dotenv()

mapping = {
    "U0680UL9X0U": "村瀬弘人",
    "U067HV2LAMV": "Takashi Hakamada",
    "U068B4H13PT": "Taiki Katsumata",
    "U067YENRVA6": "Akito Harada",
}

# Slack APIの設定
slack_token = os.getenv("SLACK_TOKEN")
client = WebClient(token=slack_token)
channel_id = os.getenv("SLACK_CHANNEL_ID")

# 90日前のtimestampを取得
timestamp_today = (datetime.now()).timestamp()
timestamp_90_days_ago = (datetime.now() - timedelta(days=90)).timestamp()

parent_response = client.conversations_history(
    channel=channel_id,
    oldest=timestamp_90_days_ago,
    latest=timestamp_today,
    inclusive=True,
)


values = []
for msg in parent_response["messages"]:
    try:
        child_response = client.conversations_replies(channel=channel_id, ts=msg["ts"])
    except Exception as e:
        print(e)
        continue
    for cr in child_response["messages"]:
        if "client_msg_id" not in cr:
            continue
        values.append(
            [
                convert_unixtime_to_datetime(cr["ts"]),
                cr["user"],
                mapping[cr["user"]],
                cr["text"],
                cr["client_msg_id"],
            ]
        )

res = import_to_gss(values)
print(res)
