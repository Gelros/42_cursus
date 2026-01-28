import sys, math

def coordinate_sys() -> None:
    print ("=== Game Coordinate System ===\n")
    
    pos1 = (10, 20, 5)
    print(f"Position created: {pos1}")
    pos2 = (0, 0, 0)
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    print(f"Distance between: {pos2} and {pos1}: {dist:.2f}")
    
    try:
        no_pars = "3,4,0"
        pars = no_pars.split(",")
        pos1 = int(pars[0]), int(pars[1]), int(pars[2])
        print(f'\nParsing coordinates: "{no_pars}"')
        print(f"Parsed position: {pos1}")
        pos2 = (0, 0, 0)
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        print(f"Distance between: {pos2} and {pos1}: {dist:.2f}")
        
        no_pars2 = "abc,ft,sjf"
        pars2 = no_pars2.split(",")
        pos1_ = int(pars2[0]), int(pars2[1]), int(pars2[2])
    except ValueError as e:
        print(f'\nParsing invalid coordinates: "{no_pars2}"')
        print("Error parsing coordinates:", e)
        print(f"Error details - Type: {type(e).__name__}, Args: {e.args}\n")
    
    print("Unpacking demonstration:")
    print(f"Player at x={x1}, y={y1}, z={z1}")
    print(f"Coordinates: X={x1}, Y={y1}, Z={z1}")

if __name__ == "__main__":
    coordinate_sys()