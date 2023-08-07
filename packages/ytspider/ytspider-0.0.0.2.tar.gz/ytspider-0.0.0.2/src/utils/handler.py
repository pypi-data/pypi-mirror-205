from .request import Request

class BaseHandler:
    def __init__(self, name=None):
        self.request = Request()
        self.name = name

    def execute(self):

        return None



class CommentHandler(BaseHandler):
    def __init__(self, n_comments=0):
        super(CommentHandler, self).__init__(name='comments')
        self.n_comments = n_comments

    def execute(self):
        return None


class CommentDefaultHandler(CommentHandler):
    def __init__(self, n_comments=0):
        super(CommentDefaultHandler, self).__init__(n_comments)

    def execute(self):

        return None


class CommentScrapingHandler(CommentHandler):
    def __init__(self, videoId, n_comments=100):
        super(CommentScrapingHandler, self).__init__(n_comments)
        self.videoId = videoId
        self.url = "https://www.youtube.com/youtubei/v1/next?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false"

    def execute(self):
        self.request.updateContextState(
            self.videoId, additional={"continuation": ""})
        firstTime = True
        token = ""
        all_comments = []
        while token is not None and len(all_comments) < self.n_comments:
            self.request.updateContextState(additional={"continuation": token})
            result = self.request.send(self.url, method="POST")
            if firstTime:
                token = result["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][3]["itemSectionRenderer"][
                    "contents"][0]["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
                firstTime = False
            else:
                try:
                    token = result["onResponseReceivedEndpoints"][-1]["reloadContinuationItemsCommand"]["continuationItems"][-1][
                        "continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
                    comments = result["onResponseReceivedEndpoints"][-1]["reloadContinuationItemsCommand"]["continuationItems"][:-1]
                except:
                    try:
                        token = result["onResponseReceivedEndpoints"][-1]["appendContinuationItemsAction"]["continuationItems"][-1][
                            "continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
                    except:
                        token = None
                    try:
                        comments = result["onResponseReceivedEndpoints"][-1]["appendContinuationItemsAction"]["continuationItems"][:-1]
                    except:
                        comments = []
                for i in range(len(comments)):
                    comment_texts = comments[i]["commentThreadRenderer"]["comment"]["commentRenderer"]["contentText"]['runs']
                    comment = " ".join(
                        list(map(lambda c: c["text"], comment_texts)))
                    all_comments.append(comment)
        return all_comments



class TranscriptionHandler(BaseHandler):
    def __init__(self, only_in_langs=[]):
        super(TranscriptionHandler, self).__init__(name='transcripts')
        self.only_in_langs = only_in_langs

    def execute(self):
        return None


class TranscriptionScrapingHandler(TranscriptionHandler):
    def __init__(self, only_in_langs=[]):
        super(TranscriptionScrapingHandler, self).__init__(only_in_langs)

    def execute(self):
        result = ["One Two THree"]
        return result


class TranscriptionDefaultHandler(TranscriptionHandler):
    def __init__(self):
        super(TranscriptionDefaultHandler, self).__init__()

    def execute(self):
        return None


class VideosHandler(BaseHandler):
    def __init__(self, n_videos=0):
        super(VideosHandler, self).__init__(name='videos')
        self.n_videos = n_videos

    def execute(self):
        return None


class VideosDefaultHandler(VideosHandler):
    def __init__(self, n_videos=0):
        super(VideosDefaultHandler, self).__init__(n_videos)

    def execute(self):
        return None


class VideosScrapingHandler(VideosHandler):
    def __init__(self, itemId, n_videos=29):
        super(VideosScrapingHandler, self).__init__(n_videos)
        self.channelId = itemId
        self.url = "https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false"

    def execute(self):
        params_token = ""
        firstTime = True
        token = ""
        all_videos = []

        self.request.updateContextState(additional={"browseId": self.channelId, "params": params_token})
        # Scrape MainPage tab
        result = self.request.send(self.url, "POST")

        try:
            # Get param which will route the scraping to Videos Tab
            tabs = result["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]
            if len(tabs) > 2 and tabs[1]["tabRenderer"]["title"] == "Videos":
                vidTabsEndPointParam = tabs[1]["tabRenderer"]["endpoint"]["browseEndpoint"]["params"]
                self.request.updateContextState(additional={"params": vidTabsEndPointParam})
                # Scrape Videos Tab
                result = self.request.send(self.url, "POST")

                tabs = result["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]
                videoItems = tabs[1]["tabRenderer"]["content"]["richGridRenderer"]["contents"]
                # Remove unnecessary request payload
                self.request.updateContextState(removables=["params", "browseId"])
                while len(all_videos) < self.n_videos:
                    for videoItem in videoItems[:-1]:
                        vidRender = videoItem["richItemRenderer"]["content"]["videoRenderer"]
                        video = {}
                        video["id"] = vidRender["videoId"]
                        video["title"] = vidRender["title"]["runs"][0]["text"]
                        video["views_count"] = vidRender["viewCountText"]["simpleText"]
                        video["publish_at"] = vidRender["publishedTimeText"]["simpleText"]

                        if len(all_videos) >= self.n_videos:
                            return all_videos
                        all_videos.append(video)
                    try:
                        # Set Continuation Parameter
                        continuationParam = videoItems[-1]["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
                    except Exception as e:
                        print(e)
                        break
                    self.request.updateContextState(additional={"continuation":continuationParam})
                    result = self.request.send(self.url, "POST")
                    try:
                        videoItems = result["onResponseReceivedActions"][0]["appendContinuationItemsAction"]["continuationItems"]
                    except Exception as e:
                        print(e)
                        break

        except Exception as e:
            print(e)
            pass
        return all_videos

        # # TODO: Scrape for first time to get "params", then use tabs[1] to get params and scrape Videos tab[1]
        # # What about making one class 'ChannelTabHandler' which takes tab name (videos, playlists), nope because each has different output (solvable but code more for fun)
