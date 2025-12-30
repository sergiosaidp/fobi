#!/usr/bin/env python3
"""
Backend API Testing for Fobi.io Clone
Tests all API endpoints with proper error handling and validation
"""

import requests
import json
import sys
import os
from datetime import datetime

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except FileNotFoundError:
        pass
    return "http://localhost:8005"

BASE_URL = get_backend_url()
print(f"Testing backend at: {BASE_URL}")

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_test_header(test_name):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}Testing: {test_name}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")

def print_success(message):
    print(f"{Colors.GREEN}[OK] {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.RED}[FAIL] {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.YELLOW}[WARN]  {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.BLUE}[INFO]  {message}{Colors.ENDC}")

# Global variables to store test data
created_chatbot_id = None
created_conversation_id = None
test_results = {
    "passed": 0,
    "failed": 0,
    "errors": []
}

def test_health_endpoints():
    """Test health check endpoints"""
    print_test_header("Health Check Endpoints")
    
    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print_success("GET /api/ - Health check passed")
                test_results["passed"] += 1
            else:
                print_error(f"GET /api/ - Unexpected response: {data}")
                test_results["failed"] += 1
                test_results["errors"].append("Health check returned non-healthy status")
        else:
            print_error(f"GET /api/ - Status code: {response.status_code}")
            test_results["failed"] += 1
            test_results["errors"].append(f"Health check failed with status {response.status_code}")
    except Exception as e:
        print_error(f"GET /api/ - Error: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"Health check endpoint error: {str(e)}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print_success("GET /api/health - Health check passed")
                test_results["passed"] += 1
            else:
                print_error(f"GET /api/health - Unexpected response: {data}")
                test_results["failed"] += 1
                test_results["errors"].append("Health endpoint returned non-healthy status")
        else:
            print_error(f"GET /api/health - Status code: {response.status_code}")
            test_results["failed"] += 1
            test_results["errors"].append(f"Health endpoint failed with status {response.status_code}")
    except Exception as e:
        print_error(f"GET /api/health - Error: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"Health endpoint error: {str(e)}")

def test_global_stats():
    """Test global statistics endpoint"""
    print_test_header("Global Statistics")
    
    try:
        response = requests.get(f"{BASE_URL}/api/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            stats = data.get("stats", {})
            
            required_fields = ["total_websites", "total_conversations", "avg_engagement_rate"]
            missing_fields = [field for field in required_fields if field not in stats]
            
            if missing_fields:
                print_error(f"GET /api/stats - Missing fields: {missing_fields}")
                test_results["failed"] += 1
                test_results["errors"].append(f"Stats missing required fields: {missing_fields}")
            else:
                print_success("GET /api/stats - All required fields present")
                print_info(f"Stats: {stats}")
                test_results["passed"] += 1
        else:
            print_error(f"GET /api/stats - Status code: {response.status_code}")
            test_results["failed"] += 1
            test_results["errors"].append(f"Stats endpoint failed with status {response.status_code}")
    except Exception as e:
        print_error(f"GET /api/stats - Error: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"Stats endpoint error: {str(e)}")

def test_create_chatbot():
    """Test chatbot creation"""
    global created_chatbot_id
    print_test_header("Create Chatbot")
    
    # Valid chatbot data
    chatbot_data = {
        "name": "Customer Support Bot",
        "google_form_url": "https://docs.google.com/forms/d/e/1FAIpQLSc_test123/viewform",
        "customization": {
            "primary_color": "#7c3aed",
            "secondary_color": "#2563eb",
            "bot_name": "Support Assistant",
            "welcome_message": "Hello! How can I help you today?",
            "position": "bottom-right",
            "size": "medium"
        },
        "embed_type": "popup"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chatbots",
            json=chatbot_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("chatbot_id"):
                created_chatbot_id = data["chatbot_id"]
                print_success(f"POST /api/chatbots - Chatbot created with ID: {created_chatbot_id}")
                
                # Check if embed code is generated
                if data.get("embed_code"):
                    print_success("Embed code generated successfully")
                else:
                    print_warning("Embed code not found in response")
                
                test_results["passed"] += 1
            else:
                print_error(f"POST /api/chatbots - Invalid response structure: {data}")
                test_results["failed"] += 1
                test_results["errors"].append("Chatbot creation response missing required fields")
        else:
            print_error(f"POST /api/chatbots - Status code: {response.status_code}")
            print_error(f"Response: {response.text}")
            test_results["failed"] += 1
            test_results["errors"].append(f"Chatbot creation failed with status {response.status_code}")
    except Exception as e:
        print_error(f"POST /api/chatbots - Error: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"Chatbot creation error: {str(e)}")

def test_invalid_google_form_url():
    """Test chatbot creation with invalid Google Form URL"""
    print_test_header("Invalid Google Form URL Test")
    
    invalid_chatbot_data = {
        "name": "Invalid Bot",
        "google_form_url": "https://example.com/not-a-google-form",
        "embed_type": "popup"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chatbots",
            json=invalid_chatbot_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 400:
            print_success("POST /api/chatbots - Correctly rejected invalid Google Form URL")
            test_results["passed"] += 1
        else:
            print_error(f"POST /api/chatbots - Expected 400, got {response.status_code}")
            test_results["failed"] += 1
            test_results["errors"].append("Invalid Google Form URL not properly rejected")
    except Exception as e:
        print_error(f"POST /api/chatbots (invalid URL) - Error: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"Invalid URL test error: {str(e)}")

def test_get_all_chatbots():
    """Test getting all chatbots"""
    print_test_header("Get All Chatbots")
    
    try:
        response = requests.get(f"{BASE_URL}/api/chatbots", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "chatbots" in data:
                print_success(f"GET /api/chatbots - Retrieved {len(data['chatbots'])} chatbots")
                print_info(f"Pagination info: page={data.get('page')}, total={data.get('total')}")
                test_results["passed"] += 1
            else:
                print_error(f"GET /api/chatbots - Invalid response structure: {data}")
                test_results["failed"] += 1
                test_results["errors"].append("Get all chatbots response missing required fields")
        else:
            print_error(f"GET /api/chatbots - Status code: {response.status_code}")
            test_results["failed"] += 1
            test_results["errors"].append(f"Get all chatbots failed with status {response.status_code}")
    except Exception as e:
        print_error(f"GET /api/chatbots - Error: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"Get all chatbots error: {str(e)}")

def test_get_chatbot_by_id():
    """Test getting specific chatbot by ID"""
    global created_chatbot_id
    print_test_header("Get Chatbot by ID")
    
    if not created_chatbot_id:
        print_warning("No chatbot ID available, skipping test")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/api/chatbots/{created_chatbot_id}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("chatbot"):
                print_success(f"GET /api/chatbots/{created_chatbot_id} - Chatbot retrieved successfully")
                
                # Check if embed code is included
                if data.get("embed_code"):
                    print_success("Embed code included in response")
                else:
                    print_warning("Embed code not found in response")
                
                test_results["passed"] += 1
            else:
                print_error(f"GET /api/chatbots/{created_chatbot_id} - Invalid response: {data}")
                test_results["failed"] += 1
                test_results["errors"].append("Get chatbot by ID response missing required fields")
        else:
            print_error(f"GET /api/chatbots/{created_chatbot_id} - Status code: {response.status_code}")
            test_results["failed"] += 1
            test_results["errors"].append(f"Get chatbot by ID failed with status {response.status_code}")
    except Exception as e:
        print_error(f"GET /api/chatbots/{created_chatbot_id} - Error: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"Get chatbot by ID error: {str(e)}")

def test_get_nonexistent_chatbot():
    """Test getting non-existent chatbot"""
    print_test_header("Get Non-existent Chatbot")
    
    fake_id = "bot_nonexistent123"
    try:
        response = requests.get(f"{BASE_URL}/api/chatbots/{fake_id}", timeout=10)
        if response.status_code == 404:
            print_success(f"GET /api/chatbots/{fake_id} - Correctly returned 404 for non-existent chatbot")
            test_results["passed"] += 1
        else:
            print_error(f"GET /api/chatbots/{fake_id} - Expected 404, got {response.status_code}")
            test_results["failed"] += 1
            test_results["errors"].append("Non-existent chatbot should return 404")
    except Exception as e:
        print_error(f"GET /api/chatbots/{fake_id} - Error: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"Non-existent chatbot test error: {str(e)}")

def test_get_chatbot_stats():
    """Test getting chatbot statistics"""
    global created_chatbot_id
    print_test_header("Get Chatbot Statistics")
    
    if not created_chatbot_id:
        print_warning("No chatbot ID available, skipping test")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/api/chatbots/{created_chatbot_id}/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("stats"):
                stats = data["stats"]
                required_fields = ["total_conversations", "completed_conversations", "total_views", "completion_rate"]
                missing_fields = [field for field in required_fields if field not in stats]
                
                if missing_fields:
                    print_error(f"GET /api/chatbots/{created_chatbot_id}/stats - Missing fields: {missing_fields}")
                    test_results["failed"] += 1
                    test_results["errors"].append(f"Chatbot stats missing required fields: {missing_fields}")
                else:
                    print_success(f"GET /api/chatbots/{created_chatbot_id}/stats - All required fields present")
                    print_info(f"Stats: {stats}")
                    test_results["passed"] += 1
            else:
                print_error(f"GET /api/chatbots/{created_chatbot_id}/stats - Invalid response: {data}")
                test_results["failed"] += 1
                test_results["errors"].append("Chatbot stats response missing required fields")
        else:
            print_error(f"GET /api/chatbots/{created_chatbot_id}/stats - Status code: {response.status_code}")
            test_results["failed"] += 1
            test_results["errors"].append(f"Chatbot stats failed with status {response.status_code}")
    except Exception as e:
        print_error(f"GET /api/chatbots/{created_chatbot_id}/stats - Error: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"Chatbot stats error: {str(e)}")

def test_update_chatbot():
    """Test updating chatbot"""
    global created_chatbot_id
    print_test_header("Update Chatbot")
    
    if not created_chatbot_id:
        print_warning("No chatbot ID available, skipping test")
        return
    
    update_data = {
        "name": "Updated Customer Support Bot",
        "customization": {
            "primary_color": "#ff6b6b",
            "bot_name": "Updated Assistant",
            "welcome_message": "Hi there! I'm here to help you."
        }
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/chatbots/{created_chatbot_id}",
            json=update_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success(f"PUT /api/chatbots/{created_chatbot_id} - Chatbot updated successfully")
                test_results["passed"] += 1
            else:
                print_error(f"PUT /api/chatbots/{created_chatbot_id} - Update failed: {data}")
                test_results["failed"] += 1
                test_results["errors"].append("Chatbot update response indicates failure")
        else:
            print_error(f"PUT /api/chatbots/{created_chatbot_id} - Status code: {response.status_code}")
            test_results["failed"] += 1
            test_results["errors"].append(f"Chatbot update failed with status {response.status_code}")
    except Exception as e:
        print_error(f"PUT /api/chatbots/{created_chatbot_id} - Error: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"Chatbot update error: {str(e)}")

def test_create_conversation():
    """Test creating a conversation"""
    global created_chatbot_id, created_conversation_id
    print_test_header("Create Conversation")
    
    if not created_chatbot_id:
        print_warning("No chatbot ID available, skipping test")
        return
    
    conversation_data = {
        "chatbot_id": created_chatbot_id,
        "user_data": {
            "user_agent": "Mozilla/5.0 Test Browser",
            "ip_address": "192.168.1.100"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/conversations",
            json=conversation_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("conversation_id"):
                created_conversation_id = data["conversation_id"]
                print_success(f"POST /api/conversations - Conversation created with ID: {created_conversation_id}")
                test_results["passed"] += 1
            else:
                print_error(f"POST /api/conversations - Invalid response: {data}")
                test_results["failed"] += 1
                test_results["errors"].append("Conversation creation response missing required fields")
        else:
            print_error(f"POST /api/conversations - Status code: {response.status_code}")
            print_error(f"Response: {response.text}")
            test_results["failed"] += 1
            test_results["errors"].append(f"Conversation creation failed with status {response.status_code}")
    except Exception as e:
        print_error(f"POST /api/conversations - Error: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"Conversation creation error: {str(e)}")

def test_update_conversation():
    """Test updating conversation"""
    global created_conversation_id
    print_test_header("Update Conversation")
    
    if not created_conversation_id:
        print_warning("No conversation ID available, skipping test")
        return
    
    update_data = {
        "status": "completed",
        "responses": [
            {"question": "What's your name?", "answer": "John Doe"},
            {"question": "What's your email?", "answer": "john@example.com"}
        ]
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/conversations/{created_conversation_id}",
            json=update_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success(f"PUT /api/conversations/{created_conversation_id} - Conversation updated successfully")
                test_results["passed"] += 1
            else:
                print_error(f"PUT /api/conversations/{created_conversation_id} - Update failed: {data}")
                test_results["failed"] += 1
                test_results["errors"].append("Conversation update response indicates failure")
        else:
            print_error(f"PUT /api/conversations/{created_conversation_id} - Status code: {response.status_code}")
            test_results["failed"] += 1
            test_results["errors"].append(f"Conversation update failed with status {response.status_code}")
    except Exception as e:
        print_error(f"PUT /api/conversations/{created_conversation_id} - Error: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"Conversation update error: {str(e)}")

def test_delete_chatbot():
    """Test deleting chatbot"""
    global created_chatbot_id
    print_test_header("Delete Chatbot")
    
    if not created_chatbot_id:
        print_warning("No chatbot ID available, skipping test")
        return
    
    try:
        response = requests.delete(f"{BASE_URL}/api/chatbots/{created_chatbot_id}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success(f"DELETE /api/chatbots/{created_chatbot_id} - Chatbot deleted successfully")
                test_results["passed"] += 1
            else:
                print_error(f"DELETE /api/chatbots/{created_chatbot_id} - Delete failed: {data}")
                test_results["failed"] += 1
                test_results["errors"].append("Chatbot deletion response indicates failure")
        else:
            print_error(f"DELETE /api/chatbots/{created_chatbot_id} - Status code: {response.status_code}")
            test_results["failed"] += 1
            test_results["errors"].append(f"Chatbot deletion failed with status {response.status_code}")
    except Exception as e:
        print_error(f"DELETE /api/chatbots/{created_chatbot_id} - Error: {str(e)}")
        test_results["failed"] += 1
        test_results["errors"].append(f"Chatbot deletion error: {str(e)}")

def print_test_summary():
    """Print final test summary"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}TEST SUMMARY{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    
    total_tests = test_results["passed"] + test_results["failed"]
    print(f"Total Tests: {total_tests}")
    print(f"{Colors.GREEN}Passed: {test_results['passed']}{Colors.ENDC}")
    print(f"{Colors.RED}Failed: {test_results['failed']}{Colors.ENDC}")
    
    if test_results["failed"] > 0:
        print(f"\n{Colors.RED}{Colors.BOLD}ERRORS ENCOUNTERED:{Colors.ENDC}")
        for i, error in enumerate(test_results["errors"], 1):
            print(f"{Colors.RED}{i}. {error}{Colors.ENDC}")
    
    success_rate = (test_results["passed"] / total_tests * 100) if total_tests > 0 else 0
    print(f"\n{Colors.BOLD}Success Rate: {success_rate:.1f}%{Colors.ENDC}")
    
    if test_results["failed"] == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}ALL TESTS PASSED!{Colors.ENDC}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}SOME TESTS FAILED{Colors.ENDC}")

def main():
    """Run all tests"""
    print(f"{Colors.BOLD}Starting Fobi.io Clone Backend API Tests{Colors.ENDC}")
    print(f"Backend URL: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests in order
    test_health_endpoints()
    test_global_stats()
    test_create_chatbot()
    test_invalid_google_form_url()
    test_get_all_chatbots()
    test_get_chatbot_by_id()
    test_get_nonexistent_chatbot()
    test_get_chatbot_stats()
    test_update_chatbot()
    test_create_conversation()
    test_update_conversation()
    test_delete_chatbot()
    
    # Print summary
    print_test_summary()
    
    # Exit with appropriate code
    sys.exit(0 if test_results["failed"] == 0 else 1)

if __name__ == "__main__":
    main()