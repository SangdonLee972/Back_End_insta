from flask import Flask, jsonify, request,make_response
import requests
from flask import Response
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

######### FIREBASE ###########
db = firestore.client()








app = Flask("instaloader")
@app.route('/addUser', methods = ['POST'])
def createuser():
    user_token = request.form.get("user_token")
    doc_ref = db.collection(u'users').document(user_token)

    doc = doc_ref.get()
    if not doc.exists:
        doc_ref.create({
            u'user_token': user_token, 
            u'savedList': []
        })
        return 'ok'
    else:
        data = doc.to_dict()
        return data.get("savedList",[])



@app.route('/save_uri', methods=['POST'])
def saved_post():
    uuid = request.form.get("uuid")
    uri = request.form.get("uri")
    
    # Find the document with the corresponding UUID
    doc_ref = db.collection(u'users').document(uuid)
    doc = doc_ref.get()
    
    if doc.exists:
        # Update the savedList field with the new URI
        data = doc.to_dict()
        saved_list = data.get("savedList", [])
        saved_list.append(uri)
        doc_ref.update({
            u'savedList': saved_list
        })
        return make_response('URI saved successfully', 200)
    else:
        # Create a new document with the UUID and the URI
        doc_ref.set({
            u'user_token': uuid,
            u'savedList': [uri]
        })
        return make_response('New document created', 201)

@app.route('/get_user_Highlight',methods=['POST'])
def get_user_hightlight():
    name = request.form.get("name")  # 클라이언트로부터 name 값을 받아옴

    user_id_response = get_user_id(name)
    user_id_json = user_id_response.json()

    user_id = user_id_json['id']
    time_gen = user_id_json['unrelated_data']['time_gen']

    url = "https://instagram-scraper-2022.p.rapidapi.com/ig/highlights_tray/"

    querystring = {"id_user":user_id}

    headers = {
        "X-RapidAPI-Key": "a6cc07d155mshef5faed51b433bbp11569ejsn9f5af6ece890",
        "X-RapidAPI-Host": "instagram-scraper-2022.p.rapidapi.com"
    }


    response = requests.get(url, headers=headers, params=querystring)

    return Response(response.content, content_type=response.headers['Content-Type'])



@app.route('/get_user_stories',methods=['POST'])
def get_user_stories():
    name = request.form.get("name")  # 클라이언트로부터 name 값을 받아옴

    user_id_response = get_user_id(name)
    user_id_json = user_id_response.json()

    user_id = user_id_json['id']
    time_gen = user_id_json['unrelated_data']['time_gen']

    url = "https://instagram-scraper-2022.p.rapidapi.com/ig/stories/"

    querystring = {"id_user":user_id}

    headers = {
        "X-RapidAPI-Key": "a6cc07d155mshef5faed51b433bbp11569ejsn9f5af6ece890",
        "X-RapidAPI-Host": "instagram-scraper-2022.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return Response(response.content, content_type=response.headers['Content-Type'])



@app.route('/get_user_reels',methods=['POST'])
def get_user_reels():
    name = request.form.get("name")  # 클라이언트로부터 name 값을 받아옴

    url = "https://instagram-scraper-2022.p.rapidapi.com/ig/reels_posts_username/"

    querystring = {"user":name}

    headers = {
        "X-RapidAPI-Key": "a6cc07d155mshef5faed51b433bbp11569ejsn9f5af6ece890",
        "X-RapidAPI-Host": "instagram-scraper-2022.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return Response(response.content, content_type=response.headers['Content-Type'])

@app.route('/get_user_post')
def download_media():
    #name = request.form.get("name")  # 클라이언트로부터 name 값을 받아옴
    name ="s_don.03"

    url = "https://instagram-scraper-2022.p.rapidapi.com/ig/posts_username/"

    querystring = {"user":name}

    headers = {
        "X-RapidAPI-Key": "a6cc07d155mshef5faed51b433bbp11569ejsn9f5af6ece890",
        "X-RapidAPI-Host": "instagram-scraper-2022.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return Response(response.content, content_type=response.headers['Content-Type'])

def get_user_id(name):
    url = "https://instagram-scraper-2022.p.rapidapi.com/ig/user_id/"

    querystring = {"user":"cr7cristianoronaldo"}

    headers = {
        "X-RapidAPI-Key": "a6cc07d155mshef5faed51b433bbp11569ejsn9f5af6ece890",
        "X-RapidAPI-Host": "instagram-scraper-2022.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())
    return Response(response.content, content_type=response.headers['Content-Type'])


if __name__ == "__main__":
    app.run('0.0.0.0',port=5000,debug=True)

    