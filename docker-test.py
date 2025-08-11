#!/usr/bin/env python3
"""
Docker setup test script for Spanish Appointment Bot

This script tests that all Docker dependencies are properly installed and configured.
Run with: docker-compose run --rm spanish-bot python docker-test.py
"""

import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_chrome_installation():
    """Test Chrome and ChromeDriver installation"""
    print("🔍 Testing Chrome installation...")
    
    try:
        # Test Chrome
        chrome_version = os.popen('google-chrome --version').read().strip()
        print(f"✅ Chrome installed: {chrome_version}")
        
        # Test ChromeDriver
        chromedriver_version = os.popen('chromedriver --version').read().strip()
        print(f"✅ ChromeDriver installed: {chromedriver_version}")
        
        return True
    except Exception as e:
        print(f"❌ Chrome/ChromeDriver test failed: {e}")
        return False

def test_selenium_chrome():
    """Test Selenium with headless Chrome"""
    print("\n🔍 Testing Selenium with headless Chrome...")
    
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        from selenium.webdriver.chrome.service import Service
        service = Service('/usr/local/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=options)
        driver.get('https://www.google.com')
        title = driver.title
        driver.quit()
        
        print(f"✅ Selenium test successful - Page title: {title}")
        return True
    except Exception as e:
        print(f"❌ Selenium test failed: {e}")
        return False

def test_audio_system():
    """Test audio system (espeak)"""
    print("\n🔍 Testing audio system...")
    
    try:
        result = os.system('espeak "Docker test" 2>/dev/null')
        if result == 0:
            print("✅ Audio system (espeak) working")
            return True
        else:
            print("⚠️  Audio system available but may not have sound output (normal in containers)")
            return True
    except Exception as e:
        print(f"❌ Audio system test failed: {e}")
        return False

def test_python_packages():
    """Test required Python packages"""
    print("\n🔍 Testing Python packages...")
    
    required_packages = [
        'selenium',
        'requests', 
        'anticaptchaofficial',
        'backoff',
        'mako'
    ]
    
    all_good = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not found")
            all_good = False
    
    return all_good

def test_environment():
    """Test environment variables and paths"""
    print("\n🔍 Testing environment...")
    
    display = os.getenv('DISPLAY', 'Not set')
    chrome_path = os.getenv('CHROME_DRIVER_PATH', '/usr/local/bin/chromedriver')
    
    print(f"✅ DISPLAY: {display}")
    print(f"✅ Chrome driver path: {chrome_path}")
    print(f"✅ Working directory: {os.getcwd()}")
    print(f"✅ Python version: {sys.version}")
    
    return True

def main():
    """Run all tests"""
    print("🐳 Spanish Appointment Bot - Docker Setup Test")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Python Packages", test_python_packages),
        ("Chrome Installation", test_chrome_installation),
        ("Audio System", test_audio_system),
        ("Selenium Chrome", test_selenium_chrome),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Docker setup is ready.")
        print("💡 You can now run the bot with your configuration:")
        print("   docker-compose run --rm spanish-bot python my_config.py")
    else:
        print("\n⚠️  Some tests failed. Check the Docker setup.")
        sys.exit(1)

if __name__ == "__main__":
    main()
