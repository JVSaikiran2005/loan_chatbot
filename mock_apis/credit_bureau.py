import random
from datetime import datetime, timedelta

class CreditBureau:
    def __init__(self):
        # Mock credit bureau data
        self.credit_scores = {
            '9876543210': {
                'score': 780,
                'last_updated': datetime.now() - timedelta(days=15),
                'credit_history': 'Excellent',
                'payment_history': 'No defaults in last 24 months',
                'credit_utilization': 0.25,
                'credit_inquiries': 2
            },
            '9876543211': {
                'score': 720,
                'last_updated': datetime.now() - timedelta(days=30),
                'credit_history': 'Good',
                'payment_history': '1 late payment in last 12 months',
                'credit_utilization': 0.35,
                'credit_inquiries': 1
            },
            '9876543212': {
                'score': 750,
                'last_updated': datetime.now() - timedelta(days=20),
                'credit_history': 'Very Good',
                'payment_history': 'No defaults in last 18 months',
                'credit_utilization': 0.30,
                'credit_inquiries': 3
            },
            '9876543213': {
                'score': 680,
                'last_updated': datetime.now() - timedelta(days=45),
                'credit_history': 'Fair',
                'payment_history': '2 late payments in last 12 months',
                'credit_utilization': 0.45,
                'credit_inquiries': 4
            },
            '9876543214': {
                'score': 710,
                'last_updated': datetime.now() - timedelta(days=25),
                'credit_history': 'Good',
                'payment_history': 'No defaults in last 12 months',
                'credit_utilization': 0.40,
                'credit_inquiries': 2
            },
            '9876543215': {
                'score': 760,
                'last_updated': datetime.now() - timedelta(days=10),
                'credit_history': 'Very Good',
                'payment_history': 'No defaults in last 24 months',
                'credit_utilization': 0.20,
                'credit_inquiries': 1
            },
            '9876543216': {
                'score': 790,
                'last_updated': datetime.now() - timedelta(days=5),
                'credit_history': 'Excellent',
                'payment_history': 'No defaults in last 36 months',
                'credit_utilization': 0.15,
                'credit_inquiries': 1
            },
            '9876543217': {
                'score': 740,
                'last_updated': datetime.now() - timedelta(days=35),
                'credit_history': 'Good',
                'payment_history': 'No defaults in last 18 months',
                'credit_utilization': 0.30,
                'credit_inquiries': 2
            },
            '9876543218': {
                'score': 730,
                'last_updated': datetime.now() - timedelta(days=12),
                'credit_history': 'Good',
                'payment_history': 'No defaults in last 12 months',
                'credit_utilization': 0.35,
                'credit_inquiries': 3
            },
            '9876543219': {
                'score': 770,
                'last_updated': datetime.now() - timedelta(days=18),
                'credit_history': 'Very Good',
                'payment_history': 'No defaults in last 24 months',
                'credit_utilization': 0.25,
                'credit_inquiries': 1
            }
        }
        
        # Default credit score for unknown customers
        self.default_score = 650
    
    def get_credit_score(self, phone_number):
        """Fetch credit score from credit bureau"""
        if phone_number in self.credit_scores:
            return self.credit_scores[phone_number]
        else:
            # Generate a random score for new customers
            score = random.randint(600, 800)
            return {
                'score': score,
                'last_updated': datetime.now(),
                'credit_history': 'Limited' if score < 700 else 'Good',
                'payment_history': 'Limited credit history',
                'credit_utilization': random.uniform(0.2, 0.5),
                'credit_inquiries': random.randint(0, 3)
            }
    
    def get_credit_report(self, phone_number):
        """Get detailed credit report"""
        credit_data = self.get_credit_score(phone_number)
        
        # Add additional mock data
        credit_data.update({
            'active_accounts': random.randint(2, 8),
            'total_credit_limit': random.randint(200000, 2000000),
            'outstanding_balance': random.randint(50000, 800000),
            'oldest_account_age': random.randint(12, 120),  # months
            'recent_inquiries': random.randint(0, 5),
            'public_records': 0,  # No bankruptcies or liens
            'delinquent_accounts': 0 if credit_data['score'] > 700 else random.randint(0, 2)
        })
        
        return credit_data
    
    def calculate_credit_rating(self, score):
        """Convert numeric score to rating"""
        if score >= 800:
            return 'Excellent'
        elif score >= 750:
            return 'Very Good'
        elif score >= 700:
            return 'Good'
        elif score >= 650:
            return 'Fair'
        else:
            return 'Poor'
    
    def is_credit_worthy(self, score, loan_amount, monthly_income):
        """Determine if customer is credit worthy for given loan amount"""
        # Basic credit worthiness check
        if score < 600:
            return False, "Credit score too low"
        
        # Income to loan ratio check
        if loan_amount > monthly_income * 20:  # Loan amount should not exceed 20x monthly income
            return False, "Loan amount too high relative to income"
        
        return True, "Credit worthy"

