from flask import Flask
from flask import make_response, render_template
from flask_restful import Resource, Api
import recommendations
import numpy as np

app = Flask(__name__)
api = Api(app)




class Home(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)

class Recommendation(Resource):
    def get(self):
        return "Please give in your userId in the url "

class Recommendation_Name(Resource):
    def get(self, user_id):
        user = np.array(int(user_id))
        rec = recommendations.getRecommendations(user)
        # select columns
        recColumns = rec[['item', 'score']]
        # select row (normally not needed)
        rowSeries = recColumns.iloc[0]
        item = rowSeries.values[0]
        score = rowSeries.values[1]
        return item


api.add_resource(Home, '/home')
api.add_resource(Recommendation, '/recommendation')
api.add_resource(Recommendation_Name, '/recommendation/<user_id>')


@app.route("/")
def hello():
    return "hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
