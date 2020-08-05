import sys
from kb import KB

def load_knowledge_base(kb_path):
    kb = KB(kb_path)

def main(argv):
    kb_path = argv[0]
    kb = load_knowledge_base(kb_path)
    
if __name__ == '__main__':
    main(sys.argv[1:])