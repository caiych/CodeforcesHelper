#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python
import urllib2,sys,re,os

prob = sys.argv[1]

#handle [dig][alphabet]

r = re.compile('^([0-9]+)([a-zA-Z])$')
res = re.findall(r,prob)
if res:
    prob = res[0][0] + '/' + res[0][1]

# get HTML

try:
    fd = urllib2.urlopen( 'http://codeforces.com/problemset/problem/'+prob )
except:
    print 'bad problem ID'
    sys.exit(0)

con = fd.read()
fd.close()

#get input & output

from HTMLParser import HTMLParser

inp = []
out = []
class IOGetter(HTMLParser):
    def handle_starttag(self,tag,attr):
        attrs = dict( attr )
        try:
            if tag == 'div' and attrs['class'] == 'input':
                self.status = 'input'
            if tag == 'div' and attrs['class'] == 'output':
                self.status = 'output'
            if tag == 'pre':
                self.pre = True
                self.content = ''
            if tag == 'br' and self.pre:
                self.content += '\n'
        except:
            pass
    def handle_endtag(self,tag):
        if tag == 'pre':
            self.pre = False
            if self.status == 'input':
                inp.append( self.content )
            elif self.status == 'output':
                out.append( self.content )
    def handle_data(self,data):
        try:
            if self.pre:
                self.content += data
        except:
            pass

parser = IOGetter()
parser.feed(con)

#create dirs
dir2do = os.path.curdir + '/' + prob[:-2] + prob[-1]
if not os.path.exists(dir2do):
    os.makedirs( dir2do )

#generate test script

testscript = """#! /usr/bin/python
"""+ 'inp = %s\nout= %s\n'%(str(inp),str(out)) + r"""

from itertools import izip
import os,sys
try:
    fname = sys.argv[1]
except:
    print 'input a filename'
    sys.exit(0)

if fname.endswith('.cc') or fname.endswith('.cpp'):
    print 'compiling %s'%fname
    os.popen('g++ %s -o .tmp'%fname)
    command = './.tmp'
elif fname.endswith('.py'):
    command = 'python %s'%fname
else:
    command = './%s'%fname

num = 0
for a,b in izip(inp,out):
    num += 1
    print 'Testcase #%d: '%num
    f = open('.in','w')
    f.write(a)
    f.close()
    o = os.popen(command+'< .in').read()
    if o == b:
        print 'Accepted\n'
    else:
        print 'Wrong\nInput:\n%s\nExpect:\n%s\nReturned:\n%s\n'%(a,b,o)
    os.remove('.in')
    
os.remove('.tmp')
"""

f = open(dir2do+'/test','w')
f.write( testscript )
f.close()

#make the script executable
try:
    os.popen( 'chmod a+x '+dir2do+'/test')
except:
    pass

