#!/usr/bin/env python3
"""
Visual configuration file for Spanish Appointment Bot in Docker with VNC

This configuration runs Chrome in visual mode so you can watch the process via VNC.
Copy this file to my_config_visual.py and customize with your real data.

To use:
1. Build VNC image: docker build -f Dockerfile.vnc -t spanish-bot-vnc .
2. Run with VNC: docker run -p 5900:5900 -v $(pwd)/my_config_visual.py:/app/my_config_visual.py spanish-bot-vnc python my_config_visual.py
3. Connect VNC client to localhost:5900 to watch
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bcncita import CustomerProfile, DocType, Office, OperationType, Province, start_with

def init_visual_webdriver(context):
    """Custom webdriver initialization for visual mode"""
    options = Options()
    
    # Visual mode - remove headless option
    # options.add_argument('--headless')  # Commented out for visual mode
    
    # Essential Chrome options for container
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280,720')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')  # Faster loading
    
    # User agent
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
    options.add_argument(f'--user-agent={ua}')
    
    # Create service
    service = Service('/usr/local/bin/chromedriver')
    
    print("🌐 Starting Chrome in VISUAL mode...")
    print("👀 You should see the browser window in your VNC client!")
    
    browser = webdriver.Chrome(service=service, options=options)
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return browser

if __name__ == "__main__":
    # Get environment variables if available
    anticaptcha_key = os.getenv('ANTICAPTCHA_API_KEY', 'your_key_here')
    sms_webhook = os.getenv('SMS_WEBHOOK_TOKEN', '')
    
    customer = CustomerProfile(
        # REQUIRED: Your personal information
        name="YOUR FULL NAME",  # Replace with your actual name
        doc_type=DocType.NIE,  # DocType.NIE, DocType.PASSPORT, or DocType.DNI
        doc_value="Y1234567Z",  # Replace with your actual document number
        phone="600000000",  # Replace with your actual phone number
        email="your.email@example.com",  # Replace with your actual email
        
        # Location and operation settings
        province=Province.BARCELONA,  # Change to your province
        operation_code=OperationType.TOMA_HUELLAS,  # Change to your operation type
        country="ESPAÑA",  # Change to your country
        year_of_birth="1990",  # Replace with your birth year (if required)
        
        # Office preferences (optional)
        offices=[Office.BARCELONA, Office.MATARO],  # Preferred offices in order
        except_offices=[],  # Offices to avoid
        
        # Anti-captcha settings
        anticaptcha_api_key=anticaptcha_key,
        auto_captcha=False,  # Set to False for visual mode to manually solve captcha
        
        # Automation settings
        auto_office=True,
        chrome_driver_path="/usr/local/bin/chromedriver",  # Docker path
        save_artifacts=True,  # Save screenshots in /app/artifacts
        
        # SMS automation (optional)
        sms_webhook_token=sms_webhook if sms_webhook else None,
        
        # Date/time constraints (optional)
        min_date=None,  # "dd/mm/yyyy" format
        max_date=None,  # "dd/mm/yyyy" format
        min_time=None,  # "hh:mm" format
        max_time=None,  # "hh:mm" format
        
        # Timing settings (optional)
        wait_exact_time=None,  # [[minute, second]] to hit submit at exact time
        
        # Reason (required for some operations like asylum)
        reason_or_type="solicitud de asilo",  # Adjust based on your operation
    )
    
    print("🎬 Starting Spanish Appointment Bot in VISUAL mode...")
    print(f"Operation: {customer.operation_code}")
    print(f"Province: {customer.province}")
    print(f"Document: {customer.doc_type} - {customer.doc_value}")
    print("👁️  Visual mode enabled - you can watch the browser!")
    print("🔗 Connect your VNC client to localhost:5900")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Use custom visual webdriver
        driver = init_visual_webdriver(customer)
        start_with(driver, customer, cycles=200)  # Try 200 times
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
        print("Check your configuration and try again.")
