"""
Test script for Web Research Assistant API
==========================================
"""

import requests
import json
import time

# API configuration
API_BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test API health endpoint"""
    print("🏥 Testing API health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API is healthy")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure it's running on http://localhost:8000")
        return False

def test_sample_queries():
    """Test sample queries endpoint"""
    print("\n📝 Testing sample queries...")
    try:
        response = requests.get(f"{API_BASE_URL}/research/samples")
        if response.status_code == 200:
            data = response.json()
            print("✅ Sample queries retrieved")
            print(f"   Available samples: {len(data['sample_queries'])}")
            for i, query in enumerate(data['sample_queries'][:3], 1):
                print(f"   {i}. {query}")
            return True
        else:
            print(f"❌ Sample queries failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_research_endpoint():
    """Test research endpoint with a simple query"""
    print("\n🔬 Testing research endpoint...")
    
    # Test query
    test_query = "Latest developments in artificial intelligence 2024"
    
    payload = {
        "query": test_query,
        "thread_id": f"test_{int(time.time())}"
    }
    
    print(f"   Query: {test_query}")
    print("   Starting research...")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}/research",
            json=payload,
            timeout=300  # 5 minute timeout
        )
        processing_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Research completed in {processing_time:.2f} seconds")
            
            if data["success"]:
                result = data["data"]
                print(f"   Sources found: {result['sources_found']}")
                print(f"   Pages processed: {result['pages_processed']}")
                print(f"   Report length: {result['report_length']} characters")
                print(f"   Citations: {len(result['citations'])}")
                
                # Show first 200 characters of report
                report_preview = result['report'][:200] + "..." if len(result['report']) > 200 else result['report']
                print(f"\n   📊 Report Preview:")
                print(f"   {report_preview}")
                
                return True
            else:
                print(f"❌ Research failed: {data['error']}")
                return False
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (5 minutes)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_sessions_endpoint():
    """Test sessions management endpoints"""
    print("\n📚 Testing sessions endpoints...")
    try:
        # List sessions
        response = requests.get(f"{API_BASE_URL}/research/sessions")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sessions listed: {data['total_sessions']} total")
            return True
        else:
            print(f"❌ Sessions listing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all API tests"""
    print("🧪 Web Research Assistant API Test Suite")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_api_health),
        ("Sample Queries", test_sample_queries),
        ("Research Endpoint", test_research_endpoint),
        ("Sessions Management", test_sessions_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API setup.")

if __name__ == "__main__":
    main()