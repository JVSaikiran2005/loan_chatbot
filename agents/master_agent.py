import json
import re
from datetime import datetime
from typing import Any, Dict, Optional


class MasterAgent:
    def __init__(self):
        self.conversation_state = "greeting"
        self.customer_info = {}
        self.loan_requirements = {}
        
    def process_message(
        self,
        user_message: str,
        session_id: str,
        conversation_data: Dict[str, Any],
        sales_agent,
        verification_agent,
        underwriting_agent,
        sanction_generator,
        ml_model: Optional[Any] = None,
    ):
        """
        Main orchestrator that manages the conversation flow and coordinates worker agents
        """
        user_message = user_message.lower().strip()
        
        # Determine current state and next action
        if conversation_data['status'] == 'initial':
            return self._handle_initial_contact(user_message, conversation_data)
        
        elif conversation_data['status'] == 'sales':
            return self._handle_sales_phase(user_message, conversation_data, sales_agent)
        
        elif conversation_data['status'] == 'verification':
            return self._handle_verification_phase(user_message, conversation_data, verification_agent)
        
        elif conversation_data['status'] == 'underwriting':
            return self._handle_underwriting_phase(user_message, conversation_data, underwriting_agent)
        
        elif conversation_data['status'] == 'sanction':
            return self._handle_sanction_phase(user_message, conversation_data, sanction_generator)
        
        elif conversation_data['status'] == 'completed':
            return self._handle_completion(user_message, conversation_data)
        
        else:
            # Fallback: if an ML model is available, use it for a more
            # natural-language response instead of a fixed template.
            if ml_model is not None:
                generated = ml_model.generate_response(user_message, conversation_data)
                return {
                    "message": generated,
                    "requires_input": True,
                }
            return {
                "message": "I'm sorry, I didn't understand. Could you please rephrase?",
                "requires_input": True
            }
    
    def _handle_initial_contact(self, user_message, conversation_data):
        """Handle initial customer contact and greeting"""
        greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
        
        if any(greeting in user_message for greeting in greetings):
            conversation_data['status'] = 'sales'
            return {
                "message": "Hello! Welcome to Tata Capital's Personal Loan Assistant. I'm here to help you get the best personal loan offer tailored to your needs. I can help you with loan amounts up to ₹40 lakhs with competitive interest rates starting from 10.99% per annum. Would you like to explore our personal loan options?",
                "requires_input": True
            }
        elif 'loan' in user_message or 'personal loan' in user_message:
            conversation_data['status'] = 'sales'
            return {
                "message": "Great! I'd be happy to help you with a personal loan. Let me gather some information to provide you with the best offer. What's your name?",
                "requires_input": True,
                "input_type": "text"
            }
        else:
            return {
                "message": "Hello! I'm Tata Capital's Personal Loan Assistant. I can help you with personal loans up to ₹40 lakhs. Would you like to know more about our loan products?",
                "requires_input": True
            }
    
    def _handle_sales_phase(self, user_message, conversation_data, sales_agent):
        """Handle sales conversation and collect customer requirements"""
        if not conversation_data['customer_data'].get('name'):
            # Extract name from message
            name = self._extract_name(user_message)
            if name:
                conversation_data['customer_data']['name'] = name
                return sales_agent.get_loan_amount_inquiry(name)
            else:
                return {
                    "message": "Great! I'd be happy to help you with a personal loan. What is your full name, please?",
                    "requires_input": True,
                    "input_type": "text"
                }
        
        elif not conversation_data['customer_data'].get('phone'):
            # Extract phone number
            phone = self._extract_phone(user_message)
            if phone:
                conversation_data['customer_data']['phone'] = phone
                return sales_agent.get_loan_purpose_inquiry(conversation_data['customer_data']['name'])
            else:
                return {
                    "message": f"Thank you, {conversation_data['customer_data']['name']}. Please provide your 10-digit mobile number for verification.",
                    "requires_input": True,
                    "input_type": "phone"
                }
        
        elif not conversation_data['loan_details'].get('amount'):
            # Extract loan amount
            amount = self._extract_loan_amount(user_message)
            if amount:
                conversation_data['loan_details']['amount'] = amount
                return sales_agent.get_loan_tenure_inquiry(amount)
            else:
                return {
                    "message": "What loan amount are you looking for? (Please enter amount in rupees, e.g., 500000 for ₹5 lakhs)",
                    "requires_input": True,
                    "input_type": "number"
                }
        
        elif not conversation_data['loan_details'].get('tenure'):
            # Extract tenure
            tenure = self._extract_tenure(user_message)
            if tenure:
                conversation_data['loan_details']['tenure'] = tenure
                return sales_agent.get_employment_inquiry()
            else:
                return {
                    "message": "What loan tenure would you prefer? (Please enter in months, e.g., 24 for 2 years)",
                    "requires_input": True,
                    "input_type": "number"
                }
        
        elif not conversation_data['customer_data'].get('employment'):
            conversation_data['customer_data']['employment'] = user_message
            return sales_agent.get_monthly_income_inquiry()
        
        elif not conversation_data['customer_data'].get('monthly_income'):
            income = self._extract_income(user_message)
            if income:
                conversation_data['customer_data']['monthly_income'] = income
                # Move to verification phase
                conversation_data['status'] = 'verification'
                return {
                    "message": f"Perfect! Thank you for providing your details, {conversation_data['customer_data']['name']}. Now I'll verify your information and check your eligibility. This will take just a moment.",
                    "requires_input": False
                }
            else:
                return {
                    "message": "Please enter your monthly income in rupees (e.g., 50000)",
                    "requires_input": True,
                    "input_type": "number"
                }
        
        # Fallback response in case of unexpected state
        return {
            "message": "I'm here to help! Could you please provide the information I'm requesting?",
            "requires_input": True
        }
    
    def _handle_verification_phase(self, user_message, conversation_data, verification_agent):
        """Handle KYC verification"""
        if not conversation_data['verification_status']:
            # Start verification process
            verification_result = verification_agent.verify_customer(conversation_data['customer_data'])
            
            if verification_result['verified']:
                conversation_data['verification_status'] = True
                conversation_data['status'] = 'underwriting'
                return {
                    "message": f"✅ Verification successful! Your details have been confirmed. Now I'll check your credit score and loan eligibility. This process typically takes 2-3 minutes.",
                    "requires_input": False
                }
            else:
                return {
                    "message": f"❌ Verification failed: {verification_result['reason']}. Please contact our customer service at 1800-209-8808 for assistance.",
                    "requires_input": False
                }
    
    def _handle_underwriting_phase(self, user_message, conversation_data, underwriting_agent):
        """Handle credit evaluation and underwriting"""
        if not conversation_data['underwriting_status']:
            # Start underwriting process
            underwriting_result = underwriting_agent.evaluate_loan(
                conversation_data['customer_data'],
                conversation_data['loan_details']
            )
            
            conversation_data['underwriting_result'] = underwriting_result
            
            if underwriting_result['approved']:
                conversation_data['underwriting_status'] = True
                conversation_data['status'] = 'sanction'
                return {
                    "message": f"🎉 Congratulations! Your loan application has been approved! Loan Amount: ₹{conversation_data['loan_details']['amount']:,}, Interest Rate: {underwriting_result['interest_rate']}% p.a., EMI: ₹{underwriting_result['emi']:,} for {conversation_data['loan_details']['tenure']} months. I'll now generate your sanction letter.",
                    "requires_input": False
                }
            else:
                return {
                    "message": f"❌ Unfortunately, your loan application has been declined. Reason: {underwriting_result['reason']}. You can reapply after 6 months or contact our customer service for alternative options.",
                    "requires_input": False
                }
    
    def _handle_sanction_phase(self, user_message, conversation_data, sanction_generator):
        """Handle sanction letter generation"""
        if not conversation_data.get('sanction_letter'):
            # Generate sanction letter
            sanction_letter_path = sanction_generator.generate_sanction_letter(
                conversation_data['customer_data'],
                conversation_data['loan_details'],
                conversation_data['underwriting_result']
            )
            
            conversation_data['sanction_letter'] = sanction_letter_path
            conversation_data['status'] = 'completed'
            
            return {
                "message": f"✅ Your sanction letter has been generated successfully! You can download it using the link below. Your loan will be disbursed within 24-48 hours after document verification. Thank you for choosing Tata Capital!",
                "requires_input": False
            }
    
    def _handle_completion(self, user_message, conversation_data):
        """Handle post-completion interactions"""
        if 'thank' in user_message or 'thanks' in user_message:
            return {
                "message": "You're welcome! If you have any questions about your loan or need assistance in the future, feel free to contact us. Have a great day!",
                "requires_input": False
            }
        else:
            return {
                "message": "Is there anything else I can help you with regarding your loan or other Tata Capital services?",
                "requires_input": True
            }
    
    def _extract_name(self, text):
        """Extract name from user input"""
        # Simple name extraction - look for capitalized words
        words = text.split()
        name_words = []
        for word in words:
            # Remove punctuation and check if word starts with uppercase
            clean_word = word.strip('.,!?;:\'"')
            if clean_word and clean_word[0].isupper() and len(clean_word) > 1:
                name_words.append(clean_word)
        
        if name_words:
            return ' '.join(name_words)
        return None
    
    def _extract_phone(self, text):
        """Extract phone number from user input"""
        # Extract 10-digit phone number
        phone_match = re.search(r'\b\d{10}\b', text)
        if phone_match:
            return phone_match.group()
        return None
    
    def _extract_loan_amount(self, text):
        """Extract loan amount from user input"""
        # Extract numbers that could be loan amounts
        numbers = re.findall(r'\d+', text)
        for num in numbers:
            amount = int(num)
            if 10000 <= amount <= 4000000:  # Reasonable loan amount range
                return amount
        return None
    
    def _extract_tenure(self, text):
        """Extract loan tenure from user input"""
        numbers = re.findall(r'\d+', text)
        for num in numbers:
            tenure = int(num)
            if 6 <= tenure <= 60:  # 6 months to 5 years
                return tenure
        return None
    
    def _extract_income(self, text):
        """Extract monthly income from user input"""
        numbers = re.findall(r'\d+', text)
        for num in numbers:
            income = int(num)
            if 10000 <= income <= 1000000:  # Reasonable income range
                return income
        return None

