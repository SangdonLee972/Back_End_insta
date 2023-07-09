from flask import Flask, jsonify, request
import instaloader
from instaloader import Profile, Post



app = Flask("instaloader")
@app.route("/imageDownload")
def download_media():
    # 클라이언트로부터 name 값을 받아옴
    #name = request.form.get("name")
    name = "s_don.03"
    # Instaloader 인스턴스 생성
    # Instaloader 인스턴스 생성
    loader = instaloader.Instaloader()

    # 특정 계정의 피드 가져오기
    profile = instaloader.Profile.from_username(loader.context, name)
    feed = profile.get_posts()

    # 이미지와 영상 URL 추출
    media_urls = []
    video_urls = []
    print("sex")
    for post in feed:           
        if post.is_video:
            video_urls.append(post.video_url)
        else:
            media_urls.append(post.url)

    response = {
        "media_urls": media_urls,
        "video_urls": video_urls
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run('0.0.0.0',port=5000,debug=True)

    