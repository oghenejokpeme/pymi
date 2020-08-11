import unittest
from src.modules.kb import load_kb

class TestKb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adb = load_kb('./tests/kbs/aplus.tsv')
        cls.tdb = load_kb('./tests/kbs/thesis.tsv')
    
    def test_kb_sro(self):
        ares = {'<Adam>' :{'<LivesIn>'   :{'<Paris>', '<Rome>'},
                           '<wasBornIn>' :{'<Paris>'}},
                '<Bob>'  :{'<LivesIn>'   :{'<Zurich>'}},
                '<Carl>' :{'<wasBornIn>' :{'<Rome>'}}
               }
        tres = {'<Jean>'    :{'<LivesIn>'   :{'<Paris>'},
                              '<wasBornIn>' :{'<Paris>'}},
                '<Thomas>'  :{'<LivesIn>'   :{'<Munich>'},
                              '<wasBornIn>' :{'<Munich>'}},
                '<Antoine>' :{'<LivesIn>'   :{'<Paris>'},
                              '<wasBornIn>' :{'<Colmar>'}},
                '<Danai>'   :{'<LivesIn>'   :{'<Marseille>'}}
               }

        self.assertEqual(self.adb['kb']['SRO'], ares)
        self.assertEqual(self.tdb['kb']['SRO'], tres)

    def test_kb_sor(self):
        ares = {'<Adam>' :{'<Paris>'  :{'<LivesIn>', '<wasBornIn>'},
                           '<Rome>'   :{'<LivesIn>'}},
                '<Bob>'  :{'<Zurich>' :{'<LivesIn>'}},
                '<Carl>' :{'<Rome>'   :{'<wasBornIn>'}}
               }
        tres = {'<Jean>'    :{'<Paris>'     :{'<LivesIn>', '<wasBornIn>'}},
                '<Thomas>'  :{'<Munich>'    :{'<LivesIn>', '<wasBornIn>'}},
                '<Antoine>' :{'<Paris>'     :{'<LivesIn>'},
                              '<Colmar>'    :{'<wasBornIn>'}},
                '<Danai>'   :{'<Marseille>' :{'<LivesIn>'}}
               }

        self.assertEqual(self.adb['kb']['SOR'], ares)
        self.assertEqual(self.tdb['kb']['SOR'], tres)

    def test_kb_rso(self):
        ares = {'<LivesIn>'   :{'<Adam>' :{'<Paris>', '<Rome>'},
                                '<Bob>'  :{'<Zurich>'}},
                '<wasBornIn>' :{'<Adam>' :{'<Paris>'},
                                '<Carl>' :{'<Rome>'}}
               }
        tres = {'<LivesIn>'   :{'<Jean>'    :{'<Paris>'},
                                '<Thomas>'  :{'<Munich>'},
                                '<Antoine>' :{'<Paris>'},
                                '<Danai>'   :{'<Marseille>'}},
                '<wasBornIn>' :{'<Jean>'    :{'<Paris>'},
                                '<Thomas>'  :{'<Munich>'},
                                '<Antoine>' :{'<Colmar>'}}
               }

        self.assertEqual(self.adb['kb']['RSO'], ares)
        self.assertEqual(self.tdb['kb']['RSO'], tres)

    def test_kb_ros(self):
        ares = {'<LivesIn>'   :{'<Paris>'  :{'<Adam>'},
                                '<Rome>'   :{'<Adam>'},
                                '<Zurich>' :{'<Bob>'}},
                '<wasBornIn>' :{'<Paris>'  :{'<Adam>'},
                                '<Rome>'   :{'<Carl>'}}
               }
        tres = {'<LivesIn>'   :{'<Paris>'     :{'<Jean>', '<Antoine>'},
                                '<Munich>'    :{'<Thomas>'},
                                '<Marseille>' :{'<Danai>'}},
                '<wasBornIn>' :{'<Paris>'     :{'<Jean>'},
                                '<Munich>'    :{'<Thomas>'},
                                '<Colmar>'    :{'<Antoine>'}}
               }

        self.assertEqual(self.adb['kb']['ROS'], ares)
        self.assertEqual(self.tdb['kb']['ROS'], tres)

    def test_kb_osr(self):
        ares = {'<Paris>'  :{'<Adam>' :{'<LivesIn>', '<wasBornIn>'}},
                '<Rome>'   :{'<Adam>' :{'<LivesIn>'},
                             '<Carl>' :{'<wasBornIn>'}},
                '<Zurich>' :{'<Bob>'  :{'<LivesIn>'}}
               }
        tres = {'<Paris>'     :{'<Jean>'    :{'<LivesIn>', '<wasBornIn>'},
                                '<Antoine>' :{'<LivesIn>'}},
                '<Munich>'    :{'<Thomas>'  :{'<LivesIn>', '<wasBornIn>'}},
                '<Marseille>' :{'<Danai>'   :{'<LivesIn>'}},
                '<Colmar>'    :{'<Antoine>' :{'<wasBornIn>'}}
               }

        self.assertEqual(self.adb['kb']['OSR'], ares)
        self.assertEqual(self.tdb['kb']['OSR'], tres)

    def test_kb_ors(self):
        ares = {'<Paris>'  :{'<LivesIn>'   :{'<Adam>'},
                             '<wasBornIn>' :{'<Adam>'}},
                '<Rome>'   :{'<LivesIn>'   :{'<Adam>'},
                             '<wasBornIn>' :{'<Carl>'}},
                '<Zurich>' :{'<LivesIn>'   :{'<Bob>'}}
               }
        tres = {'<Paris>'     :{'<LivesIn>'   :{'<Jean>', '<Antoine>'},
                                '<wasBornIn>' :{'<Jean>'}},
                '<Munich>'    :{'<LivesIn>'   :{'<Thomas>'},
                                '<wasBornIn>' :{'<Thomas>'}},
                '<Marseille>' :{'<LivesIn>'   :{'<Danai>'}},
                '<Colmar>'    :{'<wasBornIn>' :{'<Antoine>'}}
               }

        self.assertEqual(self.adb['kb']['ORS'], ares)
        self.assertEqual(self.tdb['kb']['ORS'], tres)
    
    def test_kb_agg_p(self):
        """Tests relations aggregated index."""
        ares = {'<LivesIn>'   :{('<Adam>', '<LivesIn>', '<Paris>'),
                                ('<Adam>', '<LivesIn>', '<Rome>'),
                                ('<Bob>',  '<LivesIn>', '<Zurich>')},
                '<wasBornIn>' :{('<Adam>', '<wasBornIn>', '<Paris>'),
                                ('<Carl>', '<wasBornIn>', '<Rome>')}
               }
        tres = {'<LivesIn>'   :{('<Jean>',    '<LivesIn>', '<Paris>'),
                                ('<Thomas>',  '<LivesIn>', '<Munich>'),
                                ('<Antoine>', '<LivesIn>', '<Paris>'),
                                ('<Danai>',   '<LivesIn>', '<Marseille>')},
                '<wasBornIn>' :{('<Jean>',    '<wasBornIn>', '<Paris>'),
                                ('<Thomas>',  '<wasBornIn>', '<Munich>'),
                                ('<Antoine>', '<wasBornIn>', '<Colmar>')}
               }

        self.assertEqual(self.adb['agg_index']['P'], ares)
        self.assertEqual(self.tdb['agg_index']['P'], tres)

    def test_kb_agg_s(self):
        """Tests subjects aggregated index."""
        ares = {'<Adam>' :{('<Adam>', '<LivesIn>', '<Paris>'),
                           ('<Adam>', '<LivesIn>', '<Rome>'),
                           ('<Adam>', '<wasBornIn>', '<Paris>')},
                '<Bob>'  :{('<Bob>',  '<LivesIn>', '<Zurich>')},
                '<Carl>' :{('<Carl>', '<wasBornIn>', '<Rome>')}
               }
        tres = {'<Jean>'    :{('<Jean>',    '<LivesIn>', '<Paris>'),
                              ('<Jean>',    '<wasBornIn>', '<Paris>')},
                '<Thomas>'  :{('<Thomas>',  '<LivesIn>', '<Munich>'),
                              ('<Thomas>',  '<wasBornIn>', '<Munich>')},
                '<Antoine>' :{('<Antoine>', '<LivesIn>', '<Paris>'),
                              ('<Antoine>', '<wasBornIn>', '<Colmar>')},
                '<Danai>'   :{('<Danai>',   '<LivesIn>', '<Marseille>')}}

        self.assertEqual(self.adb['agg_index']['S'], ares)
        self.assertEqual(self.tdb['agg_index']['S'], tres)

    def test_kb_agg_o(self):
        """Tests objects aggregated index."""
        ares = {'<Paris>'  :{('<Adam>', '<LivesIn>', '<Paris>'),
                             ('<Adam>', '<wasBornIn>', '<Paris>')},
                '<Rome>'   :{('<Adam>', '<LivesIn>', '<Rome>'),
                             ('<Carl>', '<wasBornIn>', '<Rome>')},
                '<Zurich>' :{('<Bob>',  '<LivesIn>', '<Zurich>')}}
        tres = {'<Paris>'     :{('<Jean>',    '<LivesIn>', '<Paris>'),
                                ('<Jean>',    '<wasBornIn>', '<Paris>'),
                                ('<Antoine>', '<LivesIn>', '<Paris>')},
                '<Munich>'    :{('<Thomas>',  '<LivesIn>', '<Munich>'),
                                ('<Thomas>',  '<wasBornIn>', '<Munich>')},
                '<Marseille>' :{('<Danai>',   '<LivesIn>', '<Marseille>')},
                '<Colmar>'    :{('<Antoine>', '<wasBornIn>', '<Colmar>')}}

        self.assertEqual(self.adb['agg_index']['O'], ares)
        self.assertEqual(self.tdb['agg_index']['O'], tres)

if '__name__' == '__main__':
    unittest.main()