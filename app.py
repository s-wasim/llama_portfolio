from flask import Flask, request, jsonify
from flask_cors import CORS
from commons.index import Index
import logging
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Index instance
try:
    chat_index = Index('load', 'storage')
    logger.info("Index initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Index: {str(e)}")
    raise

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "portfolio-chat-api"})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint that processes messages"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                "error": "Invalid request",
                "message": "Message field is required"
            }), 400

        message = data['message'].strip()
        response = chat_index(message)
        
        return jsonify({
            "status": "success",
            "response": response
        })

    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500
    
if __name__ == '__main__':
    app.run(host=os.environ.get('API_HOST_URL'), port=os.environ.get('API_PORT'))
