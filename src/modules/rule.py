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