import sys

def load_knowledge_base(kb_path):
    with open(kb_path, 'r') as f:
        for line in f:
            nline = line.strip()[:-1].split('\t')
            sub, rel, obj = nline
            
def main(argv):
    kb_path = argv[0]
    kb = load_knowledge_base(kb_path)
    
if __name__ == '__main__':
    main(sys.argv[1:])