import tarfile
import os
import json

from time import perf_counter

start = perf_counter()

# Create archive
with tarfile.open("archive.tar.gz", "w:gz") as tar:
    tar.add("files", arcname=os.path.basename("files"))

print("Archive created")
end = perf_counter()
print("Time taken", f"{(end - start) * 1000:.2f} ms")
print("=================================================")


files = {}

with open("archive.tar.gz", "rb") as fd:
    tar = tarfile.open(fileobj=fd)
    for member in tar.getmembers():
        if member.isfile():
            arc_fd = tar.extractfile(member)
            files[member.path] = json.load(arc_fd)
                # print(type(files[member.path]))

end = perf_counter()
print("Archive read")
print("Time taken", f"{(end - start) * 1000:.2f} ms")


# modify files
for k, v in files.items():
    v[0] = {"modified data": 123}
print("=================================================")

with tarfile.open("archive2.tar.gz", "w:gz") as tar:
    for k, v in files.items():
        import io
        file_data = json.dumps(v).encode()
        bio = io.BytesIO(file_data)
        tarinfo = tarfile.TarInfo(name=k)
        tarinfo.size = len(file_data)
        tar.addfile(tarinfo, fileobj=bio)

print("Modified data and created new archive")
end = perf_counter()
print("Time taken", f"{(end - start) * 1000:.2f} ms")

print("=================================================")
with open("archive2.tar.gz", "rb") as fd:
    with tarfile.open(fileobj=fd) as tar:
        for member in tar.getmembers():
            if member.isfile():
                arc_fd = tar.extractfile(member)
                # Print modified data in each file
                print(json.load(arc_fd)[0])

end = perf_counter()
print("Time taken", f"{(end - start) * 1000:.2f} ms")

