# First naive implementation, refactor later.
class Rule:
    def __init__(self, atoms):
        self.rule = [('x', atom, 'y') for atom in atoms]
    
    def is_closed(self):
        pass

    def get_instantiations(self, kb):
        """The intersection of all instantiations for each atom in a
        rule."""
        insts = kb.rels[self.rule[0][1]]
        for atom in self.rule[1:]:
            _, rel, _ = atom
            insts = insts.intersection(kb.rels[rel])
        
        return insts

    def support(self, kb):
        return len(self.get_instantiations(kb))
    
    def size(self, kb):
        head_rel = self.rule[0][1]
        return len(kb.rels[head_rel])

    def head_coverage(self, kb):
        return self.support(kb)/self.size(kb)

    def standard_confidence(self, kb):
        # Note: Loops through rule twice. Refactor later.
        insts = set()
        for atom in self.rule[1:]:
            _, rel, _ = atom
            insts = insts.union(kb.rels[rel])
        
        return self.support(kb)/len(insts)
    
    # Still incorrect, fix next.
    def pca_confidence(self, kb):
        insts = self.get_instantiations(kb)
        
        neg_count = 0
        for atom in self.rule:
            _, rel, _ = atom
            for sub, obj in insts:
                neg_objs = kb.rso[rel][sub] - {obj}    
                neg_count += len(neg_objs)
        support = self.support(kb)

        return support/(support+neg_count)

    # For developement
    def print_details(self, kb):
        print(self.rule)
        print('Support: ', self.support(kb))
        print('HC: ', self.head_coverage(kb))
        print('Std Conf: ', self.standard_confidence(kb))
        print('PCA Conf: ', self.pca_confidence(kb))
        print('')