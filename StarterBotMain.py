import os
import time
import re
from slackclient import SlackClient
import API_Getter
import requests
import json

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
NA_1 = "na1"
NA = "na"
RANKED_DATA = "r"
# instantiate Slack
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
ClIENT_IP = "RGAPI-b3c2d17c-ddfb-46ff-8cb7-bc726d80c59e" #Need to set this to enviroment variable - SF

def handle_command(command, channel):
    commandMutator = command
    slackIn = (str(commandMutator)).split(" ", 1)#str(command).replace(" ","").lower()
    print(slackIn)
    if len(slackIn) == 2:

        slackOption = slackIn[0]
        slackValue = slackIn[1]
        print(slackOption)
        print(slackValue)

        if slackOption == "r":

            slackValue.replace(" ", "").lower()

            summonerJSON = API_Getter.requestSummonerData(NA_1, slackValue, ClIENT_IP)
            if "status" in summonerJSON:
                slack_client.api_call("chat.postMessage", channel=channel,
                                      text=str(summonerJSON['status']['message']), as_user=True)
            else:
                summonerRankedJSON = API_Getter.requestRankedData(NA, (str(summonerJSON['id'])), ClIENT_IP)
                if "status" in summonerRankedJSON:
                    slack_client.api_call("chat.postMessage", channel=channel,
                                          text="Player is noob and unranked, no stats at this time.", as_user=True)
                else:
                    summonerName = summonerJSON['name']
                    summonerID = str(summonerJSON['id'])
                    summonerTier = summonerRankedJSON[summonerID][0]['tier']
                    summonerDivision = summonerRankedJSON[summonerID][0]['entries'][0]['division']
                    summonerLeaguePoints =  str(summonerRankedJSON[summonerID][0]['entries'][0]['leaguePoints'])
                    displayText = summonerName + " is " + summonerTier + " division " + summonerDivision + " with " + summonerLeaguePoints + "LP"
                    summonerRankedInfoTitle = "RANKED INFO FOR THE KID: " + summonerName
                    attachmentRankedInfo = json.dumps([
                            {
                                "fallback":"Woops, something appears to be fucked up. Sorry.",
                                "color": "#42c8f4",
                                "author_name": "Provided by: CanWeFckingGroup",
                                "author_link": "",
                                "author_icon":"",
                                "title": summonerRankedInfoTitle,
                                "title_link":"",
                                "fields": [
                                    {
                                        "title": "Summoner Name",
                                        "value": summonerName,
                                        "short": "false"
                                    },

                                    {
                                        "title": "Tier",
                                        "value": summonerTier,
                                        "short": "false"
                                    },
                                    {
                                        "title": "Division",
                                        "value": summonerDivision,
                                        "short": "false"
                                    },
                                    {
                                        "title": "League Points",
                                        "value": summonerLeaguePoints,
                                        "short": "false"
                                    }

                                ],
                                "image_url": "",
                                "thumb_url": "",
                                "footer": "Team Shadow Games",
                                "footer_icon":"",
                                "ts":123456789
                    }])

                    slack_client.api_call("chat.postMessage", channel=channel,
                                       attachments=attachmentRankedInfo, as_user=True)
        elif slackOption == "l":
            championLoreData = API_Getter.requestChampionLoreData()
            slackValue = re.sub("(^|\s)(\S)", API_Getter.spacedWordsToCamelCase, slackValue).replace(" ","")
            if slackValue == "Wukong": slackValue = "MonkeyKing"
            if "status" in championLoreData:
                slack_client.api_call("chat.postMessage", channel=channel,
                                      text=str(championLoreData['status']['message']), as_user=True)
            else:
                slack_client.api_call("chat.postMessage", channel=channel,
                                      text=championLoreData["data"][slackValue]["lore"], as_user=True)
        elif str(list(slackOption)[0]) == "i":
            championImageData = API_Getter.requestChampionImages()
            slackValue = re.sub("(^|\s)(\S)", API_Getter.spacedWordsToCamelCase, slackValue).replace(" ", "")
            if slackValue == "Wukong": slackValue = "MonkeyKing"
            if "status" in championImageData:
                slack_client.api_call("chat.postMessage", channel=channel,
                                      text=str(championImageData['status']['message']), as_user=True)
            else:
                imageURL = str(championImageData["data"][slackValue]["image"]["full"]).replace(".png","_" + list(slackOption)[1] +".jpg")
                print(imageURL)
                attach = [{"title": slackValue, "image_url": "http://ddragon.leagueoflegends.com/cdn/img/champion/loading/" + imageURL}]
                slack_client.api_call("chat.postMessage", channel=channel,
                                      attachments=attach, as_user=True)
        else:
             slack_client.api_call("chat.postMessage", channel=channel,
                                   text="I stand resolute! Enter a real option.", as_user=True)
             """
                 Receives commands directed at the bot and determines if they
                 are valid commands. If so, then acts on the commands. If not,
                 returns back what it needs for clarification."""
    else:
        slack_client.api_call("chat.postMessage", channel=channel,
                              text="I stand resolute! Enter a real option.", as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Irelia connected and running!")
        while True:

            command, channel = parse_slack_output(slack_client.rtm_read())

            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")