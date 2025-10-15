import random
from datetime import datetime, timedelta

class OfferMart:
    def __init__(self):
        # Mock pre-approved loan offers
        self.pre_approved_offers = {
            '9876543210': {
                'customer_id': '9876543210',
                'pre_approved_amount': 800000,
                'interest_rate': 11.99,
                'tenure_options': [12, 24, 36, 48, 60],
                'offer_valid_until': datetime.now() + timedelta(days=30),
                'offer_type': 'Pre-approved',
                'special_conditions': 'No processing fee'
            },
            '9876543211': {
                'customer_id': '9876543211',
                'pre_approved_amount': 500000,
                'interest_rate': 12.99,
                'tenure_options': [12, 24, 36, 48],
                'offer_valid_until': datetime.now() + timedelta(days=45),
                'offer_type': 'Pre-approved',
                'special_conditions': 'Quick approval'
            },
            '9876543212': {
                'customer_id': '9876543212',
                'pre_approved_amount': 1200000,
                'interest_rate': 11.49,
                'tenure_options': [12, 24, 36, 48, 60],
                'offer_valid_until': datetime.now() + timedelta(days=60),
                'offer_type': 'Pre-approved',
                'special_conditions': 'Premium customer rate'
            },
            '9876543213': {
                'customer_id': '9876543213',
                'pre_approved_amount': 300000,
                'interest_rate': 13.99,
                'tenure_options': [12, 24, 36],
                'offer_valid_until': datetime.now() + timedelta(days=15),
                'offer_type': 'Pre-approved',
                'special_conditions': 'Limited time offer'
            },
            '9876543214': {
                'customer_id': '9876543214',
                'pre_approved_amount': 600000,
                'interest_rate': 12.49,
                'tenure_options': [12, 24, 36, 48],
                'offer_valid_until': datetime.now() + timedelta(days=20),
                'offer_type': 'Pre-approved',
                'special_conditions': 'Existing customer rate'
            },
            '9876543215': {
                'customer_id': '9876543215',
                'pre_approved_amount': 700000,
                'interest_rate': 11.99,
                'tenure_options': [12, 24, 36, 48, 60],
                'offer_valid_until': datetime.now() + timedelta(days=40),
                'offer_type': 'Pre-approved',
                'special_conditions': 'New customer welcome offer'
            },
            '9876543216': {
                'customer_id': '9876543216',
                'pre_approved_amount': 1000000,
                'interest_rate': 10.99,
                'tenure_options': [12, 24, 36, 48, 60],
                'offer_valid_until': datetime.now() + timedelta(days=90),
                'offer_type': 'Pre-approved',
                'special_conditions': 'VIP customer rate'
            },
            '9876543217': {
                'customer_id': '9876543217',
                'pre_approved_amount': 900000,
                'interest_rate': 11.49,
                'tenure_options': [12, 24, 36, 48, 60],
                'offer_valid_until': datetime.now() + timedelta(days=35),
                'offer_type': 'Pre-approved',
                'special_conditions': 'Loyalty customer rate'
            },
            '9876543218': {
                'customer_id': '9876543218',
                'pre_approved_amount': 400000,
                'interest_rate': 12.99,
                'tenure_options': [12, 24, 36, 48],
                'offer_valid_until': datetime.now() + timedelta(days=25),
                'offer_type': 'Pre-approved',
                'special_conditions': 'Student loan rate'
            },
            '9876543219': {
                'customer_id': '9876543219',
                'pre_approved_amount': 1100000,
                'interest_rate': 11.24,
                'tenure_options': [12, 24, 36, 48, 60],
                'offer_valid_until': datetime.now() + timedelta(days=50),
                'offer_type': 'Pre-approved',
                'special_conditions': 'Business owner rate'
            }
        }
    
    def get_pre_approved_offer(self, customer_id):
        """Get pre-approved loan offer for customer"""
        if customer_id in self.pre_approved_offers:
            offer = self.pre_approved_offers[customer_id]
            # Check if offer is still valid
            if offer['offer_valid_until'] > datetime.now():
                return offer
            else:
                return None
        return None
    
    def calculate_loan_eligibility(self, customer_data, credit_score):
        """Calculate loan eligibility based on customer profile"""
        monthly_income = customer_data.get('monthly_income', 0)
        existing_emis = sum([loan['emi'] for loan in customer_data.get('current_loans', [])])
        
        # Calculate maximum EMI capacity (50% of income minus existing EMIs)
        max_emi_capacity = (monthly_income * 0.5) - existing_emis
        
        # Calculate maximum loan amount based on EMI capacity
        # Using 12% interest rate and 36 months tenure for calculation
        if max_emi_capacity > 0:
            max_loan_amount = self._calculate_loan_amount_from_emi(max_emi_capacity, 12.0, 36)
        else:
            max_loan_amount = 0
        
        # Adjust based on credit score
        if credit_score >= 750:
            eligibility_multiplier = 1.0
        elif credit_score >= 700:
            eligibility_multiplier = 0.8
        elif credit_score >= 650:
            eligibility_multiplier = 0.6
        else:
            eligibility_multiplier = 0.4
        
        max_loan_amount = max_loan_amount * eligibility_multiplier
        
        return {
            'eligible_amount': min(max_loan_amount, 4000000),  # Cap at 40 lakhs
            'max_emi_capacity': max_emi_capacity,
            'existing_emis': existing_emis,
            'eligibility_score': eligibility_multiplier
        }
    
    def _calculate_loan_amount_from_emi(self, emi, rate, tenure_months):
        """Calculate loan amount from EMI"""
        if rate == 0:
            return emi * tenure_months
        
        monthly_rate = rate / (12 * 100)
        loan_amount = (emi * ((1 + monthly_rate) ** tenure_months - 1)) / \
                     (monthly_rate * (1 + monthly_rate) ** tenure_months)
        return round(loan_amount, 2)
    
    def get_interest_rate(self, customer_data, credit_score, loan_amount):
        """Get interest rate based on customer profile and credit score"""
        base_rate = 10.99
        
        # Credit score adjustment
        if credit_score >= 800:
            rate_adjustment = -1.0
        elif credit_score >= 750:
            rate_adjustment = -0.5
        elif credit_score >= 700:
            rate_adjustment = 0.0
        elif credit_score >= 650:
            rate_adjustment = 0.5
        else:
            rate_adjustment = 1.5
        
        # Employment type adjustment
        employment = customer_data.get('employment', '').lower()
        if 'government' in employment or 'public sector' in employment:
            rate_adjustment -= 0.5
        elif 'salaried' in employment:
            rate_adjustment -= 0.25
        elif 'business' in employment or 'self-employed' in employment:
            rate_adjustment += 0.25
        
        # Income adjustment
        monthly_income = customer_data.get('monthly_income', 0)
        if monthly_income > 100000:
            rate_adjustment -= 0.25
        elif monthly_income < 30000:
            rate_adjustment += 0.5
        
        # Loan amount adjustment
        if loan_amount > 1000000:
            rate_adjustment -= 0.25  # Better rate for higher amounts
        elif loan_amount < 100000:
            rate_adjustment += 0.25  # Higher rate for smaller amounts
        
        final_rate = max(base_rate + rate_adjustment, 10.99)  # Minimum rate
        return round(final_rate, 2)
    
    def generate_loan_offer(self, customer_data, credit_score, requested_amount, tenure):
        """Generate comprehensive loan offer"""
        eligibility = self.calculate_loan_eligibility(customer_data, credit_score)
        interest_rate = self.get_interest_rate(customer_data, credit_score, requested_amount)
        
        # Calculate EMI
        monthly_rate = interest_rate / (12 * 100)
        emi = (requested_amount * monthly_rate * (1 + monthly_rate) ** tenure) / \
              ((1 + monthly_rate) ** tenure - 1)
        
        return {
            'approved_amount': min(requested_amount, eligibility['eligible_amount']),
            'interest_rate': interest_rate,
            'tenure': tenure,
            'emi': round(emi, 2),
            'total_amount': round(emi * tenure, 2),
            'total_interest': round((emi * tenure) - requested_amount, 2),
            'processing_fee': min(requested_amount * 0.02, 20000),  # 2% or max 20k
            'eligibility_details': eligibility,
            'offer_valid_until': datetime.now() + timedelta(days=7)
        }

