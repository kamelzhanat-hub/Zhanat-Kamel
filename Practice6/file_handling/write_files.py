file_path = "sample.txt"

# Write data to file
with open(file_path, "w", encoding="utf-8") as f:
    f.write("Hello, this is a sample file.\n")
    f.write("Python file handling practice.\n")

# Append new lines
with open(file_path, "a", encoding="utf-8") as f:
    f.write("This line was appended.\n")
    f.write("Another appended line.\n")

print("New lines appended.")