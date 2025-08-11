#!/usr/bin/env python3
"""
Example configuration file for Spanish Appointment Bot in Docker

Copy this file to my_config.py and customize with your real data.
Then run: docker-compose run --rm spanish-bot python my_config.py
"""

import os
from bcncita import CustomerProfile, DocType, Office, OperationType, Province, try_cita

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
        auto_captcha=True if anticaptcha_key != 'your_key_here' else False,
        
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
    
    print("Starting Spanish Appointment Bot...")
    print(f"Operation: {customer.operation_code}")
    print(f"Province: {customer.province}")
    print(f"Document: {customer.doc_type} - {customer.doc_value}")
    print(f"Anti-captcha enabled: {customer.auto_captcha}")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        try_cita(context=customer, cycles=200)  # Try 200 times
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
        print("Check your configuration and try again.")

# Available Operation Types:
# OperationType.AUTORIZACION_DE_REGRESO
# OperationType.BREXIT  
# OperationType.CARTA_INVITACION
# OperationType.CERTIFICADOS_NIE
# OperationType.CERTIFICADOS_NIE_NO_COMUN
# OperationType.CERTIFICADOS_RESIDENCIA
# OperationType.CERTIFICADOS_UE
# OperationType.RECOGIDA_DE_TARJETA
# OperationType.SOLICITUD_ASILO
# OperationType.TOMA_HUELLAS
# OperationType.ASIGNACION_NIE
# OperationType.FINGERP_RINT

# Available Provinces:
# Province.BARCELONA, Province.MADRID, Province.VALENCIA, etc.
# See bcncita/cita.py for complete list

# Available Offices (Barcelona example):
# Office.BARCELONA, Office.MATARO, Office.SABADELL, etc.
# See bcncita/cita.py for complete list
