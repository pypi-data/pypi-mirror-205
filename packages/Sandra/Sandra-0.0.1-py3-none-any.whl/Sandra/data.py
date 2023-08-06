import os
print(os.listdir() )
files = dict()
with open('./txt/taylor_swift_1KB.txt', 'rb') as f:
    files[1] = f.read()
with open('./txt/taylor_swift_5KB.txt', 'rb') as f:
    files[5] = f.read()
with open('./txt/taylor_swift_10KB.txt', 'rb') as f:
    files[10] = f.read()
with open('./txt/taylor_swift_100KB.txt', 'rb') as f:
    files[100] = f.read()
def dataloader(size):
    print(os.getcwd())
    if size not in [1,5,10,100] :
        raise ValueError("Size must be either 1, 5, 10, 100")
    return files[size]