from flask import Flask, render_template, request, jsonify, send_from_directory
from commons.index import Index

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    index = Index('load', 'storage')

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/chat', methods=['POST'])
    def chat():
        mssg = request.form['mssg']
        response = index(mssg=mssg)
        return jsonify({'response': response.response})

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory('static', 'favicon.ico')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
