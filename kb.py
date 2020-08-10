class KB:
    def __init__(self, kb_path):
        # Direct maps.
        self.rels = {} #P
        self.subs = {} #S
        self.objs = {} #O

        # Linked KB
        self.sro = {}
        self.sor = {}
        self.rso = {}
        self.ros = {}
        self.osr = {}
        self.ors = {}
        self.process_kb(kb_path)
    
    def add_to_subkb(self, enta, entb, entc, subkb):
        """The idea here is that this one method can be used to
        update all the sub knowledge bases depending on what is
        passed for enta, entb, or entc. etnX can be one of sub,
        rel, or obj. 
        """
        if enta in subkb:
            try:
                subkb[enta][entb].add(entc)
            except KeyError:
                subkb[enta][entb] = {entc}                
        else:
            subkb[enta] = {entb: {entc}}
    
    def add_to_dmap(self, key, atom, dmap):
        try:
            dmap[key].add(atom)
        except KeyError:
            dmap[key] = {atom}

    def process_kb(self, kb_path):
        with open(kb_path, 'r') as f:
            for line in f:
                atom = line.strip()[:-1].split('\t')
                sub, rel, obj = atom
                self.add_to_dmap(rel, (sub, rel, obj), self.rels)
                self.add_to_dmap(sub, (sub, rel, obj), self.subs)
                self.add_to_dmap(obj, (sub, rel, obj), self.objs)

                self.add_to_subkb(sub, rel, obj, self.sro)
                self.add_to_subkb(sub, obj, rel, self.sor)
                self.add_to_subkb(rel, sub, obj, self.rso)
                self.add_to_subkb(rel, obj, sub, self.ros)
                self.add_to_subkb(obj, sub, rel, self.osr)
                self.add_to_subkb(obj, rel, sub, self.ors)
    
    def instantiate_relation(self, atom):
        svar, rel, ovar = atom
        ls = len(svar)
        os = len(ovar)

        try:
            if ls == 1 and os == 1:
                return self.rels[rel]
            
            elif ls == 1 and os == 2:
                insts = {(sub, rel, ovar[1]) 
                         for sub in self.ros[rel][ovar[1]]}
                
                return insts

            elif ls == 2 and os == 1:
                insts = {(svar[1], rel, obj) 
                         for obj in self.rso[rel][svar[1]]}
                
                return insts
            
            elif ls == 2 and os == 2:
                srels = self.sor[svar[1]][ovar[1]]
                orels = self.osr[ovar[1]][svar[1]]

                if rel in srels and rel in orels:
                    return {(svar[1], rel, ovar[1])}
                else:
                    return {}
        
        except KeyError:
            return {}

    def get_atom_size(self, atom):
        svar, rel, ovar = atom
        ls = len(svar)
        os = len(ovar)
        try:
            if ls == 1 and os == 1:
                return len(self.rels[rel])
            
            elif ls == 1 and os != 1:
                return len(self.ros[rel][ovar[1]])  

            elif ls != 1 and os == 1:
                return len(self.rso[rel][svar[1]])

            elif ls != 1 and os != 1:
                srels = self.sor[svar[1]][ovar[1]]
                orels = self.osr[ovar[1]][svar[1]]

                if rel in srels and rel in orels:
                    return 1
                else:
                    return 0
        except KeyError:
            return 0

    def instantiate_rule_with_bindings(self, atom, inst, rule):
        asvar, rel, aovar = atom
        assym = asvar[0]
        aosym = aovar[0]
        sinst, _, oinst = inst

        brule = []
        for batom in rule:
            bsvar, brel, bovar = batom
            bssym = bsvar[0]
            bosym = bovar[0]
           
            if assym == bssym and aosym == bosym:
                brule.append(([bssym, sinst], brel, [bosym, oinst]))

            elif assym == bssym and aosym != bosym:
                brule.append(([bssym, sinst], brel, [bosym]))

            elif assym != bssym and aosym == bosym:
                brule.append(([bssym], brel, [bosym, oinst]))

            elif assym == bosym and aosym == bssym:
                brule.append(([bssym, oinst], brel, [bosym, sinst]))

            elif assym == bosym and aosym != bssym:
                brule.append(([bssym], brel, [bosym, sinst]))

            elif assym != bosym and aosym == bssym:
                brule.append(([bssym, oinst], brel, [bosym]))

        return brule

    # Checks for binding for conjuctive query.
    def exists(self, q):
        if len(q) == 1:
            return self.get_atom_size(q[0]) > 0
        else:
            s = [self.get_atom_size(atom) for atom in q]
            sidx = s.index(min(s))
            satom = q[sidx]
            q = [atom for atom in q if atom != satom]
            insts = self.instantiate_relation(satom)

            for inst in insts:
                print(' ', inst)
                qp = self.instantiate_rule_with_bindings(satom, inst, q)
                if self.exists(qp):
                    return True
        
        return False

    def instantiate_rule_with_variable(self, var, atom, sinst, oinst, rule):
        asvar, rel, aovar = atom
        assym = asvar[0]
        aosym = aovar[0]
        
        brule = []
        for batom in rule:
            bsvar, brel, bovar = batom
            bssym = bsvar[0]
            bosym = bovar[0]

            temp_sub = [bssym]
            temp_obj = [bosym]

            if assym == bssym == var:
                temp_sub.append(sinst)
            if aosym == bosym == var:
                temp_obj.append(oinst)
            if assym == bosym == var:
                temp_obj.append(sinst)
            if aosym == bssym == var:
                temp_sub.append(oinst)

            brule.append((temp_sub, brel, temp_obj)) 

        return brule        

    def select_distinct(self, var, rule):
        result = set()
        
        s = [self.get_atom_size(atom) for atom in rule]
        sidx = s.index(min(s))
        satom = rule[sidx]
        svar, srel, ovar = satom
        print(satom)
        insts = self.instantiate_relation(satom)

        if var == svar[0] or var == ovar[0]:
            #print('*')
            for inst in insts:
                sinst, _, oinst = inst
                qp = self.instantiate_rule_with_variable(var, satom, sinst, 
                                                         oinst, rule)

                if self.exists(qp):
                    if var == svar[0]:
                        result.add(sinst)
                    if var == ovar[0]:
                        result.add(oinst)
                
        else:
            #print('!')
            q = [atom for atom in rule if atom != satom]
            for inst in insts:
                qp = self.instantiate_rule_with_bindings(satom, inst, q)
                result.union(self.select_distinct(var, qp))
                
        return result
    
    def select_count(self, rule):
        print('ORule: ', rule)
        head_rel = rule[0]
        sub, _, obj = head_rel
        sub_var = sub[0]
        obj_var = obj[0]
        
        c = 0
        sub_distinct = self.select_distinct(sub_var, rule)
        print(' Subs: ', len(sub_distinct))
        for sub in sub_distinct:
            qp = self.instantiate_rule_with_variable(sub_var, head_rel, sub, 
                                                     '', rule)
            #print('  QP: ', sub, qp)
            obj_distinct = self.select_distinct(obj_var, qp)
            #print(obj_distinct)
            #print(' Objs: ', obj_distinct)
            c += len(obj_distinct)
        
        return c