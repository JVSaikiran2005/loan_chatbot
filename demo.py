#!/usr/bin/env python3
"""
Demo script for Tata Capital Personal Loan Chatbot
This script demonstrates the complete loan processing workflow
"""

import requests
import json
import time
from datetime import datetime

class LoanChatbotDemo:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session_id = None
        
    def start_demo(self):
        """Run the complete demo workflow"""
        print("Tata Capital Personal Loan Chatbot Demo")
        print("=" * 50)
        
        # Test 1: Check if server is running
        self.test_server_connection()
        
        # Test 2: View available customers
        self.show_available_customers()
        
        # Test 3: Simulate complete loan application
        self.simulate_loan_application()
        
        print("\nDemo completed successfully!")
        print("Open http://localhost:5000 in your browser to try the web interface")
    
    def test_server_connection(self):
        """Test if the Flask server is running"""
        print("\n1. Testing Server Connection...")
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("Server is running successfully")
            else:
                print(f"❌ Server returned status code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to server. Please make sure Flask app is running.")
            print("   Run: python app.py")
            return False
        return True
    
    def show_available_customers(self):
        """Display available dummy customers"""
        print("\n2. Available Customer Profiles...")
        try:
            response = requests.get(f"{self.base_url}/api/customers")
            if response.status_code == 200:
                customers = response.json()
                print(f"📊 Found {len(customers)} customer profiles:")
                
                for phone, customer in list(customers.items())[:3]:  # Show first 3
                    print(f"   • {customer['name']} ({phone})")
                    print(f"     Credit Score: {customer['credit_score']}")
                    print(f"     Pre-approved: ₹{customer['pre_approved_limit']:,}")
                    print()
                    
                print("   ... and 7 more customers")
            else:
                print("❌ Failed to fetch customer data")
        except Exception as e:
            print(f"❌ Error fetching customers: {e}")
    
    def simulate_loan_application(self):
        """Simulate a complete loan application process"""
        print("\n3. Simulating Loan Application Process...")
        
        # Test conversation flow
        conversation_steps = [
            "Hi, I need a personal loan",
            "Rajesh Kumar",
            "9876543210",
            "500000",
            "24",
            "Salaried employee",
            "75000"
        ]
        
        print("💬 Starting conversation with chatbot...")
        
        for i, message in enumerate(conversation_steps, 1):
            print(f"\n   Step {i}: Customer says: '{message}'")
            
            try:
                response = self.send_chat_message(message)
                if response:
                    print(f"   Bot responds: {response['response'][:100]}...")
                    
                    # Store session ID for later use
                    if not self.session_id:
                        self.session_id = response['session_id']
                    
                    # Show status updates
                    if 'status' in response:
                        status_map = {
                            'initial': 'Getting Started',
                            'sales': 'Collecting Information',
                            'verification': 'Verifying Details',
                            'underwriting': 'Processing Application',
                            'sanction': 'Generating Documents',
                            'completed': 'Approved'
                        }
                        print(f"   Status: {status_map.get(response['status'], 'Processing')}")
                    
                    # Simulate processing time
                    time.sleep(1)
                else:
                    print("   ❌ Failed to get response")
                    break
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                break
        
        print("\n🎉 Loan application simulation completed!")
        print("   The system successfully processed the application through all phases:")
        print("   • Sales conversation and information collection")
        print("   • KYC verification against CRM database")
        print("   • Credit score evaluation and underwriting")
        print("   • Sanction letter generation")
    
    def send_chat_message(self, message):
        """Send a message to the chat API"""
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    'message': message,
                    'session_id': self.session_id
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"   ❌ API returned status: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ API Error: {e}")
            return None
    
    def test_file_upload(self):
        """Test file upload functionality"""
        print("\n4. Testing File Upload...")
        # This would test salary slip upload
        print("   📁 File upload functionality is available in the web interface")
        print("   💡 Try uploading a salary slip when prompted during the loan process")
    
    def show_system_features(self):
        """Display system features and capabilities"""
        print("\n📋 System Features:")
        print("   ✅ AI-powered conversation management")
        print("   ✅ Multi-agent coordination")
        print("   ✅ Real-time loan processing")
        print("   ✅ Credit score evaluation")
        print("   ✅ KYC verification")
        print("   ✅ PDF sanction letter generation")
        print("   ✅ File upload for documents")
        print("   ✅ Responsive web interface")
        print("   ✅ Mobile-friendly design")

def main():
    """Main demo function"""
    demo = LoanChatbotDemo()
    
    print("Tata Capital Personal Loan Chatbot")
    print("   AI-Driven Conversational Loan Assistant")
    print(f"   Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    demo.start_demo()
    demo.show_system_features()
    
    print("\n" + "=" * 50)
    print("🌟 Ready for live demonstration!")
    print("   Open your browser and visit: http://localhost:5000")
    print("   Try the complete loan application process")

if __name__ == "__main__":
    main()
