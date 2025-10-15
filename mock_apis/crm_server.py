import random
from datetime import datetime, timedelta

class CRMServer:
    def __init__(self):
        # Dummy customer data with KYC details
        self.customers = {
            '9876543210': {
                'name': 'Rajesh Kumar',
                'phone': '9876543210',
                'email': 'rajesh.kumar@email.com',
                'address': '123 MG Road, Bangalore, Karnataka 560001',
                'age': 35,
                'city': 'Bangalore',
                'current_loans': [
                    {'type': 'Home Loan', 'amount': 2500000, 'emi': 25000, 'remaining_tenure': 180}
                ],
                'credit_score': 780,
                'pre_approved_limit': 800000,
                'kyc_verified': True,
                'last_updated': datetime.now() - timedelta(days=30)
            },
            '9876543211': {
                'name': 'Priya Sharma',
                'phone': '9876543211',
                'email': 'priya.sharma@email.com',
                'address': '456 Park Street, Mumbai, Maharashtra 400001',
                'age': 28,
                'city': 'Mumbai',
                'current_loans': [],
                'credit_score': 720,
                'pre_approved_limit': 500000,
                'kyc_verified': True,
                'last_updated': datetime.now() - timedelta(days=15)
            },
            '9876543212': {
                'name': 'Amit Patel',
                'phone': '9876543212',
                'email': 'amit.patel@email.com',
                'address': '789 Connaught Place, New Delhi, Delhi 110001',
                'age': 42,
                'city': 'New Delhi',
                'current_loans': [
                    {'type': 'Car Loan', 'amount': 800000, 'emi': 15000, 'remaining_tenure': 36}
                ],
                'credit_score': 750,
                'pre_approved_limit': 1200000,
                'kyc_verified': True,
                'last_updated': datetime.now() - timedelta(days=7)
            },
            '9876543213': {
                'name': 'Sunita Reddy',
                'phone': '9876543213',
                'email': 'sunita.reddy@email.com',
                'address': '321 Brigade Road, Chennai, Tamil Nadu 600001',
                'age': 31,
                'city': 'Chennai',
                'current_loans': [],
                'credit_score': 680,
                'pre_approved_limit': 300000,
                'kyc_verified': True,
                'last_updated': datetime.now() - timedelta(days=45)
            },
            '9876543214': {
                'name': 'Vikram Singh',
                'phone': '9876543214',
                'email': 'vikram.singh@email.com',
                'address': '654 Marine Drive, Kochi, Kerala 682001',
                'age': 38,
                'city': 'Kochi',
                'current_loans': [
                    {'type': 'Personal Loan', 'amount': 400000, 'emi': 12000, 'remaining_tenure': 24}
                ],
                'credit_score': 710,
                'pre_approved_limit': 600000,
                'kyc_verified': True,
                'last_updated': datetime.now() - timedelta(days=20)
            },
            '9876543215': {
                'name': 'Meera Joshi',
                'phone': '9876543215',
                'email': 'meera.joshi@email.com',
                'address': '987 Commercial Street, Pune, Maharashtra 411001',
                'age': 26,
                'city': 'Pune',
                'current_loans': [],
                'credit_score': 760,
                'pre_approved_limit': 700000,
                'kyc_verified': True,
                'last_updated': datetime.now() - timedelta(days=10)
            },
            '9876543216': {
                'name': 'Suresh Kumar',
                'phone': '9876543216',
                'email': 'suresh.kumar@email.com',
                'address': '147 Residency Road, Hyderabad, Telangana 500001',
                'age': 45,
                'city': 'Hyderabad',
                'current_loans': [
                    {'type': 'Home Loan', 'amount': 3000000, 'emi': 30000, 'remaining_tenure': 240},
                    {'type': 'Car Loan', 'amount': 600000, 'emi': 12000, 'remaining_tenure': 48}
                ],
                'credit_score': 790,
                'pre_approved_limit': 1000000,
                'kyc_verified': True,
                'last_updated': datetime.now() - timedelta(days=5)
            },
            '9876543217': {
                'name': 'Anita Gupta',
                'phone': '9876543217',
                'email': 'anita.gupta@email.com',
                'address': '258 Mall Road, Chandigarh, Punjab 160001',
                'age': 33,
                'city': 'Chandigarh',
                'current_loans': [],
                'credit_score': 740,
                'pre_approved_limit': 900000,
                'kyc_verified': True,
                'last_updated': datetime.now() - timedelta(days=25)
            },
            '9876543218': {
                'name': 'Ravi Nair',
                'phone': '9876543218',
                'email': 'ravi.nair@email.com',
                'address': '369 MG Road, Trivandrum, Kerala 695001',
                'age': 29,
                'city': 'Trivandrum',
                'current_loans': [
                    {'type': 'Education Loan', 'amount': 500000, 'emi': 8000, 'remaining_tenure': 60}
                ],
                'credit_score': 730,
                'pre_approved_limit': 400000,
                'kyc_verified': True,
                'last_updated': datetime.now() - timedelta(days=12)
            },
            '9876543219': {
                'name': 'Kavita Desai',
                'phone': '9876543219',
                'email': 'kavita.desai@email.com',
                'address': '741 Linking Road, Ahmedabad, Gujarat 380001',
                'age': 37,
                'city': 'Ahmedabad',
                'current_loans': [],
                'credit_score': 770,
                'pre_approved_limit': 1100000,
                'kyc_verified': True,
                'last_updated': datetime.now() - timedelta(days=18)
            }
        }
    
    def verify_customer(self, phone_number):
        """Verify customer KYC details"""
        if phone_number in self.customers:
            customer = self.customers[phone_number]
            return {
                'verified': customer['kyc_verified'],
                'customer_data': customer,
                'reason': 'Customer verified successfully' if customer['kyc_verified'] else 'KYC not completed'
            }
        else:
            return {
                'verified': False,
                'customer_data': None,
                'reason': 'Customer not found in our database'
            }
    
    def get_customer_by_phone(self, phone_number):
        """Get customer details by phone number"""
        return self.customers.get(phone_number)
    
    def get_customer_by_name(self, name):
        """Get customer details by name (fuzzy match)"""
        name_lower = name.lower()
        for phone, customer in self.customers.items():
            if name_lower in customer['name'].lower():
                return customer
        return None
    
    def update_customer_data(self, phone_number, updated_data):
        """Update customer information"""
        if phone_number in self.customers:
            self.customers[phone_number].update(updated_data)
            self.customers[phone_number]['last_updated'] = datetime.now()
            return True
        return False
    
    def get_all_customers(self):
        """Get all customer data (for admin purposes)"""
        return self.customers
    
    def search_customers(self, search_term):
        """Search customers by name, phone, or email"""
        results = []
        search_lower = search_term.lower()
        
        for phone, customer in self.customers.items():
            if (search_lower in customer['name'].lower() or 
                search_lower in phone or 
                search_lower in customer['email'].lower()):
                results.append(customer)
        
        return results

