#!/usr/bin/env python
# -*- coding: utf-8 -*

import json

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
