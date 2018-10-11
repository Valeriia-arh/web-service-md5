import requests, shutil
import hashlib
import celery

def md5sum(file):
    if file is False:
	raise Exception('File doesnt exist')
    m = hashlib.md5()
    with open(file, 'rb') as f:
    	b = f.read()
    	m.update(b)
    return m.hexdigest()
 

def download_file(path):
    filereq = requests.get(path,stream = True)
    file="/home/valeriia/sample/test.txt"
    with open(file, "wb") as receive:
        shutil.copyfileobj(filereq.raw,receive)
    del filereq

test_file = "http://data.enteromics.com/robots.txt"
    
output = ''
rootpath = '/home/valeriia/sample/'
  
for dirname, dirnames, filenames in os.walk(rootpath):
    for filename in filenames:
        fname = os.path.join(dirname, filename).replace('\\', '/')
        md5sum = getMD5sum(fname)
        output+='{0}:{1}\n'.format(fname.replace(rootpath, ''), md5sum)

        
f = open('/home/valeriia/sample/checksums.csv', 'w')
f.write(output)
f.close()
