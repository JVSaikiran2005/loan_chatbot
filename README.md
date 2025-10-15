# Tata Capital Personal Loan Chatbot

An AI-driven conversational loan assistant that simulates a human-like sales process for personal loans. The system uses a Master Agent to orchestrate multiple Worker AI agents to handle the complete loan process from conversation to sanction letter generation.

## Features

### 🤖 AI Agent Architecture
- **Master Agent**: Main orchestrator managing conversation flow and coordinating worker agents
- **Sales Agent**: Handles loan negotiation, terms discussion, and customer engagement
- **Verification Agent**: Verifies KYC details from CRM server
- **Underwriting Agent**: Evaluates credit scores and loan eligibility
- **Sanction Letter Generator**: Creates automated PDF sanction letters

### 💼 Loan Processing Capabilities
- Personal loans up to ₹40 lakhs
- Interest rates starting from 10.99% per annum
- Tenure options from 6 to 60 months
- Real-time credit score evaluation
- Pre-approved loan limit checking
- Salary slip verification for higher amounts
- Automated EMI calculations

### 🎯 Customer Experience
- Natural conversation flow
- Real-time loan information updates
- File upload for salary slips
- Instant sanction letter generation
- Responsive web interface
- Mobile-friendly design

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **PDF Generation**: ReportLab
- **Styling**: Custom CSS with modern design
- **Icons**: Font Awesome

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd loan-chat-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
loan-chat-bot/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                      # Project documentation
├── agents/                        # AI Agent implementations
│   ├── __init__.py
│   ├── master_agent.py           # Main orchestrator
│   ├── sales_agent.py            # Sales and negotiation
│   ├── verification_agent.py     # KYC verification
│   ├── underwriting_agent.py     # Credit evaluation
│   └── sanction_letter_generator.py # PDF generation
├── mock_apis/                     # Mock external services
│   ├── __init__.py
│   ├── crm_server.py            # Customer data
│   ├── credit_bureau.py         # Credit scores
│   └── offer_mart.py            # Pre-approved offers
├── templates/                     # HTML templates
│   └── index.html               # Main chat interface
├── static/                       # Static assets
│   ├── css/
│   │   └── style.css           # Styling
│   └── js/
│       └── chat.js             # Frontend logic
├── uploads/                      # File upload directory
└── sanction_letters/            # Generated PDFs
```

## Usage

### Starting a Loan Application

1. **Initial Contact**: The chatbot greets customers and introduces loan products
2. **Information Collection**: Gathers customer details (name, phone, loan amount, tenure, income)
3. **Verification**: Verifies customer details against CRM database
4. **Underwriting**: Evaluates credit score and loan eligibility
5. **Document Generation**: Creates sanction letter if approved

### Sample Customer Data

The system includes 10 dummy customers with complete profiles:
- Rajesh Kumar (Phone: 9876543210) - Pre-approved: ₹8,00,000
- Priya Sharma (Phone: 9876543211) - Pre-approved: ₹5,00,000
- Amit Patel (Phone: 9876543212) - Pre-approved: ₹12,00,000
- And 7 more customers with varying credit profiles

### Loan Approval Logic

1. **Credit Score Check**: Minimum 700 required
2. **Pre-approved Limit**: Instant approval if within limit
3. **Extended Limit**: Up to 2x pre-approved limit with salary slip
4. **EMI Capacity**: Maximum 50% of monthly income
5. **Income Verification**: Salary slip required for higher amounts

## API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat` - Send message to chatbot
- `POST /api/upload` - Upload salary slip
- `GET /api/download/<session_id>` - Download sanction letter
- `GET /api/customers` - View dummy customer data

## Configuration

### Loan Parameters
- Minimum loan amount: ₹50,000
- Maximum loan amount: ₹40,00,000
- Minimum tenure: 6 months
- Maximum tenure: 60 months
- Base interest rate: 10.99%

### Credit Evaluation
- Minimum credit score: 700
- Pre-approved limit multiplier: 2x
- Maximum EMI to income ratio: 50%

## Testing

### Sample Conversation Flow

1. **Customer**: "Hi, I need a personal loan"
2. **Bot**: "Great! What's your name?"
3. **Customer**: "Rajesh Kumar"
4. **Bot**: "Nice to meet you, Rajesh! What loan amount are you looking for?"
5. **Customer**: "500000"
6. **Bot**: "What's your 10-digit mobile number?"
7. **Customer**: "9876543210"
8. **Bot**: "What loan tenure would you prefer?"
9. **Customer**: "24"
10. **Bot**: "What's your monthly income?"
11. **Customer**: "75000"
12. **Bot**: "✅ Verification successful! Your loan has been approved..."

## Features in Detail

### Master Agent
- Manages conversation state and flow
- Coordinates between worker agents
- Handles user input processing
- Maintains session data

### Sales Agent
- Engages customers with personalized messages
- Negotiates loan terms and conditions
- Calculates EMI and interest rates
- Provides loan product information

### Verification Agent
- Cross-verifies customer information
- Checks KYC compliance
- Validates document uploads
- Maintains verification status

### Underwriting Agent
- Fetches credit scores from bureau
- Evaluates loan eligibility
- Applies business rules
- Generates approval/rejection decisions

### Sanction Letter Generator
- Creates professional PDF documents
- Includes all loan terms and conditions
- Generates unique loan references
- Provides download functionality

## Future Enhancements

- Integration with real banking APIs
- Advanced document verification using OCR
- Machine learning for better conversation flow
- Multi-language support
- Voice interface integration
- Real-time loan status tracking

## Support

For technical support or questions:
- Email: support@tatacapital.com
- Phone: 1800-209-8808
- Website: www.tatacapital.com

## License

This project is developed for Tata Capital's BFSI challenge demonstration purposes.

