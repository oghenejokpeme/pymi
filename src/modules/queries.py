from .rule import Atom

def get_atom_instantiations(atom, db):
    try:
        if not atom.subinst and not atom.objinst:
            return {atom.make_general_instance(fact) 
                    for fact in db['agg_index']['P'][atom.rel]}
                
        elif atom.subinst and not atom.objinst:
            return {atom.make_object_instance(objinst) for objinst 
                    in db['kb']['RSO'][atom.rel][atom.subinst]}
        
        elif not atom.subinst and atom.objinst:
            return {atom.make_subject_instance(subinst) for subinst 
                    in db['kb']['ROS'][atom.rel][atom.objinst]}
        
        elif atom.subinst and atom.objinst:
            fact = (atom.subinst, atom.rel, atom.objinst)
            if fact in db['agg_index']['P'][atom.rel]:
                return {atom}
            else:
                return set()
    
    except KeyError:
        return set()

def get_atom_size(atom, db):
    return len(get_atom_instantiations(atom, db))

def instantiate_query_with_atom_bindings(query, iatom):
    """Insantantiates the subject and object of the atoms in a query 
    with the subject and object of an input atom (iatom). Does not
    care if the atoms in the query have already been initialized. 
    They get re-initialized if they already have been."""
    
    nquery = set()
    for qatom in query:
        sv, si, rel, ov, oi = qatom

        if iatom.subvar == qatom.subvar:
            si = iatom.subinst
        if iatom.objvar == qatom.objvar:
            oi = iatom.objinst
        if iatom.subvar == qatom.objvar:
            oi = iatom.subinst
        if iatom.objvar == qatom.subvar:
            si = iatom.objinst

        nquery.add(Atom(sv, si, rel, ov, oi))
    
    return nquery

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

def is_expensive(head, body):
    """A rule is expensive if:
    1. It contains variables other than those that appear in the head
       atom.
    2. If these additional variables define a single path between head
       variables."""
    # @TODO: Move to rule file. This is a rule only computation.
    sub, _, obj = head
    checks = {True:0, False:0}
    for batom in body:
        bsub, _, bobj = batom
        if sub[0] == bsub[0] and obj[0] == bobj[0]:
            checks[False] += 1
        elif sub[0] == bobj[0] and obj[0] == bsub[0]:
            checks[False] += 1
        else:
            checks[True] += 1

    if checks[False] == len(body):
        return False
    else:
        # Still needs the code that checks for condition 2 above.
        return True

def get_count(head, body, db):
    """The query may or may not include the head of a rule.
    Support -> Head and body.
    CWA numerator -> Just body. Head = None."""

    q = body
    if head:
        if not is_expensive(head, body):
            q = body.union({head}) 
        else:
            # Perform approximate metric computation.
            return False
    else:
        import random
        head = random.sample(body, 1)[0]
        
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

def get_pca_count(fvar, head, body, db):
    hsub, _, hobj = head
    hsubvar = hsub[0]
    hobjvar = hobj[0]
    
    ypvar = ''
    if fvar == hsubvar:
        ypvar = hobjvar
    elif fvar == hobjvar:
        ypvar = hsubvar

    insts = get_atom_instantiations(head, db)
    dn = set()
    for ainst in insts:
        asub, _, aobj = ainst
        asvar, asent = asub
        aovar, aoent = aobj 

        _, qp = instantiate_query_with_var_bindings(fvar, body, ainst)
        obj_distinct = select_distinct_for_query(ypvar, qp, db, set())
        
        for dobj in obj_distinct:
            if fvar == asvar:
                dn.add((asent, dobj))
            elif fvar == aovar:
                dn.add((aoent, dobj))
    
    return len(dn)