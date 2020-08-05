class KB:
    def __init__(self, kb_path):
        self.rso = {}
        self.process_kb(kb_path)
    
    def process_kb(self, kb_path):
        with open(kb_path, 'r') as f:
            for line in f:
                atom = line.strip()[:-1].split('\t')
                sub, rel, obj = atom