from flask import Flask, render_template, request, jsonify
from brain import SerraBrain  # Inasoma ubongo wako uleule
import os

app = Flask(__name__)
serra = SerraBrain()

@app.route('/')
def home():
    # Hapa inatafuta folder la 'templates' na file la 'index.html'
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_query = data.get('query')
    # Inachukua jibu kutoka kwenye Brain yako
    response = serra.get_ai_reply(user_query)
    return jsonify({'reply': response})

if __name__ == '__main__':
    app.run(debug=True)
