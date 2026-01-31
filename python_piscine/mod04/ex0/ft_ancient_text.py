def main():
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")
    
    filename = "ancient_fragment.txt"
    
    try:
        file = open(filename, 'r')
        
        print(f"Accessing Storage Vault: {filename}")
        print("Connection established...")
        print()
        print("RECOVERED DATA:")
        
        content = file.read()
        print(content)
        
        file.close()
        
        print("\nData recovery complete. Storage unit disconnected.")
        
    except FileNotFoundError:
        print("ERROR: Storage vault not found. Run data generator first.")

if __name__ == "__main__":
    main()