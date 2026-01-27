#Data types

x = "Hello World"	# str	
x = 20	# int	
x = 20.5	# float	
x = 1j	# complex	
x = ["apple", "banana", "cherry"]	# list	
x = ("apple", "banana", "cherry")	# tuple	
x = range(6)	# range	
x = {"name" : "John", "age" : 36}	# dict	
x = {"apple", "banana", "cherry"}	# set	
x = frozenset({"apple", "banana", "cherry"})	# frozenset	
x = True	# bool	
x = b"Hello"	# bytes	
x = bytearray(5)	# bytearray	
x = memoryview(bytes(5))	# memoryview	
x = None	# NoneType

# To check the data type of a variable

print(type(x))

# Setting the specific data type

x = str("Hello World")
x = int(20)
x = float(20.5)
x = complex(1j)
x = list(("apple", "banana", "cherry"))
x = tuple(("apple", "banana", "cherry"))	
x = range(6)	
x = dict(name="John", age=36)	
x = set(("apple", "banana", "cherry"))	
x = frozenset(("apple", "banana", "cherry"))
x = bool(5)
x = bytes(5)	
x = bytearray(5)	
x = memoryview(bytes(5))