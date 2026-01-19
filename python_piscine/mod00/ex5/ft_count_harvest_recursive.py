def ft_count_harvest_recursive(x):
    if x == -1:
        x = int(input("Days until harvest: "))
    if x > 0:
        ft_count_harvest_recursive(x - 1)
        print("day", x)
    else:
        print("Harvest time!")

ft_count_harvest_recursive(-1)
