import unittest
from src.modules.kb import load_kb
from src.modules.queries import *

class TestQueries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adb = load_kb('./tests/kbs/aplus.tsv')
        cls.tdb = load_kb('./tests/kbs/thesis.tsv')
        cls.ydb = load_kb('./tests/kbs/yago2_sample.tsv')

    def test_legal_atom_instantiation(self):
        adba = (('?a',), '<LivesIn>', ('?b',))
        adba_res = {(('?a', '<Adam>'), '<LivesIn>', ('?b', '<Paris>')), 
                    (('?a', '<Adam>'), '<LivesIn>', ('?b', '<Rome>')),
                    (('?a', '<Bob>'),  '<LivesIn>', ('?b', '<Zurich>'))}
        
        adbb = (('?a', '<Adam>'), '<LivesIn>', ('?b',))
        adbb_res = {(('?a', '<Adam>'), '<LivesIn>', ('?b', '<Paris>')), 
                    (('?a', '<Adam>'), '<LivesIn>', ('?b', '<Rome>'))}

        adbc = (('?a',), '<LivesIn>', ('?b', '<Rome>'))
        adbc_res = {(('?a', '<Adam>'), '<LivesIn>', ('?b', '<Rome>'))}
        
        adbd = (('?a', '<Adam>'), '<LivesIn>', ('?b', '<Rome>'))
        adbd_res = {(('?a', '<Adam>'), '<LivesIn>', ('?b', '<Rome>'))}
        
        tdba = (('?a',), '<LivesIn>', ('?b',))
        tdba_res = {(('?a', '<Jean>'),    '<LivesIn>', ('?b', '<Paris>')), 
                    (('?a', '<Thomas>'),  '<LivesIn>', ('?b', '<Munich>')),
                    (('?a', '<Antoine>'), '<LivesIn>', ('?b', '<Paris>')),
                    (('?a', '<Danai>'),   '<LivesIn>', ('?b', '<Marseille>'))}
        
        tdbb = (('?a', '<Danai>'), '<LivesIn>', ('?b',))
        tdbb_res = {(('?a', '<Danai>'), '<LivesIn>', ('?b', '<Marseille>'))}

        tdbc = (('?a',), '<wasBornIn>', ('?b', '<Colmar>'))
        tdbc_res = {(('?a', '<Antoine>'), '<wasBornIn>', ('?b', '<Colmar>'))}

        tdbd = (('?a',), '<LivesIn>', ('?b', '<Paris>'))
        tdbd_res = {(('?a', '<Jean>'),    '<LivesIn>', ('?b', '<Paris>')),
                    (('?a', '<Antoine>'), '<LivesIn>', ('?b', '<Paris>'))}
        tdbe = (('?a', '<Antoine>'), '<wasBornIn>', ('?b', '<Colmar>'))
        tdbe_res = {(('?a', '<Antoine>'), '<wasBornIn>', ('?b', '<Colmar>'))}

        self.assertEqual(get_atom_instantiations(adba, self.adb), adba_res)
        self.assertEqual(get_atom_instantiations(adbb, self.adb), adbb_res)
        self.assertEqual(get_atom_instantiations(adbc, self.adb), adbc_res)
        self.assertEqual(get_atom_instantiations(adbd, self.adb), adbd_res)

        self.assertEqual(get_atom_instantiations(tdba, self.tdb), tdba_res)
        self.assertEqual(get_atom_instantiations(tdbb, self.tdb), tdbb_res)
        self.assertEqual(get_atom_instantiations(tdbc, self.tdb), tdbc_res)
        self.assertEqual(get_atom_instantiations(tdbd, self.tdb), tdbd_res)
        self.assertEqual(get_atom_instantiations(tdbe, self.tdb), tdbe_res)

    def test_illegal_atom_instantiation(self):
        a = (('?a', '<a>', '<a>'), '<LivesIn>', ('?b',))
        b = (('?a',), '<LivesIn>', ('?b', '<b>', '<b>'))
        c = (('?a', '<a>', '<a>'), '<LivesIn>', ('?b', '<b>', '<b>'))
        
        with self.assertRaises(Exception): 
            get_atom_instantiations(a, self.adb)
            get_atom_instantiations(b, self.adb)
            get_atom_instantiations(c, self.adb)

    def test_atom_size(self):
        adba = (('?a',), '<LivesIn>', ('?b',))
        adbb = (('?a', '<Adam>'), '<LivesIn>', ('?b',))
        adbc = (('?a',), '<LivesIn>', ('?b', '<Rome>'))
        adbd = (('?a', '<Adam>'), '<LivesIn>', ('?b', '<Rome>'))
        adbe = (('?a', '<Adam>'), '<LivesIn>', ('?b', '<Spain>'))
        
        tdba = (('?a',), '<LivesIn>', ('?b',))
        tdbb = (('?a', '<Danai>'), '<LivesIn>', ('?b',))
        tdbc = (('?a',), '<wasBornIn>', ('?b', '<Colmar>'))
        tdbd = (('?a',), '<LivesIn>', ('?b', '<Paris>'))
        tdbe = (('?a', '<Antoine>'), '<wasBornIn>', ('?b', '<Colmar>'))

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
    
    def test_instantiate_query_with_atom_bindings(self):
        iaa = (('?a',), '<rel>', ('?b',))
        iab = (('?a', '<svar>'), '<rel>', ('?b',))
        iac = (('?a',), '<rel>', ('?b', '<ovar>'))
        iad = (('?a', '<svar>'), '<rel>', ('?b', '<ovar>'))  
        
        q = {(('?a',), '<relA>', ('?b',))}
        self.assertEqual(instantiate_query_with_atom_bindings(q, iaa), 
                         {(('?a',), '<relA>', ('?b',))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iab), 
                         {(('?a', '<svar>'), '<relA>', ('?b',))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iac), 
                         {(('?a',), '<relA>', ('?b', '<ovar>'))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iad), 
                         {(('?a', '<svar>'), '<relA>', ('?b', '<ovar>'))})
        
        q = {(('?a',), '<relA>', ('?c',))}
        self.assertEqual(instantiate_query_with_atom_bindings(q, iaa), 
                         {(('?a',), '<relA>', ('?c',))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iab), 
                         {(('?a', '<svar>'), '<relA>', ('?c',))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iac), 
                         {(('?a',), '<relA>', ('?c',))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iad), 
                         {(('?a', '<svar>'), '<relA>', ('?c',))})
        
        q = {(('?e',), '<relA>', ('?b',))}
        self.assertEqual(instantiate_query_with_atom_bindings(q, iaa), 
                         {(('?e',), '<relA>', ('?b',))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iab), 
                         {(('?e',), '<relA>', ('?b',))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iac), 
                         {(('?e',), '<relA>', ('?b', '<ovar>'))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iad), 
                         {(('?e',), '<relA>', ('?b', '<ovar>'))})

        q = {(('?e',), '<relA>', ('?f',))}
        self.assertEqual(instantiate_query_with_atom_bindings(q, iaa), 
                         {(('?e',), '<relA>', ('?f',))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iab), 
                         {(('?e',), '<relA>', ('?f',))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iac), 
                         {(('?e',), '<relA>', ('?f',))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iad), 
                         {(('?e',), '<relA>', ('?f',))})

        q = {(('?b',), '<relA>', ('?a',))}
        self.assertEqual(instantiate_query_with_atom_bindings(q, iaa), 
                         {(('?b',), '<relA>', ('?a',))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iab), 
                         {(('?b',), '<relA>', ('?a', '<svar>'))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iac), 
                         {(('?b', '<ovar>'), '<relA>', ('?a',))})
        self.assertEqual(instantiate_query_with_atom_bindings(q, iad), 
                         {(('?b', '<ovar>'), '<relA>', ('?a', '<svar>'))})
        
        q = {(('?a',), '<relA>', ('?b',)), (('?a',), '<relB>', ('?b',))}
        aq = {(('?a',), '<relA>', ('?b',)), (('?a',), '<relB>', ('?b',))}
        self.assertEqual(instantiate_query_with_atom_bindings(q, iaa), aq)
        aq = {(('?a', '<svar>'), '<relA>', ('?b',)), 
              (('?a', '<svar>'), '<relB>', ('?b',))}
        self.assertEqual(instantiate_query_with_atom_bindings(q, iab), aq)
        aq = {(('?a',), '<relA>', ('?b', '<ovar>')), 
              (('?a',), '<relB>', ('?b', '<ovar>'))}
        self.assertEqual(instantiate_query_with_atom_bindings(q, iac), aq)
        aq = {(('?a', '<svar>'), '<relA>', ('?b', '<ovar>')), 
              (('?a', '<svar>'), '<relB>', ('?b', '<ovar>'))}
        self.assertEqual(instantiate_query_with_atom_bindings(q, iad), aq)

        q = {(('?a',), '<relA>', ('?e',)), (('?b',), '<relB>', ('?f',))}
        aq = {(('?a',), '<relA>', ('?e',)), (('?b',), '<relB>', ('?f',))}
        self.assertEqual(instantiate_query_with_atom_bindings(q, iaa), aq)
        aq = {(('?a', '<svar>'), '<relA>', ('?e',)), 
              (('?b',), '<relB>', ('?f',))}
        self.assertEqual(instantiate_query_with_atom_bindings(q, iab), aq)
        aq = {(('?a',), '<relA>', ('?e',)), 
              (('?b', '<ovar>'), '<relB>', ('?f',))}
        self.assertEqual(instantiate_query_with_atom_bindings(q, iac), aq)
        aq = {(('?a', '<svar>'), '<relA>', ('?e',)), 
              (('?b', '<ovar>'), '<relB>', ('?f',))}
        self.assertEqual(instantiate_query_with_atom_bindings(q, iad), aq)

    def test_check_query_existence(self):
        adbq = {(('?a',), '<LivesIn>', ('?b',))} 
        self.assertEqual(check_query_existence(adbq, self.adb), True)

        adbq = {(('?a',), '<LivesIn>', ('?b',)),
                (('?a',), '<wasBornIn>', ('?c',))}
        self.assertEqual(check_query_existence(adbq, self.adb), True)

        adbq = {(('?a',), '<DiedIn>', ('?b',)),
                (('?a',), '<wasBornIn>', ('?b',))}
        self.assertEqual(check_query_existence(adbq, self.adb), False)

        ydbq = {(('?a',), '<wasBornIn>', ('?b',))}
        self.assertEqual(check_query_existence(ydbq, self.ydb), True)

        ydbq = {(('?f',), '<hasChild>', ('?b',)),
                (('?a',), '<isMarriedTo>', ('?f',))}
        self.assertEqual(check_query_existence(ydbq, self.ydb), True)

        ydbq = {(('?e',), '<graduatedFrom>', ('?b',)), 
                (('?e',), '<hasAcademicAdvisor>', ('?a',))}
        self.assertEqual(check_query_existence(ydbq, self.ydb), True)


if '__name__' == '__main__':
    unittest.main()