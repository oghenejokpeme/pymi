from . import rule

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

        nquery.add(rule.Atom(sv, si, rel, ov, oi))
    
    return nquery

def check_query_existence(query, db):
    """The query is the set of all body atoms of a rule. That is, it
    is the rule with or without the head atom."""

    if len(query) == 1:
        return get_atom_size(query.pop(), db) > 0
    else:
        s = {get_atom_size(atom, db):atom for atom in query}
        satom = s[min(s)]
        query.remove(satom)
        insts = get_atom_instantiations(satom, db)

        for iatom in insts:
            qp = instantiate_query_with_atom_bindings(query, iatom)
            if check_query_existence(qp, db):
                return True
    
    return False

def instantiate_query_with_var_bindings(var, query, iatom):
    """Instantiates the object/object of the atoms in a query given
    an input atom (iatom) and the variabe one would like instantiate
    or change its current instantiation."""
    
    nquery = set()
    for qatom in query:
        sv, si, rel, ov, oi = qatom

        if iatom.subvar == sv == var:
            si = iatom.subinst
        elif iatom.objvar == ov == var:
            oi = iatom.objinst
        elif iatom.subvar == ov == var:
            oi = iatom.subinst
        elif iatom.objvar == sv == var:
            si = iatom.objinst
        
        nquery.add(rule.Atom(sv, si, rel, ov, oi))

    if iatom.subvar == var:
        return (iatom.subinst, nquery)
    elif iatom.objvar == var:
        return (iatom.objinst, nquery)
    else:
        raise Exception('Variable binding error!')

def select_distinct_for_query(var, query, db, result):
    """Identifies all entities for ?var in a query which satisfies 
    the query conjunction."""
    # Note: Need to handle the case where ?var is not in any of the 
    # query atoms.

    s = {get_atom_size(atom, db):atom for atom in query}
    satom = s[min(s)]
    insts = get_atom_instantiations(satom, db)

    if satom.var_in_atom(var):
        for iatom in insts:
            ent, qp = instantiate_query_with_var_bindings(var, query, iatom)
            
            if check_query_existence(qp, db):
                result.add(ent)
    
    else:
        query.remove(satom)
        for iatom in insts:
            qp = instantiate_query_with_atom_bindings(query, iatom)
            result.union(select_distinct_for_query(var, qp, db, result))

    return result

def supp_cwa_denom_calc(q, head, db):
    """Main algorithm for calculating support and the CWA denominator."""

    count = 0
    sub_distinct = select_distinct_for_query(head.subvar, q, db, set())
    for subinst in sub_distinct:
        iatom = head.make_subject_instance(subinst)
        _, qp = instantiate_query_with_var_bindings(head.subvar, q, iatom)
        obj_distinct = select_distinct_for_query(head.objvar, qp, db, set())
        count += len(obj_distinct)

    return count

def calc_standard_support(head, body, db):
    """Calculates standard support for a rule. Assumes that rule is 
    not 'expensive'."""
    
    q = body.union({head})
    return supp_cwa_denom_calc(q, head, db)
    
def calc_standard_cwa_denom(hsubvar, body, db):
    """Calculates standard CWA denominator. Assumes that rule is not 
    'expensive'."""
    for atom in body:
        if atom.var_in_atom(hsubvar):
            head = atom
            q = body.copy()
            return supp_cwa_denom_calc(q, head, db)

    raise Exception('Cannot compute standard CWA denominator.')

def calc_standard_pca_denom(fvar, head, body, db):
    """Calculates standard PCA denominator. Assumes that rule is not 
    'expensive'."""

    ypvar = ''
    if fvar == head.subvar: ypvar = head.objvar
    elif fvar == head.objvar: ypvar = head.subvar

    dn = set()
    insts = get_atom_instantiations(head, db)
    for iatom in insts:
        _, qp = instantiate_query_with_var_bindings(fvar, body, iatom)
        obj_distinct = select_distinct_for_query(ypvar, qp, db, set())
        
        for dobj in obj_distinct:
            if fvar == iatom.subvar:
                dn.add((iatom.subinst, dobj))
            elif fvar == iatom.objvar:
                dn.add((iatom.objinst, dobj))
    
    return len(dn)