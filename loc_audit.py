#!/usr/bin/env python3
"""
DreamHome Studio — Line of Code (LOC) Auditing Tool
Scans source files across backend (Python, SQL), frontend (HTML, CSS, JS),
and automated tests, excluding blank lines and pure comment lines.
Provides breakdown reports by directory, file type, and total meaningful LOC.
"""

import os
import sys
from pathlib import Path

# Directories to ignore
IGNORE_DIRS = {
    '__pycache__', '.git', '.pytest_cache', 'venv', 'env', '.venv',
    'node_modules', '.idea', '.vscode', 'dist', 'build'
}

# File extensions to audit
EXTENSION_MAP = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.html': 'HTML',
    '.css': 'CSS',
    '.sql': 'SQL',
    '.md': 'Markdown'
}

def is_meaningful_line(line: str, ext: str) -> bool:
    """Determine if a line is a meaningful line of code (not blank, not pure comment)."""
    stripped = line.strip()
    if not stripped:
        return False
    
    # Python & Shell comments
    if ext in ['.py', '.sh'] and stripped.startswith('#'):
        return False
        
    # JavaScript & CSS comments
    if ext in ['.js', '.css']:
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
            return False
            
    # HTML comments
    if ext == '.html' and (stripped.startswith('<!--') or stripped.endswith('-->')):
        return False
        
    # SQL comments
    if ext == '.sql' and (stripped.startswith('--') or stripped.startswith('/*')):
        return False
        
    return True

def audit_directory(root_path: Path):
    """Recursively scan directory and calculate LOC per file and extension."""
    file_stats = []
    category_totals = {
        'Python': 0,
        'JavaScript': 0,
        'HTML': 0,
        'CSS': 0,
        'SQL': 0,
        'Markdown': 0
    }
    
    total_files = 0
    total_raw_lines = 0
    total_meaningful_lines = 0
    
    for current_root, dirs, files in os.walk(root_path):
        # Prune ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file_name in files:
            file_path = Path(current_root) / file_name
            ext = file_path.suffix.lower()
            
            if ext not in EXTENSION_MAP:
                continue
                
            lang = EXTENSION_MAP[ext]
            raw_lines = 0
            meaningful_lines = 0
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        raw_lines += 1
                        if is_meaningful_line(line, ext):
                            meaningful_lines += 1
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue
                
            total_files += 1
            total_raw_lines += raw_lines
            total_meaningful_lines += meaningful_lines
            category_totals[lang] += meaningful_lines
            
            # Record relative path for reporting
            rel_path = file_path.relative_to(root_path)
            file_stats.append({
                'path': str(rel_path),
                'lang': lang,
                'raw': raw_lines,
                'meaningful': meaningful_lines
            })
            
    return {
        'files': file_stats,
        'totals': category_totals,
        'total_files': total_files,
        'total_raw': total_raw_lines,
        'total_meaningful': total_meaningful_lines
    }

def print_audit_report(results: dict):
    """Print formatted audit report to stdout."""
    print("=" * 80)
    print("                DREAMHOME STUDIO — SOURCE CODE LOC AUDIT               ")
    print("=" * 80)
    print(f"{'Category / Language':<25} | {'Meaningful LOC':<18} | {'% of Total':<12}")
    print("-" * 80)
    
    total_meaningful = results['total_meaningful']
    for lang, count in sorted(results['totals'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_meaningful * 100) if total_meaningful > 0 else 0
        print(f"{lang:<25} | {count:<18,d} | {percentage:<11.2f}%")
        
    print("-" * 80)
    print(f"{'TOTAL MEANINGFUL LOC':<25} | {total_meaningful:<18,d} | 100.00%")
    print(f"{'TOTAL RAW LINES':<25} | {results['total_raw']:<18,d} |")
    print(f"{'TOTAL FILES AUDITED':<25} | {results['total_files']:<18,d} |")
    print("=" * 80)
    
    # Check 50K LOC requirement
    target = 50000
    if total_meaningful >= target:
        print(f"[OK] SUCCESS: Project meets and exceeds the {target:,} meaningful LOC requirement!")
    else:
        remaining = target - total_meaningful
        print(f"[INFO] ATTENTION: Project currently has {total_meaningful:,} meaningful LOC ({remaining:,} short of target {target:,}).")
    print("=" * 80)

if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent
    results = audit_directory(root_dir)
    print_audit_report(results)
