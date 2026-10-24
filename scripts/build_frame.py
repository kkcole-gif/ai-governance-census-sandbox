import openpyxl, random, collections, sys
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

SEED = 20261023
src = sys.argv[1]; out = sys.argv[2]
wb = openpyxl.load_workbook(src, read_only=True)
rows = list(wb['data'].iter_rows(values_only=True))
h = rows[0]; ix = {k:i for i,k in enumerate(h)}
d = [r for r in rows[1:] if r[ix['unitid']] is not None]

STATES = {'Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming'}
CONTROL = {1:'Public',2:'Private not-for-profit',3:'Private for-profit'}
ALF = {1:'Associate',2:'Associate/Baccalaureate',3:'Baccalaureate',4:"Undergraduate/Graduate-Master's",5:'Undergraduate/Graduate-Doctorate',6:'Graduate-focused'}
SETTING = {1:'Highly residential',2:'Primarily residential',3:'Residential',4:'Primarily non-residential',5:'Primarily online',6:'Online and on-campus learning',7:'Mostly full-time, not residential',8:'Mostly part-time, not residential',9:'Graduate-focused'}
SIZE = {1:'Very Small',2:'Small',3:'Medium',4:'Large',5:'Very Large'}

# Existing corpus institutions (38) matched by IPEDS name fragments
EXISTING = {
 'American Public University System':'American Public University','Carnegie Mellon University':'Carnegie Mellon','Columbia University in the City of New York':'Columbia',
 'Cornell University':'Cornell','East Carolina University':'East Carolina','Georgia Institute of Technology-Main Campus':'Georgia Tech','Harvard University':'Harvard',
 'Johns Hopkins University':'Johns Hopkins','Massachusetts Institute of Technology':'MIT','North Carolina State University at Raleigh':'NC State',
 'Ohio State University-Main Campus':'Ohio State','Pennsylvania State University-Main Campus':'Penn State','Stanford University':'Stanford',
 'University of North Carolina at Chapel Hill':'UNC Chapel Hill','University of North Carolina at Charlotte':'UNC Charlotte','University of North Carolina at Greensboro':'UNC Greensboro',
 'University of Arizona':'Arizona','University of California-Los Angeles':'UCLA','University of Chicago':'Chicago','University of Florida':'Florida',
 'University of Michigan-Ann Arbor':'Michigan','University of Notre Dame':'Notre Dame','University of Wisconsin-Madison':'Wisconsin-Madison','Vanderbilt University':'Vanderbilt',
 'Brown University':'Brown','Austin Community College District':'Austin CC','The University of Texas at Austin':'UT Austin','Yale University':'Yale','Princeton University':'Princeton',
 'Duke University':'Duke','Georgetown University':'Georgetown','University of California-Berkeley':'UC Berkeley','Indiana University-Bloomington':'Indiana',
 'Arizona State University Campus Immersion':'ASU','Rutgers University-New Brunswick':'Rutgers','Swarthmore College':'Swarthmore','Bard College':'Bard','University of Pennsylvania':'UPenn',
}
names = {r[ix['instnm']] for r in d}
missing = [k for k in EXISTING if k not in names]
print('existing not matched:', missing)

def rec(r, stratum, draw):
    return {
      'Stratum': stratum, 'Draw': draw, 'UNITID': r[ix['unitid']], 'Institution': r[ix['instnm']], 'City': r[ix['city']], 'State': r[ix['stabbr']],
      'Control': CONTROL.get(r[ix['control']]), 'Award level focus': ALF.get(r[ix['ic2025alf']]), 'Institutional classification 2025': r[ix['ic2025name']],
      'Research designation 2025': r[ix['research2025name']], 'Size': SIZE.get(r[ix['ic2025size']]), 'Setting': SETTING.get(r[ix['setting2025']]),
      'Avg enrollment': round(r[ix['size_avg']]) if isinstance(r[ix['size_avg']], (int,float)) else None,
      'HBCU': 'Yes' if r[ix['hbcu']]==1 else '', 'HSI': 'Yes' if r[ix['hsi']]==1 else '', 'Tribal': 'Yes' if r[ix['tribal']]==1 else '', 'Land-grant': 'Yes' if r[ix['landgrant']]==1 else '',
      'In existing corpus': EXISTING.get(r[ix['instnm']], ''),
      'Website': '', 'Search status': '', 'Documents found (n)': '', 'Searched on': '', 'Notes': '',
    }

# Frame: 50 states + DC, not special focus (ic2025 1..20)
JURIS = STATES | {'Puerto Rico'}
def core(r):
    # public or private nonprofit, four-year award focus, not special focus (R1/R2 exempt from the special-focus rule), never a medical school or center
    if r[ix['control']] == 3: return False
    ic = r[ix['ic2025']]
    if ic is None or ic == 27: return False
    if r[ix['research2025']] in (1,2): return True
    return (1 <= ic <= 20 or ic == 22) and r[ix['ic2025alf']] in (3,4,5)
def in_frame(r): return r[ix['stabbr']] in JURIS and core(r)
frame = [r for r in d if in_frame(r)]
excl_territory = [r for r in d if r[ix['stabbr']] not in JURIS]
excl_forprofit = [r for r in d if r[ix['stabbr']] in JURIS and r[ix['control']]==3]
excl_assoc = [r for r in d if r[ix['stabbr']] in JURIS and r[ix['control']]!=3 and r[ix['ic2025alf']] in (1,2) and r[ix['research2025']] not in (1,2)]
excl_medical_r = [r for r in d if r[ix['stabbr']] in JURIS and r[ix['control']]!=3 and r[ix['ic2025']]==27 and r[ix['research2025']] in (1,2)]
excl_special = [r for r in d if r[ix['stabbr']] in JURIS and r[ix['control']]!=3 and not in_frame(r) and r not in excl_assoc and r not in excl_medical_r]
STATESIDE = [r for r in frame if r[ix['stabbr']] in STATES]
PR = [r for r in frame if r[ix['stabbr']]=='Puerto Rico']
print('frame', len(frame), 'territory excl', len(excl_territory), 'special focus excl', len(excl_special))

R1 = [r for r in STATESIDE if r[ix['research2025']]==1]
R2 = [r for r in STATESIDE if r[ix['research2025']]==2]
DOC_other = [r for r in STATESIDE if r[ix['ic2025alf']]==5 and r[ix['research2025']] not in (1,2)]
MAST = [r for r in STATESIDE if r[ix['ic2025alf']]==4 and r[ix['research2025']] not in (1,2)]
BACC = [r for r in STATESIDE if r[ix['ic2025alf']]==3 and r[ix['research2025']] not in (1,2)]
ONLINE = [r for r in STATESIDE if r[ix['setting2025']]==5 and (r[ix['ic2025size']] or 0) >= 4]
PR_R2 = [r for r in PR if r[ix['research2025']]==2]
PR_other = [r for r in PR if r[ix['research2025']]!=2]
for n,l in [('R1',R1),('R2',R2),('Doctoral other',DOC_other),('Masters',MAST),('Bacc',BACC),('Online large',ONLINE),('PR R2',PR_R2),('PR other',PR_other)]:
    print(n, len(l), collections.Counter(CONTROL.get(r[ix['control']]) for r in l))

rng = random.Random(SEED)
def prop_sample(pool, n):
    # proportional allocation by control, largest-remainder rounding, random within cell
    groups = collections.defaultdict(list)
    for r in pool: groups[r[ix['control']]].append(r)
    total = len(pool)
    quotas = {k: n*len(v)/total for k,v in groups.items()}
    alloc = {k: int(q) for k,q in quotas.items()}
    rem = n - sum(alloc.values())
    for k,_ in sorted(quotas.items(), key=lambda kv: -(kv[1]-int(kv[1])))[:rem]: alloc[k]+=1
    out=[]
    for k in sorted(groups):
        pool_k = sorted(groups[k], key=lambda r: r[ix['unitid']])
        out += rng.sample(pool_k, min(alloc[k], len(pool_k)))
    return sorted(out, key=lambda r: r[ix['instnm']])

SIZES = {'R2':40,'Doctoral other':25,'Masters':40,'Bacc':30,'PR':8}
strata = [
 ('1 R1 census', sorted(R1, key=lambda r:r[ix['instnm']]), 'census'),
 ('2 R2 sample', prop_sample(R2, SIZES['R2']), 'random, proportional by control'),
 ('3 Doctoral not R1-R2 sample', prop_sample(DOC_other, SIZES['Doctoral other']), 'random, proportional by control'),
 ('4 Masters sample', prop_sample(MAST, SIZES['Masters']), 'random, proportional by control'),
 ('5 Baccalaureate sample', prop_sample(BACC, SIZES['Bacc']), 'random, proportional by control'),
 ('6 Puerto Rico', sorted(PR_R2, key=lambda r:r[ix['instnm']]) + prop_sample(PR_other, SIZES['PR']), 'both R2 (census) plus random 8, proportional by control'),
 ('7 Online large purposive', sorted(ONLINE, key=lambda r:r[ix['instnm']]), 'purposive: primarily online, Large or Very Large, public or nonprofit'),
]
sampled_ids = {r[ix['unitid']] for _,l,_ in strata for r in l}
# existing corpus institutions not drawn: purposive carry-over
carry = sorted([r for r in frame if r[ix['instnm']] in EXISTING and r[ix['unitid']] not in sampled_ids], key=lambda r:r[ix['instnm']])
strata.append(('8 Existing corpus carry-over', carry, 'purposive: already in the 38-institution corpus, in frame, not drawn above'))
outside = sorted([r for r in d if r[ix['instnm']] in EXISTING and not in_frame(r)], key=lambda r:r[ix['instnm']])
strata.append(('9 Corpus outside frame', outside, 'already in the 38-institution corpus but outside the frame (for-profit or associate); decision pending'))

owb = openpyxl.Workbook()
hdr_font = Font(bold=True); hdr_fill = PatternFill('solid', fgColor='DDE4EE')
def write_sheet(ws, recs):
    if not recs: return
    keys = list(recs[0].keys()); ws.append(keys)
    for c in ws[1]: c.font = hdr_font; c.fill = hdr_fill; c.alignment = Alignment(wrap_text=True, vertical='top')
    for rr in recs: ws.append([rr[k] for k in keys])
    widths = {'Institution':44,'Institutional classification 2025':40,'Research designation 2025':34,'Stratum':28,'Draw':30,'Notes':40,'In existing corpus':18,'City':16,'State':16,'Control':20,'Award level focus':26,'Setting':26}
    for i,k in enumerate(keys,1): ws.column_dimensions[get_column_letter(i)].width = widths.get(k, 13)
    ws.freeze_panes = 'D2'

# README
ws = owb.active; ws.title = 'README'
lines = [
 'AI governance census, sampling frame. Built from the 2025 Carnegie Classifications Public Data File (carnegieclassifications.acenet.edu), 3,928 institutions.',
 f'Random seed {SEED} (Python random.Random, sampling within control cells sorted by UNITID). Re-running build_frame.py with this seed reproduces every draw.',
 'Frame: public and private nonprofit institutions in the 50 states, DC, and Puerto Rico with a four-year award-level focus (Baccalaureate, Undergraduate/Graduate-Master\'s, Undergraduate/Graduate-Doctorate) in a Mixed or Professions-focused 2025 Institutional Classification (codes 1 to 20) or in Special Focus: Arts and Sciences (code 22, where the 2025 scheme files liberal arts colleges such as Williams, Swarthmore, and Davidson), plus every R1 or R2 institution whatever its classification (the 2025 scheme files MIT, Caltech, Carnegie Mellon, Georgia Tech and other engineering universities as Special Focus). Excluded: private for-profit institutions, associate-focus institutions, R1 and R2 medical schools and health science centers (code 27), other Special Focus categories, and territories other than Puerto Rico. Each exclusion list is on its own tab.',
 'Strata: 1 R1 (census). 2 R2 (random 40, allocated proportionally to control). 3 Doctoral-focus institutions with no R1 or R2 designation (random 25). 4 Master\'s-focus (random 40). 5 Baccalaureate-focus (random 30). 6 Puerto Rico (both R2 institutions plus a random 8 of the other 28 in-frame institutions). 7 Primarily online, Large or Very Large (purposive, all in frame). 8 Institutions already in the 38-institution corpus, in frame, not drawn in 1 to 7 (purposive carry-over, report separately). 9 Institutions already in the corpus but outside the frame (decision pending).',
 'Strata 2 to 5 exclude R1 and R2 institutions, which are covered by strata 1 and 2, so the strata do not overlap. Control allocation uses largest-remainder rounding. Within each control cell, the draw is a simple random sample.',
 'Puerto Rico: many in-frame institutions are campuses of three systems (University of Puerto Rico, Inter American University, Universidad Ana G. Mendez). Where a campus is drawn, the search covers the system-level policy as well, recorded against the campus row. Spanish-language documents are in scope and the protocol should say so.',
 'Columns Website, Search status, Documents found, Searched on, and Notes are empty and belong to the search phase.',
 'Tab All drawn lists every institution in strata 1 to 8 in one sheet for the search phase. Tab Frame counts gives population and sample sizes by stratum and control.',
]
for l in lines: ws.append([l])
ws.column_dimensions['A'].width = 140
for row in ws.iter_rows():
    for c in row: c.alignment = Alignment(wrap_text=True, vertical='top')

all_recs=[]
for name, lst, draw in strata:
    recs = [rec(r, name, draw) for r in lst]; all_recs += recs
    write_sheet(owb.create_sheet(name[:31]), recs)
write_sheet(owb.create_sheet('All drawn'), all_recs)

# counts
ws = owb.create_sheet('Frame counts')
ws.append(['Stratum','Population in frame','Drawn','Public (pop)','Private NFP (pop)','For-profit (pop)','Public (drawn)','Private NFP (drawn)','For-profit (drawn)'])
pops = {'1 R1 census':R1,'2 R2 sample':R2,'3 Doctoral not R1-R2 sample':DOC_other,'4 Masters sample':MAST,'5 Baccalaureate sample':BACC,'6 Puerto Rico':PR,'7 Online large purposive':ONLINE,'8 Existing corpus carry-over':carry,'9 Corpus outside frame':outside}
for name,lst,_ in strata:
    pop = pops[name]; cp = collections.Counter(r[ix['control']] for r in pop); cd = collections.Counter(r[ix['control']] for r in lst)
    ws.append([name, len(pop), len(lst), cp[1],cp[2],cp[3], cd[1],cd[2],cd[3]])
ws.append(['Total', len(frame), len(all_recs)])
for c in ws[1]: c.font = hdr_font; c.fill = hdr_fill
ws.column_dimensions['A'].width = 30

# exclusions
def excl_sheet(title, lst):
    ws = owb.create_sheet(title)
    ws.append(['UNITID','Institution','State','Control','Institutional classification 2025','Research designation 2025'])
    for c in ws[1]: c.font = hdr_font; c.fill = hdr_fill
    for r in sorted(lst, key=lambda r: (r[ix['stabbr']] or '', r[ix['instnm']])):
        ws.append([r[ix['unitid']], r[ix['instnm']], r[ix['stabbr']], CONTROL.get(r[ix['control']]), r[ix['ic2025name']], r[ix['research2025name']]])
    ws.column_dimensions['B'].width=44; ws.column_dimensions['E'].width=40; ws.column_dimensions['F'].width=34
excl_sheet('Excluded R1-R2 medical centers', excl_medical_r)
excl_sheet('Excluded for-profit', excl_forprofit)
excl_sheet('Excluded associate', excl_assoc)
excl_sheet('Excluded special focus', excl_special)
excl_sheet('Excluded territories', excl_territory)
owb.save(out)
print('total drawn', len(all_recs))
