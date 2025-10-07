from flask import Flask, render_template

from endpoints.cnn_bp import cnn_bp
from endpoints.fnn_bp import fnn_bp
from endpoints.rnn_bp import rnn_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'uma-chave-secreta'

app.register_blueprint(cnn_bp, url_prefix='/cnn')
app.register_blueprint(fnn_bp, url_prefix='/fnn')
app.register_blueprint(rnn_bp, url_prefix='/rnn')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)