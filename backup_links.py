import os, re, subprocess

ROOT = "backup/downloads"
AGENT = "Mozilla/5.0 (compatible; LinkBackup/1.0)"

def get_safe_name(s):
    return re.sub(r'[\\*?:"<>|/]', '', s).strip() or 'untitled'

for root, _, files in os.walk('.'):
    if 'backup' in root.split(os.sep) or 'videos' in root: continue
    
    for file in files:
        if not file.endswith('.md') or 'videos' in file: continue
        
        src = os.path.join(root, file)
        rel = os.path.relpath(root, '.')
        dst_base = os.path.join(ROOT, rel, file[:-3])
        
        try:
            txt = open(src).read()
        except Exception as e:
            print(f"[!] Error reading {src}: {e}")
            continue

        seen = {}
        for name, url in re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)', txt):
            safe = get_safe_name(name)
            seen[safe] = count = seen.get(safe, 0) + 1
            if count > 1: safe += f"_{count}"
            
            target = os.path.join(dst_base, safe)
            if not os.path.exists(target): os.makedirs(target)
            
            print(f"[*] Downloading {name} -> {target}")
            cmd = ['wget', '-E', '-N', '-nv', '-p', '-k', '-H', '-np', 
                   '-T', '10', '-t', '1', '-U', AGENT, '-P', target, url]
            subprocess.run(cmd)

