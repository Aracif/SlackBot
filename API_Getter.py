
import requests
import re

#Updated query to use V3 since v2 is being deprecated - Sal 5/16/17
def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.5/league/by-summoner/" + ID + "/entry?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestChampionLoreData():
    response = requests.get("https://na1.api.riotgames.com/lol/static-data/v3/champions?champListData=lore&dataById=false&locale=en_US&api_key=RGAPI-b3c2d17c-ddfb-46ff-8cb7-bc726d80c59e")
    return response.json()
def requestChampionImages():
    response = requests.get("https://na1.api.riotgames.com/lol/static-data/v3/champions?champListData=image&dataById=false&locale=en_US&api_key=RGAPI-b3c2d17c-ddfb-46ff-8cb7-bc726d80c59e")
    return response.json()
def spacedWordsToCamelCase(m):
    return m.group(1) + m.group(2).upper()

if __name__ == "__main__":
    sumData = requestSummonerData("na1","canwefckinggroup","RGAPI-b3c2d17c-ddfb-46ff-8cb7-bc726d80c59e")
    if "status" in sumData:
        print(sumData['status']['message'])
    else:
        sumID = (str(sumData['id']))
        rankedData = requestRankedData("na", sumID, "RGAPI-b3c2d17c-ddfb-46ff-8cb7-bc726d80c59e")
        summonerJSON = requestSummonerData("na1","canwefckinggroup","RGAPI-b3c2d17c-ddfb-46ff-8cb7-bc726d80c59e")
        summonerRankedJSON = requestRankedData("na",(str(summonerJSON['id'])),"RGAPI-b3c2d17c-ddfb-46ff-8cb7-bc726d80c59e")
        championLoreData = requestChampionLoreData()
        print((str(summonerRankedJSON[sumID][0]['tier'])))
        print(championLoreData["data"]["Jax"]["lore"])