import os
from os.path import join, dirname
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app=Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = "./static/profile_pics"

SECRET_KEY = "SPARTA"
TOKEN_KEY = 'mytoken'




MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]
users_collection = db["users"]

@app.route('/')
def main():
    return render_template("index.html" , active_page='home')

@app.route('/home')
def home():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("home.html" , active_page='home',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))


@app.route('/login')
def login():
    return render_template("login.html")
    
@app.route('/register')
def register():
    return render_template("register.html" )

@app.route('/heroes')
def heroes():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("heroes.html" , active_page='heroes',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/hero_story',methods=['GET'])
def hero_story():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("hero_story.html" , active_page='hero_story',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/skin')
def skin():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("skin.html" , active_page='skin',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/jungle')
def jungle():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("jungle.html" , active_page='jungle',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/interactive_maps')
def maps():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("interactive_maps.html" , active_page='interactive_maps',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/discussion')
def discussion():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("discussion.html" , active_page='discussion',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))


@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'username': payload['username']})
        comment_receive = request.form['comment_give']
        date_receive = request.form['date_give']
        doc = {
            'username': user_info['username'],
            'comment': comment_receive,
            'date': date_receive,
            'replies': []
        }
        db.posts.insert_one(doc)
        return jsonify({'result': 'success', 'msg': 'Posting successful!'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))

@app.route('/edit/<id>', methods=['POST'])
def edit(id):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'username': payload['username']})
        comment_receive = request.form['comment_give']
        doc = {
            'comment': comment_receive,
        }
        db.posts.update_one({'_id': ObjectId(id)}, {'$set': doc})
        return jsonify({'result': 'success', 'msg': 'Edit successful!'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))

@app.route('/posts/<id>/reply', methods=['POST'])
def reply_post(id):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'username': payload['username']})
        reply_receive = request.form['reply_give']
        reply = {
            'username': user_info['username'],
            'comment': reply_receive,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        db.posts.update_one({'_id': ObjectId(id)}, {'$push': {'replies': reply}})
        return jsonify({'result': 'success', 'msg': 'Reply successful!'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))
    except Exception as e:
        print(f"Error: {e}")  # Add logging here
        return jsonify({'result': 'error', 'msg': str(e)})


@app.route("/edit_heroes/<id>", methods=["POST"])
def edit_heroes(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # We should create a new post here
        user_info = db.users.find_one({"username": payload["username"]})
        username = user_info["username"]
        
        heroes = request.form["hero"]
        role = request.form["roles"]
        doc = {
            "heroes": heroes,
            "roles": role
        }
        if 'icon' in request.files:
            icon = request.files["icon"]
            filename = secure_filename(icon.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{filename}.{extension}"
            icon.save("./static/" + file_path)
            doc["icon"] = file_path

        db.heroes.update_one({"_id": ObjectId(id)}, {"$set": doc})
        return jsonify({"result": "success", "msg": "Edit successful!"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/hapus/<id>", methods=["POST"])
def hapus(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # We should create a new post here

        db.posts.delete_one({"_id": ObjectId(id)})
        return jsonify({"result": "success", "msg": "Delete successful!"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/hapus_heroes/<id>", methods=["POST"])
def hapus_heroes(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # We should create a new post here

        db.heroes.delete_one({"_id": ObjectId(id)})
        return jsonify({"result": "success", "msg": "Delete successful!"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/get_posts", methods=["GET"])
def get_posts():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # We should fetch the full list of posts here
        posts = list(db.posts.find({}).sort("date", -1).limit(20))
        for post in posts:
            post["_id"] = str(post["_id"])
            post["count_heart"] = db.likes.count_documents(
                {"post_id": post["_id"], "type": "heart"}
            )
            post["count_star"] = db.likes.count_documents(
                {"post_id": post["_id"], "type": "star"}
            )
            post["count_thumbsup"] = db.likes.count_documents(
                {"post_id": post["_id"], "type": "thumbsup"}
            )
            post["heart_by_me"] = bool(
                db.likes.find_one(
                    {"post_id": post["_id"], "type": "heart", "username": payload["id"]}
                )
            )
            post["star_by_me"] = bool(
                db.likes.find_one(
                    {"post_id": post["_id"], "type": "star", "username": payload["id"]}
                )
            )
            post["thumbsup_by_me"] = bool(
                db.likes.find_one(
                    {"post_id": post["_id"], "type": "thumbsup", "username": payload["id"]}
                )
            )
        return jsonify(
            {
                "result": "success",
                "msg": "Successful fetched all posts",
                "posts": posts,
            }
        )
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))



@app.route('/get_heroes')
def get_heroes():
    heroes = list(db.heroes.find({}))
    for hero in heroes:
        hero['_id'] = str(hero['_id'])
    return jsonify({"result": "success", "heroes": heroes})

@app.route('/mypost')
def mypost():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        username = payload["username"]
        status = username == payload["id"]
        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template("mypost.html" , active_page='mypost',user_info=user_info, status=status)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/dashboard_discussion')
def dashboard_discussion():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )

        return render_template("dashboard_discussion.html" , active_page='dashboard_discussion',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/dashboard_content')
def dashboard_content():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("dashboard_content_heroes.html" , active_page='dashboard_content_heroes',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))

@app.route('/dashboard_heroes')
def dashboard_heroes():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("dashboard_heroes.html" , active_page='dashboard_heroes',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))
    

@app.route('/tambah', methods=["POST"])
def tambah():
    token_receive = request.cookies.get(TOKEN_KEY)
    icon = request.files["icon"]
    heroes = request.form["hero"]
    role = request.form["roles"]
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        doc = {
            "heroes": heroes,
            "roles": role
        }
        filename = secure_filename(icon.filename)
        extension = filename.split(".")[-1]
        file_path = f"profile_pics/{filename}.{extension}"
        icon.save("./static/" + file_path)
        doc["icon"] = file_path

        db.heroes.insert_one(doc)
        return jsonify({"result": "success", "msg": "Heroes updated!"})
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))


@app.route('/dashboard_story')
def dashboard_story():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return render_template("dashboard_hero_story.html" , active_page='dashboard_hero_story',user_info=payload,)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))


@app.route('/sign_in', methods=['POST'])
def sign_in():
    email_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()

    result = db.users.find_one({
        "email": email_receive,
        "password": pw_hash,
    })

    if result:
        payload = {
            "id": email_receive,
            "username": result['username'],
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }

        if "roles" in result and result["roles"] == 'admin':
            payload["admin"] = True

           
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            # Arahkan ke halaman dashboard jika admin berhasil login
            return jsonify({"result": "success", "token": token, "admin": True})

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        print(token)
        return jsonify({"result": "success", "token": token})
    
    return jsonify({"result": "failure", "message": "Invalid credentials"})
    
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form.get('username_give')
    email_recive = request.form.get('email_give')
    password_receive = request.form.get('password_give')
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # id
        "email" : email_recive,                                     # email
        "password": password_hash,                                  # password
        "roles":"user",
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form.get('username_give')
    exists = bool(db.users.find_one({"email": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/profile/<keyword>')
def profile(keyword):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        
        return render_template("profile.html" ,user_info=payload)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))
    
# hero_story
    
@app.route("/edit_story/<id>", methods=["POST"])
def edit_story(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # Assuming 'db' is your MongoDB connection

        # Make sure to use 'stories' collection name instead of 'story'
        # Adjust the following line according to your actual collection name
        user_info = db.stories.find_one({"_id": ObjectId(id), "username": payload["username"]})
        if user_info:
            heroes = request.form["hero"]
            story = request.form["story"]
            doc = {
                "heroes": heroes,
                "story": story
            }

            if 'icon' in request.files:
                icon = request.files["icon"]
                filename = secure_filename(icon.filename)
                extension = filename.split(".")[-1]
                file_path = f"profile_pics/{filename}.{extension}"
                icon.save("./static/" + file_path)
                doc["icon"] = file_path

            # Use the correct collection name ('stories' in this case)
            db.stories.update_one({"_id": ObjectId(id)}, {"$set": doc})
            return jsonify({"result": "success", "msg": "Edit successful!"})
        else:
            # Handle case where the user does not have permission to edit
            return jsonify({"result": "error", "msg": "Unauthorized access"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/hapus_story/<id>", methods=["POST"])
def hapus_story(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        # We should create a new post here

        db.story.delete_one({"_id": ObjectId(id)})
        return jsonify({"result": "success", "msg": "Delete successful!"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route('/tambah_story', methods=["POST"])
def tambah_story():
    token_receive = request.cookies.get(TOKEN_KEY)
    icon = request.files["icon"]
    heroes = request.form["hero"]
    story = request.form["story"]
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        doc = {
            "heroes": heroes,
            "story": story
        }
        filename = secure_filename(icon.filename)
        extension = filename.split(".")[-1]
        file_path = f"profile_pics/{filename}.{extension}"
        icon.save("./static/" + file_path)
        doc["icon"] = file_path

        db.story.insert_one(doc)
        return jsonify({"result": "success", "msg": "Heroes updated!"})
    except jwt.ExpiredSignatureError:
        msg = 'Your Token has expired'
        return redirect(url_for('login', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = ' There was a problem logging you in'
        return redirect(url_for('login', msg=msg))
    
@app.route('/get_story')
def get_story():
    stories = list(db.story.find({}))
    for story in stories:
        story['_id'] = str(story['_id'])
    return jsonify({"result": "success", "stories": stories})

@app.route('/accounts')
def accounts():
    users = list(users_collection.find())  # Fetch all user documents and convert to list
    total_users = users_collection.count_documents({})  # Count total number of users
    return render_template('accounts.html', users=users, total_users=total_users)

@app.route('/update_like', methods=['POST'])
def update_like():
    try:
        post_id = request.form['post_id']
        action = request.form['action']
        post = db.posts.find_one({'_id': ObjectId(post_id)})

        if post:
            if action == 'like':
                db.posts.update_one(
                    {'_id': ObjectId(post_id)},
                    {'$inc': {'likes': 1}}
                )
            elif action == 'unlike':
                db.posts.update_one(
                    {'_id': ObjectId(post_id)},
                    {'$inc': {'likes': -1}}
                )
            return jsonify({'result': 'success', 'msg': 'Like updated!'})
        else:
            return jsonify({'result': 'error', 'msg': 'Post not found'})
    except Exception as e:
        return jsonify({'result': 'error', 'msg': str(e)})
    
@app.route('/total_posts')
def total_posts():
    posts = list(db.posts.find())  # Fetch all post documents and convert to list
    total_posts = db.posts.count_documents({})  # Count total number of posts
    return render_template('total_posts.html', posts=posts, total_posts=total_posts)





if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)