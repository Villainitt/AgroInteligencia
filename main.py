from flask import Flask, render_template

from endpoints.cnn_bp import cnn_bp
from endpoints.fnn_bp import fnn_bp 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil-de-adivinhar'

app.register_blueprint(cnn_bp)
app.register_blueprint(fnn_bp)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)