"""
End-to-end test for the RAG chatbot integration.
This script tests the complete flow from question input to UI display.
"""
import asyncio
import json
import requests
import time
from typing import Dict, Any

def test_api_health():
    """Test that the API health endpoint is working."""
    print("Testing API health endpoint...")
    try:
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check passed: {data}")
            return True
        else:
            print(f"✗ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check failed with error: {e}")
        return False

def test_query_endpoint():
    """Test the query endpoint with a sample question."""
    print("\nTesting query endpoint...")
    try:
        # Sample query
        payload = {
            "query": "What is humanoid robotics?",
            "context_mode": "full_book"
        }

        response = requests.post(
            "http://localhost:8000/api/query",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✓ Query successful: Response length = {len(data.get('response', ''))} chars")
            print(f"  Processing time: {data.get('processing_time', 0):.2f}s")
            print(f"  Sources found: {len(data.get('sources', []))}")
            return True
        else:
            print(f"✗ Query failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Query failed with error: {e}")
        return False

def test_selected_text_query():
    """Test the query endpoint with selected text context."""
    print("\nTesting selected text query...")
    try:
        # Sample query with selected text
        payload = {
            "query": "Explain this concept",
            "selected_text": "Humanoid robotics is a branch of robotics focused on creating robots that resemble humans in form and behavior.",
            "context_mode": "selected_text"
        }

        response = requests.post(
            "http://localhost:8000/api/query",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✓ Selected text query successful: Response length = {len(data.get('response', ''))} chars")
            print(f"  Processing time: {data.get('processing_time', 0):.2f}s")
            print(f"  Sources found: {len(data.get('sources', []))}")
            return True
        else:
            print(f"✗ Selected text query failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Selected text query failed with error: {e}")
        return False

def test_context_mode_switching():
    """Test switching between different context modes."""
    print("\nTesting context mode switching...")
    try:
        # Test full_book mode
        payload1 = {
            "query": "What is AI?",
            "context_mode": "full_book"
        }

        response1 = requests.post(
            "http://localhost:8000/api/query",
            json=payload1,
            headers={"Content-Type": "application/json"}
        )

        success1 = response1.status_code == 200
        if success1:
            print("✓ Full book context mode works")
        else:
            print(f"✗ Full book context mode failed: {response1.status_code}")

        # Test selected_text mode
        payload2 = {
            "query": "What does this mean?",
            "selected_text": "Machine learning is a subset of artificial intelligence.",
            "context_mode": "selected_text"
        }

        response2 = requests.post(
            "http://localhost:8000/api/query",
            json=payload2,
            headers={"Content-Type": "application/json"}
        )

        success2 = response2.status_code == 200
        if success2:
            print("✓ Selected text context mode works")
        else:
            print(f"✗ Selected text context mode failed: {response2.status_code}")

        return success1 and success2
    except Exception as e:
        print(f"✗ Context mode switching test failed with error: {e}")
        return False

def test_communication_reliability():
    """Test communication reliability under various conditions."""
    print("\nTesting communication reliability...")
    try:
        # Test multiple rapid requests to check for stability
        success_count = 0
        total_tests = 5

        for i in range(total_tests):
            payload = {
                "query": f"Test query {i+1} for reliability",
                "context_mode": "full_book"
            }

            try:
                response = requests.post(
                    "http://localhost:8000/api/query",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30  # 30 second timeout
                )

                if response.status_code == 200:
                    success_count += 1
                    print(f"  Request {i+1}: ✓ Success")
                else:
                    print(f"  Request {i+1}: ✗ Failed with status {response.status_code}")
            except requests.exceptions.Timeout:
                print(f"  Request {i+1}: ✗ Timeout")
            except requests.exceptions.RequestException as e:
                print(f"  Request {i+1}: ✗ Error - {e}")

        success_rate = success_count / total_tests
        print(f"Reliability test: {success_count}/{total_tests} successful ({success_rate*100:.1f}%)")

        # Consider it passing if at least 80% succeed
        return success_rate >= 0.8

    except Exception as e:
        print(f"✗ Communication reliability test failed with error: {e}")
        return False

def run_end_to_end_tests():
    """Run all end-to-end tests."""
    print("Starting end-to-end tests for RAG Chatbot Integration...\n")

    tests = [
        ("API Health Check", test_api_health),
        ("Full Book Query", test_query_endpoint),
        ("Selected Text Query", test_selected_text_query),
        ("Context Mode Switching", test_context_mode_switching),
        ("Communication Reliability", test_communication_reliability),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)  # Brief pause between tests

    print(f"\n{'='*50}")
    print("END-TO-END TEST RESULTS:")
    print(f"{'='*50}")

    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False

    print(f"\nOverall result: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    return all_passed

if __name__ == "__main__":
    run_end_to_end_tests()