#!/usr/bin/env python3
import hashlib,json,os
from pathlib import Path
IGNORED_NAMES={".git",".cogentnexus-openclaw","__pycache__",".pytest_cache"}
def _file_hash(path):
 d=hashlib.sha256()
 with path.open("rb") as h:
  for chunk in iter(lambda:h.read(1048576),b""): d.update(chunk)
 return d.hexdigest()
def fingerprint(path):
 path=Path(path).resolve()
 if not path.exists(): return {"kind":"missing","target":str(path),"digest":None,"fileCount":0,"totalBytes":0}
 if path.is_file(): return {"kind":"file","target":str(path),"digest":_file_hash(path),"fileCount":1,"totalBytes":path.stat().st_size}
 if not path.is_dir(): raise ValueError(f"unsupported artifact type: {path}")
 entries=[]; total=0
 for item in sorted(path.rglob("*"),key=lambda p:p.relative_to(path).as_posix()):
  relative=item.relative_to(path)
  if any(part in IGNORED_NAMES for part in relative.parts): continue
  name=relative.as_posix()
  if item.is_symlink(): entries.append({"path":name,"kind":"symlink","target":os.readlink(item)})
  elif item.is_file():
   size=item.stat().st_size; total+=size
   entries.append({"path":name,"kind":"file","size":size,"sha256":_file_hash(item)})
 encoded=json.dumps(entries,sort_keys=True,separators=(",",":")).encode()
 return {"kind":"directory","target":str(path),"digest":hashlib.sha256(encoded).hexdigest(),"fileCount":sum(x["kind"]=="file" for x in entries),"totalBytes":total}
def matches(expected):
 current=fingerprint(expected["target"])
 return current.get("kind")==expected.get("kind") and current.get("digest")==expected.get("digest")
