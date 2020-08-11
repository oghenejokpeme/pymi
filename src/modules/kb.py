def add_atom_to_kb(db, subkb, enta, entb, entc):
    if enta not in db['kb'][subkb]:
        db['kb'][subkb][enta] = {entb: {entc}} 
    else:
        try:
            db['kb'][subkb][enta][entb].add(entc)
        except KeyError:
            db['kb'][subkb][enta][entb] = {entc}

    return

def add_to_agg_index(db, index, key, atom):
    """Adds fact/atom to aggregated index. Originally, this should
    return the number of facts for which the key occurs in. However,
    we store the actual facts, as the number of facts can be returned
    using len().
    P -> relation, S -> Subject, O -> Object."""

    try:
        db['agg_index'][index][key].add(atom)
    except KeyError:
        db['agg_index'][index][key] = {atom}

def load_kb(kb_path):
    db = {'kb': {'SRO':{}, 'SOR':{}, 
                 'RSO':{}, 'ROS':{},
                 'OSR':{}, 'ORS':{}},
          'agg_index': {'P':{}, 'S':{}, 'O':{}}
         }

    with open(kb_path, 'r') as f:
        for line in f:
            atom = line.strip()[:-1].split('\t')
            sub, rel, obj = atom
            add_to_agg_index(db, 'P', rel, (sub, rel, obj))
            add_to_agg_index(db, 'S', sub, (sub, rel, obj))
            add_to_agg_index(db, 'O', obj, (sub, rel, obj))
    
            add_atom_to_kb(db, 'SRO', sub, rel, obj)
            add_atom_to_kb(db, 'SOR', sub, obj, rel)
            add_atom_to_kb(db, 'RSO', rel, sub, obj)
            add_atom_to_kb(db, 'ROS', rel, obj, sub)
            add_atom_to_kb(db, 'OSR', obj, sub, rel)
            add_atom_to_kb(db, 'ORS', obj, rel, sub)
            
    return db