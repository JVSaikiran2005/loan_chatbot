import os
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import uuid

class SanctionLetterGenerator:
    def __init__(self):
        self.output_dir = 'sanction_letters'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_sanction_letter(self, customer_data, loan_details, underwriting_result):
        """Generate PDF sanction letter"""
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"sanction_letter_{customer_data.get('phone', 'unknown')}_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6
        )
        
        # Build content
        story = []
        
        # Header
        story.append(Paragraph("TATA CAPITAL FINANCIAL SERVICES LIMITED", title_style))
        story.append(Paragraph("Personal Loan Sanction Letter", heading_style))
        story.append(Spacer(1, 20))
        
        # Date and Reference
        current_date = datetime.now().strftime('%B %d, %Y')
        loan_ref = f"TC/PL/{datetime.now().strftime('%Y%m%d')}/{str(uuid.uuid4())[:8].upper()}"
        
        story.append(Paragraph(f"Date: {current_date}", normal_style))
        story.append(Paragraph(f"Loan Reference: {loan_ref}", normal_style))
        story.append(Spacer(1, 20))
        
        # Customer Details
        story.append(Paragraph("Dear Sir/Madam,", normal_style))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph(
            f"We are pleased to inform you that your Personal Loan application has been approved. "
            f"Please find below the details of your sanctioned loan:",
            normal_style
        ))
        story.append(Spacer(1, 20))
        
        # Loan Details Table
        loan_data = [
            ['Particulars', 'Details'],
            ['Borrower Name', customer_data.get('name', 'N/A')],
            ['Mobile Number', customer_data.get('phone', 'N/A')],
            ['Sanctioned Amount', f"₹{underwriting_result.get('approved_amount', 0):,}"],
            ['Interest Rate', f"{underwriting_result.get('interest_rate', 0)}% per annum"],
            ['Loan Tenure', f"{loan_details.get('tenure', 0)} months"],
            ['EMI Amount', f"₹{underwriting_result.get('emi', 0):,}"],
            ['Total Amount Payable', f"₹{underwriting_result.get('total_amount', 0):,}"],
            ['Total Interest', f"₹{underwriting_result.get('total_interest', 0):,}"],
            ['Processing Fee', f"₹{underwriting_result.get('processing_fee', 0):,}"],
            ['Credit Score', str(underwriting_result.get('credit_score', 0))],
            ['Sanction Date', current_date]
        ]
        
        loan_table = Table(loan_data, colWidths=[2.5*inch, 3*inch])
        loan_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        story.append(loan_table)
        story.append(Spacer(1, 20))
        
        # Terms and Conditions
        story.append(Paragraph("Terms and Conditions:", heading_style))
        
        terms = [
            "1. This sanction is valid for 30 days from the date of this letter.",
            "2. The loan will be disbursed within 24-48 hours after completion of documentation.",
            "3. Interest will be calculated on a reducing balance method.",
            "4. EMI payments are due on the same date each month as the disbursement date.",
            "5. Prepayment charges: 2% of outstanding principal for prepayment within 12 months.",
            "6. Late payment charges: ₹500 per month for delayed EMI payments.",
            "7. The borrower must maintain the same employment status during the loan tenure.",
            "8. Any change in contact details must be communicated to Tata Capital immediately.",
            "9. The loan is subject to final verification of documents and KYC compliance.",
            "10. Tata Capital reserves the right to recall the loan in case of any misrepresentation."
        ]
        
        for term in terms:
            story.append(Paragraph(term, normal_style))
        
        story.append(Spacer(1, 20))
        
        # Next Steps
        story.append(Paragraph("Next Steps:", heading_style))
        next_steps = [
            "1. Review and accept the loan terms mentioned above.",
            "2. Complete the loan agreement and other required documents.",
            "3. Provide bank account details for loan disbursement.",
            "4. Submit any additional documents if requested.",
            "5. Loan disbursement will be processed within 24-48 hours."
        ]
        
        for step in next_steps:
            story.append(Paragraph(step, normal_style))
        
        story.append(Spacer(1, 30))
        
        # Contact Information
        story.append(Paragraph("For any queries, please contact:", normal_style))
        story.append(Paragraph("Customer Service: 1800-209-8808", normal_style))
        story.append(Paragraph("Email: customer.service@tatacapital.com", normal_style))
        story.append(Paragraph("Website: www.tatacapital.com", normal_style))
        
        story.append(Spacer(1, 30))
        
        # Footer
        story.append(Paragraph("Thank you for choosing Tata Capital!", normal_style))
        story.append(Spacer(1, 20))
        story.append(Paragraph("Yours sincerely,", normal_style))
        story.append(Paragraph("Tata Capital Financial Services Limited", normal_style))
        story.append(Paragraph("Personal Loans Division", normal_style))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def generate_loan_agreement(self, customer_data, loan_details, underwriting_result):
        """Generate loan agreement document"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"loan_agreement_{customer_data.get('phone', 'unknown')}_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Add content for loan agreement
        story.append(Paragraph("LOAN AGREEMENT", styles['Title']))
        story.append(Spacer(1, 20))
        
        # Add agreement terms and conditions
        agreement_content = [
            "This Loan Agreement is entered into between Tata Capital Financial Services Limited and the borrower.",
            f"Loan Amount: ₹{underwriting_result.get('approved_amount', 0):,}",
            f"Interest Rate: {underwriting_result.get('interest_rate', 0)}% per annum",
            f"Tenure: {loan_details.get('tenure', 0)} months",
            f"EMI: ₹{underwriting_result.get('emi', 0):,}",
            "",
            "The borrower agrees to repay the loan as per the terms and conditions specified in this agreement.",
            "This agreement is governed by the laws of India and subject to the jurisdiction of courts in Mumbai."
        ]
        
        for content in agreement_content:
            story.append(Paragraph(content, styles['Normal']))
        
        doc.build(story)
        return filepath
    
    def get_sanction_letter_template(self):
        """Get sanction letter template structure"""
        return {
            'header': {
                'company_name': 'TATA CAPITAL FINANCIAL SERVICES LIMITED',
                'document_type': 'Personal Loan Sanction Letter'
            },
            'customer_section': [
                'name', 'phone', 'email', 'address'
            ],
            'loan_section': [
                'sanctioned_amount', 'interest_rate', 'tenure', 'emi',
                'total_amount', 'processing_fee', 'credit_score'
            ],
            'terms_section': [
                'validity_period', 'disbursement_time', 'interest_calculation',
                'emi_due_date', 'prepayment_charges', 'late_payment_charges'
            ],
            'contact_section': [
                'customer_service_phone', 'email', 'website'
            ]
        }

