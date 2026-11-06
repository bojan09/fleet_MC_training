"""Validate visual coverage, local files, and SVG syntax using only Python stdlib."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/content.json').read_text())
manifest=json.loads((root/'assets/manifest.json').read_text())
known={a['file'] for a in manifest}
assert len(known)==len(manifest),'Duplicate asset manifest entries'
assert len(data['lessons'])==18
count=0
for lesson in data['lessons']:
 assert len(lesson['notes'])==len(lesson['visualNotes']),lesson['id']
 assert lesson['referenceImage'] in known
 assert lesson['overviewImage'] in known
 assert lesson['overviewAlt']
 assert lesson['referenceAlt']
 for note in lesson['visualNotes']:
  assert note['title'] and note['text'] and note['alt']
  assert note['image'] in known
  count+=1
assert count==117
for term in data['glossary']:
 assert term['image'] in known and term['alt']
for asset in manifest:
 path=root/asset['file']
 assert path.is_file(),str(path)
 if path.suffix=='.svg':ET.parse(path)
print(f'Validated {len(data["lessons"])} lessons, {count} illustrated notes, {len(data["glossary"])} illustrated terms, and {len(manifest)} asset records.')
