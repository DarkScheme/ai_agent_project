from functions.get_files_info import get_files_info

print("Result for current direcory:")
print(get_files_info("calculator", "."))


print("Result for 'pkg' direcory:")
print(get_files_info("calculator", "pkg"))


print("Result for '/bin' direcory:")
print(get_files_info("calculator", "/bin"))


print("Result for '../' direcory:")
print(get_files_info("calculator", "../"))