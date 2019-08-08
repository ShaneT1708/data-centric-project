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
    all_counties = mongo.db.counties.find()
    return render_template("home.html", ads=all_ads, categories=all_categories, counties=all_counties)


@app.route('/get_ad/<ad_id>')
def get_ad(ad_id):
    the_ad = mongo.db.ads.find_one({"_id": ObjectId(ad_id)})
    all_categories = mongo.db.categories.find()
    return render_template('ad.html', ad=the_ad, categories=all_categories)


@app.route('/add_ad')
def add_ad():

    return render_template('addad.html', categories=mongo.db.categories.find(), date=datetime.datetime.today(), counties=mongo.db.counties.find())


@app.route('/insert_ad', methods=['POST'])
def insert_ad():
    ads = mongo.db.ads
    all_ads = mongo.db.ads.find().sort("date_created" , 1).skip(0).limit(8)
    ads.insert_one(request.form.to_dict())
    
    return render_template("home.html", ads=all_ads, )
    # return redirect(url_for('go_home'))

@app.route('/by_cat/<cat_name>')
def by_cat(cat_name):
    # the_ad = mongo.db.ads.find_one({"_id": ObjectId(ad_id)})
    cat_ads = mongo.db.ads.find({"category_name": cat_name}).sort("date_created" , 1).skip(0)
    # one_category = mongo.db.categories.find_one({"category_name": cat_name})
    return render_template('catbrowse.html', ads=cat_ads)

@app.route('/by_cou/<cou_name>')
def by_cou(cou_name):
    cou_ads = mongo.db.ads.find({"county_name": cou_name}).sort("date_created" , 1).skip(0)
    return render_template('catbrowse.html', ads=cou_ads)


@app.route('/edit_ad/<ad_id>')
def edit_ad(ad_id):
    the_ad =  mongo.db.ads.find_one({"_id": ObjectId(ad_id)})
    all_categories =  mongo.db.categories.find()
    all_counties =  mongo.db.counties.find()
    return render_template('editad.html', ad=the_ad, categories=all_categories, counties=all_counties)



@app.route('/update_ad/<ad_id>', methods=["POST"])
def update_ad(ad_id):
    ads = mongo.db.ads
    all_ads = mongo.db.ads.find().sort("date_created" , 1).skip(0).limit(8)
    ads.update( {'_id': ObjectId(ad_id)},
    {
        'ad_name':request.form.get('ad_name'),
        'category_name':request.form.get('category_name'),
        'ad_image': request.form.get('ad_description'),
        'asking_price': request.form.get('asking_price'),
        'seller_name':request.form.get('seller_name'),
        'phone_number':request.form.get('phone_number'),
        'location':request.form.get('location'),
        
    })
    return render_template("home.html", ads=all_ads, )

@app.route('/delete_ad/<ad_id>')
def delete_ad(ad_id):
    all_ads = mongo.db.ads.find().sort("date_created" , 1).skip(0).limit(8)
    mongo.db.ads.remove({'_id': ObjectId(ad_id)})
    return render_template("home.html", ads=all_ads, )


@app.route('/all_ads')
def all_ads():

    all_ads = mongo.db.ads.find().sort("date_created" , 1).skip(0)
    all_categories = mongo.db.categories.find()
    return render_template("allads.html", ads=all_ads, categories=all_categories)

@app.route('/search', methods=['POST'])
def search():
    # mongo.db.recipes.drop_indexes()
    query = request.form.get('query')
    results = mongo.db.ads.find({'$text': {'$search': query}})
    return render_template("allads.html", ads=results, type='searched', query=query)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)