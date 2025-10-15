# Tata Capital Personal Loan Chatbot
## AI-Driven Conversational Loan Assistant

---

## Slide 1: Executive Summary

### 🎯 **Solution Overview**
- **AI-Powered Loan Assistant** for Tata Capital's personal loan sales
- **Master Agent** orchestrates multiple Worker AI agents
- **End-to-End Process**: From initial chat to sanction letter generation
- **Human-like Sales Experience** with personalized customer engagement

### 📊 **Key Metrics**
- **Loan Amount Range**: ₹50,000 - ₹40,00,000
- **Interest Rates**: Starting from 10.99% p.a.
- **Processing Time**: 24-48 hours
- **Customer Data**: 10+ dummy profiles with complete KYC

### 🏆 **Business Impact**
- Improved sales success rate through AI-driven conversations
- Automated loan processing and approval workflow
- Enhanced customer experience with instant responses
- Reduced manual intervention in loan processing

---

## Slide 2: AI Agent Architecture

### 🤖 **Master Agent (Main Orchestrator)**
- **Role**: Manages conversation flow and coordinates workflow
- **Responsibilities**:
  - Handles customer conversations
  - Transitions between different phases
  - Coordinates Worker Agents
  - Maintains session state

### 👥 **Worker AI Agents**

#### 1. **Sales Agent**
- Negotiates loan terms and conditions
- Discusses customer needs, amount, tenure, and interest rates
- Provides personalized loan offers
- Handles customer objections and queries

#### 2. **Verification Agent**
- Confirms KYC details from dummy CRM server
- Cross-verifies customer information
- Validates document uploads
- Maintains verification status

#### 3. **Underwriting Agent**
- Fetches credit scores from mock credit bureau API
- Validates loan eligibility based on business rules
- Applies approval/rejection logic
- Generates loan offers

#### 4. **Sanction Letter Generator**
- Creates automated PDF sanction letters
- Includes all loan terms and conditions
- Generates unique loan references
- Provides download functionality

---

## Slide 3: End-to-End Customer Journey

### 📱 **Phase 1: Initial Contact & Sales**
1. **Customer lands** on web chatbot via digital ads/emails
2. **Master Agent greets** and introduces loan products
3. **Sales Agent engages** in personalized conversation
4. **Information Collection**:
   - Customer name and contact details
   - Loan amount and tenure requirements
   - Monthly income and employment status
   - Loan purpose and preferences

### 🔍 **Phase 2: Verification & KYC**
1. **Verification Agent** checks customer details against CRM
2. **Cross-verification** of provided information
3. **KYC compliance** validation
4. **Document verification** (if required)

### 💳 **Phase 3: Credit Evaluation & Underwriting**
1. **Credit Bureau API** fetches credit scores
2. **Eligibility validation** based on business rules:
   - Credit score ≥ 700
   - Loan amount ≤ pre-approved limit (instant approval)
   - Loan amount ≤ 2× pre-approved limit (with salary slip)
   - EMI ≤ 50% of monthly income
3. **Risk assessment** and approval decision

### 📄 **Phase 4: Sanction Letter Generation**
1. **Automated PDF creation** with loan terms
2. **Professional document** with all conditions
3. **Instant download** capability
4. **Loan disbursement** within 24-48 hours

---

## Slide 4: Technical Implementation

### 🛠 **Technology Stack**
- **Backend**: Python Flask framework
- **Frontend**: HTML5, CSS3, JavaScript
- **PDF Generation**: ReportLab library
- **Styling**: Modern responsive design
- **APIs**: RESTful endpoints for all operations

### 🏗 **System Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │   Master Agent  │    │  Worker Agents  │
│   (HTML/CSS/JS) │◄──►│  (Orchestrator) │◄──►│  (Sales/Verify/ │
└─────────────────┘    └─────────────────┘    │  Underwrite/    │
                                              │  Sanction)      │
┌─────────────────┐    ┌─────────────────┐    └─────────────────┘
│   Mock APIs     │    │   Data Storage  │
│   (CRM/Credit/  │◄──►│   (Session/     │
│   Offer Mart)   │    │    Customer)    │
└─────────────────┘    └─────────────────┘
```

### 📊 **Mock Data & APIs**
- **CRM Server**: 10 dummy customers with complete profiles
- **Credit Bureau**: Credit scores and history data
- **Offer Mart**: Pre-approved loan limits and rates
- **File Upload**: Salary slip verification system

---

## Slide 5: Business Rules & Loan Logic

### 💰 **Loan Approval Criteria**

#### **Instant Approval**
- Credit score ≥ 700
- Loan amount ≤ pre-approved limit
- Valid KYC verification

#### **Conditional Approval**
- Loan amount ≤ 2× pre-approved limit
- Salary slip upload required
- EMI ≤ 50% of monthly income

#### **Rejection Criteria**
- Credit score < 700
- Loan amount > 2× pre-approved limit
- EMI > 50% of monthly income
- Invalid KYC information

### 📈 **Interest Rate Calculation**
- **Base Rate**: 10.99% per annum
- **Credit Score Adjustment**: -1.0% to +1.5%
- **Employment Type**: Government (-0.5%), Salaried (-0.25%), Business (+0.25%)
- **Income Level**: High income (-0.25%), Low income (+0.5%)
- **Loan Amount**: High amount (-0.25%), Small amount (+0.25%)

### 🎯 **Sample Customer Profiles**
- **Rajesh Kumar**: ₹8,00,000 pre-approved, Credit Score: 780
- **Priya Sharma**: ₹5,00,000 pre-approved, Credit Score: 720
- **Amit Patel**: ₹12,00,000 pre-approved, Credit Score: 750
- **7 more customers** with varying credit profiles

---

## 🚀 **Demo & Next Steps**

### 🎬 **Live Demonstration**
- **Web Interface**: http://localhost:5000
- **Complete Customer Journey**: From greeting to sanction letter
- **Real-time Processing**: All agents working in coordination
- **File Upload**: Salary slip verification
- **PDF Generation**: Automated sanction letter creation

### 🔮 **Future Enhancements**
- **Real Banking APIs**: Integration with actual systems
- **OCR Technology**: Advanced document verification
- **Machine Learning**: Improved conversation flow
- **Multi-language Support**: Regional language capabilities
- **Voice Interface**: Speech-to-text integration
- **Mobile App**: Native mobile application

### 📞 **Contact Information**
- **Customer Service**: 1800-209-8808
- **Email**: customer.service@tatacapital.com
- **Website**: www.tatacapital.com

---

## Thank You!

### **Questions & Discussion**

*Ready to revolutionize personal loan sales with AI-driven conversations!*

