import requests
import falcon

from lib.config import Config

class TestEntryDateParser:
  def on_post(self, req, res):
    doc    = req.context["doc"]
    parser = doc["parser"]
    date   = doc["date"]
    
    api_url = "{}/parser/entryDate".format(Config.BASE_EXTRACT_API)
    print("[TestEntryDateParser] Calling api: {}".format(api_url))
    r                     = requests.post(api_url, json={
      "parser": parser,
      "date": date
    })
    res.context["result"] = r.json()
    res.status            = falcon.HTTP_200