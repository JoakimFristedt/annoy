#!flask/bin/python

import os

from rest.IndexController import app

if __name__ == '__main__':
    app.run(debug=True)
