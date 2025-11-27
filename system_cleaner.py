"""
System Cleaner Script
Clears temporary files, prefetch files, and empties the recycle bin.
Run as Administrator for full access to prefetch folder.
"""

import os
import shutil
import ctypes
import subprocess
import tempfile
from pathlib import Path

def is_admin():
    """Check if script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def clear_folder(folder_path, folder_name):
    """Clear all files and folders in the specified directory."""
    deleted_count = 0
    error_count = 0
    
    if not os.path.exists(folder_path):
        print(f"[!] {folder_name} folder not found: {folder_path}")
        return
    
    print(f"\n[*] Cleaning {folder_name}: {folder_path}")
    
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
                deleted_count += 1
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                deleted_count += 1
        except PermissionError:
            error_count += 1
        except Exception as e:
            error_count += 1
    
    print(f"    [+] Deleted: {deleted_count} items")
    if error_count > 0:
        print(f"    [-] Skipped (in use): {error_count} items")

def clear_temp_folder():
    """Clear the Windows temporary folder."""
    temp_path = tempfile.gettempdir()  # Usually C:\Users\<user>\AppData\Local\Temp
    clear_folder(temp_path, "Temp")

def clear_windows_temp():
    """Clear the Windows\Temp folder."""
    windows_temp = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Temp')
    clear_folder(windows_temp, "Windows Temp")

def clear_prefetch():
    """Clear the Windows prefetch folder (requires admin)."""
    prefetch_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Prefetch')
    
    if not is_admin():
        print(f"\n[!] Prefetch folder requires Administrator privileges.")
        print(f"    Skipping: {prefetch_path}")
        return
    
    clear_folder(prefetch_path, "Prefetch")

def empty_recycle_bin():
    """Empty the Windows Recycle Bin."""
    print("\n[*] Emptying Recycle Bin...")
    try:
        # Use SHEmptyRecycleBin from shell32.dll
        # Flags: SHERB_NOCONFIRMATION = 0x1, SHERB_NOPROGRESSUI = 0x2, SHERB_NOSOUND = 0x4
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x7)
        print("    [+] Recycle Bin emptied successfully!")
    except Exception as e:
        print(f"    [-] Error emptying Recycle Bin: {e}")

def get_folder_size(folder_path):
    """Calculate total size of a folder in bytes."""
    total_size = 0
    if os.path.exists(folder_path):
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total_size += os.path.getsize(fp)
                except:
                    pass
    return total_size

def format_size(size_bytes):
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

def main():
    print("=" * 50)
    print("       SYSTEM CLEANER - Temp & Cache Cleaner")
    print("=" * 50)
    
    if is_admin():
        print("[+] Running with Administrator privileges")
    else:
        print("[!] Running without Administrator privileges")
        print("    (Run as Admin to clean Prefetch folder)")
    
    # Get folder paths
    temp_path = tempfile.gettempdir()
    windows_temp = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Temp')
    prefetch_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Prefetch')
    
    # Calculate sizes before cleaning
    print("\n[*] Calculating space to be freed...")
    temp_size = get_folder_size(temp_path)
    win_temp_size = get_folder_size(windows_temp)
    prefetch_size = get_folder_size(prefetch_path) if is_admin() else 0
    
    print(f"    Temp folder: {format_size(temp_size)}")
    print(f"    Windows Temp: {format_size(win_temp_size)}")
    if is_admin():
        print(f"    Prefetch: {format_size(prefetch_size)}")
    
    total_before = temp_size + win_temp_size + prefetch_size
    print(f"\n    Total to clean: {format_size(total_before)}")
    
    # Perform cleaning
    print("\n" + "-" * 50)
    print("Starting cleanup...")
    print("-" * 50)
    
    clear_temp_folder()
    clear_windows_temp()
    clear_prefetch()
    empty_recycle_bin()
    
    print("\n" + "=" * 50)
    print("       CLEANUP COMPLETE!")
    print("=" * 50)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
