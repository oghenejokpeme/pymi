# First naive implementation, currently does not account for variables.
class Rule:
    def __init__(self, atoms):
        self.rule = [atom for atom in atoms]
    
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
    
    def body_size(self, kb):
        """Calculates numerator for standard confidence calculation.
        """
        insts = set()
        for atom in self.rule[1:]:
            _, rel, _ = atom
            insts = insts.union(kb.rels[rel])
        
        return len(insts)

    def pca_body_size(self, kb):
        """Calculates numerator for PCA standard confidence calculation.
        """
        sopairs = set()
        hsubs = set(kb.rso[self.rule[0][1]].keys())
        for atom in self.rule[1:]:
            _, rel, _ = atom
            asubs = set(kb.rso[rel].keys())
            isubs = hsubs.intersection(asubs)
            for sub in isubs:
                for obj in kb.rso[rel][sub]:
                    sopairs.add((sub, obj))
                #print(sub,' -> ', kb.rso[rel][sub])

        return len(sopairs)

    def support(self, kb):
        return len(self.get_instantiations(kb))
    
    def head_predicted(self, kb):
        return len(kb.rels[self.rule[0][1]])

    def head_coverage(self, kb):
        return self.support(kb)/self.head_predicted(kb)

    def standard_confidence(self, kb):
        try:
            return self.support(kb)/self.body_size(kb)
        except ZeroDivisionError:
            return float('inf')

    def pca_confidence(self, kb):
        # For empty rules, as rules must have body atoms.
        if len(self.rule) == 1:
            return float('inf')

        return self.support(kb)/self.pca_body_size(kb) 

    # For developement
    def print_details(self, kb):
        print(self.rule)
        print('Support: ', self.support(kb))
        print('HC: ', self.head_coverage(kb))
        print('Std Conf: ', self.standard_confidence(kb))
        print('PCA Conf: ', self.pca_confidence(kb))
        print('Body Size: ', self.body_size(kb))
        print('PCA Body Size: ', self.pca_body_size(kb))
        print('')