import urllib.request
import json


def flipDict(d):
    result = {}
    for (k, v) in d.items():
        result[v] = [k]
    return result


class handleData:
    def __init__(self, url):
        self.url = url
        self.duplicates = 'None'
        self.data = type(json)
        self.names = type(json)
        self.unpackData()
        self.findDuplicates()
        self.makeNumered()

    def unpackData(self):
        resp = urllib.request.urlopen(self.url)
        self.data = json.load(resp)
        with open('data.json', 'w') as data:
            json.dump(self.data, data, indent=4)
        self.updateNamesFile()

    def updateNamesFile(self):
        d = {}
        disallowed_characters = r"""1234567890!@#$%^&*()\|][{};':"./?>,<-=+"""
        for i in self.data['products']:
            outcome = i
            for character in disallowed_characters:
                outcome = outcome.replace(character, '')
            outcome = outcome.replace('_', ' ')
            d[i] = outcome.lower().title()
        with open('names.json', 'w') as jsonFile:
            json.dump(d, jsonFile, indent=4)
        self.names = d

    def findDuplicates(self):
        result = {}
        for (k, v) in self.names.items():
            if v not in result:
                result[v] = [k]
            else:
                result[v].append(k)
        finalResult = []
        for (k, v) in result.items():
            if len(result[k]) > 1:
                finalResult.append(v)
        self.duplicates = finalResult

    def returnPrices(self, item):
        result = {'item_id': item, 'name': self.names[item],
                  'sellPrice': self.data['products'][item]['quick_status']['sellPrice'],
                  'buyPrice': self.data['products'][item]['quick_status']['buyPrice']}
        return result

    def makeNumered(self):
        with open('names.json', 'r') as jsonFile:
            names = json.load(jsonFile)
        c = 1
        newDict = {}
        for k in names:
            newDict[c] = k
            c += 1
        with open('numbers.json', 'w') as jsonFile:
            json.dump(newDict, jsonFile, indent=4)


