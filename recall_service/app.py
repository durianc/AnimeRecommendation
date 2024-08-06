from flask import Flask, jsonify, request
from recall.context import Context
import service.recall_service_logic as recall_service_logic


app = Flask('recall-service')


@app.route("/recall/<int:user_id>")
def get_anime(user_id):
    print(f"Calling user {user_id}...")
    context = Context(user_id)
    res = recall_service_logic.anime_recall(context)
    return jsonify(res)


@app.route("/sim/<int:anime_id>")
def get_sim_anime(anime_id):
    if anime_id is None:
        return 'Bad anime id!', 400

    context = Context(None, anime_id)
    res = recall_service_logic.similar_animes(context)
    return jsonify(res)


if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=5001, debug=True)
