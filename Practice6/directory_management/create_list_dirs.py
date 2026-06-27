import os

# create directories
os.makedirs("test_dir/sub_dir", exist_ok=True)

print("Directories created.")

# current directory
print("Current directory:", os.getcwd())

# list files
files = os.listdir(".")
print("\nFiles in current directory:")

for f in files:
    print(f)