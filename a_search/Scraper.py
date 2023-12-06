from bs4 import BeautifulSoup
import requests
import urllib.parse

class magnetFinder:
    def __init__(self,baseUrl, search_Uri):
        self.baseUrl = baseUrl
        self.search_Uri = search_Uri
    
    def query(self, search_text, parser, numRes=5 , optUri = "&order=seeders&by=DESC"):
        search_url = self.baseUrl + self.search_Uri + search_text + optUri
        print(search_url)
        soup = BeautifulSoup(requests.get(search_url).text, 'html.parser')
        queryResults = parser(soup, numRes, self.baseUrl)
        return queryResults

class metaFinder:
    def __init__(self):
        self.parsers = {
            "rarbg": self.parseRarbg,
            "1337x": self.parse1337x,
            "torrentz2": self.parseTorrentz2
        }

        self.optUris = {
            "rarbg": "&order=seeders&by=DESC",
            "1337x": "/seeders/desc/1/",
            "torrentz2": ""
        }

        self.finders = {
            "rarbg": magnetFinder("https://www2.rarbggo.to", "/search/?search="),
            "1337x": magnetFinder("https://www.1337x.to", "/sort-search/"),
            "torrentz2": magnetFinder("https://torrentz2.nz", "/search?q=")
        }

    def query(self, search_text, numRes=5):
        magnetUrls = []
        for name, finder in self.finders.items():
            magnetUrls += (finder.query(search_text, self.parsers[name], numRes, self.optUris[name]))   
        magnetUrls = list(set(magnetUrls))
        magnetNames = self.extractName(magnetUrls)
        return magnetUrls, magnetNames
    

    def parseRarbg(self,soup, numRes, baseUrl):
        linkElements = soup.find_all(lambda tag: tag.name == 'a' and tag["href"][:8] == "/torrent" and not tag.has_attr("onmouseover"))
        links = [link["href"] for link in linkElements]
        magnetLinks = []
        for link in links[:min(numRes, len(links))]:
            torrentPage = requests.get(baseUrl +  link)
            torrentPage_soup = BeautifulSoup(torrentPage.text, 'html.parser')
            magnetElement = torrentPage_soup.find(lambda tag: tag.name == 'a' and tag.has_attr("href") and tag["href"][:8] == "magnet:?")
            if magnetElement:
                magnetLinks.append(magnetElement["href"])
        return magnetLinks

    def parse1337x(self,soup, numRes, baseUrl):
        return self.parseRarbg(soup, numRes, baseUrl)

    def parseTorrentz2(self,soup, numRes, baseUrl):
        linkElements = soup.find_all(lambda tag: tag.name == 'a' and tag.has_attr("href") and tag["href"][:8] == "magnet:?")
        links = [link["href"] for link in linkElements]
        return links[:min(numRes, len(links))]
    
    def extractName(self, magnetUrls):
        magnetNames = []
        for magnetUrl in magnetUrls:
            magnetNames.append(urllib.parse.unquote(magnetUrl
                                .split("dn=")[1]
                                .split("&tr")[0]
                                .replace("+", " ")
                                .replace(".", " ")))

        return magnetNames