from __future__ import annotations
from pathlib import Path
import hashlib
import urllib.request

PDEBENCH_FILES={
    "advection_beta1":{
        "filename":"1D_Advection_Sols_beta1.0.hdf5",
        "url":"https://darus.uni-stuttgart.de/api/access/datafile/255675",
        "md5":"1fe41923a4123db55bf4e89bea32e142"
    },
    "burgers_nu001":{
        "filename":"1D_Burgers_Sols_Nu0.01.hdf5",
        "url":"https://darus.uni-stuttgart.de/api/access/datafile/281363",
        "md5":"e6d9a4f62baf9a29121a816b919e2770"
    }
}

def md5_file(path,chunk=8<<20):
    h=hashlib.md5()
    with open(path,"rb") as f:
        while True:
            b=f.read(chunk)
            if not b: break
            h.update(b)
    return h.hexdigest()

def ensure_pdebench_file(task,directory):
    spec=PDEBENCH_FILES[task]
    directory=Path(directory); directory.mkdir(parents=True,exist_ok=True)
    path=directory/spec["filename"]
    if path.exists() and md5_file(path)==spec["md5"]:
        return path
    urllib.request.urlretrieve(spec["url"],path)
    got=md5_file(path)
    if got!=spec["md5"]:
        path.unlink(missing_ok=True)
        raise RuntimeError(f"MD5 mismatch for {task}: {got}")
    return path
