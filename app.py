from flask import Flask, render_template
from flask_restful import Resource, Api
import json
import dev_posts

app = Flask(__name__)
api = Api(app)


############# See Readme.md to use this ######################
# @app.route('/getallposts', methods=['GET'])
# class GetAllPosts(Resource):
#     def get(self, user):
#         json_data = dev_posts.getAllPosts(user)
#         data = json.loads(json_data)
#         return data
##############################################################


@app.route('/getlastposts', methods=['GET'])
class GetLastPosts(Resource):
    def get(self, user):
        json_data = dev_posts.getLastPosts(user)
        data = json.loads(json_data)
        return data


@app.route('/checklastpost', methods=['GET'])
class CheckLastPost(Resource):
    def get(self, user):
        data = dev_posts.checkLastPost(user)
        return data


@app.route('/getntotalposts', methods=['GET'])
class GetNTotalPosts(Resource):
    def get(self, user):
        data = dev_posts.getNTotalPosts(user)
        return data


@app.route('/', methods=['GET'])
def get():
    return """<p>Get more info in my github <a href="https://github.com/djdany01/DevtoPosts">DevtoPosts</a></p>"""


### Can't use it in heroku because uses selenium with chromedriver, but functions perfect locally. See Readme.md to use it.
# api.add_resource(GetAllPosts, '/getallposts/<user>')
api.add_resource(GetLastPosts, '/getlastposts/<user>')
api.add_resource(CheckLastPost, '/checklastpost/<user>')
api.add_resource(GetNTotalPosts, '/getntotalposts/<user>')


if __name__ == '__main__':
    app.run(port='8009')
