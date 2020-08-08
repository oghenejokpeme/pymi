import sys
from kb import KB
from rule import Rule

def init_rules(kb, minconf):
    rules = [Rule([atom]) for atom in list(kb.rso.keys())]
    c = []
    for rule in rules:
        sconf = rule.standard_confidence(kb)
        pconf = rule.pca_confidence(kb)
        hc = rule.head_coverage(kb)
        print(rule.rule, rule.support(kb))

def get_rules(kb, minconf=0.1):
    rules = init_rules(kb, minconf)

def main(argv):
    kb = KB(argv[0])

    r = Rule(['<wasBornIn>', '<LivesIn>'])
    r.print_details(kb)
    #print(r.support(kb))
    #print(r.head_coverage(kb))
    #get_rules(kb)
    
if __name__ == '__main__':
    main(sys.argv[1:])