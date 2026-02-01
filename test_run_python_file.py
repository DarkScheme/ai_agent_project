from functions.run_python_file import run_python_file

a = run_python_file("calculator", "main.py")
print(a)

b = run_python_file("calculator", "main.py", ["3 + 5"])
print(b)

c = run_python_file("calculator", "tests.py")
print(c)

d = run_python_file("calculator", "../main.py")
print(d)

e = run_python_file("calculator", "nonexistent.py")
print(e)

f = run_python_file("calculator", "lorem.txt")
print(f)