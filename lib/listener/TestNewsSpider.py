import falcon
import requests
import weblib

from lib.config import Config

from grab import Grab

class TestNewsSpider:
  """ TestNewsSpider """
  def _article_test(self, url=None, xpath=None):
    """ _article_test """
    assert url is not None, "url is not defined."
    assert xpath is not None, "xpath is not defined."

    api_url = "{}/spider/news/extract/article".format(Config.BASE_EXTRACT_API)
    r       = requests.post(api_url, json={"xpath": xpath, "url": url})
    return r.json()
  
  def _article_url_test(self, url=None, xpath=None):
    """ _article_url_test """
    assert url is not None, "url is not defined."
    assert xpath is not None, "xpath is not defined."
    
    api_url = "{}/spider/news/extract/articleUrl".format(Config.BASE_EXTRACT_API)
    r       = requests.post(api_url, json={"xpath": xpath, "url": url})
    return r.json()
  
  def on_post(self, req, res):
    """ handle POST request """
    doc       = req.context["doc"]
    test_type = doc["type"]
    xpath     = doc["xpath"]
    url       = doc["url"]
        
    result = {}
    if test_type == "Article Test":
      result = self._article_test(url, xpath)
    elif test_type == "Article URL Test":
      result = self._article_url_test(url, xpath)

    res.status            = falcon.HTTP_200
    res.context["result"] = result