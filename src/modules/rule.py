from dataclasses import dataclass

@dataclass(eq=True, frozen=True)
class Atom:
    subvar: str  # Subject variable.
    subinst: str # Subject instantiation.
    rel: str     # Atom relation.
    objvar: str  # Object variable.
    objinst: str # Object instantiation.

    def __iter__(self):
        return iter((self.subvar, self.subinst, self.rel, self.objvar, self.objinst))

    def make_general_instance(self, fact):
        """Creates a new atom by substituting subinst and objinst 
        with the subject and object in the fact and returns a new
        atom object.
        """
        
        if self.subinst == None and self.objinst == None:
            fsubinst, _, fobjinst = fact
            return Atom(self.subvar, fsubinst, self.rel, self.objvar, fobjinst)
        else:
            out = ('Attempting general instantiation of already instantiated' +
                   'atom variable.')
            raise Exception(out)

    def make_object_instance(self, fobjinst):
        """Creates a new atom by substituting the objinst with the
        object from the fact.
        """
        
        if self.objinst == None:
            return Atom(self.subvar, self.subinst, self.rel, self.objvar, fobjinst)
        else:
            out = ('Attempting object instantiation of already instantiated' +
                   'atom variable.')
            raise Exception(out)
    
    def make_subject_instance(self, fsubinst):
        """Creates a new atom by substituting the objinst with the
        object from the fact.
        """
        
        if self.subinst == None:
            return Atom(self.subvar, fsubinst, self.rel, self.objvar, self.objinst)
        else:
            out = ('Attempting subject instantiation of already instantiated' +
                   'atom variable.')
            raise Exception(out)

    def var_in_atom(self, var):
        if self.subvar == var or self.objvar == var:
            return True
        else:
            return False
    
    def get_non_functional_var(self, fvar):
        if fvar == self.subvar:
            return self.objvar
        elif fvar == self.objvar:
            return self.subvar

# @NOTE: This should all probably be part of a Rule class.
def has_only_head_variables(head, body):
    hvars = {head.subvar, head.objvar}
    for atom in body:
        if atom.subvar not in hvars or atom.objvar not in hvars:
            return False

    return True

def has_single_head_variable_occurence(head, body):
    """Checks if head variables occur exactly once in the body atoms.
    """
    hvars = {head.subvar:0, head.objvar:0}
    for batom in body:
        if batom.subvar in hvars:
            hvars[batom.subvar] += 1
            if hvars[batom.subvar] > 1: return False
        if batom.objvar in hvars:
            hvars[batom.objvar] += 1
            if hvars[batom.objvar] > 1: return False

    return True

def make_canonical(fvar, head, body):
    """Canonicalization is done based on the provided functional
    variable which must be either the subject or object variable
    of the head atom. Also assumes that the head subject and 
    object variables only occur once in the body atoms.
    """
    lvar = head.get_non_functional_var(fvar)

    fconfig = ()
    lconfig = ()
    flatoms = set()
    for batom in body:
        # First body atom.
        if fvar == batom.subvar:
            fconfig = (0, batom.rel, batom.subvar, batom.objvar)
            flatoms.add(batom)
        if fvar == batom.objvar:
            fconfig = (1, batom.rel, batom.objvar, batom.subvar)
            flatoms.add(batom)

        # Last body atom.
        if lvar == batom.subvar:
            lconfig = (1, batom.rel, batom.objvar, batom.subvar)
            flatoms.add(batom)
        if lvar == batom.objvar:
            lconfig = (0, batom.rel, batom.subvar, batom.objvar)
            flatoms.add(batom)
    
    join_order = [fconfig]
    tbody = body - flatoms

    for tatom in tbody:
        for ordatom in join_order:
            if lconfig[2] == tatom.subvar:
                ent = (1, tatom.rel, tatom.objvar, tatom.subvar)
                join_order.append(ent)
                break
            
            if lconfig[2] == tatom.objvar:
                ent = (0, tatom.rel, tatom.subvar, tatom.objvar)
                join_order.append(ent)
                break
            
            if ordatom[3] == tatom.subvar:
                ent = (0, tatom.rel, tatom.subvar, tatom.objvar)
                join_order.append(ent)
                break 

            elif ordatom[3] == tatom.objvar:
                ent = (1, tatom.rel, tatom.objvar, tatom.subvar)   
                join_order.append(ent)
                break
    join_order.append(lconfig)
    
    return join_order  

def make_join_graph(join_order):
    jgraph = {}
    for atom in join_order:
        _, _, subvar, objvar = atom
        try:
            jgraph[subvar].append(objvar)
        except KeyError:
            jgraph[subvar] = [objvar]
    jgraph[join_order[-1][3]] = None

    return jgraph

def find_join_paths(sv, obv, g, path=None):
    paths = []
    if path is None:
        path = []
    path.append(sv)
    objs = g[sv]
    if objs:
        for obj in objs:
            paths.extend(find_join_paths(obj, obv, g, path[:]))
    else:
        if path[-1] == obv:
            paths.append(path)
    
    return paths

def has_single_path(fvar, head, body):
    join_order = make_canonical(fvar, head, body)
    join_graph = make_join_graph(join_order)
    join_paths = find_join_paths(fvar, head.get_non_functional_var(fvar), 
                                 join_graph, None)


def is_expensive(fvar, head, body):
    """Checks if rule is expensive."""
    if not head.var_in_atom(fvar):
        # @TODO: Make this text more informative.
        oe = 'Unable to canonicalize. Functional variable mismatch.'
        raise Exception(oe)
    
    if has_only_head_variables(head, body):
        return False
    if has_single_head_variable_occurence(head, body):
        # It may or may not be expensive
        if has_single_path(fvar, head, body):
            return True
        else:
            return False
    else:
        return True