import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'data-centric-project'
app.config["MONGO_URI"] = 'mongodb+srv://FLAF:{}@myfirstcluster-vpr1r.mongodb.net/data-centric-project?retryWrites=true&w=majority'.format(os.environ.get('PASSWORD'))

mongo = PyMongo(app)


@app.route('/')
@app.route('/go_home')
def go_home():
    all_ads = mongo.db.ads.find()

    return render_template("home.html", ads=all_ads)


@app.route('/get_ad/<ad_id>')
def get_ad(ad_id):
    the_ad = mongo.db.ads.find_one({"_id": ObjectId(ad_id)})
    all_categories = mongo.db.categories.find()
    return render_template('ad.html', ad=the_ad, categories=all_categories)


# @app.route('/add_task')
# def add_task():
#     return render_template('addtask.html',
#                           categories=mongo.db.categories.find())


# @app.route('/insert_task', methods=['POST'])
# def insert_task():
#     tasks = mongo.db.tasks
#     tasks.insert_one(request.form.to_dict())
#     return redirect(url_for('get_tasks'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)