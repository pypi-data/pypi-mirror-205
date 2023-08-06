A capture moudle return base64image

# Install

pip install Vulncapture

# Use

```
from Vulncapture import Vulncapture
import base64
image=Vulncapture.run_snapshot(url='http://www.baidu.com',keyword='换一换')
print(image) # str
imgdata=base64.b64decode(image)
file=open('1.jpg','wb')
file.write(imgdata)
file.close()
```
run_snapshot()
'''
url : aim url
keyword : str
cookie = ''
'''
if your aim url need to login , please set cookie

```
from Vulncapture import Vulncapture
import base64
imgdata2= Vulncapture.txt2image('123','1',False)
print(imgdata2)
imgdata=base64.b64decode(imgdata2)
file=open('2.jpg','wb')
file.write(imgdata)
file.close()
```

