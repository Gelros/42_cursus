def main():
    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===\n")
    
    print("Initiating secure vault access...")
    print("Vault connection established with failsafe protocols\n")
    
    print("SECURE EXTRACTION:")
    with open("classified_data.txt", 'r') as vault:
        content = vault.read()
        print(content)
    
    print("\nSECURE PRESERVATION:")
    with open("security_protocol.txt", 'w') as vault:
        vault.write("[CLASSIFIED] New security protocols archived")
        print("[CLASSIFIED] New security protocols archived")
        print("Vault automatically sealed upon completion\n")
    
    print("All vault operations completed with maximum security.")
        
if __name__ == "__main__":
    main()