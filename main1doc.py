import string
src= open("src1.txt","r")
output= open("op1.txt","w")
deftab= open("deftab1.txt","r+")
count= -1
expanding=False
lines=[]
namtab=[]
argtab=[]
proto=[]
e=[]
d=[]  
data= list(src.readlines())

# removing the blank lines
for line in data:
	if(line=='\n' or line=='\n\t' or line=='\t\n'):
		pass
	else:
		lines.append(line)

# getline function will return next line either from deftab or from the src file depending on the value of expanding boolean variable
def getline():
	if expanding:
		global i
		i+=1
		for j in range(0,len(p)):
			st= "?"+str(j)
			if st in e[i]:
				if p[j]!='':
					# substituting the values specified in invocation stmt
					e[i]= str.replace(e[i],st,p[j])
				else:
					# substituting the default values when not given
					e[i]= str.replace(e[i],st,d1[j])
				
		return e[i]
	else:
		global count
		count+=1
		return lines[count]

# define function will add the definition of macro into the deftab
def define(line):
	#deftab= open("deftab1.txt","a")
	l= line.split()
	# if macro definition already exists then do nothing
	for j in range(0,len(namtab)):
		if l[1]==namtab[j]:
			return
	if len(l)>2:
		p= l[2].split(',')
	else:
		p=[]
	global d1
	d1=[]
	# getting the default values
	for i in range(0,len(p)):
		p1= p[i].split('=')
		if len(p1)>1:
			d1.append(p1[1])
			p[i]=p1[0]
		else:
			d1.append('')
	global d
	d.append(d1)		
	global argtab
	argtab.append(p);
	namtab.append(l[1])
	deftab.write(line)
	level=1
	while level>0:
		line= getline()
		# removing the comments
		if line.strip().startswith("!!"):
			continue
		if expanding and line.strip()!="MEND" and "MBEGIN" not in line:
			output.write(line)
		# replacing the parameters in amcro body with their positions
		for w in p:
			if w in line:
				line = str.replace(line,w,"?"+str(p.index(w)))
		deftab.write(line)
		if line.strip().startswith("MBEGIN"):
			level=level+1
		elif line.strip()=="MEND":
			level= level-1

# expand function will expand the macro invocation stmt
# also it will define in case of nested macro definition
def expand(line):
	global expanding
	expanding=True
	l= line.split()
	global e
	deftab.seek(0)
	e= list(deftab.readlines())
	global i
	i=0
	for i in range(0,len(e)):
		if l[0] in e[i]:
			break;
	proto= e[i].strip()
	pro= proto.split()
	index= namtab.index(pro[1])
	global p
	p= line.split()
	if len(p)>1:
		p= p[1].split(',')
	else:
		p=[]
	if len(pro)>2:
		pro= pro[2].split(',')
	else:
		pro=[]
	global d1
	d1=[]
	for k in range(0,len(pro)):
		t= pro[k].split('=')
		if len(t)>1:
			d1.append(t[1])
		else:
			d1.append('')
	while True:	
		line=getline()
		if line.strip()=="MEND":
			break
		processline(line)
	expanding=False

# procesline function will call the necessary function depending on the requirement
def processline(line):
	flag=0
	l= line.split()
	if len(l)==0:
		return
	for i in range(0,len(namtab)):
		if l[0]==namtab[i]:
			flag=1
			break;
			
	if flag==1:
		#print((deftab.read()))
		#expand the macro call stmt
		expand(line)
	elif l[0]=="MBEGIN":
		# define the new macro
		define(line)
	else:
		output.write(line)
		

while count<len(lines)-1:
	line=getline()
	processline(line)
	
	
#deftab.truncate(0)	
src.close()
output.close()

