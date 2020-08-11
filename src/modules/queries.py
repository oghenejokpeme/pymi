def get_atom_instantiations(atom, db):
    """Returns the set of all instantiations of an atom. Atoms can 
    take one of the following forms:
    a. ((?svar), relation, (?ovar))
    b. ((?svar, subject), relation, (?ovar))
    c. ((?svar), relation, (?ovar, object))
    d. ((?svar, subject), relation, (?ovar, object))
    """
    sub, rel, obj = atom
    
    if len(sub) > 2:
        raise Exception
        #raise Exception(f'Illegal atom subject in: {atom}.')
    if len(obj) > 2:
        raise Exception(f'Illegal atom object in: {atom}.')

    try:
        if len(sub) == 1 and len(obj) == 1:
            subvar = sub[0]
            objvar = obj[0]
            
            insts = set()
            for fact in db['agg_index']['P'][rel]:
                fsub, _, fobj = fact
                insts.add(((subvar, fsub), rel, (objvar, fobj)))
            
            return insts

        elif len(sub) == 2 and len(obj) == 1:
            subvar, subinst = sub
            objvar = obj[0]

            return {(sub, rel, (objvar, iobj)) 
                    for iobj in db['kb']['RSO'][rel][subinst]}
        
        elif len(sub) == 1 and len(obj) == 2:
            subvar = sub[0]
            objvar, objinst = obj

            return {((subvar, isub), rel, obj) 
                    for isub in db['kb']['ROS'][rel][objinst]}
        
        elif len(sub) == 2 and len(obj) == 2:
            _, subinst = sub
            _, objinst = obj

            if (subinst, rel, objinst) in db['agg_index']['P'][rel]:
                return {atom}
            else:
                return set()
    
    except KeyError:
        return set()