from flask import Flask, jsonify, request, abort, render_template
import api.service_client as client
from api.anime import get_anime

app = Flask("api-service", template_folder="../templates")


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/recommends/<int:user_id>")
def get_recommends(user_id):
    # 直接从URL路径获取user_id
    rec_anime_ids = client.get_anime(user_id)

    # 检查rec_anime_ids是否有效，如果无效则返回空列表
    if not rec_anime_ids:
        return jsonify([]), 200

    # 通过列表推导式获取推荐动画的详细信息
    res = [get_anime(id) for id in rec_anime_ids]

    # 创建JSON响应，并设置CORS头部
    response = jsonify(res)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


@app.route("/sim/<int:anime_id>")
def get_similar_animes(anime_id):
    # 检查anime_id是否有效
    if anime_id is None:
        return 'bad anime id', 400
    # 直接从URL路径获取anime_id
    sim_anime_ids = client.get_similar_anime(anime_id)

    # 检查sim_anime_ids是否有效，如果无效则返回空列表
    if not sim_anime_ids:
        return jsonify([]), 200

    # 通过列表推导式获取相似动画的详细信息
    res = [get_anime(id) for id in sim_anime_ids]

    # 创建JSON响应，并设置CORS头部
    response = jsonify(res)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


@app.route("/anime/<int:anime_id>")
def anime_detail(anime_id):
    # 检查anime_id是否有效
    if anime_id is None:
        return 'bad anime id', 400

    anime = get_anime(anime_id)
    if anime is None:
        abort(404)  # 如果没有找到对应的动漫，返回404 Not Found

    response = jsonify(anime)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)
