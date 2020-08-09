# First naive implementation, currently does not account for variables.
class Rule:
    def __init__(self, atoms):
        self.rule = [atom for atom in atoms]
    
    # For developement
    def print_details(self, kb):
        print(self.rule)
        '''
        print('Support: ', self.support(kb))
        print('HC: ', self.head_coverage(kb))
        print('Std Conf: ', self.standard_confidence(kb))
        print('PCA Conf: ', self.pca_confidence(kb))
        print('Body Size: ', self.body_size(kb))
        print('PCA Body Size: ', self.pca_body_size(kb))
        print('')
        #'''