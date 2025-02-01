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

    @app.route('/work-history')
    def work_history():
        try:
            with open('portfolio_documents/Work_History.txt', 'r') as file:
                content = file.read()
                # Parse the content into structured data
                companies = []
                current_company = None
                current_project = None
                
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('    •'):
                        # This is a company line
                        if ' [' in line:
                            company_name, role = line.split(' [')
                            role = role.rstrip(']')
                            current_company = {
                                'name': company_name,
                                'role': role,
                                'projects': []
                            }
                            companies.append(current_company)
                    elif line.startswith('    •'):
                        # This is a project
                        project_name = line.lstrip('    • ')
                        current_project = {
                            'name': project_name,
                            'details': []
                        }
                        current_company['projects'].append(current_project)
                    elif line.startswith('    ') and current_project:
                        # This is a project detail
                        current_project['details'].append(line.strip())
                
                return jsonify(companies)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory('static', 'favicon.ico')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
