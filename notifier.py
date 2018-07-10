#!env python

import re
import subprocess
from twython import Twython

ENV = {}
with open('.env', 'r') as envfile:
    for line in envfile:
        match = re.match(r'([^=]+)\=(.*)', line)
        if match is not None:
            key = match.group(1)
            value = match.group(2)
            ENV[key] = value

hashtag = ENV["HASHTAG"]
tw_api = Twython(ENV["CONSUMER_KEY"], ENV["CONSUMER_SECRET"],
    ENV["ACCESS_TOKEN"], ENV["ACCESS_TOKEN_SECRET"])

try:
    user_handle = tw_api.show_user(user_id=ENV["USER_ID"])["screen_name"]
except Exception as e:
    print("bad user_id!")
    exit

results = tw_api.search(q='from:%s #%s' %(user_handle, hashtag),
    result_type='recent', count=1)

try:
    tweet = results["statuses"][0]
    # tw_date = tweet["created_at"]
    tw_text = tweet["text"]
    day = re.search(r'D(\d+)', tw_text).group(1)
    day = int(day) + 1
except Exception as e:
    day = -1

# TODO get day from tw_date - START_DATE

notify_message = '<span font="2"> \\n</span>What have I ' +            \
    '<span font_weight="bold" font_family="Hack" fgcolor="#fdb540" bgcolor="#335599">' + \
    ' coded </span> today?\\n<span font_size="x-small" font_weight="ultrabold">' + \
    'Day <span font_size="larger" fgcolor="#55e566">' + str(day) + '</span>/100</span>'
notify_title = hashtag
notify_icon = "dialog-question"
notify_timeout = 15
subprocess.Popen(["notify-send", "-t", str(notify_timeout * 1000),
        "-i", notify_icon, notify_title, notify_message],
    close_fds=True)
