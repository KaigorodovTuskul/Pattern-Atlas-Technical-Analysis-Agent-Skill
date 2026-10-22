#!/usr/bin/env python3
"""Offline, safe installer for the portable Pattern Atlas skill (Python 3.9+)."""
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills' / 'pattern-atlas'
TARGETS = {
    'codex': '.agents/skills',
    'claude-code': '.claude/skills',
    'cursor': '.cursor/skills',
    'opencode': '.opencode/skills',
    'gemini': '.gemini/skills',
    'copilot': '.github/skills',
    'generic': '.agents/skills',
}


def install(project, agent='generic', force=False, dry_run=False):
    project = Path(project).resolve()
    if not project.is_dir():
        raise ValueError('Project directory does not exist')
    if agent not in TARGETS:
        raise ValueError('Unknown agent: ' + agent)
    if not (SOURCE/'SKILL.md').is_file():
        raise FileNotFoundError('Canonical skill not found')
    dest = project / TARGETS[agent] / SOURCE.name
    if dest.resolve() == SOURCE.resolve():
        raise ValueError('Refusing to install onto canonical skill')
    if dest.exists() or dest.is_symlink():
        if dest.is_symlink():
            raise ValueError('Refusing to overwrite a symlinked skill directory')
        if not force:
            raise FileExistsError('Already installed; pass --force to replace: ' + str(dest))
    if dry_run:
        print('DRY RUN: '+str(SOURCE)+' -> '+str(dest))
        return dest
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(SOURCE, dest,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    print('Installed: '+str(dest))
    return dest


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--project',type=Path,required=True)
    ap.add_argument('--agent',choices=sorted(TARGETS),default='generic')
    ap.add_argument('--force',action='store_true')
    ap.add_argument('--dry-run',action='store_true')
    args=ap.parse_args(argv)
    try: install(args.project,args.agent,args.force,args.dry_run)
    except (OSError,ValueError) as exc:ap.error(str(exc))
    return 0
if __name__=='__main__':sys.exit(main())
