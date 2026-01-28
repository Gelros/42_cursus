import sys

def ft_inventory_system() -> None:
    print("=== Inventory System Analysis ===")
    inventory = dict()
    n_item = 0
    for p in sys.argv[1:]:
        part = p.split(":")
        key = part[0]
        val = int(part[1])
        n_item += val
        inventory.update({key: val})
    len_inventory = len(inventory)
    print("Total items in inventory:",n_item)
    print("Unique item types:", len_inventory)
        
    print("\n=== Current Inventory ===")
    for key, number in inventory.items():
        percent = float(number / n_item * 100)
        print(f"{key}: {number} units ({percent:.1f}%)")
        
    print("\n=== Inventory Statistics ===")
    max_val = max(inventory.values())
    min_val = min(inventory.values())
    for key, val in inventory.items():
        if val == max_val:
            print(f"Most abundant: {key} {val} units")
            break
    for key, val in inventory.items():
        if val == min_val:
            print(f"Least abundant: {key} {val} units")
            break
    
    print("\n=== Item Categories ===")
    common = dict()
    rare = dict()
    for key, val in inventory.items():
        if key == "sword" or key == "shield" or key == "armor" or key == "helmet":
            rare.update({key: val})
        else:
            common.update({key: val})
    print(f"Moderate: {common}")
    print(f"Scarce: {rare}")
    
    print("\n=== Management Suggestions ===")
    restock = []
    dict_key = []
    dict_val = []
    for key, val in inventory.items():
        if val <= 1:
            restock.append(key)
        dict_key.append(key)
        dict_val.append(val)
    print("Restock needed:",restock)
    
    print("\n=== Dictionary Properties Demo ===")
    print(f"Dictionary keys: {dict_key}")
    print(f"Dictionary values: {dict_val}")
    lookup = "sword"
    is_here = lookup in inventory
    print(f"Sample lookup - '{lookup}' in inventory: {is_here}")
    
if __name__ == "__main__":
    ft_inventory_system()