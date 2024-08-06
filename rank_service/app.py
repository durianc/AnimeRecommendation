from flask import Flask, jsonify, request
from service import rank
from context import Context

app = Flask('rank-service')


@app.route('/rank/<int:user_id>')
def get_ranked_anime(user_id):
    context = Context(user_id)
    return jsonify(rank.anime_rank(context, 20))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
