"""Reproduce source-backed icon/objective evidence; requires json5, no game execution."""
import io,json,zipfile,hashlib,itertools,re,argparse
from pathlib import Path
import json5
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--export',required=True,type=Path)
parser.add_argument('--sdk',required=True,type=Path)
parser.add_argument('--write',action='store_true',help='regenerate the checked-in receipt rather than compare it')
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
vs=args.sdk/'assets'
export=args.export
ledger=json.loads((root/'docs/evidence/butchering-sources.json').read_text())
assert hashlib.sha256(export.read_bytes()).hexdigest()==ledger['sha256']
z=zipfile.ZipFile(export)
for member, expected in ledger['members'].items():
 if '!/' in member:
  archive, nested=member.split('!/',1)
  raw=zipfile.ZipFile(io.BytesIO(z.read(archive))).read(nested)
 else:raw=z.read(member)
 assert hashlib.sha256(raw).hexdigest()==expected, 'Source hash mismatch: '+member
b=zipfile.ZipFile(io.BytesIO(z.read('mods/butchering_1.14.3.zip')))
assert hashlib.sha256(z.read('mods/butchering_1.14.3.zip')).hexdigest()==ledger['members']['mods/butchering_1.14.3.zip']
assets=[]
for n in b.namelist():
 if n.endswith('.json') and '/patches/' not in n and ('/itemtypes/' in n or '/blocktypes/' in n):assets.append(('butchering',n,b.read(n),'Butchering 1.14.3'))
for modname,domain in [('armoryfork_1.11.4.zip','armory'),('rusticcookery_1.2.0.zip','rusticcookery')]:
 a=zipfile.ZipFile(io.BytesIO(z.read('mods/'+modname)))
 for n in a.namelist():
  if n.endswith('.json') and '/patches/' not in n and ('/itemtypes/' in n or '/blocktypes/' in n):assets.append((domain,n,a.read(n),modname))
for filename in ['tool/knife','resource/hide','resource/leather','food/redmeat','food/bushmeat','food/poultry']:
 p=vs/('survival/itemtypes/'+filename+'.json');assets.append(('game',str(p.relative_to(vs)),p.read_bytes(),'Vintage Story 1.22.7'))
objectives=json.loads((root/'docs/evidence/butchering-objectives.json').read_text())
icons={q['icon'] for q in objectives['quests'].values()}
results={}; examples={}
for domain,name,raw,provider in assets:
 d=json5.loads(raw.decode()); low={k.lower():v for k,v in d.items()};base=low['code']; groups=[];properties=[]
 for g in low.get('variantgroups',[]):
  if 'states' in g:groups.append(g['states'])
  else:
   nameprop=g['loadFromProperties'].removeprefix('game:');p=vs/('survival/worldproperties/'+nameprop+'.json');rawprop=p.read_bytes();states=[s['code'] for s in json5.loads(rawprop.decode())['variants']];groups.append(states);properties.append({'path':str(p.relative_to(vs)),'sha256':hashlib.sha256(rawprop).hexdigest(),'states':states})
 codes=[domain+':'+base+'-'+'-'.join(s) if s else domain+':'+base for s in itertools.product(*groups)]
 # Respect skip/allow wildcards as authored; these assets have explicit variant states.
 def match(p,c):return re.fullmatch(p[1:] if p.startswith('@') else re.escape(p).replace(r'\*','.*'),c.split(':',1)[1]) is not None
 codes=[c for c in codes if not any(match(p,c) for p in low.get('skipvariants',[])) and (not low.get('allowedvariants') or any(match(p,c) for p in low['allowedvariants']))]
 used=icons.intersection(codes)
 for icon in used:results[icon]={'provider':provider,'asset':name,'sha256':hashlib.sha256(raw).hexdigest(),'baseCode':base,'variantGroups':low.get('variantgroups',[]),'worldProperties':properties}
 for id,q in objectives['quests'].items():
  t=q['tasks'][0];target=t.get('item') or t.get('block')
  if not target:continue
  dom,pat=target.split(':',1)
  pat=pat[1:] if pat.startswith('@') else re.escape(pat).replace(r'\*','.*')
  found=[c for c in codes if c.startswith(dom+':') and re.fullmatch(pat,c.split(':',1)[1])]
  if found and id not in examples:examples[id]={'code':found[0],'asset':name,'sha256':hashlib.sha256(raw).hexdigest(),'kind':'block' if '/blocktypes/' in name else 'item'}
assert icons==set(results),('UNRESOLVED ICONS',icons-set(results))
assert set(examples)==set(objectives['quests'])-{'first-hunt'},('UNRESOLVED TASKS',set(objectives['quests'])-set(examples))
assert all(examples[id]['kind']==('block' if 'block' in q['tasks'][0] else 'item') for id,q in objectives['quests'].items() if id!='first-hunt')
receipt={'boundary':'Static variant expansion, not native game asset/handbook registration. Reproduce against hash-pinned export and official 1.22.7 SDK assets; JSON5 parser used for native asset syntax.','archiveSha256':ledger['sha256'],'icons':dict(sorted(results.items())),'taskExamples':dict(sorted(examples.items())),'guides':{n:json5.loads(b.read(n).decode())['pageCode'] for n in b.namelist() if '/config/handbook/' in n and n.endswith('.json')}}
output=root/'docs/evidence/butchering-assets.json'
if args.write:output.write_text(json.dumps(receipt,indent=2)+'\n')
else:assert json.loads(output.read_text())==receipt, 'Stale source evidence: inspect before regenerating with --write'
print('Verified',len(results),'icon codes and',len(examples),'automatic output task examples, native variant groups, both guide pageCodes and primary archive hash')
