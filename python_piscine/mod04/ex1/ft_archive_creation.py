def main():
    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")
    filename = "new_discovery.txt"
    
    print(f"Initializing new storage unit: {filename}\n")
    file = open(filename, 'w')
    
    print("Storage unit created successfully...")
    print("Inscribing preservation data...\n")
    
    file.write("[ENTRY 001] New quantum algorithm discovered\n")
    print("[ENTRY 001] New quantum algorithm discovered")
    
    file.write("[ENTRY 002] Efficiency increased by 347%\n")
    print("[ENTRY 002] Efficiency increased by 347%")
    
    file.write("[ENTRY 003] Archived by Data Archivist trainee\n")
    print("[ENTRY 003] Archived by Data Archivist trainee")
    
    file.close()
    
    print("\nData inscription complete. Storage unit sealed.")
    print(f"Archive '{filename}' ready for long-term preservation.")

if __name__ == "__main__":
    main()