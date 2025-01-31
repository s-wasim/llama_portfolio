from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os
from typing import Dict
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__, instance_relative_config=True)

class PortfolioAPIClient:
    def __init__(
        self, 
        host: str = "localhost", 
        port: int = 5000, 
        protocol: str = "http",
        timeout: int = 30
    ):
        """
        Initialize the Portfolio API client
        
        Args:
            host: API host address (default: localhost)
            port: API port (default: 5000)
            protocol: http or https (default: http)
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = f"{protocol}://{host}:{port}"
        self.timeout = timeout
    
    def health_check(self) -> Dict:
        """Check if the API is healthy"""
        response = self.session.get(
            f"{self.base_url}/health",
            timeout=self.timeout
        )
        return response.json()
    
    def chat(self, message: str) -> Dict:
        """Send a chat message and get response"""
        payload = {"message": message}
        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=self.timeout
        )
        return response.json()

def create_app():
    load_dotenv()
    client = PortfolioAPIClient(
        os.environ.get('API_HOST_URL'),
        os.environ.get('API_PORT'),
        os.environ.get('API_PROTOCOL')
    )

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/chat', methods=['POST'])
    def chat():
        mssg = request.form['mssg'].strip()
        response = client.chat(mssg)
        return jsonify(response)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory('static', 'favicon.ico')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
