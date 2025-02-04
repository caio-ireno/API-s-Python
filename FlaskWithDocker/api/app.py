from flask import Flask, jsonify
import user
import os

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

@app.route("/")
def index():
    return "API"

@app.route('/nome', methods=['GET'])
def getNome():
      dados = user.users
      return jsonify(dados["user"])

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=port)
