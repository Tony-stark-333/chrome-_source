#!/usr/bin/env python3
"""
Email Service Diagnosis for Vian Scientific Platform
Comprehensive diagnosis of Gmail SMTP authentication issues
"""

import os
import smtplib
from dotenv import load_dotenv

def diagnose_email_service():
    """Diagnose email service configuration and connectivity"""
    
    print("📧 EMAIL SERVICE DIAGNOSIS")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv('/app/backend/.env')
    
    host = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    port = int(os.getenv('EMAIL_PORT', '587'))
    username = os.getenv('EMAIL_USERNAME')
    password = os.getenv('EMAIL_PASSWORD')
    
    print(f"📋 Configuration:")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Username: {username}")
    print(f"   Password: {'*' * len(password) if password else 'NOT SET'}")
    print(f"   Password Length: {len(password) if password else 0}")
    print()
    
    # Test 1: Basic connectivity
    print("🔍 Test 1: SMTP Server Connectivity")
    try:
        with smtplib.SMTP(host, port) as server:
            print("   ✅ Successfully connected to SMTP server")
            
            # Test EHLO
            code, message = server.ehlo()
            print(f"   ✅ EHLO successful: {code}")
            
            # Test STARTTLS
            server.starttls()
            print("   ✅ TLS connection established")
            
            # Test EHLO after TLS
            code, message = server.ehlo()
            print(f"   ✅ EHLO after TLS successful: {code}")
            
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False
    
    print()
    
    # Test 2: Authentication
    print("🔐 Test 2: SMTP Authentication")
    try:
        with smtplib.SMTP(host, port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            
            # Try authentication
            server.login(username, password)
            print("   ✅ Authentication successful!")
            return True
            
    except smtplib.SMTPAuthenticationError as e:
        print(f"   ❌ Authentication failed: {e}")
        
        # Analyze the error
        error_str = str(e)
        if "535" in error_str and "BadCredentials" in error_str:
            print("\n🚨 DIAGNOSIS: Gmail App Password Required")
            print("   The error indicates Gmail is rejecting the credentials.")
            print("   This typically happens when:")
            print("   1. The Gmail account has 2FA (Two-Factor Authentication) enabled")
            print("   2. You're using a regular password instead of an App Password")
            print("   3. 'Less secure app access' is disabled (default for new accounts)")
            print()
            print("🔧 SOLUTION:")
            print("   1. Enable 2FA on the Gmail account if not already enabled")
            print("   2. Generate an App Password:")
            print("      - Go to Google Account settings")
            print("      - Security > 2-Step Verification > App passwords")
            print("      - Generate a new app password for 'Mail'")
            print("   3. Replace EMAIL_PASSWORD in .env with the App Password")
            print("   4. App passwords are 16 characters without spaces")
            print()
            print("📝 Current password analysis:")
            print(f"   - Length: {len(password)} characters")
            print(f"   - Format: {'Looks like regular password' if len(password) < 16 else 'Could be App Password'}")
            
        elif "334" in error_str:
            print("\n🚨 DIAGNOSIS: SMTP Authentication Sequence Issue")
            print("   The server is asking for password but authentication is failing.")
            
        return False
        
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_email_service_integration():
    """Test the email service integration"""
    print("\n🧪 Test 3: Email Service Integration")
    
    try:
        import sys
        sys.path.append('/app/backend')
        from email_service import email_service
        
        print("   ✅ Email service module imported successfully")
        
        # Test configuration loading
        if hasattr(email_service, 'username') and email_service.username:
            print(f"   ✅ Email service configured with username: {email_service.username}")
        else:
            print("   ❌ Email service not properly configured")
            return False
            
        # Test email sending (dry run)
        print("   📤 Testing email sending capability...")
        
        # This will fail but we can catch the specific error
        result = email_service.send_welcome_email("test@example.com", "Test User")
        
        if result:
            print("   ✅ Email service is working!")
            return True
        else:
            print("   ❌ Email service failed (expected due to authentication issue)")
            return False
            
    except Exception as e:
        print(f"   ❌ Integration test failed: {e}")
        return False

def main():
    """Run complete email service diagnosis"""
    
    connectivity_ok = diagnose_email_service()
    integration_ok = test_email_service_integration()
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSIS SUMMARY")
    print("=" * 50)
    
    if connectivity_ok:
        print("✅ SMTP connectivity: WORKING")
        print("✅ Email service: READY TO USE")
        print("\n🎉 Email service is fully functional!")
    else:
        print("❌ SMTP authentication: FAILED")
        print("❌ Email service: NOT WORKING")
        print("\n🔧 Action required: Fix Gmail App Password configuration")
        print("\n📋 Next Steps:")
        print("1. Generate Gmail App Password (see instructions above)")
        print("2. Update EMAIL_PASSWORD in /app/backend/.env")
        print("3. Restart the backend service")
        print("4. Re-run this diagnosis")
    
    return connectivity_ok

if __name__ == "__main__":
    main()