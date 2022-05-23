import tarfile

from typing import Dict
from io import BytesIO


def extract(archive: BytesIO) -> dict:
    """Extract files and return file set stored in memory"""
    files = {}
    with tarfile.open(fileobj=archive) as tar: 
        print(tar.getmembers())        
        for member in tar.getmembers():
            if member.isfile():
                file = tar.extractfile(member)
                files[member.path] = BytesIO(file.read())

    return files


def compress(files: Dict[str, BytesIO]):
    """Compress files into an in memory tar file"""
    archive = BytesIO()
    with tarfile.open(fileobj=archive, mode='w:gz') as tar:
        for path, file_data in files.items():
            tarinfo = tarfile.TarInfo(name=path)
            tarinfo.size = file_data.tell()
            file_data.seek(0)

            tar.addfile(tarinfo, fileobj=file_data)

    archive.seek(0)
    return archive