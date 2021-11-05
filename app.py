from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)


    def __init__(self, title, price):
        self.title = title
        self.price = price

class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "price")
        

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

@app.route("/post/add", methods =["POST"])
def add_post():
    title = request.json.get("title")
    price = request.json.get("price")

    record = Post(title, price)
    db.session.add(record)
    db.session.commit()

    return jsonify(post_schema.dump(record))

@app.route("/post/get", methods=["GET"])
def get_all_posts():
    all_posts = Post.query.all()
    return jsonify(posts_schema.dump(all_posts)) 

if __name__ == '__main__':
    app.run(debug=True)