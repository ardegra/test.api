import weblib
import json

import falcon
import requests

from lib.config import Config

from grab import Grab

class TestForumSpider:
    def _post_test(self, url=None, xpath=None):
      """ _post_test """
      assert url is not None, "url is not defined."
      assert xpath is not None, "xpath is not defined."
        
      result  = {"postList": [], "lastPageUrl": False, "prevPageUrl": False, "nextPageUrl": False}
      api_url = "{}/spider/forum/extract/post".format(Config.BASE_EXTRACT_API)
      r       = requests.post(api_url, json={"xpath": xpath, "url": url})
      result.update({"postList": r.json()["postList"]})
      
      api_url = "{}/spider/forum/extract/post/firstPostId".format(Config.BASE_EXTRACT_API)
      r       = requests.post(api_url, json={"xpath": xpath, "url": url})
      result.update({"firstPostId": r.json()["firstPostId"]})
      
      api_url       = "{}/spider/forum/extract/thread/lastPageUrl".format(Config.BASE_EXTRACT_API)
      r             = requests.post(api_url, json={"xpath": xpath, "url": url})
      last_page_url = r.json()["lastPageUrl"]
      result.update({"lastPageUrl": last_page_url})

      api_url       = "{}/spider/forum/extract/thread/nextPageUrl".format(Config.BASE_EXTRACT_API)
      r             = requests.post(api_url, json={"xpath": xpath, "url": url})
      next_page_url = r.json()["nextPageUrl"]
      result.update({"nextPageUrl": next_page_url})

      if last_page_url is not None:
        api_url       = "{}/spider/forum/extract/thread/prevPageUrl".format(Config.BASE_EXTRACT_API)
        r             = requests.post(api_url, json={"xpath": xpath, "url": last_page_url})
        prev_page_url = r.json()["prevPageUrl"]
        result.update({"prevPageUrl": prev_page_url})
      return result

    def _thread_test(self, url=None, xpath=None):
      """ _thread_test """
      assert url is not None, "url is not defined."
      assert xpath is not None, "xpath is not defined."
      
      grab = Grab()
      page = grab.go(url)
      
      result  = {"threadList": [], "lastPageUrl": False, "prevPageUrl": True}
      api_url = "{}/spider/forum/extract/threadUrl".format(Config.BASE_EXTRACT_API)
      r       = requests.post(api_url, json={"xpath": xpath, "url": url})
      result["threadList"] = r.json()["threadList"]
        
      api_url       = "{}/spider/forum/extract/category/lastPageUrl".format(Config.BASE_EXTRACT_API)
      r             = requests.post(api_url, json={"xpath": xpath, "url": url})
      last_page_url = r.json()["lastPageUrl"]
      result.update({"lastPageUrl": last_page_url})
      
      if last_page_url is not None:
        api_url       = "{}/spider/forum/extract/category/prevPageUrl".format(Config.BASE_EXTRACT_API)
        r             = requests.post(api_url, json={"xpath": xpath, "url": url})
        prev_page_url = r.json()["prevPageUrl"]
        result.update({"prevPageUrl": prev_page_url})
      return result

    def on_post(self, req, res):
      """ handles POST requests """
      doc       = req.context["doc"]
      test_type = doc["type"]
      xpath     = doc["xpath"]
      url       = doc["url"]
      
      result = {}
      if test_type == "Post Test":
        result = self._post_test(url, xpath)
      elif test_type == "Thread Test":
        result = self._thread_test(url, xpath)

      res.status            = falcon.HTTP_200
      res.context["result"] = result
