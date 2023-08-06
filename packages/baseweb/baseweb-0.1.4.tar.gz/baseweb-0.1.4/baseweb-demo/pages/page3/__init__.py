import os


from baseweb.interface import register_component
from baseweb.config    import app

# register the Vue component for the UI
register_component("page3.js", os.path.dirname(__file__))

# setup some additional config
app["baseweb-demo"] = {
  "a few" : "app specific",
  "configuration" : "settings"
}
