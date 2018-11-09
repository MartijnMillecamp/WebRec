from flask import Flask
from flask import request, jsonify
from flask import make_response, render_template
from flask_restful import Resource, Api, reqparse
import recommendations
# import ratings
import numpy as np

app = Flask(__name__)
api = Api(app)




class Home(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'), 200, headers)

class Recommendation(Resource):
    def get(self):
        return "Invalid request, no user id"

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

class Ratings(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user', type=int)
        parser.add_argument('item', type=int)
        request = parser.parse_args()
        user_id = request['user']
        item_id = request['item']
        rating = ratings.getRating(user_id, item_id)
        print(rating)
        print(type(rating))
        data = [
            {'user_id': user_id,
            'item_id': item_id,
            'rating': rating
            }
        ]
        return jsonify(data)

api.add_resource(Home, '/home')
api.add_resource(Recommendation, '/recommendation')
api.add_resource(Recommendation_Name, '/recommendation/<user_id>')
api.add_resource(Ratings, '/ratings')



@app.route("/")
def hello():
    return "hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
