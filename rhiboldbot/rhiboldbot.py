import time
from slackclient import SlackClient

token = "your token here"# found at https://api.slack.com/web#authentication
sc = SlackClient(token)
if sc.rtm_connect():
    while True:
        result = sc.rtm_read()
        #print result
        for item in result:
            print item
            if (item["type"] == "message") and (item["user"] == "U1AT0FNF6"): #rhi
                newMessage = "*"+ item["text"] + "*"
                print sc.api_call("chat.postMessage", channel=item["channel"], text=newMessage, as_user="true")
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"