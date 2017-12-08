from slackclient import SlackClient
import time

SLACK_BOT_TOKEN = ''  # Enter your slack bot token here
MEGA_TOKEN = ''  # Enter your slack mega token, check README
slack_client = SlackClient(SLACK_BOT_TOKEN)
slack_mega_client = SlackClient(MEGA_TOKEN)


def get_username(user_id):  # gets username by userid
    user_name = slack_client.api_call("users.info", user=user_id)
    return user_name['user']['name']


def del_msg(channel,ts):  # delete message for bots
    slack_mega_client.api_call("chat.delete", channel=channel,
                               ts=ts)


def handle_command(channel, ts, user_id, authed_users):  # checks if user is authed, if not, deletes
    if get_username(user_id) not in authed_users:
        del_msg(channel, ts)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            print(output)
            if output and 'text' in output and 'user' in output:
                return output['channel'], \
                       output['ts'], \
                       output['user']
            else:
                try:
                    if output and 'bot_message' in output['subtype']:
                        return output['channel'], output['ts']
                    else:
                        break
                except KeyError:
                    break


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("DeleteBot connected and running!")
        while True:

            variables = parse_slack_output(slack_client.rtm_read())
            if variables:
                try:
                    if len(variables) == 3:  # user sent message in channel
                        channel = variables[0]
                        ts = variables[1]
                        user_id = variables[2]
                        try:
                            f = open("auths/{0}.txt".format(channel), 'r')
                            authed_users = f.read()
                            handle_command(channel, ts, user_id, authed_users)
                        except FileNotFoundError:
                            f = open("auths/{0}.txt".format(channel), 'w+')
                            f.close()
                            f = open("auths/{0}.txt".format(channel), 'r')
                            authed_users = f.read()
                            handle_command(channel, ts, user_id, authed_users)
                    elif len(variables) == 2:  # all bots get their message deleted here
                        channel = variables[0]
                        ts = variables[1]
                        del_msg(channel,ts)
                except TypeError:
                    continue
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token?")
