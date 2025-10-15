import time
import random

class UnderwritingAgent:
    def __init__(self, credit_bureau, offer_mart):
        self.credit_bureau = credit_bureau
        self.offer_mart = offer_mart
        self.underwriting_rules = {
            'min_credit_score': 700,
            'max_loan_to_income_ratio': 20,  # Loan amount should not exceed 20x monthly income
            'max_emi_to_income_ratio': 0.5,  # EMI should not exceed 50% of monthly income
            'min_tenure': 6,
            'max_tenure': 60,
            'min_loan_amount': 50000,
            'max_loan_amount': 4000000
        }
    
    def evaluate_loan(self, customer_data, loan_details):
        """Comprehensive loan evaluation and underwriting"""
        # Simulate underwriting process delay
        time.sleep(2)  # Simulate processing time
        
        phone_number = customer_data.get('phone')
        loan_amount = loan_details.get('amount', 0)
        tenure = loan_details.get('tenure', 12)
        monthly_income = customer_data.get('monthly_income', 0)
        
        # Step 1: Get credit score
        credit_data = self.credit_bureau.get_credit_score(phone_number)
        credit_score = credit_data['score']
        
        # Step 2: Get pre-approved limit
        pre_approved_offer = self.offer_mart.get_pre_approved_offer(phone_number)
        pre_approved_limit = pre_approved_offer['pre_approved_amount'] if pre_approved_offer else 0
        
        # Step 3: Perform underwriting checks
        underwriting_result = self._perform_underwriting_checks(
            customer_data, loan_details, credit_score, pre_approved_limit
        )
        
        if underwriting_result['approved']:
            # Generate final loan offer
            loan_offer = self.offer_mart.generate_loan_offer(
                customer_data, credit_score, loan_amount, tenure
            )
            
            return {
                'approved': True,
                'credit_score': credit_score,
                'pre_approved_limit': pre_approved_limit,
                'approved_amount': loan_offer['approved_amount'],
                'interest_rate': loan_offer['interest_rate'],
                'tenure': tenure,
                'emi': loan_offer['emi'],
                'total_amount': loan_offer['total_amount'],
                'total_interest': loan_offer['total_interest'],
                'processing_fee': loan_offer['processing_fee'],
                'approval_conditions': underwriting_result.get('conditions', []),
                'underwriting_notes': underwriting_result.get('notes', '')
            }
        else:
            return {
                'approved': False,
                'credit_score': credit_score,
                'pre_approved_limit': pre_approved_limit,
                'reason': underwriting_result['reason'],
                'suggestions': underwriting_result.get('suggestions', [])
            }
    
    def _perform_underwriting_checks(self, customer_data, loan_details, credit_score, pre_approved_limit):
        """Perform detailed underwriting checks"""
        loan_amount = loan_details.get('amount', 0)
        tenure = loan_details.get('tenure', 12)
        monthly_income = customer_data.get('monthly_income', 0)
        
        checks = {
            'credit_score_check': False,
            'loan_amount_check': False,
            'income_check': False,
            'tenure_check': False,
            'pre_approved_check': False
        }
        
        conditions = []
        notes = []
        
        # 1. Credit Score Check
        if credit_score >= self.underwriting_rules['min_credit_score']:
            checks['credit_score_check'] = True
            notes.append(f"Credit score {credit_score} meets minimum requirement")
        else:
            notes.append(f"Credit score {credit_score} below minimum requirement of {self.underwriting_rules['min_credit_score']}")
        
        # 2. Loan Amount Check
        if (self.underwriting_rules['min_loan_amount'] <= loan_amount <= 
            self.underwriting_rules['max_loan_amount']):
            checks['loan_amount_check'] = True
            notes.append(f"Loan amount ₹{loan_amount:,} within acceptable range")
        else:
            notes.append(f"Loan amount ₹{loan_amount:,} outside acceptable range")
        
        # 3. Income Check
        if monthly_income > 0:
            # Check loan to income ratio
            loan_to_income_ratio = loan_amount / monthly_income
            if loan_to_income_ratio <= self.underwriting_rules['max_loan_to_income_ratio']:
                checks['income_check'] = True
                notes.append(f"Loan to income ratio {loan_to_income_ratio:.1f} is acceptable")
            else:
                notes.append(f"Loan to income ratio {loan_to_income_ratio:.1f} too high")
        else:
            notes.append("Monthly income not provided")
        
        # 4. Tenure Check
        if (self.underwriting_rules['min_tenure'] <= tenure <= 
            self.underwriting_rules['max_tenure']):
            checks['tenure_check'] = True
            notes.append(f"Tenure {tenure} months is acceptable")
        else:
            notes.append(f"Tenure {tenure} months outside acceptable range")
        
        # 5. Pre-approved Limit Check
        if pre_approved_limit > 0:
            if loan_amount <= pre_approved_limit:
                checks['pre_approved_check'] = True
                notes.append(f"Loan amount within pre-approved limit of ₹{pre_approved_limit:,}")
                return {
                    'approved': True,
                    'conditions': ['Standard approval based on pre-approved limit'],
                    'notes': notes
                }
            elif loan_amount <= (pre_approved_limit * 2):
                # Need salary slip verification
                notes.append(f"Loan amount exceeds pre-approved limit, salary slip verification required")
                conditions.append("Salary slip upload required")
                
                # Check if salary slip is uploaded
                if customer_data.get('salary_slip_uploaded', False):
                    # Verify EMI capacity
                    emi = self._calculate_emi(loan_amount, 12.0, tenure)  # Using 12% for calculation
                    if emi <= (monthly_income * 0.5):
                        checks['pre_approved_check'] = True
                        notes.append("Salary slip verified, EMI within 50% of income")
                        return {
                            'approved': True,
                            'conditions': ['Salary slip verification completed'],
                            'notes': notes
                        }
                    else:
                        notes.append(f"EMI ₹{emi:,} exceeds 50% of monthly income")
                else:
                    return {
                        'approved': False,
                        'reason': 'Salary slip upload required for loan amount exceeding pre-approved limit',
                        'suggestions': ['Upload salary slip', 'Reduce loan amount to pre-approved limit']
                    }
            else:
                notes.append(f"Loan amount exceeds 2x pre-approved limit")
        else:
            notes.append("No pre-approved limit available")
        
        # Determine final approval
        critical_checks = ['credit_score_check', 'loan_amount_check', 'income_check', 'tenure_check']
        critical_passed = all(checks[check] for check in critical_checks)
        
        if critical_passed:
            return {
                'approved': True,
                'conditions': conditions,
                'notes': notes
            }
        else:
            failed_checks = [check for check in critical_checks if not checks[check]]
            suggestions = self._generate_suggestions(failed_checks, customer_data, loan_details)
            
            return {
                'approved': False,
                'reason': f"Underwriting failed: {', '.join(failed_checks)}",
                'suggestions': suggestions
            }
    
    def _calculate_emi(self, principal, rate, tenure_months):
        """Calculate EMI using standard formula"""
        if rate == 0:
            return principal / tenure_months
        
        monthly_rate = rate / (12 * 100)
        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
              ((1 + monthly_rate) ** tenure_months - 1)
        return round(emi, 2)
    
    def _generate_suggestions(self, failed_checks, customer_data, loan_details):
        """Generate improvement suggestions based on failed checks"""
        suggestions = []
        
        if 'credit_score_check' in failed_checks:
            suggestions.extend([
                "Improve credit score by paying existing loans on time",
                "Reduce credit card utilization",
                "Avoid new credit applications for 6 months"
            ])
        
        if 'loan_amount_check' in failed_checks:
            loan_amount = loan_details.get('amount', 0)
            if loan_amount > 4000000:
                suggestions.append("Reduce loan amount to maximum ₹40,00,000")
            elif loan_amount < 50000:
                suggestions.append("Increase loan amount to minimum ₹50,000")
        
        if 'income_check' in failed_checks:
            suggestions.extend([
                "Provide additional income proof",
                "Consider a co-applicant with higher income",
                "Reduce loan amount to match income capacity"
            ])
        
        if 'tenure_check' in failed_checks:
            suggestions.extend([
                "Choose tenure between 6 to 60 months",
                "Consider longer tenure to reduce EMI"
            ])
        
        return suggestions
    
    def get_underwriting_summary(self, customer_data, loan_details):
        """Get underwriting summary without full evaluation"""
        phone_number = customer_data.get('phone')
        credit_data = self.credit_bureau.get_credit_score(phone_number)
        pre_approved_offer = self.offer_mart.get_pre_approved_offer(phone_number)
        
        return {
            'credit_score': credit_data['score'],
            'credit_rating': self.credit_bureau.calculate_credit_rating(credit_data['score']),
            'pre_approved_limit': pre_approved_offer['pre_approved_amount'] if pre_approved_offer else 0,
            'pre_approved_rate': pre_approved_offer['interest_rate'] if pre_approved_offer else None,
            'estimated_eligibility': self.offer_mart.calculate_loan_eligibility(customer_data, credit_data['score'])
        }

