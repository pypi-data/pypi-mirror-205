def sim():
    x = int(input("Enter the first number: "))
    y = int(input("Enter the second number: "))
    math_type = input("Press 0 to add or 1 to multiply: ")
    if math_type == 0:
        return x+y
    elif math_type == 1:
        return x*y

# def main():
#    print("Hi")
# if __name__ == '__main__':
#    main()
