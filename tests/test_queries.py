import unittest
from src.modules.kb import load_kb
from src.modules.queries import *

class TestQueries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adb = load_kb('./tests/kbs/aplus.tsv')
        cls.tdb = load_kb('./tests/kbs/thesis.tsv')

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

if '__name__' == '__main__':
    unittest.main()