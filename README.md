# Slack-read-only-channel-bot
Bot for Slack, makes the channel read only: deletes all messages except if the user is allowed
This was written in python 3.6

HOW TO:
Install SlackClient module - https://pypi.python.org/pypi/slackclient

Get your bot token  and place it in SLACK_BOT_TOKEN

get your mega token and place it in MEGA_TOKEN   #  mega token is a token you can get if you are a slack owner, if you are just an admin you can also create a service user, make it admin as well and get that user token. keep in mind that the user will have to be invited to the same channel where the bot is.

create a folder called "auths" where the .py file is

run the code and the bot should be online~

When the bot is running and you invite it to a new channel, it will delete all messages.
you will need to give access to your desired users. the way it works is as follows:
User write in the channel, the bot searches if that channel is new, if its new it will create a .txt file in auths folder.
then next time a user writes in that channel, it will look in that .txt file for the username there, if its there, the message will not be deleted. You will have to add usernames to that .txt file manually. (the .txt file names are the channel's id)

Enjoy
