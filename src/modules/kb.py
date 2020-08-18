def add_atom_to_kb(db, subkb, enta, entb, entc):
    if enta not in db['kb'][subkb]:
        db['kb'][subkb][enta] = {entb: {entc}} 
    else:
        try:
            db['kb'][subkb][enta][entb].add(entc)
        except KeyError:
            db['kb'][subkb][enta][entb] = {entc}

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

def process_kb(kb_path):
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

def estimate_relation_functionalities(db):
    """Calculates and adds the functionality and inverse functionality
    for  all relations in the db."""

    db['funct'] = {}
    db['inv_funct'] = {}

    # The functionality of the relation, r is given by:
    # func(r) = #x:Ey:r(x,y) / #(x,y):r(x,y).
    # The inverse functionality is calculated by reversing x and y in r.
    # See Equation 5 in Appendix A of PARIS: Probabilitic Alignment of
    # Relations, Instances, and Schema (https://arxiv.org/pdf/1111.7164.pdf)
    for rel in db['agg_index']['P']:
        func = len(db['kb']['RSO'][rel])/len(db['agg_index']['P'][rel])
        ifunc = len(db['kb']['ROS'][rel])/len(db['agg_index']['P'][rel])
        db['funct'][rel] = round(func, 3)
        db['inv_funct'][rel] = round(ifunc, 3)

def estimate_overlaps(db):
    """Calculates the overlaps for all pairs of relations in the KB."""
    from itertools import combinations

    db['overlap'] = {'dom_dom':{}, 'rng_rng':{},
                     'dom_rng':{}, 'rng_dom':{}}

    for rel_pair in combinations(db['agg_index']['P'], 2):
        rela, relb = rel_pair
        doma = set(db['kb']['RSO'][rela])
        rnga = set(db['kb']['ROS'][rela])
        domb = set(db['kb']['RSO'][relb])
        rngb = set(db['kb']['ROS'][relb])
        
        dd = len(doma.intersection(domb))
        db['overlap']['dom_dom'][(rela, relb)] = dd
        db['overlap']['dom_dom'][(relb, rela)] = dd
        
        rr = len(rnga.intersection(rngb))
        db['overlap']['rng_rng'][(rela, relb)] = rr
        db['overlap']['rng_rng'][(relb, rela)] = rr
                
        rda = len(rnga.intersection(domb))
        db['overlap']['rng_dom'][(rela, relb)] = rda

        rdb = len(rngb.intersection(doma))
        db['overlap']['rng_dom'][(relb, rela)] = rdb

        dra = len(doma.intersection(rngb))
        db['overlap']['dom_rng'][(rela, relb)] = dra

        drb = len(domb.intersection(rnga))
        db['overlap']['dom_rng'][(relb, rela)] = drb

def load_kb(kb_path):
    db = process_kb(kb_path)
    estimate_relation_functionalities(db)
    estimate_overlaps(db)

    return db