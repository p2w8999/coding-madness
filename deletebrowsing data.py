import os
import sqlite3
import shutil
from datetime import datetime

def delete_chrome_history():
    """Delete Chrome browsing history"""
    chrome_paths = [
        os.path.expanduser('~') + '/AppData/Local/Google/Chrome/User Data/Default/History',
        os.path.expanduser('~') + '/Library/Application Support/Google/Chrome/Default/History',
        os.path.expanduser('~') + '/.config/google-chrome/Default/History'
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            try:
                # Chrome locks the database while running, so we need to copy it first
                temp_path = path + '_temp'
                shutil.copy2(path, temp_path)
                
                conn = sqlite3.connect(temp_path)
                cursor = conn.cursor()
                
                # Delete URLs and visits
                cursor.execute("DELETE FROM urls")
                cursor.execute("DELETE FROM visits")
                cursor.execute("DELETE FROM keyword_search_terms")
                
                conn.commit()
                conn.close()
                
                # Replace the original file
                shutil.move(temp_path, path)
                print(f"Chrome history deleted successfully")
                return True
            except Exception as e:
                print(f"Error deleting Chrome history: {e}")
                return False
    return False

def delete_firefox_history():
    """Delete Firefox browsing history"""
    firefox_paths = [
        os.path.expanduser('~') + '/AppData/Local/Mozilla/Firefox/Profiles',
        os.path.expanduser('~') + '/Library/Application Support/Firefox/Profiles',
        os.path.expanduser('~') + '/.mozilla/firefox'
    ]
    
    for base_path in firefox_paths:
        if os.path.exists(base_path):
            for profile in os.listdir(base_path):
                if profile.endswith('.default') or profile.endswith('.default-release'):
                    places_path = os.path.join(base_path, profile, 'places.sqlite')
                    if os.path.exists(places_path):
                        try:
                            # Firefox locks the database while running
                            temp_path = places_path + '_temp'
                            shutil.copy2(places_path, temp_path)
                            
                            conn = sqlite3.connect(temp_path)
                            cursor = conn.cursor()
                            
                            # Delete history entries
                            cursor.execute("DELETE FROM moz_places")
                            cursor.execute("DELETE FROM moz_historyvisits")
                            cursor.execute("DELETE FROM moz_inputhistory")
                            
                            conn.commit()
                            conn.close()
                            
                            # Replace the original file
                            shutil.move(temp_path, places_path)
                            print(f"Firefox history deleted successfully")
                            return True
                        except Exception as e:
                            print(f"Error deleting Firefox history: {e}")
                            return False
    return False

def delete_edge_history():
    """Delete Microsoft Edge browsing history"""
    edge_paths = [
        os.path.expanduser('~') + '/AppData/Local/Microsoft/Edge/User Data/Default/History',
        os.path.expanduser('~') + '/Library/Application Support/Microsoft Edge/Default/History',
        os.path.expanduser('~') + '/.config/microsoft-edge/Default/History'
    ]
    
    for path in edge_paths:
        if os.path.exists(path):
            try:
                temp_path = path + '_temp'
                shutil.copy2(path, temp_path)
                
                conn = sqlite3.connect(temp_path)
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM urls")
                cursor.execute("DELETE FROM visits")
                
                conn.commit()
                conn.close()
                
                shutil.move(temp_path, path)
                print(f"Edge history deleted successfully")
                return True
            except Exception as e:
                print(f"Error deleting Edge history: {e}")
                return False
    return False

def delete_safari_history():
    """Delete Safari browsing history (macOS only)"""
    safari_path = os.path.expanduser('~') + '/Library/Safari/History.db'
    
    if os.path.exists(safari_path):
        try:
            temp_path = safari_path + '_temp'
            shutil.copy2(safari_path, temp_path)
            
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM history_items")
            cursor.execute("DELETE FROM history_visits")
            
            conn.commit()
            conn.close()
            
            shutil.move(temp_path, safari_path)
            print(f"Safari history deleted successfully")
            return True
        except Exception as e:
            print(f"Error deleting Safari history: {e}")
            return False
    return False

if __name__ == "__main__":
    print("Browser History Deletion Tool")
    print("=" * 30)
    
    print("\nSelect browser to clear history:")
    print("1. Chrome")
    print("2. Firefox")
    print("3. Edge")
    print("4. Safari")
    print("5. All browsers")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == "1":
        delete_chrome_history()
    elif choice == "2":
        delete_firefox_history()
    elif choice == "3":
        delete_edge_history()
    elif choice == "4":
        delete_safari_history()
    elif choice == "5":
        delete_chrome_history()
        delete_firefox_history()
        delete_edge_history()
        delete_safari_history()
    else:
        print("Invalid choice!")
