from SPI import build
import os

# Add typechecking
# Add const and type declarations
# Let readln accept different types of values

def main():

    path = "program.txt"
    if os.path.isfile(path):
        try:
            f = open(path, "r")
            program = f.read()
            build(program)
            f.close()
        except:
            print("Error opening file")
    else:
        print("FIle not found")

if __name__ == '__main__':
    main()

