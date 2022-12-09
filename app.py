from crypt import methods
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fgalvan:!31Jerusalem@localhost/tennis_users'
db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Review: {self.description}"
    
    def __init__(self, description):
        self.description = description

def format_review(review):
    return {
        "description": review.description,
        "id": review.id,
        "created_at": review.created_at
    }

#index route
@app.route('/')
def hello():
    return "hey"


#create route
@app.route('/review', methods = ['POST'])
def create__review():
    description = request.json['description']
    review = Review(description)
    db.session.add(review)
    db.session.commit()
    return format_review(review)

#read (get all)
@app.route('/review', methods= ['GET'])
def get_reviews():
    reviews = Review.query.order_by(Review.id.asc()).all()
    review_list = []
    for review in reviews:
        review_list.append(format_review(review))
    return{'reviews': review_list}

#read (single)
@app.route('/review/<id>', methods=['GET'])
def get_review(id):
    review = Review.query.filter_by(id=id).one()
    formatted_review = format_review(review)
    return{'review': formatted_review}


#update route
@app.route('/review/<id>', methods= ['PUT'])
def update_review(id):
    review = Review.query.filter_by(id=id)
    description = request.json['description']
    review.update(dict(description = description, created_at = datetime.utcnow()))
    db.session.commit()
    return {"review": format_review(review.one())}


#delete route
@app.route('/review/<id>', methods = ['DELETE'])
def delete_review(id):
    review = Review.query.filter_by(id=id).one()
    db.session.delete(review)
    db.session.commit()
    return 'Review Deleted'

@app.route('/search', methods = ['GET'])
def search_index():
    req = request.get('https://hotels4.p.rapidapi.com/v2/get-meta-data')
    print(req.content)
 

if __name__ == '__main__':
    app.run()