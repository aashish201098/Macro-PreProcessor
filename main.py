import string
src= open("src.txt","r")
output= open("op.txt","w")

count= -1
expanding=False
lines=[]
namtab=[]
argtab=[]
proto=[]
data= list(src.readlines())
for line in data:
	if(line=='\n' or line=='\n\t' or line=='\t\n'):
		pass
	else:
		lines.append(line)
	
def getline():	
	global count
	count+=1
	return lines[count]
	
def define(line):
	deftab= open("deftab.txt","a")
	l= line.split()
	print(l)
	p= l[2].split(',')
	print(p)
	global argtab
	argtab+= p;
	namtab.append(l[1])
	deftab.write(line)
	level=1
	while level>0:
		line= getline()
		if line.strip().startswith("!!"):
			continue
		for w in p:
			if w in line:
				line = str.replace(line,w,"?"+str(p.index(w)))
		print(line)
		deftab.write(line)
		if line.startswith("MSTART"):
			level=level+1
		elif line.strip()=="MEND":
			level= level-1
	deftab.close()
			
def expand(line):
	deftab= open("deftab.txt","r")
	global expanding
	expanding=True
	l= line.split()
	e= list(deftab.readlines())
	i=0
	for i in range(0,len(e)):
		if l[0] in e[i]:
			break;
	proto= e[i].strip()
	pro= proto.split()
	index= namtab.index(pro[1])
	p= line.split()
	p= p[1].split(',')
	while True:
		i=i+1
		line= e[i]
		if line.strip()=="MEND":
			break
		for j in range(0,len(p)):
			st= "?"+str(j)
			if st in line:
				line= str.replace(line,st,p[j])
		output.write(line)
	deftab.close()
	
def processline(line):
	flag=0
	l= line.split()
	for i in range(0,len(namtab)):
		if l[0]==namtab[i]:
			flag=1
			break;
			
	if flag==1:
		expand(line)
	elif l[0]=="MBEGIN":
		print("yess")
		define(line)
	else:
		output.write(line)
		

while count<len(lines)-1:
	line=getline()
	print(line)
	processline(line)
	

