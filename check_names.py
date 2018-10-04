import glob
import re


def check_file_names(path: str):
    file_names = [f for f in glob.glob(path + "\\*")]
    allowed = ['speed', 'size', 'both']
    for name in file_names:
        
        # Check year
        if not name.startswith(path + "\\Year "):
            print(name, "| file name must start with 'Year '")
        else:
            result = re.search('Year (.*) - ', name)
            try:
                int(result.group(1))
            except Exception as e:
                if result is None:
                    print("Year must be between 02 and 68. Example: Year 02 - Welcome, New Employees (both).txt")
                else:
                    print("Year must be between 02 and 68. Got:", result.group(1))

        # Check file type
        if not name.endswith('.txt'):
            print(name, "| file name must end with .txt")

        # Check solution type
        result = re.search('\((.*)\)', name)
        if result is None:
            print(name, "| file name must specify speed, size or both between brackets")
        else:
            result = result.group(1)
            if not (result in allowed):
                for item in allowed:
                    if item in result.lower():
                        new_name = name.replace(name[name.find("(") + 1:name.find(")")], item)
                        print(name, "->", new_name)
                        name = ""
                if name != "":
                    print(name, "| file name must specify speed, size or both")


def main():
    check_file_names("Solutions99+")
    check_file_names("Solutions50+")


main()
