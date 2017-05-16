
import requests


def requestSummonerData(region, summonerName, APIKey):
    # Here is how I make my URL.  There are many ways to create these.
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + summonerName + "?api_key=" + APIKey
    print(URL)
    response = requests.get(URL)
    return response.json()


def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.5/league/by-summoner/" + ID + "/entry?api_key=" + APIKey
    print(URL)
    response = requests.get(URL)
    return response.json()


def GetChampStats(region, summonerName, APIKey):

    responseJSON = requestSummonerData(region, summonerName, APIKey)

    ID = responseJSON[summonerName]['id']
    ID = str(ID)
    print(ID)
    responseJSON2 = requestRankedData(region, ID, APIKey)
    return (str(responseJSON2[ID][0]['tier'])), (str(responseJSON2[ID][0]['entries'][0]['division'])),(str(responseJSON2[ID][0]['entries'][0]['leaguePoints']))

    #print(str(responseJSON2[ID][0]['tier']))
    #print(str(responseJSON2[ID][0]['entries'][0]['division']))
    #print(responseJSON2[ID][0]['entries'][0]['leaguePoints'])
