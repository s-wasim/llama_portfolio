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
                companies = []
                current_company = None
                current_project = None
                
                lines = content.split('\n')
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    
                    # Parse company info
                    if line and not line.startswith('PROJECT'):
                        if '[' in line:
                            company_parts = line.split('[')
                            company_name = company_parts[0].strip()
                            role = company_parts[1].rstrip(']').strip()
                            current_company = {
                                'name': company_name,
                                'role': role,
                                'projects': []
                            }
                            companies.append(current_company)
                    
                    # Parse project info
                    elif line.startswith('PROJECT NAME:'):
                        project_name = line.replace('PROJECT NAME:', '').strip()
                        current_project = {
                            'name': project_name,
                            'details': [],
                            'tools': []
                        }
                        current_company['projects'].append(current_project)
                    
                    # Parse project details
                    elif line.startswith('PROJECT DETAILS:'):
                        i += 1
                        while i < len(lines) and not lines[i].strip().startswith('PROJECT'):
                            detail = lines[i].strip()
                            if detail and not detail.startswith('PROJECT'):
                                current_project['details'].append(detail)
                            i += 1
                        i -= 1
                        
                    # Parse project tools
                    elif line.startswith('PROJECT TOOLS:'):
                        tools = line.replace('PROJECT TOOLS:', '').strip()
                        if tools:
                            current_project['tools'] = [t.strip() for t in tools.split(',')]
                    
                    i += 1
                
                return jsonify(companies)
                
        except Exception as e:
            logger.error(f"Error parsing work history: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/education-details')
    def education_details():
        try:
            with open('portfolio_documents/Education_Details.txt', 'r') as file:
                content = file.read()
                schools = []
                
                lines = content.split('\n')
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    
                    if line.startswith('School:'):
                        school_name = line.replace('School:', '').strip()
                        location = lines[i + 1].replace('Location:', '').strip()
                        studied = lines[i + 2].replace('Studied:', '').strip()
                        grades = lines[i + 3].replace('Grades:', '').strip()
                        
                        school = {
                            'name': school_name,
                            'location': location,
                            'studied': studied,
                            'grades': grades
                        }
                        schools.append(school)
                    
                    i += 4
                
                return jsonify(schools)
                
        except Exception as e:
            logger.error(f"Error parsing education details: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/certification-details')
    def certification_details():
        try:
            with open('portfolio_documents/Certification_Details.txt', 'r') as file:
                content = file.read()
                certifications = []
                
                lines = content.split('\n')
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    
                    if line.startswith('Certification Name:'):
                        name = line.replace('Certification Name:', '').strip()
                        link = lines[i + 1].replace('Verification Link:', '').strip()
                        details = []
                        i += 2
                        while i < len(lines) and lines[i].strip():
                            details.append(lines[i])
                            i += 1
                        
                        certification = {
                            'name': name,
                            'link': link,
                            'details': '\n'.join(details)
                        }
                        certifications.append(certification)
                    
                    i += 1
                
                return jsonify(certifications)
                
        except Exception as e:
            logger.error(f"Error parsing certification details: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/courses-studied')
    def courses_studied():
        try:
            with open('portfolio_documents/Courses_Studied.txt', 'r') as file:
                content = file.read()
                courses = []
                
                lines = content.split('\n')
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    
                    if line and not line.startswith('1)'):
                        course_name = line
                        link = lines[i + 1].replace('Link to Achievement:', '').strip()
                        libraries = ''
                        i += 2
                        while i < len(lines) and lines[i].strip():
                            if lines[i].startswith('Libraries Used:'):
                                libraries = lines[i].replace('Libraries Used:', '').strip()
                            i += 1
                        
                        course = {
                            'name': course_name,
                            'link': link,
                            'libraries': libraries
                        }
                        courses.append(course)
                    
                    i += 1
                
                return jsonify(courses)
                
        except Exception as e:
            logger.error(f"Error parsing courses studied: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory('static', 'favicon.ico')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
