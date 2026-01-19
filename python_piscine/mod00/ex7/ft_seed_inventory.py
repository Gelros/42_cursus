def ft_seed_inventory(seed_type:  str, quantity:  int, unit:  str) -> None:
    header = f"{seed_type.capitalize()} seeds:"
    
    if unit == "packets":
        print(f"{header} {quantity} packets available")
    elif unit == "grams":
        print(f"{header} {quantity} grams total")
    elif unit == "area":
        print(f"{header} covers {quantity} square meters")
    else:
        print("Unknown unit type")
ft_seed_inventory("carot", 3, "grams")