#!/usr/bin/env python3
"""
Simple VNC test script to verify VNC connection is working

This script opens a simple browser window that you should be able to see via VNC
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def test_vnc_browser():
    print("🔧 Setting up Chrome for VNC testing...")
    
    options = Options()
    # Remove headless for visual mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1200,800')
    options.add_argument('--disable-extensions')
    
    service = Service('/usr/local/bin/chromedriver')
    
    print("🌐 Starting Chrome browser...")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        print("📱 Navigating to test page...")
        driver.get('https://www.google.com')
        
        print("✅ Browser should now be visible in VNC!")
        print("🎯 You should see Google homepage in your VNC client")
        print("⏰ Browser will stay open for 30 seconds...")
        
        # Keep browser open for viewing
        time.sleep(30)
        
        print("🔄 Navigating to another page...")
        driver.get('https://httpbin.org/html')
        
        print("⏰ Staying on second page for 20 seconds...")
        time.sleep(20)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("🏁 Closing browser...")
        driver.quit()
        print("✅ VNC test completed!")

if __name__ == "__main__":
    print("🧪 VNC Browser Test Starting...")
    print("👀 Make sure your VNC client is connected to localhost:5900")
    print("-" * 50)
    test_vnc_browser()
