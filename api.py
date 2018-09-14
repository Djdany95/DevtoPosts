from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json
import dev_posts

app = Flask(__name__)
api = Api(app)

@app.route('/getallposts', methods=['GET'])
class getAllPosts(Resource):
    def get(self, user):
        json_data = dev_posts.getAllPosts(user)
        data = json.loads(json_data)
        return data

@app.route('/getlastposts', methods=['GET'])
class getLastPosts(Resource):
    def get(self, user):
        json_data = dev_posts.getLastPosts(user)
        data = json.loads(json_data)
        return data

@app.route('/checklastpost', methods=['GET'])
class checkLastPost(Resource):
    def get(self, user):
        data = dev_posts.checkLastPost(user)
        return data

@app.route('/getntotalposts', methods=['GET'])
class getNTotalPosts(Resource):
    def get(self, user):
        data = dev_posts.getNTotalPosts(user)
        return data


api.add_resource(getAllPosts, '/getallposts/<user>')
api.add_resource(getLastPosts, '/getlastposts/<user>')
api.add_resource(checkLastPost, '/checklastpost/<user>')
api.add_resource(getNTotalPosts, '/getntotalposts/<user>')

if __name__ == '__main__':
    app.run(port='8009')
