import unittest
from src.modules.kb import load_kb
from src.modules.rule import Atom
from src.modules.queries import *

class TestQueries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adb = load_kb('./tests/kbs/aplus.tsv')
        cls.tdb = load_kb('./tests/kbs/thesis.tsv')
        cls.ydb = load_kb('./tests/kbs/yago2_sample.tsv')

    def test_legal_atom_instantiation(self):
        adba = Atom('?a', None, '<LivesIn>', '?b', None)
        adba_res = {Atom('?a', '<Adam>', '<LivesIn>', '?b', '<Paris>'),
                    Atom('?a', '<Adam>', '<LivesIn>', '?b', '<Rome>'),
                    Atom('?a', '<Bob>', '<LivesIn>', '?b', '<Zurich>')}

        adbb = Atom('?a', '<Adam>', '<LivesIn>', '?b', None)
        adbb_res = {Atom('?a', '<Adam>', '<LivesIn>', '?b', '<Paris>'),
                    Atom('?a', '<Adam>', '<LivesIn>', '?b', '<Rome>')}
            
        adbc = Atom('?a', None, '<LivesIn>', '?b', '<Rome>')
        adbc_res = {Atom('?a', '<Adam>', '<LivesIn>', '?b', '<Rome>')}
                
        adbd = Atom('?a', None, '<LivesIn>', '?b', '<Rome>')
        adbd_res = {Atom('?a', '<Adam>', '<LivesIn>', '?b', '<Rome>')}
        
        tdba = Atom('?a', None, '<LivesIn>', '?b', None)
        tdba_res = {Atom('?a', '<Jean>',    '<LivesIn>', '?b', '<Paris>'),
                    Atom('?a', '<Thomas>',  '<LivesIn>', '?b', '<Munich>'),
                    Atom('?a', '<Antoine>', '<LivesIn>', '?b', '<Paris>'),
                    Atom('?a', '<Danai>',   '<LivesIn>', '?b', '<Marseille>')}

        tdbb = Atom('?a', '<Danai>', '<LivesIn>', '?b', None)
        tdbb_res = {Atom('?a', '<Danai>',   '<LivesIn>', '?b', '<Marseille>')}

        tdbc = Atom('?a', None, '<wasBornIn>', '?b', '<Colmar>')
        tdbc_res = {Atom('?a', '<Antoine>',   '<wasBornIn>', '?b', '<Colmar>')}

        tdbd = Atom('?a', None, '<LivesIn>', '?b', '<Paris>')
        tdbd_res = {Atom('?a', '<Jean>',    '<LivesIn>', '?b', '<Paris>'),
                    Atom('?a', '<Antoine>', '<LivesIn>', '?b', '<Paris>')}

        tdbe = Atom('?a', '<Antoine>', '<wasBornIn>', '?b', '<Colmar>')
        tdbe_res = {Atom('?a', '<Antoine>', '<wasBornIn>', '?b', '<Colmar>')}

        self.assertEqual(get_atom_instantiations(adba, self.adb), adba_res)
        self.assertEqual(get_atom_instantiations(adbb, self.adb), adbb_res)
        self.assertEqual(get_atom_instantiations(adbc, self.adb), adbc_res)
        self.assertEqual(get_atom_instantiations(adbd, self.adb), adbd_res)

        self.assertEqual(get_atom_instantiations(tdba, self.tdb), tdba_res)
        self.assertEqual(get_atom_instantiations(tdbb, self.tdb), tdbb_res)
        self.assertEqual(get_atom_instantiations(tdbc, self.tdb), tdbc_res)
        self.assertEqual(get_atom_instantiations(tdbd, self.tdb), tdbd_res)
        self.assertEqual(get_atom_instantiations(tdbe, self.tdb), tdbe_res)

    def test_atom_size(self):
        adba = Atom('?a', None, '<LivesIn>', '?b', None)
        adbb = Atom('?a', '<Adam>', '<LivesIn>', '?b', None)
        adbc = Atom('?a', None, '<LivesIn>', '?b', '<Rome>')
        adbd = Atom('?a', '<Adam>', '<LivesIn>', '?b', '<Rome>')
        adbe = Atom('?a', '<Adam>', '<LivesIn>', '?b', '<Spain>')

        tdba = Atom('?a', None, '<LivesIn>', '?b', None)
        tdbb = Atom('?a', '<Danai>', '<LivesIn>', '?b', None)
        tdbc = Atom('?a', None, '<wasBornIn>', '?b', '<Colmar>')
        tdbd = Atom('?a', None, '<LivesIn>', '?b', '<Paris>')
        tdbe = Atom('?a', '<Antoine>', '<wasBornIn>', '?b', '<Colmar>')

        self.assertEqual(get_atom_size(adba, self.adb), 3)
        self.assertEqual(get_atom_size(adbb, self.adb), 2)
        self.assertEqual(get_atom_size(adbc, self.adb), 1)
        self.assertEqual(get_atom_size(adbd, self.adb), 1)
        self.assertEqual(get_atom_size(adbe, self.adb), 0)

        self.assertEqual(get_atom_size(tdba, self.tdb), 4)
        self.assertEqual(get_atom_size(tdbb, self.tdb), 1)
        self.assertEqual(get_atom_size(tdbc, self.tdb), 1)
        self.assertEqual(get_atom_size(tdbd, self.tdb), 2)
        self.assertEqual(get_atom_size(tdbe, self.tdb), 1)
    
    def test_instantiate_with_atom_bindings(self):
        iaa = Atom('?a', None, '<rel>', '?b', None)
        iab = Atom('?a', '<svar>', '<rel>', '?b', None)
        iac = Atom('?a', None, '<rel>', '?b', '<ovar>')
        iad = Atom('?a', '<svar>', '<rel>', '?b', '<ovar>') 
        
        q = Atom('?a', None, '<relA>', '?b', None)
        self.assertEqual(instantiate_with_atom_bindings(iaa, q), 
                         Atom('?a', None, '<relA>', '?b', None))
        self.assertEqual(instantiate_with_atom_bindings(iab, q), 
                         Atom('?a', '<svar>', '<relA>', '?b', None))
        self.assertEqual(instantiate_with_atom_bindings(iac, q), 
                         Atom('?a', None, '<relA>', '?b', '<ovar>'))
        self.assertEqual(instantiate_with_atom_bindings(iad, q), 
                         Atom('?a', '<svar>', '<relA>', '?b', '<ovar>'))
    
        q = Atom('?a', None, '<relA>', '?c', None)  
        self.assertEqual(instantiate_with_atom_bindings(iaa, q), 
                         Atom('?a', None, '<relA>', '?c', None))
        self.assertEqual(instantiate_with_atom_bindings(iab, q), 
                         Atom('?a', '<svar>', '<relA>', '?c', None))
        self.assertEqual(instantiate_with_atom_bindings(iac, q), 
                         Atom('?a', None, '<relA>', '?c', None))
        self.assertEqual(instantiate_with_atom_bindings(iad, q), 
                         Atom('?a', '<svar>', '<relA>', '?c', None))

        
        q = Atom('?e', None, '<relA>', '?b', None)
        self.assertEqual(instantiate_with_atom_bindings(iaa, q), 
                         Atom('?e', None, '<relA>', '?b', None))
        self.assertEqual(instantiate_with_atom_bindings(iab, q), 
                         Atom('?e', None, '<relA>', '?b', None))
        self.assertEqual(instantiate_with_atom_bindings(iac, q), 
                         Atom('?e', None, '<relA>', '?b', '<ovar>'))
        self.assertEqual(instantiate_with_atom_bindings(iad, q), 
                         Atom('?e', None, '<relA>', '?b', '<ovar>'))


        q = Atom('?e', None, '<relA>', '?f', None)
        self.assertEqual(instantiate_with_atom_bindings(iaa, q), 
                         Atom('?e', None, '<relA>', '?f', None))
        self.assertEqual(instantiate_with_atom_bindings(iab, q), 
                         Atom('?e', None, '<relA>', '?f', None))
        self.assertEqual(instantiate_with_atom_bindings(iac, q), 
                         Atom('?e', None, '<relA>', '?f', None))
        self.assertEqual(instantiate_with_atom_bindings(iad, q), 
                         Atom('?e', None, '<relA>', '?f', None))

        q = Atom('?b', None, '<relA>', '?a', None)
        self.assertEqual(instantiate_with_atom_bindings(iaa, q), 
                         Atom('?b', None, '<relA>', '?a', None))
        self.assertEqual(instantiate_with_atom_bindings(iab, q), 
                         Atom('?b', None, '<relA>', '?a', '<svar>'))
        self.assertEqual(instantiate_with_atom_bindings(iac, q), 
                         Atom('?b', '<ovar>', '<relA>', '?a', None))
        self.assertEqual(instantiate_with_atom_bindings(iad, q), 
                         Atom('?b', '<ovar>', '<relA>', '?a', '<svar>'))
      
        
    def test_check_query_existence(self):
        adbq = {Atom('?a', None, '<LivesIn>', '?b', None)} 
        self.assertEqual(check_query_existence(adbq, self.adb), True)

        adbq = {Atom('?a', None, '<LivesIn>', '?b', None),
                Atom('?a', None, '<wasBornIn>', '?c', None)}
        self.assertEqual(check_query_existence(adbq, self.adb), True)

        adbq = {Atom('?a', None, '<DiedIn>', '?b', None),
                Atom('?a', None, '<wasBornIn>', '?c', None)}
        self.assertEqual(check_query_existence(adbq, self.adb), False)

        ydbq = {Atom('?a', None, '<wasBornIn>', '?b', None)}
        self.assertEqual(check_query_existence(ydbq, self.ydb), True)

        ydbq = {Atom('?f', None, '<hasChild>', '?b', None),
                Atom('?a', None, '<isMarriedTo>', '?f', None)}
        self.assertEqual(check_query_existence(ydbq, self.ydb), True)

        ydbq = {Atom('?e', None, '<graduatedFrom>', '?b', None), 
                Atom('?e', None, '<hasAcademicAdvisor>', '?a', None)}
        self.assertEqual(check_query_existence(ydbq, self.ydb), True)

if '__name__' == '__main__':
    unittest.main()