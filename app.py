from flask import Flask, jsonify
import user
app = Flask(__name__)

@app.route('/nome', methods=['GET'])
def getNome():
      dados = user.users
      return jsonify(dados["user"])

if __name__ == '__main__':
    app.run(debug=True)
