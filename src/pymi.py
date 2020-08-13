import sys
from modules import kb, queries, rule

def main(argv):
    db = kb.load_kb(argv[0])

if __name__ == '__main__':
    main(sys.argv[1:])