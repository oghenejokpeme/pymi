import sys
from kb import KB
from rule import Rule

def init_rules(kb, minconf):
    rules = [Rule([atom]) for atom in list(kb.rso.keys())]

def get_rules(kb, minconf=0.1):
    rules = init_rules(kb, minconf)

def main(argv):
    kb = KB(argv[0])

if __name__ == '__main__':
    main(sys.argv[1:])