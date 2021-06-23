import logging
import os

from flask import Flask, url_for, request, render_template
from markupsafe import escape
from argparse import ArgumentParser
import werkzeug._internal

def demi_logger(type, message,*args,**kwargs):
    pass

werkzeug._internal._log = demi_logger

logging.basicConfig(filename='record.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
from views import *


def create_app(deploy_version=None):
    #with open("../best_model_version.txt", "r") as model_version_file:
    #    best_model_version = model_version_file.readline()
    app.config['deploy_version'] = None # deploy_version or best_model_version
    print('Passed item: ', app.config['deploy_version'])
    return app


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-deploy_version')
    args = parser.parse_args()
    app = create_app(args.deploy_version)
    app.run(host="0.0.0.0", port="5100")

