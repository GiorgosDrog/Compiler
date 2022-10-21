#Drongoulas Georgios 4358 cse84358
#Plachouras Diamadis 4476 cse4476
#!/usr/bin/python
import sys 

filename = sys.argv[1] #to onoma toy arxeiou pou 8elw na kanw compile 
charlist = [] #lista me ka8e xaraktira ksexwrista 
linelist = [] #lista me ka8e gramh tou arxeioy ksexwrista  
newstate="start" 
elements=[] #bazw oti diabasa mexri na teleiwsei h lektikh mou monada 
keywords=["program","declare","if","else","while","switchcase","forcase","incase","case","default","not","and","or","function","procedure","call","return","inout","input","print"]

parentheseis=["(",")","{","}","[","]"]

delimeter=[".",",",";"]

add_operator=["+","-"]

mult_operator=["*","/"]

comment ="#"

tokens=[]

lines = 1

colum = 1

maxlength = 0 

class token:

    def __init__(self,recognized_string, family, line_number):
        
        self.recognized_string=recognized_string
        self.family = family
        self.line_number = line_number

    def __str__(self):
        return self.recognized_string +" is "+self.family+" the token is at line:"+ str(self.line_number)

##################################################

def numState(n):
    switcher={0:"start",1:"dig",2:"idk",3:"error",4:"rem",5:"addOperator",6:"mulOperator",7:"groupSymbol",8:"delimiter",9:"assignment",10:"relOperator",11:"real",12:"undefined"}
    return switcher.get(n)


                                                       
#fortwnei toys characters tou arxeiou  
def loadFile():
    data = open(filename ,"r")
    for line in data:
        for char in line:
            charlist.append(char)
    charlist.append("") #gia na mhn gemizei h lista mou
            
def check_keywords(keys):#an brw keyword ftiaxe token kai epestrepse 1 gia na to katalavw 
    if keys in keywords:
        return 1
    else:
        return 0  


def check_symbols(symbols):
    if symbols in parentheseis:
        return "parenthesh"
    elif symbols in delimeter:
        return "delimetersymbols" 
    elif symbols in add_operator:
        return "add"        
    elif symbols in mult_operator:
        return "mult"
    else:
        pass

def isEof(i):
    if i+1 == maxlength :
        return True
    return False


def check_line():
    return lines
      

def CommentState(newstate):
    if newstate == numState(4):
        return True
    else: 
        return False

def lexAnalyzer():
    global newstate
    global elements
    global lines
     #wedwed 22#
    loadFile()
    maxlength = len(charlist)

    ###########
    i=0
    while i < maxlength:

        if charlist[i].isspace() == True:
            if  charlist[i] == '\n':
                lines +=1   

        elif((isEof(i)==False and charlist[i] == "#") or newstate == numState(4)): #single line comments #
            newstate = numState(4)
            i += 1
            if(isEof(i) == True):
                print("Reached eof while comment is open")
                exit()
            while (isEof(i) == False and charlist[i] != "#"):
                i += 1
            if(isEof(i) == True):
                print("Error comment not closed and reach eof")
                exit()
            newstate = numState(12)


        elif(( charlist[i].isdigit() == True or newstate == numState(11))and CommentState(newstate) == False):
            if (not newstate == numState(11)):
                newstate = numState(1)   #dig
                elements.append(charlist[i]) #bazw tous ari8mous poy diabazw se mia lista 
            if  isEof(i) == True  or charlist[i+1].isdigit() == False and not charlist[i+1] == '.':
                recognized_num="".join(elements) 
                num = token(recognized_num, newstate, check_line())
                tokens.append(num)
                #print(num)
                elements=[]
                newstate = numState(0)
            elif isEof(i)==True or charlist[i+1].isdigit() == False:
                newstate = numState(11) #bale state gia floats
                #elements.append(charlist[i])
                #float = token den exw ftiaksei ta token gia ta floats
                #ftiaxe sunarthsh opou me kathe klhsh tha tsekarei ton elements gia keywords dld: check_keywords(){ if elements == "if" tote kane token keyword if
                #kai state = start
                #return 1 gia na mhn kanw kati allo parakatw kai na kanw to loop, else return -1klp}
        
        elif ((charlist[i].isalpha() == True or newstate == numState(2)) and CommentState(newstate) == False):
            newstate = numState(2) #gramma
            elements.append(charlist[i])

            while(charlist[i+1].isdigit() == True):
                elements.append(charlist[i+1])
                i+=1

            keywordOrID ="".join(elements)
            if check_keywords(keywordOrID) == 1:
                keyword = token(keywordOrID,"keyword",check_line())
                tokens.append(keyword)
                #print(keyword)
                newstate=numState(0) #state = start kai sunexizw to input #exw kanei token prepei na to xeiristw
                elements=[] 
            #analysh gia id

            elif isEof(i) == True or charlist[i+1].isalpha() == False:  
                identifier = "".join(elements)
                ident = token(identifier,newstate,check_line())
                tokens.append(ident)
                #print(ident)
                newstate=numState(0)
                elements=[] 

        #gia na breiskei ekxwriseis
        elif charlist[i] == ":" and CommentState(newstate) == False:
            elements.append(charlist[i])
            if isEof(i) == True:
                print("Error expected := not :")
                newstate = numState(3)
                quit()

            if(charlist[i+1] == "="):
                newstate = numState(9)
                elements.append(charlist[i+1])
                assignmentStr = "".join(elements)
                assing = token (assignmentStr,newstate,check_line())
                tokens.append(assing)
                #print(assing)
                i+=1
            elements=[] #apo ti stigmh poy brika to := 8a sbhsw thn lista moy 

        #gia na briskei opetators
        elif charlist[i] == "<" and CommentState(newstate) == False:
            newstate = numState(10)
            elements.append(charlist[i])
            
            if isEof(i) == True:
                relop = token (elements[0],newstate,check_line())

            elif (charlist[i+1] == ">" or charlist[i+1] == "="):
                elements.append(charlist[i+1])
                i+=1
                relOperatorStr = "".join(elements)
                relopS = token (relOperatorStr,newstate,check_line())
                
            relOperatorStr = "".join(elements)
            relopS= token (relOperatorStr,newstate,check_line())
            tokens.append(relopS)
            #print(relopS)
            elements=[]

        elif charlist[i] == ">" and CommentState(newstate) == False:
            newstate = numState(10)
            elements.append(charlist[i])
            
            if isEof(i) == True:
                relop = token (elements[0],newstate,check_line())

            elif (charlist[i+1] == "="):
                elements.append(charlist[i+1])
                i+=1
                relOperatorStr = "".join(elements)
                relop = token (relOperatorStr,newstate,check_line())
           
            relOperatorStr = "".join(elements)
            relop = token (relOperatorStr,newstate,check_line())
            tokens.append(relop)
            #print(relop)
            elements=[]

        elif isEof(i)==False and charlist[i] =="=" and CommentState(newstate) == False:
            newstate = numState(10)
            relop = token(charlist[i],newstate,check_line())
            #print(relop)
            tokens.append(relop)

        elif check_symbols(charlist[i]) == "parenthesh" and CommentState(newstate) == False:
            newstate = numState(7)
            groupSymb = token(charlist[i],newstate,check_line())
            #print(groupSymb)
            tokens.append(groupSymb)
       
        elif check_symbols(charlist[i]) == "delimetersymbols" and CommentState(newstate) == False:
            newstate = numState(8)
            delimeterT = token(charlist[i],newstate,check_line())
            #print(delimeterT)
            tokens.append(delimeterT)

        elif check_symbols(charlist[i]) == "add" and CommentState(newstate) == False:
            newstate = numState(5)
            add = token(charlist[i],newstate,check_line())
            #print(add)
            tokens.append(add)
        
        elif check_symbols(charlist[i]) == "mult" and CommentState(newstate) == False: 
            newstate = numState(6)
            mult = token(charlist[i],newstate,check_line())
            #print(mult) 
            tokens.append(mult)
        else:
            #print("running")
            newstate = numState(12) #undefined character
            eof = token("",newstate,check_line())
            #print(eof)
            tokens.append(eof)
            pass
        #bhma
        i+=1

###################################################
#################quadHelper.py########################

#Dronggulas Giwrgos 4358
#Diamantis plachouras  4476
exitList= [] 
QuadList = [] #oles oi tetrades 
label = 1	  
tempNum = 0
#############################
class Quad:
	
	def __init__(self,operator,operand1,operand2,operand3):
		global label 
		self.operator = operator  #einai o telesths  
		self.operand1 = operand1  #einai oi teloumenoi
		self.operand2 = operand2
		self.operand3 = operand3
		self.label = label 

	def write(self):
		string = str(self.label) +": ,"+ self.operator +"," + self.operand1 +"," + self.operand2 + ","+ self.operand3 + "\n"
		return string
		
	def __str__(self): 				#100 : begin_block , _ , _ , _ 
		return str(self.label) +": ,"+ self.operator +"," + self.operand1 +"," + self.operand2 + ","+ self.operand3
#############################

class rule:

	def __init__(self , trueList , falseList):
		self.trueList = trueList
		self.falseList = falseList

#############################

def genQuad(operator,operand1,operand2,operand3):
	global label  
	newQuad = Quad(operator,operand1,operand2,operand3)
	QuadList.append(newQuad)
	label = label + 1
	return newQuad

def emptyList():
	global exitList
	return exitList

def newTemp(): # 8a epistrefei to onoma tis epomenhs temporary metabliths 
	global tempNum 
	temp = "T_"+str(tempNum)
	tempNum += 1  
	return temp

def nextQuad(): #epistrefei thn etiketa ths epomenhs tetradas 
	global label 
	x = label 
	return x   # prepei na gurnaei etiketa 

def makeList(label): #exei mesa monadiko stoixeio thn etiketa tou label
	tmpList = []
	tmpList.append(label)

	return tmpList 

def mergeList(list1 ,list2):
	tmpList =[]
	tmpList = list2+list1
	tmpList.reverse()
	return tmpList

def backpatch(list,blabel):
	global QuadList
	i=0
	j=0 
													#[3]
	if (len(list) == 0 ):
		print("den exei stoixeia h lista ")			 #[q1][a2][a3][a4][a5]
		exit()

	while(i < len(list) ): # des tis etiketes twn tetradwn 
		while( j < len (QuadList)): #bres tis tetrades 
			if(list[i] == QuadList[j].label): # an oi etiketes poy exei h lista yparxoun sth lista twn tetradwn
				QuadList[j].operand3 = str(blabel) # tote syblirwse to teleutaio stixeio twn tetradwn (gia ta jumps)
				break 
			j=j+1
		i=i+1

	#list.clear() #meta thn backpacth apodesmevw th lista 

def printAllquads():
	global QuadList
	i=0
	f = open("test.int","w")
	for x in range(0,len(QuadList)):
		#print(QuadList[x])
		f.write(QuadList[x].write())

	f.close()

######################################################
#####################table.py#########################

#Dronggulas Giwrgos 4358
#Diamantis plachouras  4476

import sys 


table = [] #the table
scopeNum = -1 #scopelevel

##############
class scope():
    def __init__(self):
        self.entitylist = []

##############
class Entity():

    def __init__(self,name):
        global scopeNum
        self.name = name

############        
class SymbolicConstant(Entity): #den to xrhsimopoiw 
    datatype = "integer"

    def __init__(self,name,value):
        Entity.__init__(self,name)
        self.value = value

#############
class Variable(Entity): #child of entity 

    def __init__(self,name,datatype,offset,scopeLevel):
        Entity.__init__(self, name)
        self.datatype =datatype
        self.offset = offset
        self.scopeLevel = scopeLevel
        
        if (self.scopeLevel == 0): # the variable is global 
            self.isglobal = True 
        else:
            self.isglobal = False

    def __str__(self):
        return self.name +" is the Variable with offset " + str(self.offset) + " the scope level is " + str(self.scopeLevel)
############
class FormalParameter(Entity):

    def __init__(self,name,datatype,offset,mode,scopeLevel):
        Entity.__init__(self,name)
        self.datatype = datatype
        self.offset = offset
        self.mode = mode
        self.scopeLevel = scopeLevel
        self.isglobal = False
        
    def __str__(self):
        return self.name +"/"+ self.mode +"/"+ str(self.offset)+ " the scope level is " + str(self.scopeLevel)

############
class parameter(Variable,FormalParameter):

    def __init__(self,name,datatype,offset,mode,scopeLevel):
        Variable.__init__(self,name,datatype,offset,scopeLevel)
        FormalParameter.__init__(self,name,datatype,offset,mode,scopeLevel)

    def __str__(self):
        return self.name +"/"+ self.mode +"/"+ str(self.offset)+ " the scope level is " + str(self.scopeLevel)
############
class Procedure(Entity):

    def __init__(self,name,startingQuad,framelength,formalParameter,offset,scopeLevel):
        Entity.__init__(self,name)
        self.startingQuad = startingQuad
        self.framelength = framelength
        self.formalParameter = formalParameter
        self.offset=offset
        self.scopeLevel = scopeLevel

    def set_startingQuad(self , x ):
        self.startingQuad = x 

    def set_framelength(self , x ):
        self.framelength = x 

    def set_formalParameter(self , x ):
        self.formalParameter = x 

    def getNumOfParameters(self):
        return len(self.formalParameter)

    def __str__(self):
        return self.name +" "+str(self.startingQuad)+ " " + str(self.framelength) +" "+ str(self.offset)

############
class function(Procedure):

    def __init__(self,name,startingQuad,framelength,formalParameter,datatype,offset,scopeLevel):
        Procedure.__init__(self,name,startingQuad,framelength,formalParameter,offset,scopeLevel)
        self.datatype = datatype

    def getNumOfParameters(self):
        return len(self.formalParameter)

    def __str__(self):
        return self.name +" "+str(self.startingQuad)+ " " + str(self.framelength) +" "+ str(self.offset) 
############
class TemporaryVariable(Variable):
    
    def __init__(self,name,datatype,offset,scopeLevel):
        Variable.__init__(self,name,datatype,offset,scopeLevel)

    def __str__(self):
        return self.name +" is the TemporaryVariable with offset " + str(self.offset) + " the scope level is " + str(self.scopeLevel)
############
# help functions 

def addEntity(entityObj): #pros8ikh eggrafhs 8a balw mesa se ka8e scope ta entities  
    global table
    global scopeNum

    table[scopeNum].entitylist.append(entityObj)
    #print(entityObj.__class__.__name__)
    #print("appending to scopeNum " + str(scopeNum))
    print(entityObj)
    #print(entityObj.getScope())

def addScope(): #mesa ston table tha balw ta scopes 
    global scopeNum 
    global table 

    scopeNum += 1
    scopeObj = scope()
    table.append(scopeObj)
    print("added scope!" + " " +str(scopeNum))

def deleteScope():
    global table 
    global scopeNum

    scopeNum -= 1

    if(len(table) == 0 ):
        print("dont have scope to delete it ")
        exit()
    #print(scopeNum)
    table.pop()

def getScopeNum():
    global scopeNum
    return scopeNum

def printScope(scope):
    global table

    for i in range(len(table[scope].entitylist)):
        print(table[scope].entitylist[i].name)#boh8itikh 

def printTable():# na kanw 
    global table 
    i = 0
    j = 0
    while (i < len(table)):
        while(j < len(table[i].entitylist)):
            print(table[i].entitylist[j].name +" "+ str(table[i].entitylist[j].offset))
            j=j+1
        i=i+1

def UpdateFields(Obj,framelength,startingQuad,formalParameter):

    Obj.set_framelength(framelength) #ebala to length tou 
    Obj.set_startingQuad(startingQuad) #enhmwrwsa me to arxiko lebel tou endoiamesou 
    Obj.set_formalParameter(formalParameter) #kratise tis parametrous 
    return Obj

def searchEntity(name): #ka8e fora poy 8elw na prs8esw kati thn kalw 
    global table 
    global scopeNum


    if(scopeNum == 0):
        for i in range(len(table[0].entitylist)):
            if(name == table[0].entitylist[i].name):
                return table[0].entitylist[i]

    else:
        for scope in range(scopeNum, -1, -1):
            for i in range(len(table[scope].entitylist)):
                if(name == table[scope].entitylist[i].name):
                    return table[scope].entitylist[i]


    #print("Couldn't find symbol " + name)
    return None

def searchEntityScope(name): #8elw na brw to epipedo pou exei ena entity se poio scope vrisketai dld 
    global table 
    global scopeNum

    #gia scope > 0 
    for scope in range(scopeNum, -1, -1):
        for i in range(len(table[scope].entitylist)):
            if(name == table[scope].entitylist[i].name):
                return scope #gurna to scope pou brikes to entity
    #exei ginei o elegxos gia to an yparxei to entity apo thn allh search 

def addVariable(name,framelength,scopeLevel):
    boolEntity = searchEntity(name)

    if(not boolEntity == None and scopeLevel == 0 ): #globalnum = 0 means the variable is global
        print("Error you have allready declare this veriable before " + name)
        exit()  

    varObj =Variable(name,"integer",framelength,scopeLevel) #ftiaxnw to obj variable 
    return varObj

def addTemporaryVariable(name,datatype,offset,scopeLevel):
    temporaryVariable = TemporaryVariable(name,datatype,offset,scopeLevel)
    addEntity(temporaryVariable)

#########################################################
###########################final.py######################

#Drongoulas Georgios 4358 cse84358 
#Plachouras Diamadis 4476 cse84476

finalist=[]
firstLabelCall = 0 
f = open("test.asm" , "w")

######################
class Finalobj():

	def __init__(self,label,opp,reg1,reg2,reg3_label,mainstatus):
		self.label=label 
		self.opp=opp
		self.reg1=reg1
		self.reg2=reg2
		self.reg3_label=reg3_label
		self.mainstatus = mainstatus

	def printObj(self):
		return "	"+self.opp +" "+self.reg1+" "+self.reg2+" "+ self.reg3_label + "\n"	

	def __str__(self):
		if(str(self.label).isdigit()== True):
			return str(self.label)+"	"+self.opp +" "+self.reg1+" "+self.reg2+" "+ self.reg3_label
		return self.label+"	"+self.opp +" "+self.reg1+" "+self.reg2+" "+ self.reg3_label
######################


def produce(label ,opp , reg1 , reg2 , reg3_label):
	#global f
	global finalist
	notmain = "nomain"
	final = Finalobj(label,opp,reg1,reg2,reg3_label,notmain)
	finalist.append(final)
	#toWriteLineOfFinal = writeFinal(opp , reg1 , reg2 , reg3_label)
	#f.write(toWriteLineOfFinal)

def produceMain(label ,opp , reg1 , reg2 , reg3_label,main):
	global finalist
	final = Finalobj(label,opp,reg1,reg2,reg3_label,main)
	finalist.append(final)

def closeWriteFinal():
	global f 
	f.close()

#def readEndoiameso():
#gurnaei ston reg t0 thn timh ths dif8unshs ths metablhths poy psaxnw 
# gia prospelash metablhtwn pou briskontai se diaforetiko eggrafima drastiriopoihshs 
def gnlvcode(name,quad): 
	#1) search the verible in table 
	x = searchEntity(name)	
	#if cant find the veriable then x =none 
	if(x== None):
		print("Error that veriable "+ name +" counld't find in symbol table")
		exit()

	offsetV = 0 - x.offset

	#2) find the level that the veriable has been found 
	level = searchEntityScope(name) #level of entity scope tha prepei na anebei mexri to epipedo level 
	#print(level)
	#print("level of value that i search")
	if (level >= 1 ): # den einai global auth pou psaxnw 
		produce(quad.label,"lw","t0","-4(sp)","")
	
		scopeNum = getScopeNum() # se poio scope eimai auto einai to trexon scope 
		#print(scopeNum)
		#print(" this is scopenum")
		hops = scopeNum - level # hops is hops that i must do to reach the variable 
		#print(hops)
		#print("the hops")
		if(scopeNum > level):

			for i in range(hops-1):
				produce(quad.label,"lw","t0","-4(t0)","")
		#3) prosethese to offset gia na breis thn metablhth pou 8es 	
		produce(quad.label,"addi","t0","t0",str(offsetV))

	else: 
		print("this variable is global, that goes wrong")
		
def loadvr(vName,regName,quad):
	#take info from table 
	if(vName.isdigit()== True):
		produce(quad.label,"li" , regName , vName ,"")
	else:
		v = searchEntity(vName) #to entity(variable) pou prepei na ftasw 
		offsetV = 0 - v.offset
		
		if (v.isglobal == True ): #the v is global variable 
			produce(quad.label,"lw", regName, str(offsetV)+"(gp)", "") #using the gp 

		elif(v.scopeLevel == getScopeNum() and isinstance(v,Variable)): # an einai local metablhth me scope to trexon scope  h einai temporary variable
			produce(quad.label,"lw", regName, str(offsetV)+"(sp)", "")

		elif(v.scopeLevel == getScopeNum() and isinstance(v,FormalParameter) and v.mode == "cv" ): # an eisai parametros kai exeis perastei me timh 
			produce(quad.label,"lw", regName, str(offsetV)+"(sp)", "")
		 	
		elif(v.scopeLevel == getScopeNum() and isinstance(v,FormalParameter) and v.mode == "ref"): #mia parametros pou exei perastei me anafora
			produce(quad.label,"lw","t0", str(offsetV)+"(sp)", "")
			produce(quad.label,"lw",regName,"(t0)", "")

		elif(v.scopeLevel < getScopeNum() and (isinstance(v,Variable) or (isinstance(v,FormalParameter) and v.mode == "cv"))): #an einai topikh metablhth h parametros me timh pou anhkei se progono
			gnlvcode(v.name,quad)
			produce(quad.label,"lw",regName,"(t0)", "")

		elif(v.scopeLevel < getScopeNum() and (isinstance(v,FormalParameter) and v.mode == "ref")): #parametros pou exei perastei se progono me anafora
			gnlvcode(v.name,quad)
			produce(quad.label,"lw","t0","(t0)","")
			produce(quad.label,"lw",regName,"(t0)","")

def storerv(regName,vName,quad):

	if(vName.isdigit()== True):
		loadvr(vName,"t0",quad)
		storerv("t0",regName,quad)
	else:
		v = searchEntity(vName)
		offsetV = 0 - v.offset

		if(v.isglobal == True): 
			produce(quad.label,"sw", regName, str(offsetV)+"(gp)", "")

		elif(v.scopeLevel == getScopeNum() and isinstance(v,Variable)):# an einai local metablhth
			produce(quad.label,"sw", regName, str(offsetV)+"(sp)", "") 

		elif(v.scopeLevel == getScopeNum() and isinstance(v,FormalParameter) and v.mode == "cv" ): # an eisai parametros kai exeis perastei me timh 
			produce(quad.label,"sw", regName, str(offsetV)+"(sp)", "") 

		elif(v.scopeLevel == getScopeNum() and isinstance(v,FormalParameter) and v.mode == "ref"): #mia parametros pou exei perastei me anafora
			produce(quad.label,"lw","t0", str(offsetV)+"(sp)", "")
			produce(quad.label,"sw",regName,"(t0)","")

		elif(v.scopeLevel < getScopeNum() and (isinstance(v,Variable) or (isinstance(v,FormalParameter) and v.mode == "cv"))):#an einai topikh metablhth h parametros me timh pou anhkei se progono
			gnlvcode(v.name,quad)
			produce("sw",regName,"(t0)","","")

		elif(v.scopeLevel < getScopeNum() and (isinstance(v,FormalParameter) and v.mode == "ref")):#parametros pou exei perastei se progono me anafora
			gnlvcode(v.name,quad)
			produce(quad.label,"lw","t0","(t0)","")
			produce(quad.label,"sw",regName,"(t0)","")
			produce(quad.label,"sw",regName,"(t0)","")

def firstfinalJump():
	produce(0,"j","main","","")

def productFinal(Quad): #this func must to call in Parser to productFinal code 
	
	if(Quad.operator == ":="): #exoume ekxwrish
		#writeLabel(Quad)
		loadvr(Quad.operand1,"t0",Quad)
		storerv("t0",Quad.operand3,Quad)

	elif(Quad.operator == "+" or Quad.operator =="-" or Quad.operator == "*" or Quad.operator =="/"): #gia oles tis prakseis 
		#writeLabel(Quad)
		loadvr(Quad.operand1,"t1",Quad)
		loadvr(Quad.operand2,"t2",Quad)
		
		if(Quad.operator == "+"):
			produce(Quad.label,"add","t1","t2","t1")
		elif(Quad.operator == "-"):
			produce(Quad.label,"sub","t1","t2","t1")
		elif(Quad.operator == "*"):
			produce(Quad.label,"mul","t1","t2","t1")
		elif(Quad.operator == "/"):
			produce(Quad.label,"div","t1","t2","t1")

		storerv("t1",Quad.operand3,Quad)

	#jumps 
	elif(Quad.operator == "jump" and Quad.operand1 == "_" and Quad.operand2 == "_"):
		produce(Quad.label,"j","L"+Quad.operand3,"","") # j label 

	elif(Quad.operator == "=" or Quad.operator == "<>" or Quad.operator == "<" or Quad.operator == ">" or Quad.operator == "<=" or Quad.operator == ">="):
		loadvr(Quad.operand1 ,"t1",Quad)
		loadvr(Quad.operand2 ,"t2",Quad)

		if(Quad.operator == "="):
			produce(Quad.label,"beq","t1","t2","L"+str(Quad.operand3))
		elif(Quad.operator == "<>"):
			produce(Quad.label,"bne","t1","t2","L"+str(Quad.operand3))
		elif(Quad.operator == "<"):
			produce(Quad.label,"blt","t1","t2","L"+str(Quad.operand3))
		elif(Quad.operator == ">"):
			produce(Quad.label,"bgt","t1","t2","L"+str(Quad.operand3))
		elif(Quad.operator == "<="):
			produce(Quad.label,"ble","t1","t2","L"+str(Quad.operand3))
		elif(Quad.operator == ">="):
			produce(Quad.label,"bge","t1","t2","L"+str(Quad.operand3))
 	
	elif(Quad.operator == "Halt"):
		produce(Quad.label,"li","a0","0","")
		produce(Quad.label,"li","a7","93","")
		produce(Quad.label,"ecall","","","")

	elif(Quad.operator == "begin_block"):
		produceMain(Quad.label,"addi","sp","sp","_","main")
		produceMain(Quad.label,"mv","gp","sp","","main")

	elif(Quad.operator == "ret"):
		loadvr(Quad.operand1,"t1",Quad)
		produce(Quad.label,"lw","t0",str(-8)+"(sp)","")
		produce(Quad.label,"sw","t1","(t0)","")

	elif(Quad.operator == "in"):
		loadvr(Quad.operand1,"t0",Quad)
		produce(Quad.label,"lw","a7","(t0)","")
		produce(Quad.label,"ecall","","","")

	elif(Quad.operator == "out"):
		produce(Quad.label,"mv","a0","t0","")
		produce(Quad.label,"a7","1","","")
		produce(Quad.label,"ecall","","","")

def productFinalForCalls(list,num,nameFunc,frame): #this list exei oles tis tetrades pou ginontai gia ena call sunarthshs h diadikasias 
	global QuadList
	global firstLabelCall
	callist=[] # exei ta quads pou 8elw gia na kanw ta kanw ta orismata se teliko 
	#addi fp sp framelength
	produce(list[0],"addi","fp","sp",str(frame))
	JalHere = 0 
	t=0
	while t < len(QuadList):
		if(QuadList[t].operator == "begin_block" and QuadList[t].operand1 == nameFunc):
			JalHere = QuadList[t].label
		t = t+1 

	x = 0 
	j=0
	while x < len(QuadList):
		while j < len(list):
			if(QuadList[x].label == list[j]):
				callist.append(QuadList[x])
				j =j+1 
			x = x +1  

	for i in range(len(callist)):
		
		if(callist[i].operator == "par" and callist[i].operand2 == "cv"):
			loadvr(callist[i].operand1,"t0",callist[i])
			produce(list[i],"sw","t0",str(-(12-4*i))+"(fp)","")
		
		elif(callist[i].operator == "par" and callist[i].operand2 == "ref"):
			parameter = searchEntity(callist[i].operand1)

			if(parameter.scopeLevel==getScopeNum() and ((isinstance(parameter,FormalParameter)) and parameter.mode =="ref")):
				produce(list[i],"lw" ,"t0",str(-parameter.offset)+"(sp)","")
				produce(list[i],"sw","t0",str(-(12-4*i))+"(fp)","")
			
			elif(parameter.scopeLevel<getScopeNum() and ((isinstance(parameter,FormalParameter)) and parameter.mode =="ref")):
				gnlvcode(parameter)
				produce(list[i],"lw" ,"t0","(t0)","")
				produce(list[i],"sw","t0",str(-(12-4*i))+"(fp)","")

			else:
				produce(list[i],"addi","t0","sp",str(-parameter.offset))
				
				if(parameter.scopeLevel == getScopeNum() or isinstance(parameter,TemporaryVariable) or (isinstance(parameter,FormalParameter) and parameter.mode =="cv" ) ):
					produce(list[i],"sw","t0",str(-(12-4*i))+"(fp)","")
				
				elif(parameter.scopeLevel == getScopeNum() or (parameter.scopeLevel < getScopeNum() and parameter.mode == "cv")):
					gnlvcode(parameter)
					produce(list[i],"sw","t0",str(-(12-4*i))+"(fp)","")

				elif(parameter.scopeLevel == 0 ):
					produce(list[i],"addi","t0","gp",str(-parameter.offset))

		elif(callist[i].operator == "par" and callist[i].operand2 == "ret"):
			x=searchEntity(callist[i].operand1)
			produce(list[i],"addi","t0","sp",str(-x.offset))
			produce(list[i],"sw","t0",str(8)+"fp","")


		elif(callist[i].operator == "Call"):

			if(searchEntity(callist[i].operand1).scopeLevel < getScopeNum()):
				produce(list[i],"sw","sp",str(-4)+"fp","")
			else:
				produce(list[i],"lw" ,"t0",str(-4)+"(sp)","")
				produce(list[i],"sw" ,"t0",str(-4)+"(fp)","")

			produce(list[i],"addi","sp","sp",str(frame))
			produce(list[i],"jal",str(JalHere),"","")
			produce(list[i],"addi","sp","sp",str(-frame))

def productFinalBegin(quad):
	if(quad.operator == "begin_block"):
		produce(quad.label,"sw","ra","(sp)","")

def productFinalForSubBlocks(list):
	global QuadList
	callist=[]
	x = 0 
	j=0
	while x < len(QuadList):
		while j < len(list):
			if(QuadList[x].label == list[j] ):
				callist.append(QuadList[x])#ola ta begin blocks
				j = j +1 
			x = x +1 

	for i in range(len(callist)):

		if(callist[i].operator =="end_block"):
			produce(callist[i].label,"lw","ra","(sp)","")
			produce(callist[i].label,"jr","ra","","")


#label kai nextquad mporei na einai arithmoi (to nextquad ama thes pes to kai nextLabel)
#psaxnw thn lista gia to (label)L23, opou auto to label tha exei entoles telikou 
#alla sto telos tha exei kai beq kai ena jump
#kai analoga (truelist h falselist) tha dialegw na patcharw to beq h to jump me to nextquad(to opoio einai nextLabel sthn ousia)
#mporeis na kaneis backpatchTrueTeliko() kai backpatchFalseTeliko() gia beq kai jump antistoixa	
def backpatchTrueTeliko(label_list,nextquad):
	global finalist
	i=0
	j=0

	while (i < len (label_list)): #des tis etiketes pou sou dinei gia to se poies tetrades tha paei na kanei branch 
		while (j < len(finalist)): # apo oles tis entoles tou telikou 
			if(label_list[i] == finalist[j].label and (finalist[j].opp == "beq" or finalist[j].opp == "bne" or finalist[j].opp == "blt" or finalist[j].opp == "bgt" or finalist[j].opp == "ble" or finalist[j].opp == "bge")):
				finalist[j].reg3_label = "L"+str(nextquad)

				break
			j=j+1
		i=i+1
	label_list.clear()

def backpatchFalseTeliko(label_list, nextquad):
	global finalist
	i=0
	j=0
	while (i < len (label_list)): #des tis etiketes pou sou dinei gia to se poies tetrades tha paei na kanei branch 
		while (j < len(finalist)): # apo oles tis entoles tou telikou 

			if(label_list[i] == finalist[j].label and (finalist[j].opp == "j")):
				finalist[j].reg1 = "L"+str(nextquad)
				break
			j=j+1
		i=i+1
	label_list.clear()

def backpatchMain(frameLength):
	global finalist
	i = 0
	while (i < len(finalist)):
		if(finalist[i].mainstatus == "main" and finalist[i].opp =="addi"):
			finalist[i].reg3_label = str(frameLength)
			break
		i=i+1 

def printList(finalist):
	global f
	global QuadList

	list = [] 
	#for i in range (len(finalist)):
	#	print(finalist[i])

	x=0
	while(x < len(finalist)-1):
		if(x == 0):
			f.write("L0"+":"+"\n")
			f.write(finalist[x].printObj())
			x=x+1
		if(not str(finalist[x].label) == str(finalist[x-1].label) and (not str(finalist[x].label) == str(finalist[x+1].label))):# na mhn uparxei allos teliko gia to idio quad
			f.write("L"+str(finalist[x].label)+":"+"\n")
			f.write(finalist[x].printObj())
			x=x+1


		if(finalist[x].mainstatus == "main"):
			f.write("Lmain:"+"\n")
			f.write(finalist[x].printObj())
			f.write(finalist[x+1].printObj())
			x=x+1

		if(int(finalist[x-1].label) < int(finalist[x].label)):
			f.write("L"+str(finalist[x].label)+":"+"\n")
			while(True):
				if(x+1 == len(finalist)):
					f.write(finalist[x].printObj())
					break
				f.write(finalist[x].printObj())
				if(int(finalist[x].label)<int(finalist[x+1].label) ):
					break
				x=x+1
		x=x+1



#######################################################
################Parser20.py############################

#Drongoulas Georgios 4358 cse84358 
#Plachouras Diamadis 4476 cse84476

oneBlock=[]
token_index = 0 # thn 8esh tou token ston pinaka tokens 
program_name=""
activation_rec_stack = []
frameLength = 12

#sunarthshs gia na diavazw ta epomena token pou exei o kanei o lex 
#  ka8e fora pou 8a bainei edw 8a katanalwnei kai ena token ara 8a afksanw ka8e fora enana metrith gia na kserw se poio token eimai 
def get_token():
    global token_index
    global tokens 

    token_index += 1 
    if(token_index < len(tokens)  ):
        new_token = tokens[token_index]  
        return new_token 

# borw na kanw tis synarthseis mou me osa exoun bei mesa sth lista oneBlock
def assignStat():
    global token
    global frameLength


    if(token.family == "idk" ):
        tString = token.recognized_string
        boolEntity = searchEntity(tString)                 # an den uparxei ston table tote exw la8os 
        if(boolEntity == None ):
            print (" Error that veriable is undetifier " + tString +" at line "+str(token.line_number) )
            exit()
        token = get_token()
        if (token.family == "assignment"):
            token = get_token()
            eplace = expression() #kanw return to t1place kai to bazw sto eplace 
            quad = genQuad(":=",eplace,"_",tString) #newquad
            productFinal(quad)
        else:
            print("Error waiting for := and find " + token.recognized_string + " at line " + str(token.line_number))
            exit()
    else:
        print("Error waiting for id and find " + token.recognized_string + " at line "  + str(token.line_number))
        exit()

def optional():
    global token
    if(token.family == "addOperator"):
        addOperator()

# na dw an exw gia float h akeraio 
def factor():   # f->(E)
    global token

    if(token.family == "dig"): # kai gia float
        tString = token.recognized_string  
        token = get_token()
        return tString

    elif(token.recognized_string == "("):
        token = get_token()
        eplace = expression()
        returnValue = eplace
        if(token.recognized_string == ")"):
            token = get_token()
        else:
            print("Error i am waiting ) and i find "+token.recognized_string+" at line "+ str(token.line_number))
            exit()
        return returnValue

    elif(token.family == "idk"): 
        tString = token.recognized_string
        token = get_token()
        idtail()
        return tString
    else:
        print("Error i am waiting for const or real or id or ( and i find"+token.recognized_string+" at line "+ str(token.line_number))
        exit()

#ADD OPERATOR 
def addOperator():
    global token

    if(token.recognized_string == "+" ):
        token = get_token()
        return "+"
    elif(token.recognized_string == "-"):
        token =get_token()
        return "-"
    else:
        print("Error i am waiting for + or - and find" + token.recognized_string+" at line " + str(token.line_number))
        exit()
        
#muloperator
def mulOperator():
    global token
    if(token.recognized_string == "*" ):
        token = get_token()
        return "*"
    if(token.recognized_string == "/"):
        token =get_token()
        return "/"
    else:
        print("Error i am waiting for * or / and find" + token.recognized_string+" at line " + str(token.line_number))
        exit()

def term(): #t -> f1 ( * f2)* 
    global token 
    global frameLength

    f1place = factor()
    while(token.recognized_string == "*" or token.recognized_string == "/"):
        operator = mulOperator()
        f2place = factor()
        w = newTemp()
        quad=genQuad(operator,f1place,f2place,w)
        #INSERT TEMPORARY VARIABLE to table
        addTemporaryVariable(w,"integer",frameLength,getScopeNum())
        frameLength +=4
        productFinal(quad) #final for * and /
        f1place = w 
    return f1place

def expression(): # E -> t1 (+ t2)*
    global  token
    global frameLength

    optional()
    t1place = term()
    while( token.recognized_string == "+" or token.recognized_string == "-"):

        operator = addOperator()
        t2place = term()
        w = newTemp() # new tmp for results t1 + t2  
        quad=genQuad(operator, t1place, t2place, w )
        #INSERT TEMPORARY VARIABLE to table
        addTemporaryVariable(w,"integer",frameLength,getScopeNum())
        frameLength +=4
        productFinal(quad) #final for + and - 
        t1place = w 
    return t1place 

def relationalOper():
    global token

    if(token.family == "relOperator"):
        tString = token.recognized_string
        token = get_token()
        return tString
    else:
        print("Error i am waiting for relOperator and i find " + token.recognized_string + " at line " + str(token.line_number))
        exit()

def boolfactor():
    global token
    if (token.recognized_string == "not"): #R -> not [B]
        token = get_token()
        if(token.recognized_string == "["):
            token = get_token()
            brule = condition()
            rtrueList = brule.falseList
            rfalseList = brule.trueList

            if(token.recognized_string == "]"):
                token = get_token()
            else:
                print("Error i am waiting ] and i find " +token.recognized_string+ " at line " + str(token.line_number))
                exit()

            return rule(rtrueList,rfalseList)

        else:
            print("Error i am waiting [ and i find " +token.recognized_string+ " at line " +str(token.line_number))
            exit()
    elif(token.recognized_string == "["): # R->B
        token = get_token()
        brule = condition()
        rtrueList = brule.trueList
        rfalseList = brule.falseList

        if(token.recognized_string == "]"):
    
            token = get_token()
        else:
            print("Error i am waiting ] and i find " +token.recognized_string+ " at line " + str(token.line_number))
            exit()
        return rule(rtrueList,rfalseList)
    else:
        e1place = expression()
        operator = relationalOper()
        e2place = expression()
        rtrueList = makeList(nextQuad())
        ##
        quad = genQuad(operator,e1place,e2place,"_")
        productFinal(quad)
        ##
        rfalseList =makeList(nextQuad())
        ##
        quad1 = genQuad("jump","_","_","_")
        productFinal(quad1)
        ##
        return rule(rtrueList,rfalseList)

def boolterm(): #Q -> r1(and r2)*
    global token
    global QuadList

    r1Rule = boolfactor()
    qtrueList = r1Rule.trueList
    qfalseList = r1Rule.falseList
    while token.recognized_string == "and":
        token = get_token()
        backpatch(qtrueList,nextQuad()) # an einai swsto 8a paw sto epomeno quad
        backpatchTrueTeliko(qtrueList,nextQuad())
        r2Rule = boolfactor()
        qtrueList = r2Rule.trueList
        qfalseList = mergeList(qfalseList,r2Rule.falseList)
    return rule(qtrueList,qfalseList)

def condition(): #B -> Q1 ( or Q2)*
    global token
    global QuadList
    q1Rule = boolterm()
    btrueList = q1Rule.trueList
    bfalseList = q1Rule.falseList
    while token.recognized_string == "or":
        token = get_token()
        backpatch(bfalseList,nextQuad())
        backpatchFalseTeliko(bfalseList,nextQuad())
        q2Rule = boolterm()
        btrueList = mergeList(btrueList,q2Rule.trueList)
        bfalseList = q2Rule.falseList
    return rule(btrueList,bfalseList) #edw guranw ton b Kanona me tis listes poy prepei na exei 

def elsepart():
    global token 
    if(token.recognized_string == "else"):
        token = get_token()
        statements()
    else:
        token =get_token() # gia na dwsei to keno 

def ifStat():
    global token
    global QuadList
    token = get_token()
    if(token.recognized_string == "("):
        token = get_token() 
        ifRule = condition()
        if(token.recognized_string == ")"):
            backpatch(ifRule.trueList,nextQuad())
            #print(ifRule.falseList)
            backpatchTrueTeliko(ifRule.trueList,nextQuad()) #teliko
            token = get_token()
            statements()
            iflist =makeList(nextQuad())
            ifQuad=genQuad("jump","_","_","_")
            productFinal(ifQuad)
            backpatch(ifRule.falseList,nextQuad())
            backpatchFalseTeliko(ifRule.falseList, nextQuad())#teliko
            elsepart()
            backpatch(iflist,nextQuad())
            #print(iflist)
            backpatchFalseTeliko(iflist, nextQuad()) 

        else:
            print("Error i am waiting to close parenthesh ) at line " + str(token.line_number))
            exit()
    else:
        print("Error you are in if stat and you dont open the condition parenthesh at line " + str(token.line_number))
        exit()

def whileStat():
    global token
    condQuad = nextQuad() #shmeiwnw thn tetrada prin to condition 
    token = get_token()
    if(token.recognized_string =="("):
        token = get_token()
        whileRule = condition()
        if(token.recognized_string ==")"):
            backpatch(whileRule.trueList,nextQuad())
            backpatchTrueTeliko(whileRule.trueList,nextQuad())
            token = get_token()
            statements()
            token =get_token()
            whileQuad=genQuad("jump","_","_",str(condQuad))
            backpatch(whileRule.falseList,nextQuad())
            backpatchFalseTeliko(whileRule.falseList,nextQuad())
            productFinal(whileQuad)
        else: 
            print("Error i am waiting to close ) at line " + str(token.line_number))
            exit()
    else:
        print("Error i am waiting to open ( for the condition of while " + str(token.line_number))
        exit()

def forStat():
    global token

    firstCondQuad = nextQuad()
    token = get_token()
    while(token.recognized_string == "case"):
        token = get_token()
        if(token.recognized_string == "("):
            token = get_token()
            ifRule = condition()
            if(token.recognized_string == ")"):
                backpatch(ifRule.trueList,nextQuad())
                backpatchTrueTeliko(ifRule.trueList,nextQuad())
                token = get_token()
                statements()
                if(token.recognized_string =="}"):
                    token =get_token()
                forQuad=genQuad("jump","_","_",str(firstCondQuad))
                backpatch(ifRule.falseList,nextQuad())
                backpatchFalseTeliko(ifRule.falseList,nextQuad())
                productFinal(forQuad)
            else:
                print("Error i am waiting to close parenthesh ) at line " + str(token.line_number))
                exit()
        else:
            print("Error i am waiting to open parenthesh ( at line " + str(token.line_number))
            exit()

    if(token.recognized_string == "default"):
        token = get_token()
        statements() 
        if(token.recognized_string =="}"):
            token =get_token()  
    else:
        print("Expected default case for For but find "+ token.recognized_string+" at line "+str(token.line_number))
        exit()

def switchStat():
    global token
    exitList = emptyList() #lista gia thn eksodo 
    token = get_token()
    while(token.recognized_string == "case"):
        token = get_token()
        if(token.recognized_string == "("):
            token = get_token()
            switchRule = condition()
            if(token.recognized_string == ")"):
                backpatch(switchRule.trueList,nextQuad())
                backpatchTrueTeliko(switchRule.trueList,nextQuad())
                token = get_token()
                statements()
                if(token.recognized_string =="}"):
                    token =get_token()
                t = makeList(nextQuad())
                switchQuad=genQuad("jump","_","_","_")
                productFinal(switchQuad)
                exitList = mergeList(exitList,t)
                backpatch(switchRule.falseList,nextQuad())
                backpatchFalseTeliko(switchRule.falseList,nextQuad())
            else:
                print("Error i am waiting to close parenthesh ) at line " + str(token.line_number))
                exit()
        else:
            print("Error i am waiting to open parenthesh ( at line " + str(token.line_number))
            exit()
    if(token.recognized_string == "default"):
        token =get_token()
        statements()
        if(token.recognized_string =="}"):
            token =get_token()
        backpatch(exitList,nextQuad())
        backpatchFalseTeliko(exitList,nextQuad())

    else:
        print("Expected default case for switch but find "+ token.recognized_string+" at line "+str(token.line_number))
        exit()

def incaseStat():
    global token

    token = get_token()
    flag = newTemp()
    firstCondQuad = nextQuad()
    genQuad(":=","0","_",flag)

    while(token.recognized_string == "case"):
        token = get_token()
        if(token.recognized_string == "("):
            token = get_token()
            incaseRule = condition()
            if(token.recognized_string == ")"):
                backpatch(incaseRule.trueList,nextQuad())
                token = get_token()
                statements()
                genQuad(":=","1","_",flag)
                backpatch(incaseRule.falseList,nextQuad())
            else:
                print("Error i am waiting to close parenthesh ) at line " + str(token.line_number))
                exit()
        else:
            print("Error i am waiting to open parenthesh ( at line " + str(token.line_number))
            exit() #EXEI ENA 8EMA 
    genQuad("=","1",flag,str(firstCondQuad))
    
def returnStat():
    global token
    
    if(token.recognized_string == "return"):
        token = get_token()
        if(token.recognized_string =="("):
            token = get_token()
            eplace = expression()
            #print(token)
            if(token.recognized_string==")"):
                token = get_token()
                quad=genQuad("ret",eplace,"_","_")
                productFinal(quad)
            else: 
                print("Error you dont close the expression an expect ) but find "+token.recognized_string+" at line " + str(token.line_number))
                exit()
        else:
            print("Error you dont close the expression an expect ) but find "+token.recognized_string+" at line " + str(token.line_number))
            exit()

def callStat(): #gia ton pinaka shmbolwn kanw search an exei ginei dhlwsh ths sunarthshs poy paw na kalesw 
    global token
    global frameLength
    callQuadlist =[]
    if(token.recognized_string =="call"):
        token = get_token()
        if(token.family == "idk"):
            tmp = token.recognized_string
            callBool = searchEntity(tmp) #an epistrafei none tote den yparxei h synartish poy 8elw na kalesw
            frame = callBool.offset
            if(callBool == None ):
                print(" undetifier function with name or in that func doest must the args " + tmp )
                exit()
            
            token = get_token()
            if(token.recognized_string == "("): #orismata
                token = get_token()

                ####################edw#################### 
                numOfparameters = actualparlist(callQuadlist)# apo thn epomenh tetrada 8a exw parametrous ara shmeiwnw apo poy ksekinaei to call
                ##############
                if(isinstance(callBool,function)):#an einai function exw epistrefomenh timh 
                    w=newTemp()
                    addTemporaryVariable(w,"integer",frameLength,getScopeNum())
                    frameLength +=4
                    callQuadlist.append(nextQuad())
                    genQuad("par",w,"ret","_") #epitstrefomenh timh gia to function

                callQuadlist.append(nextQuad())
                genQuad("Call",tmp,"_","_")

                if(token.recognized_string == ")"):
                    token =get_token()
                else:
                    print("Error expected ) to close the parameter bracket at line " + str(token.line_number))
                    exit()
                num=callBool.getNumOfParameters()
                productFinalForCalls(callQuadlist,num,tmp,frame) #kalw na kanw teliko me markarismenes tis tetrades pou kanoun to call exw ton ari8mo twn parametrwn kai to onoma ths kalousas 
                frame = 0 
                callQuadlist.clear() # otan teleiwsw me th paragwgh tou telikou diagrafw ti lista 
                if(not (num == numOfparameters)):
                    print("Error this func-->"+ tmp+" does not exit with that number of parameters")
                    exit()

            else:
                print("Error expected ( to open the parameter bracket at line " + str(token.line_number))
                exit()
        else:
            print("Erro expected idk for the name of func that you call at line "+str(token.line_number))
            exit()

def printStat(): #telikos
	global token
	if(token.recognized_string == "print"):
		token = get_token()
		if(token.recognized_string == "("):
			token = get_token()
			eplace=expression()        

			if(token.recognized_string!=")"):
				token =get_token()
				quad=genQuad("out",eplace,"_","_")
				productFinal(quad)

			elif(token.recognized_string == ")"):
				token =get_token()
				quad=genQuad("out",eplace,"_","_")
				productFinal(quad)
			else:
				print("Error expected ) to close the expression in the print at line " + str(token.line_number))
				exit()

		else:
			print("Error expected to open the expression in print at line at line " + str(token.line_number))
			exit()

def inputStat():
    global token 
    if(token.recognized_string == "input"):
        token = get_token()
        if(token.recognized_string == "("):
            token = get_token()
            if(token.family =="idk"):
                idString = token.recognized_string
                token =get_token()
                if(token.recognized_string ==")"):
                    token = get_token()
                    quad=genQuad("in",idString,"_","_")
                    productFinal(quad)
                else:
                    print("Error expected ) to close the brackets of input at line "+str(token.line_number))
                    exit()
            else:
                print("Error expected idk inside the print at line " +str(token.line_number))
                exit()
        else:
            print("Error you must open the bracket for the print at line "+str(token.line_number))
            exit()

def actualparitem(list):#to elenksa apo thn gramatikh kala einai 
    global token 
    param =""
    if(token.recognized_string == "in"):
        token =get_token()
        param =token.recognized_string + "cv"
        list.append(nextQuad())#shmeiwnw oti eida mia parametro 
        genQuad("par",token.recognized_string,"cv","_")
        expression()


    elif(token.recognized_string == "inout"):
        token = get_token()
        param =token.recognized_string +"ref"
        if(token.family == "idk"):
            list.append(nextQuad())#shmeiwnw oti eida mia parametro 
            genQuad("par",token.recognized_string,"ref","_")
            token = get_token()
        else:
            print("Error, expected ID for inout parameter at line " +str(token.line_number))
            exit()

    return param

def actualparlist(list):
    global token
    paramNum = 0  
    
    actualparitem(list)
    paramNum+=1
    while(token.recognized_string == ","):
        paramNum+=1
        token =get_token()
        actualparitem(list)

    return paramNum

def idtail():
    global token 
    if(token.recognized_string == "("):
        token = get_token()
        actualparlist()
        
#statement 
def statement():
    global token 

    tmp = token.recognized_string

    if(token.family == "idk"):
        assignStat()
    if(tmp == "if"):
        ifStat()
    if(tmp == "forcase"):
        forStat()
    if(tmp == "switchcase"):
        switchStat()
    if(tmp == "while"):
        whileStat()
    if(tmp == "incase"):
        incaseStat()
    if(tmp == "call"):
        callStat()
    if(tmp == "return"):
        returnStat()
    if(tmp == "print"):
        printStat()
    if(tmp == "input"):
        inputStat()
    if(tmp == ";"):
        return

def statements():
    global token    

    if(token.recognized_string=="{"):
        token = get_token()
        statement()
        while(token.recognized_string == ";"):
            token = get_token()
            statement()
        if(token.recognized_string == "}"):
            #token =get_token()
            return
            #print(token)
        else:
            print("Error i expect to close the bracket but i find "+token.recognized_string+" At line" +  str(token.line_number))
            exit()

    else:
        statement()
        if(token.recognized_string == ";"):
            token=get_token()
        else:
            print("Error i expect ; but i find "+token.recognized_string+" At line" +  str(token.line_number))
            exit()

def formalparlist():
    global token
    listParam = [] 


    token = get_token()
    paramObj = formalparitem()
    listParam.append(paramObj)
    while(token.recognized_string == ","):
        token = get_token()
        paramObj=formalparitem()
        listParam.append(paramObj)

    return listParam

def formalparitem(): # gia tis tetrades twn parametrwn
    global token 
    global frameLength

    mode = ""
    if(token.recognized_string == "in" or token.recognized_string == "inout"):

        if(token.recognized_string == "in"):
            mode = "cv"
        if(token.recognized_string == "inout"):
            mode = "ref"

        token = get_token()
        if(token.family == "idk"): # pernw ta orismata tis sunarthshs
            paramObj = FormalParameter(token.recognized_string,"integer",frameLength,mode,getScopeNum())
            frameLength +=4
            addEntity(paramObj)
            token = get_token()
            return paramObj
        else:
            print("Error i am waiting for idk and i find :" + token.family + " at line " + str(token.line_number))
            exit()

def subBlock(subName,mode):
    global token
    listEnd = [] 

    if(token.recognized_string =="{"):
        declarations()
        subprograms() #true an exoume kialh sunarthsh 
        #print(frameLength)
        #print("edw")
        Quad = genQuad("begin_block",subName,"_","_")
        productFinalBegin(Quad)
        blockstatements()
        #tmp = newTemp() 
        if(token.recognized_string == "}"):

            if(mode == "function"):
                #genQuad("par",tmp,"ret","_") #epitstrefomenh timh gia to function
                listEnd.append(nextQuad())
                fQuad=genQuad("end_block",subName,"_","_")
                productFinalForSubBlocks(listEnd)
               
                token = get_token()
                return Quad.label # gurnaw tn etiketa ths sunarthshs
            else:
                listEnd.append(nextQuad())
                pQuad=genQuad("end_block",subName,"_","_")
                productFinalForSubBlocks(listEnd)
          
                token = get_token()
                return Quad.label

        else:
            print("Error i am waiting for }  at line "+ str(token.line_number) + " but i find " + token.recognized_string)
            exit()

    else:
        print("Error i am waiting for {  at line "+str(token.line_number))
        exit()

def subprogram():
    global token 
    global frameLength

    if(token.recognized_string == "procedure"):
        token = get_token()
        procName =token.recognized_string
        procObj =  Procedure(procName,"_","_","_",frameLength,getScopeNum())
        addEntity(procObj)
        #8elw to frame pointer
        #backpatchFrame  
        activation_rec_stack.append(frameLength) #krataw pou htan h sunarthsh mou se poio scope 
        frameLength = 12

        if(token.family == "idk"):
            token = get_token()
            addScope() # new scope 
            print("Scope is " + str(getScopeNum()))
            paramList=formalparlist()
            token =get_token()
            labelQuad = subBlock(procName,"procedure") 
            NewprocObj = UpdateFields(procObj,frameLength,labelQuad,paramList)
            frameLength = activation_rec_stack.pop() #pernei to teleutaio stoixeio 
            frameLength += 4
            #edw prepei na kanw puching gia na parw to framelength ths produce 
            print("Deleting scope")
            deleteScope()
            addEntity(NewprocObj)
        else:
            print("Error i am waiting for id for procedure an i find "+token.recognized_string+" at line "+ str(token.line_number))
            exit()

    elif(token.recognized_string == "function"):
        token = get_token()
        #dhmiourgia shmboloy sunarthshs
        funcName = token.recognized_string
        funcObj = function(funcName,"_","_","_","integer",frameLength,getScopeNum()) #den kserw to prwto quad ka to framlength
        addEntity(funcObj)
        activation_rec_stack.append(frameLength) #krataw pou htan h sunarthsh mou se poio scope 
        frameLength = 12

        if(token.family == "idk"):
            token = get_token()
            addScope() # new scope 
            print("Scope is " + str(getScopeNum()))
            paramList=formalparlist()
            #print("meta tis parametrous")
            #print(frameLength)
            token =get_token()

            labelQuad = subBlock(funcName,"function") # 8elw na gurisei to label apo to prwto quad 
            #print("after sunBlock, framlength:" + str(frameLength))
            NewFuncObj = UpdateFields(funcObj,frameLength,labelQuad,paramList) #exw to kainourgio function object enhmerwmeno gia na to balw mesa sto scope 
            frameLength = activation_rec_stack.pop() #pernei to teleutaio stoixeio 
            frameLength += 4
            print("Deleting scope")
            deleteScope()
            addEntity(NewFuncObj)


        else:
            print("Error i am waiting for id for function an i find "+token.recognized_string+" at line "+ str(token.line_number))
            exit()

def subprograms():
    global token 
    while(token.recognized_string == "function" or token.recognized_string == "procedure"):
        subprogram()    

def blockstatements():
    global token

    statement()
    while(token.recognized_string == ";"):
        token = get_token()
        statement()
        
def varlist():
    global token
    global frameLength

    token = get_token()
    while(token.recognized_string == ","):
        token = get_token()
        if(token.family == "idk"):
            name = token.recognized_string
            varObj = addVariable(name,frameLength,getScopeNum())
            frameLength+=4
            addEntity(varObj)
            token = get_token()
        else:
            print("Expected for idk and find " +token.family+" at line "+ str(token.line_number))
            exit()

def declarations():
    global token 
    global frameLength

    token = get_token()
    while(token.recognized_string == "declare"):
        token = get_token()
        if(token.family == "idk"):

            name = token.recognized_string
            varObj = addVariable(name,frameLength,getScopeNum())
            frameLength+=4
            addEntity(varObj)
            varlist()
            if(token.recognized_string ==";"):
                token =get_token()
            else:
                print("Expected for ; and find " +token.recognized_string+" at line "+ str(token.line_number))
                exit()

        else:
            print("Error you must put one id for you declare variable at line " + str(token.line_number))
            exit()

def block():
    global token
    if(token.recognized_string == "{"):
        declarations()
        subprograms()
        begin_block=genQuad("begin_block",program_name,"_","_")
        productFinal(begin_block)
        blockstatements()
        if(token.recognized_string == "}"):
            token = get_token()

        else:
            print("Error i am waiting for }  at line "+ str(token.line_number) + " but i find " + token.recognized_string)
            exit()

    else:
        print("Error i am waiting for {  at line "+str(token.line_number))
        exit()

def program():
    global token 
    global tokens
    global program_name

    if(token.recognized_string == 'program'):
        token = get_token()
        addScope()
        print("Scope is " + str(getScopeNum()))
        if(token.family == 'idk'):
            program_name = token.recognized_string
            print(" the program you run is : "+program_name)
            token = get_token()
            # print bei sthn block kanw create to prwto jump 
            firstfinalJump() 
            block()
            if (token.recognized_string == '.'):
                #kane backpatch gia na baleis to framelength sto addi ths main 
                print("frameLength of program : " + str(frameLength))
                backpatchMain(frameLength)
                halt=genQuad("Halt","_","_","_")
                productFinal(halt)
                genQuad("end_block",program_name,"_","_")
                token = get_token()
                
            else:
                print("expected . at " + str(token.line_number) + " line to close the program \nEvery program should end with a fullstop, fullstop at the end is missing." )
                exit()
        else :
            print("The name of the program expected after the keyword “program” in line 1. The illegal program name ... appeared")
            exit()
    else:
        print("keyword “program” expected in line 1.All programs should start with the keyword “program”. Instead, the word  appeared")
        exit()

def syntax_analyzer():
    global token
    global QuadList
    global finalist
    # kalw ton lex aluth gia na gemisoun ta tokens 
    lexAnalyzer()
    token = tokens[0]
    program()
    print("\n")
    printList(finalist)
    closeWriteFinal()
    print("\n")
    printAllquads()
    print('compilation successfully completed')
	
syntax_analyzer()