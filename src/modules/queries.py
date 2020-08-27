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

def instantiate_with_atom_bindings(iatom, qatom):
    """Instantiates the subject and object of a query atom (qatom) 
    with the subject and object of an input atom (iatom). Does not
    care if the atoms in the query have already been initialized. 
    They get re-initialized if they already have been."""
    
    sv, si, rel, ov, oi = qatom
    if iatom.subvar == qatom.subvar:
        si = iatom.subinst
    if iatom.objvar == qatom.objvar:
        oi = iatom.objinst
    if iatom.subvar == qatom.objvar:
        oi = iatom.subinst
    if iatom.objvar == qatom.subvar:
        si = iatom.objinst

    return rule.Atom(sv, si, rel, ov, oi)

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
            qp = {instantiate_with_atom_bindings(iatom, qatom)
                  for qatom in query}
            if check_query_existence(qp, db):
                return True
    
    return False

def instantiate_with_var_bindings(var, iatom, qatom):
    """Instantiates the object/object of query atom (qatom) given
    an input atom (iatom) and the variable one would like instantiate
    or change its current instantiation."""

    sv, si, rel, ov, oi = qatom
    if iatom.subvar == sv == var:
        si = iatom.subinst
    elif iatom.objvar == ov == var:
        oi = iatom.objinst
    elif iatom.subvar == ov == var:
        oi = iatom.subinst
    elif iatom.objvar == sv == var:
        si = iatom.objinst

    return rule.Atom(sv, si, rel, ov, oi)

def select_distinct_for_query(var, query, db, result):
    """Identifies all entities for ?var in a query which satisfies 
    the query conjunction."""

    s = {get_atom_size(atom, db):atom for atom in query}
    satom = s[min(s)]
    insts = get_atom_instantiations(satom, db)
    
    if satom.var_in_atom(var):
        for iatom in insts:
            qp = {instantiate_with_var_bindings(var, iatom, qatom)
                  for qatom in query}

            if check_query_existence(qp, db):
                result.add(iatom.var_inst(var))
    
    else:
        query.remove(satom)
        for iatom in insts:
            qp = {instantiate_with_atom_bindings(iatom, qatom)
                  for qatom in query}

            result.union(select_distinct_for_query(var, qp, db, result))

    return result


def count_projection_for_query(var, head, body, threshold, db):
    xmap = {}
    query = body
    
    insts = get_atom_instantiations(head, db)
    if head.var_in_atom(var):        
        for iatom in insts:
            qp = query.copy()
            qp.add(iatom)
            if check_query_existence(qp, db):
                try:
                    xmap[iatom.var_inst(var)] += 1
                except KeyError:
                    xmap[iatom.var_inst(var)] = 1
    
    else:
        for iatom in insts:
            qp = query.copy()
            qp.add(iatom)
            var_distinct = select_distinct_for_query(var, qp, db, set())
            for varsub in var_distinct:
                try:
                    xmap[varsub] += 1
                except KeyError:
                    xmap[varsub] = 1
    
    return {svar:n for svar, n in xmap.items() if n >= threshold}


def calc_support(head, body, db):
    count = 0
    query = body.union({head})
    sub_distinct = select_distinct_for_query(head.subvar, query.copy(), db, set())

    for subinst in sub_distinct:
        iatom = head.make_subject_instance(subinst)
        qp = {instantiate_with_var_bindings(head.subvar, iatom, qatom)
              for qatom in query}

        obj_distinct = select_distinct_for_query(head.objvar, qp, db, set())
        count += len(obj_distinct)

    return count 
    
def calc_standard_cwa_denom(fvar, head, body, db):
    """Calculates standard CWA denominator. Assumes that rule is not 
    'expensive'."""
    query = body
    nfvar = head.get_non_functional_var(fvar)
    
    count = 0
    fvar_distinct = select_distinct_for_query(fvar, query.copy(), db, set())

    for fvarinst in fvar_distinct:
        iatom = '' 
        if head.subvar == fvar:
            iatom = head.make_subject_instance(fvarinst)
        elif head.objvar == fvar:
            iatom = head.make_object_instance(fvarinst)

        qp = {instantiate_with_var_bindings(fvar, iatom, qatom)
              for qatom in query}
        nfvar_distinct = select_distinct_for_query(nfvar, qp, db, set())
          
        count += len(nfvar_distinct)

    return count

def calc_standard_pca_denom(fvar, head, body, db):
    """Calculates standard PCA denominator. Assumes that rule is not 
    'expensive'."""

    nfvar = head.get_non_functional_var(fvar)
    dn = set()
    insts = get_atom_instantiations(head, db)
    for iatom in insts:
        qp = {instantiate_with_var_bindings(fvar, iatom, qatom)
              for qatom in body}

        obj_distinct = select_distinct_for_query(nfvar, qp, db, set())
        
        for dobj in obj_distinct:
            if fvar == iatom.subvar:
                dn.add((iatom.subinst, dobj))
            elif fvar == iatom.objvar:
                dn.add((iatom.objinst, dobj))
    
    return len(dn)