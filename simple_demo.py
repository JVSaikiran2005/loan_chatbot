#!/usr/bin/env python3
"""
Simple demo script for Tata Capital Personal Loan Chatbot
"""

import requests
import json
import time

def test_server():
    """Test if the Flask server is running"""
    print("Testing server connection...")
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("SUCCESS: Server is running")
            return True
        else:
            print(f"ERROR: Server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to server")
        print("Please run: python app.py")
        return False

def test_customers_api():
    """Test the customers API"""
    print("\nTesting customers API...")
    try:
        response = requests.get("http://localhost:5000/api/customers")
        if response.status_code == 200:
            customers = response.json()
            print(f"SUCCESS: Found {len(customers)} customers")
            
            # Show first customer
            first_phone = list(customers.keys())[0]
            first_customer = customers[first_phone]
            print(f"Sample customer: {first_customer['name']}")
            print(f"Credit Score: {first_customer['credit_score']}")
            print(f"Pre-approved: Rs. {first_customer['pre_approved_limit']:,}")
            return True
        else:
            print(f"ERROR: API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_chat_api():
    """Test the chat API"""
    print("\nTesting chat API...")
    try:
        response = requests.post(
            "http://localhost:5000/api/chat",
            json={'message': 'Hi, I need a personal loan'}
        )
        if response.status_code == 200:
            data = response.json()
            print("SUCCESS: Chat API working")
            print(f"Bot response: {data['response'][:100]}...")
            print(f"Session ID: {data['session_id']}")
            return True
        else:
            print(f"ERROR: Chat API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("Tata Capital Personal Loan Chatbot - System Test")
    print("=" * 50)
    
    # Test 1: Server connection
    if not test_server():
        return
    
    # Test 2: Customers API
    if not test_customers_api():
        return
    
    # Test 3: Chat API
    if not test_chat_api():
        return
    
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED!")
    print("The system is ready for demonstration.")
    print("Open http://localhost:5000 in your browser to try the web interface.")

if __name__ == "__main__":
    main()

