def ft_water_reminder():
    time = int(input("Days since last watering: "))
    if time > 2:
        print("Water the plants!")
    else:
        print("Plants are fine")
ft_water_reminder()