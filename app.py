# credits to https://realpython.com/flask-connexion-rest-api/

from flask import Flask
from flask import request, jsonify
from flask import make_response, render_template
from flask_restful import Resource, Api, reqparse
import connexion
# import recommendations
# import ratings
import numpy as np

#

# Create the application instance
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
