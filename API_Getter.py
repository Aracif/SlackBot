
import requests

#Updated query to use V3 since v2 is being deprecated - Sal 5/16/17
def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.5/league/by-summoner/" + ID + "/entry?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()


def GetChampStats(region, summonerName, APIKey):
    responseJSON = requestSummonerData(region, summonerName, APIKey)
    ID = responseJSON[summonerName]['id']
    ID = str(ID)
    print(ID)
    responseJSON2 = requestRankedData(region, ID, APIKey)
    return (str(responseJSON2[ID][0]['tier'])), (str(responseJSON2[ID][0]['entries'][0]['division'])),(str(responseJSON2[ID][0]['entries'][0]['leaguePoints']))

if __name__ == "__main__":
    sumData = requestSummonerData("na1","canwefckinggroup","RGAPI-b3c2d17c-ddfb-46ff-8cb7-bc726d80c59e")
    if "status" in sumData:
        print(sumData['status']['message'])
    else:
        sumID = (str(sumData['id']))
        rankedData = requestRankedData("na", sumID, "RGAPI-b3c2d17c-ddfb-46ff-8cb7-bc726d80c59e")
        summonerJSON = requestSummonerData("na1","canwefckinggroup","RGAPI-b3c2d17c-ddfb-46ff-8cb7-bc726d80c59e")
        summonerRankedJSON = requestRankedData("na",(str(summonerJSON['id'])),"RGAPI-b3c2d17c-ddfb-46ff-8cb7-bc726d80c59e")
        print((str(summonerRankedJSON[sumID][0]['tier'])))
