import time
import random

class VerificationAgent:
    def __init__(self, crm_server):
        self.crm_server = crm_server
        self.verification_status = {}
    
    def verify_customer(self, customer_data):
        """Verify customer KYC details from CRM"""
        phone_number = customer_data.get('phone')
        customer_name = customer_data.get('name')
        
        if not phone_number:
            return {
                'verified': False,
                'reason': 'Phone number not provided',
                'verification_details': None
            }
        
        # Simulate verification process delay
        time.sleep(1)  # Simulate API call delay
        
        # Check if customer exists in CRM
        crm_customer = self.crm_server.get_customer_by_phone(phone_number)
        
        if not crm_customer:
            # Try to find by name if phone not found
            crm_customer = self.crm_server.get_customer_by_name(customer_name)
        
        if not crm_customer:
            return {
                'verified': False,
                'reason': 'Customer not found in our database. Please contact customer service.',
                'verification_details': None
            }
        
        # Verify KYC status
        if not crm_customer.get('kyc_verified', False):
            return {
                'verified': False,
                'reason': 'KYC verification pending. Please complete KYC first.',
                'verification_details': crm_customer
            }
        
        # Cross-verify provided information with CRM data
        verification_checks = self._perform_verification_checks(customer_data, crm_customer)
        
        if verification_checks['all_passed']:
            return {
                'verified': True,
                'reason': 'Customer verification successful',
                'verification_details': {
                    'crm_data': crm_customer,
                    'checks_passed': verification_checks['passed_checks'],
                    'verification_timestamp': time.time()
                }
            }
        else:
            return {
                'verified': False,
                'reason': f"Verification failed: {verification_checks['failure_reason']}",
                'verification_details': {
                    'crm_data': crm_customer,
                    'failed_checks': verification_checks['failed_checks']
                }
            }
    
    def _perform_verification_checks(self, provided_data, crm_data):
        """Perform detailed verification checks"""
        checks = {
            'name_match': False,
            'phone_match': False,
            'address_verification': False,
            'kyc_status': False
        }
        
        # Name verification (fuzzy match)
        provided_name = provided_data.get('name', '').lower().strip()
        crm_name = crm_data.get('name', '').lower().strip()
        
        if provided_name and crm_name:
            # Check if provided name contains key parts of CRM name
            provided_words = set(provided_name.split())
            crm_words = set(crm_name.split())
            
            if len(provided_words.intersection(crm_words)) >= 1:
                checks['name_match'] = True
        
        # Phone verification
        provided_phone = provided_data.get('phone', '').strip()
        crm_phone = crm_data.get('phone', '').strip()
        
        if provided_phone == crm_phone:
            checks['phone_match'] = True
        
        # Address verification (simplified - just check if address exists)
        if crm_data.get('address'):
            checks['address_verification'] = True
        
        # KYC status verification
        if crm_data.get('kyc_verified', False):
            checks['kyc_status'] = True
        
        # Determine overall result
        passed_checks = [check for check, passed in checks.items() if passed]
        failed_checks = [check for check, passed in checks.items() if not passed]
        
        # At least name and phone should match for basic verification
        critical_checks = ['name_match', 'phone_match']
        critical_passed = all(checks[check] for check in critical_checks)
        
        if critical_passed and checks['kyc_status']:
            return {
                'all_passed': True,
                'passed_checks': passed_checks,
                'failed_checks': failed_checks,
                'failure_reason': None
            }
        else:
            failure_reasons = []
            if not checks['name_match']:
                failure_reasons.append('Name mismatch')
            if not checks['phone_match']:
                failure_reasons.append('Phone number mismatch')
            if not checks['kyc_status']:
                failure_reasons.append('KYC not completed')
            
            return {
                'all_passed': False,
                'passed_checks': passed_checks,
                'failed_checks': failed_checks,
                'failure_reason': '; '.join(failure_reasons)
            }
    
    def verify_documents(self, customer_data, document_type='salary_slip'):
        """Verify uploaded documents"""
        # Simulate document verification process
        time.sleep(2)  # Simulate processing time
        
        # Mock verification results
        verification_results = {
            'salary_slip': {
                'verified': True,
                'extracted_data': {
                    'company_name': 'Sample Company Ltd',
                    'monthly_salary': customer_data.get('monthly_income', 50000),
                    'employee_id': 'EMP' + str(random.randint(1000, 9999)),
                    'verification_date': time.time()
                },
                'confidence_score': random.uniform(0.85, 0.95)
            },
            'bank_statement': {
                'verified': True,
                'extracted_data': {
                    'account_balance': random.randint(50000, 500000),
                    'average_monthly_credit': customer_data.get('monthly_income', 50000),
                    'verification_date': time.time()
                },
                'confidence_score': random.uniform(0.80, 0.90)
            }
        }
        
        return verification_results.get(document_type, {
            'verified': False,
            'reason': 'Document type not supported'
        })
    
    def get_verification_status(self, customer_id):
        """Get current verification status for customer"""
        return self.verification_status.get(customer_id, {
            'status': 'not_started',
            'kyc_verified': False,
            'documents_verified': False,
            'last_updated': None
        })
    
    def update_verification_status(self, customer_id, status_update):
        """Update verification status"""
        if customer_id not in self.verification_status:
            self.verification_status[customer_id] = {
                'status': 'not_started',
                'kyc_verified': False,
                'documents_verified': False,
                'last_updated': None
            }
        
        self.verification_status[customer_id].update(status_update)
        self.verification_status[customer_id]['last_updated'] = time.time()

