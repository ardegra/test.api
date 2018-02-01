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
        
      grab = Grab()
      page = grab.go(url)
        
      result  = {"postList": [], "hasLastPage": False, "hasPrevPage": False, "hasNextPage": False}
      api_url = "{}/spider/forum/extract/post".format(Config.BASE_EXTRACT_API)
      r       = requests.post(api_url, json={"xpath": xpath, "url": url})
      result.update({"postList": r.json()["postList"]})
      result.update({"firstPostId": page.select(xpath["post"]["firstPostId"]).text()})
      
      try:
        last_page = grab.make_url_absolute(page.select(xpath["thread"]["lastPage"]).attr("href"))
        result.update({"hasLastPage": True})
        
        page = grab.go(last_page)
        try:
          prev_page = grab.make_url_absolute(page.select(xpath["thread"]["prevPage"]).attr("href"))
          result.update({"hasPrevPage": True})
        except weblib.error.DataNotFound:
          result.update({"hasPrevPage": False})
      except weblib.error.DataNotFound:
        result.update({"hasLastPage": False})
      
      page = grab.go(url)
      try:
        grab.make_url_absolute(page.select(xpath["thread"]["nextPage"]).attr("href"))
        result.update({"hasNextPage": True})
      except weblib.error.DataNotFound:
        result.update({"hasNextPage": False})
      return result

    def _thread_test(self, url=None, xpath=None):
      """ _thread_test """
      assert url is not None, "url is not defined."
      assert xpath is not None, "xpath is not defined."
      
      grab = Grab()
      page = grab.go(url)
      
      result  = {"threadList": [], "hasLastPage": False, "hasPrevPage": True}
      api_url = "{}/spider/forum/extract/threadUrl".format(Config.BASE_EXTRACT_API)
      r       = requests.post(api_url, json={"xpath": xpath, "url": url})
      result["threadList"] = r.json()["threadList"]
        
      try:
        last_page = page.select(xpath["category"]["lastPage"]).attr("href")
        last_page = grab.make_url_absolute(last_page)
        result.update({"hasLastPage": True})
        
        try:
          print("[TestForumSpider] Going to last_page: {}".format(last_page))
          page      = grab.go(grab.make_url_absolute(last_page))
          prev_page = page.select(xpath["category"]["prevPage"]).attr("href")
          result.update({"hasPrevPage": True})
        except weblib.error.DataNotFound as err:
          print("[TestForumSpider] XPATH error: {}".format(str(err)))
          result.update({"hasPrevPage": False})
      except weblib.error.DataNotFound as err:
        print("[TestForumSpider] XPATH error: {}".format(str(err)))
        result.update({"hasLastPage": False})
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
