#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
import json
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/bakeries/<int:id>',methods=["Get","PATCH"])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if request.method == "PATCH":
        name = request.form["name"]
        bakery.name = name
        db.session.add(bakery)
        db.session.commit()
    
    bakery_serialized = bakery.to_dict()    
    response = make_response(bakery_serialized,200  )
    return response

@app.route('/baked_goods',methods=["POST","GET"])
def add_baked_goods():
    if request.method == "POST":
        print(request.form)
        name = request.form["name"]
        price = request.form["price"]
        bakery_id = request.form["bakery_id"]
    
        new_goods = BakedGood(
            name = name,
            price = price,
            bakery_id = bakery_id
        )

        db.session.add(new_goods)
        db.session.commit()

        new_baked_goods = new_goods.to_dict()

        json_str = json.dumps(new_baked_goods, indent=4)
        response = make_response(json_str,201)
 
        response.headers["Content-Type"] = "application/json" 

        return response
    else:
        return "<h1>I don't know what I'm doing here at all!!!</h1>"


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

@app.route('/baked_goods/<int:id>', methods=["DELETE"])
def delete_baked_goods(id):
    # baked_good = BakedGood.query.filter_by(id=id).first()
      baked_good = BakedGood.query.get(id)
      print(baked_good)
      db.session.delete(baked_good)
      db.session.commit()
      
      message = {
          "message": "record successfull deleted"
      }
      return message     

if __name__ == '__main__':
    app.run(port=5555, debug=True)
