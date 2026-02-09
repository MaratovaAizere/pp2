#functions syntax
def my_function():
    print("Hello from a function")
#to call it we use
my_function()
#we can call it as many times as we want
my_function()
my_function()
#rule names for functions is the same as for variable
#instead if suing:
temp1 = 77
celsius1 = (temp1 - 32) * 5 / 9
print(celsius1)

temp2 = 95
celsius2 = (temp2 - 32) * 5 / 9
print(celsius2)

temp3 = 50
celsius3 = (temp3 - 32) * 5 / 9
print(celsius3)

#we can write a function

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))

#return using to stop functuion and return some value
def get_greeting():
    return "Hello from a function"

message = get_greeting()
print(message)

#function must be filled with smh
#use pass to fill it and let this func do nothin
def my_function():
    pass
    