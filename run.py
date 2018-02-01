import falcon

from grab import Grab
from falcon_cors import CORS

from lib.middleware.JSONTranslator import JSONTranslator
from lib.middleware.RequireJSON import RequireJSON

from lib.listener.TestForumSpider import TestForumSpider
from lib.listener.TestNewsSpider import TestNewsSpider

cors = CORS(
  allow_all_origins=True,
  allow_all_headers=True,
  allow_all_methods=True
)
api  = falcon.API(middleware=[cors.middleware, RequireJSON(), JSONTranslator()])

api.add_route("/spider/forum/test", TestForumSpider())
api.add_route("/spider/news/test", TestNewsSpider())

