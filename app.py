from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid

# Import our AI agents
from agents.master_agent import MasterAgent
from agents.sales_agent import SalesAgent
from agents.verification_agent import VerificationAgent
from agents.underwriting_agent import UnderwritingAgent
from agents.sanction_letter_generator import SanctionLetterGenerator
from agents.ml_model import LoanChatModel
from agents.cloud_storage import CloudStorage
from agents.manager_notify import ManagerNotifier

# Import mock APIs
from mock_apis.crm_server import CRMServer
from mock_apis.credit_bureau import CreditBureau
from mock_apis.offer_mart import OfferMart

app = Flask(__name__)
CORS(app)

# Initialize mock servers
crm_server = CRMServer()
credit_bureau = CreditBureau()
offer_mart = OfferMart()

# Initialize AI agents
master_agent = MasterAgent()
sales_agent = SalesAgent()
verification_agent = VerificationAgent(crm_server)
underwriting_agent = UnderwritingAgent(credit_bureau, offer_mart)
sanction_generator = SanctionLetterGenerator()

# Initialize Hugging Face-based ML model for fallback conversational responses
ml_model = LoanChatModel()

# Initialize local cloud storage and manager notifier
cloud_storage = CloudStorage()
manager_notifier = ManagerNotifier(cloud_storage)

# Store active conversations
active_conversations = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', str(uuid.uuid4()))
    
    # Initialize conversation if new session
    if session_id not in active_conversations:
        active_conversations[session_id] = {
            'status': 'initial',
            'customer_data': {},
            'loan_details': {},
            'verification_status': False,
            'underwriting_status': False,
            'sanction_letter': None
        }
        # keep session id inside conversation data for easier packaging
        active_conversations[session_id]['session_id'] = session_id
    
    # Get response from Master Agent
    response = master_agent.process_message(
        user_message,
        session_id,
        active_conversations[session_id],
        sales_agent,
        verification_agent,
        underwriting_agent,
        sanction_generator,
        ml_model=ml_model,
    )
    
    return jsonify({
        'response': response['message'],
        'session_id': session_id,
        'status': active_conversations[session_id]['status'],
        'requires_input': response.get('requires_input', False),
        'input_type': response.get('input_type', None)
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    session_id = request.form.get('session_id')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save to local cloud storage (simulated)
    saved_path = cloud_storage.save_file(file.stream, file.filename, metadata={'session_id': session_id})

    # Update conversation status and record saved filename
    if session_id in active_conversations:
        active_conversations[session_id]['salary_slip_uploaded'] = True
        active_conversations[session_id].setdefault('uploaded_files', []).append(saved_path)

    return jsonify({
        'message': 'File uploaded successfully',
        'filename': os.path.basename(saved_path),
        'saved_path': saved_path
    })

@app.route('/api/download/<session_id>')
def download_sanction_letter(session_id):
    if session_id not in active_conversations:
        return jsonify({'error': 'Session not found'}), 404
    
    conversation = active_conversations[session_id]
    if not conversation.get('sanction_letter'):
        return jsonify({'error': 'No sanction letter available'}), 404

    # Serve the sanction letter file
    return send_file(conversation['sanction_letter'], as_attachment=True)

@app.route('/api/customers')
def get_customers():
    """API endpoint to view dummy customer data"""
    return jsonify(crm_server.get_all_customers())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

