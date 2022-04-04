from SPI import build
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Add functions
# Add typechecking
# Add const and type declarations

def main():

    path = "program2.txt"
    if os.path.isfile(path):
        with open(path) as f:
            program = f.read()
            build(program)

if __name__ == '__main__':
    main()

