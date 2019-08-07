import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import datetime

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'data-centric-project'
app.config["MONGO_URI"] = 'mongodb+srv://FLAF:{}@myfirstcluster-vpr1r.mongodb.net/data-centric-project?retryWrites=true&w=majority'.format(os.environ.get('PASSWORD'))

mongo = PyMongo(app)


@app.route('/')
@app.route('/go_home')
def go_home():

    all_ads = mongo.db.ads.find().sort("date_created" , 1).skip(0).limit(8)
    all_categories = mongo.db.categories.find()
    return render_template("home.html", ads=all_ads, categories=all_categories)


@app.route('/get_ad/<ad_id>')
def get_ad(ad_id):
    the_ad = mongo.db.ads.find_one({"_id": ObjectId(ad_id)})
    all_categories = mongo.db.categories.find()
    return render_template('ad.html', ad=the_ad, categories=all_categories)


@app.route('/add_ad')
def add_ad():

    return render_template('addad.html', categories=mongo.db.categories.find(), date=datetime.datetime.today())


@app.route('/insert_ad', methods=['POST'])
def insert_ad():
    ads = mongo.db.ads
    all_ads = mongo.db.ads.find()
    ads.insert_one(request.form.to_dict())
    
    return render_template("home.html", ads=all_ads, )
    # return redirect(url_for('go_home'))

@app.route('/by_cat/<cat_name>')
def by_cat(cat_name):
    # the_ad = mongo.db.ads.find_one({"_id": ObjectId(ad_id)})
    cat_ads = mongo.db.ads.find({"category_name": cat_name}).sort("date_created" , 1).skip(0).limit(8)
    # one_category = mongo.db.categories.find_one({"category_name": cat_name})
    return render_template('catbrowse.html', ads=cat_ads)



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)