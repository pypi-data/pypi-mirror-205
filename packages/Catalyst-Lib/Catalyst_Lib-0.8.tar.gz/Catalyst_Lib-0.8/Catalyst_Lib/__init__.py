import sys
import requests
from . import colors, dictionaries, exporter, graphbuilder, htmlgen, lib, lists, multiLambda, progressBar, question, randomgen, table, UserProfile


this = sys.modules[__name__]


this.mode = "Production"
this.__version__ = 0.8


def update_status():
    if this.mode == "Development":
        print("Catalyst Lib running in development mode")
        status = requests.get("https://pypi.python.org/pypi/Catalyst-Lib/json")
        if status.status_code == 200:
            if float(status.json()["info"]["version"]) > this.__version__:
                print(f"Please update Catalyst Lib to the latest version ({status.json()['info']['version']})")
    if this.mode == "Production":
        pass


def thankyou():
    print("Thank you for using Catalyst Lib")


def set_status_development():
    this.mode = "Development"
    update_status()


def set_status_production():
    this.mode = "Production"
    update_status()
