import urllib.request
import json


def findDuplicates():
    result = {}
    with open('data.json', 'r') as jsonFile:
        names = json.load(jsonFile)
    print('Duplicates:')
    for (k, v) in names.items():
        if v not in result:
            result[v] = [k]
        else:
            result[v].append(k)
    for (k, v) in result.items():
        if len(result[k]) > 1:
            print(v)


def updateJsonFile(data):
    d = {}
    disallowed_characters = r"""1234567890!@#$%^&*()\|][{};':"./?>,<-=+"""
    for i in data['products']:
        outcome = i
        for character in disallowed_characters:
            outcome = outcome.replace(character, '')
        outcome = outcome.replace('_', ' ')
        d[i] = outcome.lower().title()
    with open('data.json', 'w') as jsonFile:
        json.dump(d, jsonFile, indent=4)


def main():
    url = 'https://api.hypixel.net/skyblock/bazaar'
    resp = urllib.request.urlopen(url)
    data = json.load(resp)
    updateJsonFile(data)
    findDuplicates()
    for i in data['products']:
        item = data['products'][i]['quick_status']
        sellPrice = round(item['sellPrice'], 2)
        buyPrice = round(item['buyPrice'], 2)
        with open('data.json', 'r') as jsonFile:
            names = json.load(jsonFile)
        # print(f"{names[i]}:\nSell Price: {sellPrice}\nBuy Price: {buyPrice}")


if __name__ == '__main__':
    main()
