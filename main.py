from flask import Flask, request, jsonify, render_template
from commons.index import Index
"""
app = Flask(__name__)
index = Index('init', 'portfolio_documents')

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/query")
def query_portfolio():
    question = request.args.get('question', '')
    response = index(question)
    return jsonify({"response": response})
"""
def main():
    index = Index('init', 'portfolio_documents')
    send_msg = ''
    while True:
        send_msg = input('Enter your message: ')
        if send_msg == '/exit':
            print('Bye bye')
            break
        resp = index(send_msg)
        print(resp.response)
    
if __name__ == '__main__':

    main()
    