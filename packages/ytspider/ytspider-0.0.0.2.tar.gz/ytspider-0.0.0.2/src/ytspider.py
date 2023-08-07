
import re
import json
import requests
from bs4 import BeautifulSoup

from .utils.handler import BaseHandler
from .utils.decorator import VideosScraper, CommentScraper, TranscriptScraper
from .utils.request import Request
from .utils.context import Context

# This package was built on hurry, I'll comment it later

class YTSpider:

    def __init__(self):
        self.Request = Request()
        self.__Response = {}
        self.__Context = Context()
        self.handlers = {}
        self.defaultHandlers = {}

    def attachHandler(self, handler):
        if not isinstance(handler, BaseHandler):
            raise ValueError(
                "Argument (handler) must be a subclass of BaseHandler")
        if not handler.name in self.defaultHandlers:
            self.defaultHandlers[handler.name] = handler

        self.handlers[handler.name] = handler

    def restoreDefaultHandlers(self, exclude=[]):
        for handlerName in self.defaultHandlers:
            if handlerName not in exclude:
                self.handlers[handlerName] = self.defaultHandlers[handlerName]

    def removeHandler(self, handler):
        if handler.name in self.handlers:
            del self.handlers[handler.name]
            return True
        return False

    def getHandler(self, handlerName):
        if handlerName in self.handlers:
            return self.handlers[handlerKey]
        return None

    def getAllHandlers(self):
        return self.handlers

    def executeHandlers(self, itemId):
        results = {}
        for handlerName, handler in self.handlers.items():

            result = handler.execute()
            if result is not None and result != []:
                results[handlerName] = result
        return results

    def scrape(self, itemId, continuation_token=None):
        self.__Response.clear()
        if type(itemId) == str:
            self.itemId = itemId
            self.__Response.update({itemId: self.scrapeSingle(itemId)})
        elif type(itemId) == list:
            for i, id in enumerate(itemId):
                if type(id) == str:
                    self.itemId = id
                    self.__Response.update({id: self.scrapeSingle(id)})
                else:
                    raise ValueError(
                        f"Invalid data type at index {i}. Expected str")
        return self

    def scrapeSingle(self, itemId):
        result = {itemId: None}
        return result

    def get(self):
        for itemId in self.__Response.keys():
            self.itemId = itemId
            result = self.executeHandlers(itemId)
            if itemId in self.__Response:
                self.__Response[itemId].update(result)
            else:
                self.__Response[itemId] = result
        self.restoreDefaultHandlers()
        return self.__Response



class YTSVideo(YTSpider, CommentScraper, TranscriptScraper):
    def __init__(self, commentDefaultHandler=None, transcriptDefaultHandler=None):
        super(YTSVideo, self).__init__()
        CommentScraper.__init__(self, commentDefaultHandler)
        TranscriptScraper.__init__(self, transcriptDefaultHandler)
        self.url = "https://www.youtube.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false"

        #
    def scrapeSingle(self, itemId):
        self.Request.updateContextState(itemId)
        result = self.Request.send(self.url, "POST")
        if "videoDetails" in result:
            return result["videoDetails"]
        return None

class YTSChannel(YTSpider, VideosScraper):
    def __init__(self, videosDefaultHandler=None):
        super(YTSChannel, self).__init__()
        VideosScraper.__init__(self, videosDefaultHandler)
        self.url = "https://www.youtube.com/"

    def prepareURL(self, userInput):
        if type(userInput) != str:
            raise ValueError("Argument (screenName) must be a string")

        screenNames = re.findall(r"@\w+", userInput)
        if len(screenNames) > 0:
            screenName = screenNames[0]
        else:
            raise ValueError(
                "Argument (screenName) must have a screen name as '@ChannelName'")

        return self.url + screenName.strip("/").strip()

    def __postProcessResponse(self, response):
        if isinstance(response, requests.models.Response):
            soup = BeautifulSoup(response.text)
            data = {}
            # FEATURE: add useful meta properties (attributes['property'])
            attributes = {
                "itemprop": [
                    "channelId",
                    "isFamilyFriendly",
                    "regionsAllowed",
                    "paid",
                    "name",
                    "url"
                ],
                "name": [
                    "description",
                    "keywords"
                ],
                "property": []
            }
            thumbnailUrl = soup.find("link", {"itemprop": "thumbnailUrl"})
            if thumbnailUrl is not None:
                thumbnailUrl = thumbnailUrl['href']

            for criteria in attributes:
                for metaKey in attributes[criteria]:
                    tag = soup.find("meta", {criteria: metaKey})
                    if tag is not None:
                        tagInnerContent = tag['content']
                        data[metaKey] = tagInnerContent
        self.itemId = data["channelId"]
        return data

    def scrapeSingle(self, screenName):
        endpoint = self.prepareURL(screenName)
        result = self.Request.send(endpoint)
        data = self.__postProcessResponse(result)
        return data

