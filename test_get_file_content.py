from functions.get_file_content import get_file_content

strin = get_file_content("calculator", "short_lorem.txt")
leng = len(strin)


print(f"aaaaand the length is {leng}")
print(strin)


a = get_file_content("calculator", "main.py")
b = get_file_content("calculator", "pkg/calculator.py")
c = get_file_content("calculator", "/bin/cat") 
d = get_file_content("calculator", "pkg/does_not_exist.py")

print(f"Length of a is:{len(a)}")
print(a)

print(f"Length of b is:{len(b)}")
print(b)

print(f"Length of c is:{len(c)}")
print(c)

print(f"Length of d is:{len(d)}")
print(d)