#!/usr/bin/env python3
"""Offline validator for Pattern Atlas repository, Markdown, JSON and 300+ SVGs."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/pattern-atlas'

def validate():
    errors=[]
    mandatory=['README.md','LICENSE','AGENTS.md','docs/SOURCE_AUDIT.md','gallery.html',
               'skills/pattern-atlas/SKILL.md','skills/pattern-atlas/data/catalog.json',
               'skills/pattern-atlas/data/index_names.txt','skills/pattern-atlas/data/families.json',
               'skills/pattern-atlas/references/INDEX.md','skills/pattern-atlas/references/DETECTION.md',
               'skills/pattern-atlas/scripts/search_catalog.py','skills/pattern-atlas/scripts/scan_ohlcv.py']
    for file in mandatory:
        if not (ROOT/file).is_file():errors.append('Missing: '+file)
    if errors:return errors
    skill=(SKILL/'SKILL.md').read_text(encoding='utf-8')
    match=re.match(r'\A---\s*\n(.*?)\n---\s*\n',skill,re.S)
    if not match:
        errors.append('SKILL.md missing YAML frontmatter')
    else:
        m=match.group(1)
        if not re.search(r'(?m)^name:\s*pattern-atlas\s*$',m):errors.append('Invalid skill name')
        desc=re.search(r'(?m)^description:\s*(.+)$',m)
        if not desc or not 1<=len(desc.group(1))<=1024:errors.append('Invalid skill description')
    if len(skill.splitlines())>500:errors.append('SKILL.md >500 lines')
    try:
        c=json.loads((SKILL/'data/catalog.json').read_text(encoding='utf-8'))
        fam=json.loads((SKILL/'data/families.json').read_text(encoding='utf-8'))
        records=c['records'];ids=[r['id'] for r in records]
        if len(ids)!=len(set(ids)):errors.append('Duplicate record ID')
        if len(records)!=383:errors.append(f'Unexpected record count: {len(records)}')
        if len(fam)!=38:errors.append('Unexpected family count')
        index_rows=[ln for ln in (SKILL/'data/index_names.txt').read_text(encoding='utf-8').splitlines() if ln and not re.fullmatch(r'\[[^\]]+\]',ln)]
        if len(index_rows)!=c['counts']['index_rows']:errors.append('Index row count mismatch')
        for r in records:
            tag=r.get('id','?')
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',tag):errors.append(f'Unsafe slug: {tag}')
            if r['family'] not in fam:errors.append(f'Unknown family: {tag}')
            if r['category'] not in ['pattern','event','method','study']:errors.append(f'Bad category: {tag}')
            if not r.get('name') or not r.get('description_ru') or not r.get('identification_ru') or not r.get('confirmation_ru'):
                errors.append(f'Missing essential text: {tag}')
            if r.get('source_index_url')!='https://www.thepatternsite.com/chartpatterns.html':errors.append(f'Source index mismatch: {tag}')
            if r['confidence']=='reference_verified' and not r['verified_detail_url']:errors.append(f'Missing verified url: {tag}')
            elif r['verified_detail_url'] and not r['verified_detail_url'].startswith('https://www.thepatternsite.com/'):errors.append(f'External untrusted direct URL: {tag}')
            if r.get('example') and not (SKILL/r['example']).is_file():errors.append(f'Missing SVG: {tag}')
            if r['category']=='pattern' and not r.get('example'):errors.append(f'Unillustrated pattern: {tag}')
            if not (SKILL/'patterns'/f'{tag}.md').is_file():errors.append(f'Missing entry Markdown: {tag}')
        counts=c['counts']
        if counts['unique_normalized_entries']!=len(records):errors.append('Catalog count mismatch')
        if counts['with_illustration']!=sum(bool(r.get('example')) for r in records):errors.append('Illustration count mismatch')
        if counts['with_verified_detail_url']!=sum(bool(r.get('verified_detail_url')) for r in records):errors.append('URL count mismatch')
        svg=set(SKILL.glob('assets/charts/*.svg'))
        if len(svg)!=counts['with_illustration']:errors.append(f'SVG count mismatch {len(svg)}')
        if len(list((SKILL/'patterns').glob('*.md')))!=len(records):errors.append('Unexpected article count')
        for p in svg:
            try:
                root=ET.parse(p).getroot()
                if not root.tag.endswith('svg'):errors.append(f'Not SVG: {p.name}')
                if list(root.iter()) and any(str(x.tag).lower().endswith('script') for x in root.iter()):errors.append(f'Script in SVG: {p.name}')
            except ET.ParseError as err:errors.append(f'Invalid SVG {p.name}: {err}')
        example_svg=ROOT/'docs/assets/pattern-atlas-mark.svg';ET.parse(example_svg)
        gallery=(ROOT/'gallery.html').read_text(encoding='utf-8')
        if len(re.findall(r'"confidence":',gallery))<350:errors.append('Offline gallery data incomplete')
        if 'https://cdn.' in gallery or 'fetch(' in gallery:errors.append('Gallery may depend on third-party network')
    except (OSError,ValueError,KeyError,TypeError,ET.ParseError) as exc:errors.append(f'Invalid structured data: {exc}')
    # Check every local Markdown link, including each of 383 articles. Ignore fragment anchors.
    for p in ROOT.rglob('*.md'):
        for raw in re.findall(r'\]\(([^\)]+)\)',p.read_text(encoding='utf-8')):
            if raw.startswith(('https://','http://','mailto:','#')):continue
            target=(p.parent/raw.split('#',1)[0].split('?',1)[0]).resolve()
            if not target.is_relative_to(ROOT.resolve()) or not target.exists():
                errors.append(f'Broken Markdown link in {p.relative_to(ROOT)}: {raw}')
    return errors

if __name__=='__main__':
    errors=validate()
    if errors:
        print('\n'.join('FAIL: '+x for x in errors[:80]),file=sys.stderr)
        print(f'FAIL: {len(errors)} total errors',file=sys.stderr)
        sys.exit(1)
    print('PASS: skill schema, 383 descriptions, 334 original SVG, 38 families, source provenance, docs links, gallery')
