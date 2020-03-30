import pprint
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

config = {
  'YAHOO_API_KEY': os.environ.get("YAHOO_API_KEY"),
  'GOOGLE_API_KEY': os.environ.get("GOOGLE_API_KEY"),
  'model_file': os.environ.get("model_file"),
  'label_file': os.environ.get("label_file"),
}

# pprint.pprint(config)
