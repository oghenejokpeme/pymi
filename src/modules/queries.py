def get_atom_instantiations(atom, db):
    """Returns the set of all instantiations of an atom. Atoms can 
    take one of the following forms:
    a. ((?svar), relation, (?ovar))
    b. ((?svar, subject), relation, (?ovar))
    c. ((?svar), relation, (?ovar, object))
    d. ((?svar, subject), relation, (?ovar, object))
    """
    sub, rel, obj = atom
    
    if len(sub) > 2 or len(sub) < 1:
        raise Exception(f'Illegal atom subject in: {atom}.')
    if len(obj) > 2 or len(obj) < 1:
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

def get_atom_size(atom, db):
    return len(get_atom_instantiations(atom, db))

def instantiate_query_with_atom_bindings(query, iatom):
    isub, irel, iobj = iatom
    isubvar = isub[0]
    iobjvar = iobj[0]

    bquery = set()
    for qatom in query:
        qsub, qrel, qobj = qatom
        qsubvar = qsub[0]
        qobjvar = qobj[0]
        temp_sub = qsub
        temp_obj = qobj

        if isubvar == qsubvar:
            temp_sub = isub
        if iobjvar == qobjvar:
            temp_obj = iobj
        if isubvar == qobjvar:
            temp_obj = isub
        if iobjvar == qsubvar:
            temp_sub = iobj
        
        bquery.add((temp_sub, qrel, temp_obj))
    
    return bquery

def check_query_existence(query, db):
    """The query is the list of all body atoms of a rule. That is,
    it is the rule with the head atom."""

    if len(query) == 1:
        return get_atom_size(query.pop(), db) > 0
    else:
        s = {get_atom_size(atom, db):atom for atom in query}
        satom = s[min(s)]
        query.remove(satom)
        insts = get_atom_instantiations(satom, db)

        for inst_atom in insts:
            qp = instantiate_query_with_atom_bindings(query, inst_atom)
            if check_query_existence(qp, db):
                return True
    
    return False

def instantiate_query_with_var_bindings(var, query, iatom):
    isub, _, iobj = iatom
    isubvar = isub[0]
    iobjvar = iobj[0]

    bquery = set()
    for qatom in query:
        qsub, qrel, qobj = qatom
        qsubvar = qsub[0]
        qobjvar = qobj[0]
        temp_sub = qsub
        temp_obj = qobj

        if isubvar == qsubvar == var:
            temp_sub = isub
        elif iobjvar == qobjvar == var:
            temp_obj = iobj
        elif isubvar == qobjvar == var:
            temp_obj = isub
        elif iobjvar == qsubvar == var:
            temp_sub = iobj
        
        bquery.add((temp_sub, qrel, temp_obj))
    
    if isubvar == var:
        return (isub[1], bquery)
    elif iobjvar == var:
        return (iobj[1], bquery)
    else:
        raise Exception('Variable binding error!')
    
def var_in_atom(var, atom):
    """Checks if variable is in an atom and the variable has not been
    assigned an entity."""
    sub, _, obj = atom

    if var in sub and len(sub) == 1:
        return True
    elif var in obj and len(obj) == 1:
        return True
    else:
        return False

def select_distinct_for_query(var, query, db, result):
    """Identifies all entities for ?var in a query which satisfies 
    the query conjunction."""
    # Note: Need to handle the case where ?var is not in any of the 
    # query atoms.
    
    s = {get_atom_size(atom, db):atom for atom in query}
    satom = s[min(s)]
    insts = get_atom_instantiations(satom, db)

    if var_in_atom(var, satom):
        for inst_atom in insts:
            ent, qp = instantiate_query_with_var_bindings(var, query, inst_atom)
            
            if check_query_existence(qp, db):
                result.add(ent)
    
    else:
        query.remove(satom)
        for inst_atom in insts:
            qp = instantiate_query_with_atom_bindings(query, inst_atom)
            result.union(select_distinct_for_query(var, qp, db, result))

    return result

def get_count(head, body, db):
    """The query may or may not include the head of a rule."""
    q = set()
    if head:
        q = body.union({head})
        
        sub, rel, obj = head
        subvar = sub[0]
        objvar = obj[0]

        count = 0
        sub_distinct = select_distinct_for_query(subvar, q, db, set())
        for subinst in sub_distinct:
            tiatom = ((subvar, subinst), rel, obj) 
            _, qp = instantiate_query_with_var_bindings(subvar, q, tiatom)
            obj_distinct = select_distinct_for_query(objvar, qp, db, set()) 
            count += len(obj_distinct)
        
        return count