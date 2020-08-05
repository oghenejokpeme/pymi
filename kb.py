class KB:
    def __init__(self, kb_path):
        # Direct maps.
        self.rels = {}

        # Linked KB
        self.sro = {}
        self.sor = {}
        self.rso = {}
        self.ros = {}
        self.osr = {}
        self.ors = {}
        self.process_kb(kb_path)
    
    def add_to_subkb(self, enta, entb, entc, subkb):
        """The idea here is that this one method can be used to
        update all the sub knowledge bases depending on what is
        passed for enta, entb, or entc. etnX can be one of sub,
        rel, or obj. 
        """
        if enta in subkb:
            try:
                subkb[enta][entb].add(entc)
            except KeyError:
                subkb[enta][entb] = {entc}                
        else:
            subkb[enta] = {entb: {entc}}
    
    def add_to_relmap(self, sub, rel, obj):
        try:
            self.rels[rel].add((sub, obj))
        except KeyError:
            self.rels[rel] = {(sub, obj)}

    def process_kb(self, kb_path):
        with open(kb_path, 'r') as f:
            for line in f:
                atom = line.strip()[:-1].split('\t')
                sub, rel, obj = atom
                self.add_to_relmap(sub, rel, obj)

                self.add_to_subkb(sub, rel, obj, self.sro)
                self.add_to_subkb(sub, obj, rel, self.sor)
                self.add_to_subkb(rel, sub, obj, self.rso)
                self.add_to_subkb(rel, obj, sub, self.ros)
                self.add_to_subkb(obj, sub, rel, self.osr)
                self.add_to_subkb(obj, rel, sub, self.ors)