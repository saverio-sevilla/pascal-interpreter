from SPI import build
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Add typechecking
# Add const and type declarations

def main():

    path = "program.txt"
    if os.path.isfile(path):
        try:
            f = open(path, "r")
            program = f.read()
            build(program)
            f.close()
        except EOFError:
            print("Error opening file")
    else:
        print("FIle not found")

if __name__ == '__main__':
    main()

