import random

class SalesAgent:
    def __init__(self):
        self.loan_products = {
            'personal_loan': {
                'min_amount': 50000,
                'max_amount': 4000000,
                'min_tenure': 6,
                'max_tenure': 60,
                'base_rate': 10.99
            }
        }
        
    def get_loan_amount_inquiry(self, customer_name):
        """Ask for loan amount requirement"""
        messages = [
            f"Nice to meet you, {customer_name}! I can help you with a personal loan ranging from ₹50,000 to ₹40,00,000. What loan amount are you looking for?",
            f"Hello {customer_name}! Our personal loans start from ₹50,000 and go up to ₹40,00,000. How much would you like to borrow?",
            f"Hi {customer_name}! What loan amount do you need? We offer personal loans from ₹50,000 to ₹40,00,000 with competitive rates."
        ]
        return {
            "message": random.choice(messages),
            "requires_input": True,
            "input_type": "number"
        }
    
    def get_loan_purpose_inquiry(self, customer_name):
        """Ask for loan purpose"""
        purposes = [
            "What's the purpose of this loan? (e.g., home renovation, medical emergency, wedding, education, debt consolidation, etc.)",
            "Could you tell me what you plan to use this loan for?",
            "What will you be using this personal loan for?"
        ]
        return {
            "message": random.choice(purposes),
            "requires_input": True,
            "input_type": "text"
        }
    
    def get_loan_tenure_inquiry(self, loan_amount):
        """Ask for loan tenure"""
        messages = [
            f"Great! For a loan amount of ₹{loan_amount:,}, you can choose a tenure between 6 to 60 months. What tenure would you prefer?",
            f"Excellent choice! ₹{loan_amount:,} is a good amount. How many months would you like to repay this loan? (6-60 months)",
            f"Perfect! For ₹{loan_amount:,}, what repayment period works best for you? (6-60 months)"
        ]
        return {
            "message": random.choice(messages),
            "requires_input": True,
            "input_type": "number"
        }
    
    def get_employment_inquiry(self):
        """Ask about employment status"""
        messages = [
            "What's your current employment status? (Salaried, Self-employed, Business owner, etc.)",
            "Are you currently employed? Please tell me about your employment status.",
            "What's your employment situation? (Salaried/Self-employed/Business owner)"
        ]
        return {
            "message": random.choice(messages),
            "requires_input": True,
            "input_type": "text"
        }
    
    def get_monthly_income_inquiry(self):
        """Ask for monthly income"""
        messages = [
            "What's your monthly income? This helps us determine your loan eligibility and EMI capacity.",
            "Could you share your monthly income details?",
            "What's your monthly take-home salary or income?"
        ]
        return {
            "message": random.choice(messages),
            "requires_input": True,
            "input_type": "number"
        }
    
    def calculate_emi(self, principal, rate, tenure_months):
        """Calculate EMI using standard formula"""
        if rate == 0:
            return principal / tenure_months
        
        monthly_rate = rate / (12 * 100)
        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
              ((1 + monthly_rate) ** tenure_months - 1)
        return round(emi, 2)
    
    def suggest_loan_terms(self, customer_data, loan_amount, tenure):
        """Suggest optimal loan terms based on customer profile"""
        base_rate = self.loan_products['personal_loan']['base_rate']
        
        # Adjust rate based on customer profile
        rate_adjustment = 0
        
        # Employment type adjustment
        if customer_data.get('employment', '').lower() in ['salaried', 'government employee']:
            rate_adjustment -= 0.5  # Better rate for salaried
        elif 'business' in customer_data.get('employment', '').lower():
            rate_adjustment += 0.5  # Higher rate for business owners
        
        # Income-based adjustment
        monthly_income = customer_data.get('monthly_income', 0)
        if monthly_income > 100000:
            rate_adjustment -= 0.25  # Better rate for high income
        elif monthly_income < 30000:
            rate_adjustment += 0.5   # Higher rate for low income
        
        final_rate = max(base_rate + rate_adjustment, 10.99)  # Minimum rate
        emi = self.calculate_emi(loan_amount, final_rate, tenure)
        
        return {
            'interest_rate': round(final_rate, 2),
            'emi': emi,
            'total_amount': round(emi * tenure, 2),
            'total_interest': round((emi * tenure) - loan_amount, 2)
        }
    
    def negotiate_terms(self, customer_data, initial_offer, customer_counter_offer=None):
        """Handle loan term negotiations"""
        if not customer_counter_offer:
            return {
                'message': f"Based on your profile, here's what I can offer:\n\n" +
                          f"Loan Amount: ₹{initial_offer['amount']:,}\n" +
                          f"Interest Rate: {initial_offer['interest_rate']}% p.a.\n" +
                          f"Tenure: {initial_offer['tenure']} months\n" +
                          f"EMI: ₹{initial_offer['emi']:,}\n\n" +
                          f"Does this work for you?",
                'offer': initial_offer
            }
        
        # Simple negotiation logic
        if customer_counter_offer.get('amount', 0) > initial_offer['amount']:
            return {
                'message': "I understand you'd like a higher amount. Let me check if we can accommodate that based on your income and credit profile.",
                'requires_underwriting': True
            }
        
        if customer_counter_offer.get('tenure', 0) > initial_offer['tenure']:
            return {
                'message': "A longer tenure will reduce your EMI but increase total interest. Let me recalculate with your preferred tenure.",
                'requires_recalculation': True
            }
        
        return {
            'message': "Thank you for your interest. Let me process your application with these terms.",
            'offer': customer_counter_offer
        }

