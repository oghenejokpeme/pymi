import sys
from modules import kb, queries, rule

def main(argv):
    db = kb.load_kb(argv[0])
    q = {(('?e',), '<graduatedFrom>', ('?b',)), 
         (('?e',), '<hasAcademicAdvisor>', ('?a',))}
    q = {(('?a',), '<LivesIn>', ('?b',)),
         (('?a',), '<wasBornIn>', ('?c',))}
    #v = queries.check_query_existence(q, db)
    v = queries.select_distinct_for_query('?b', q, db, set())
    print()
    print('Answer:', v)

if __name__ == '__main__':
    main(sys.argv[1:])