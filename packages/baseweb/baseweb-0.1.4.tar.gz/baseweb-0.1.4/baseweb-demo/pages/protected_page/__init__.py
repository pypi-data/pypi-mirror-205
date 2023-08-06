import os

# register the Vue component for the UI

from baseweb.interface import register_component

register_component("protected_page.js", os.path.dirname(__file__))

# setup OATK infrastructure

from flask import Response
from flask_restful import Resource, Api

from baseweb.web       import server
from baseweb.interface import register_external_script
from baseweb.config    import app

import oatk.js
from oatk import OAuthToolkit

# add discovery url and client_id from env
app["oauth"] = {
  "provider" : os.environ.get("OAUTH_PROVIDER"),
  "client_id": os.environ.get("OAUTH_CLIENT_ID")
}

# route for oatk.js from the oatk package
@server.route("/oatk.js", methods=["GET"])
def oatk_script():
  return Response(oatk.js.as_src(), mimetype="application/javascript")

# and have it included in the HTML
register_external_script("/oatk.js")

# a protected API endpoint

# API set up
api = Api(server)

# setup oatk
auth = OAuthToolkit()
auth.using_provider(os.environ["OAUTH_PROVIDER"]);
auth.with_client_id(os.environ["OAUTH_CLIENT_ID"])

class HelloWorld(Resource):
  @auth.authenticated
  def get(self):
    return {
      "message": "hello protected world"
    }

api.add_resource(HelloWorld, "/api/protected/hello")
