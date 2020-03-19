AST=0
CIRC=1
TIMES=2

figNb=0
patchNb=0

def whereIsFirst(e,L):
    if not e in L:
        return None
    for i in range(len(L)):
        if L[i]==e:
            return i
def whereIsLast(e,L):
    if not e in L:
        return None
    for i in reversed(range(len(L))):
        if L[i]==e:
            return i
def disjoint(L1,L2):
    for e in L1:
        if e in L2:
            return False
    return True

def areCompatible(L1,L2,v1,v2):
    #L1 and L2 are lists of lists
    #returns True iff L1 and L2 contain each a list that are disjoint from each other
    #and none of those contain v1 nor v2
    if L1==[]:
        return False
    if L2==[]:
        return False
    if [] in L1:
        return True
    if [] in L2:
        return True
    for l1 in L1:
        for l2 in L2:
          if v1 not in l1 and v2 not in l1:
           if v1 not in l2 and v2 not in l2:
            if disjoint(l1,l2):
                return True
    return False

class Face:
    def __init__(self,faceNb,faceSize,neigh=[],w=[],a=[],sn=[],sw=[],dist=None,label=None):
        self.nb=faceNb
        self.s =faceSize 
        self.n =neigh #list of neighbors
        self.w =w #where the actual face is in the list of neighbors of its neighbors
        self.a =a #list of incident vertices
        self.sn=sn #list of subadjacent faces
        self.sw=sw #where is face in subadjacency list of subneighbor
        self.d=dist #distance from the outer outer face
        self.label=label #ast (black), circ (white resonant) or times (white Q)
    def show(self):
        print(self.nb,self.s,self.d,self.n,self.a,self.sn,self.sw)

class Vertex:
    def __init__(self,vertexNb,neigh=[],a=[],w=[],dist=None):
        self.nb=vertexNb
        self.n = neigh #list of neighbors
        self.a = a  #list of incident faces
        self.w=w #where the vertex is in the list of neighbors of its neighbors
        self.d=dist #distance from the outer outer face
    def show(self):
        print(self.nb,self.d,self.n,self.a)

class qpath:
    def __init__(self,timesFaces,astFaces,forVer):
        self.timesFaces=timesFaces #TIMES faces of a Q-path
        self.astFaces=astFaces #AST faces o a Q-path
        self.forVer=forVer #vertices of the Q-edges of the Q-path
        
class Patch:
    def __init__(self,f4,f5,f6,f=[],v=[],nb=0,boundary=[],nbOuterFaces=0,t=None,meta="",success=[False,False],initialAstFaces=[],Qpaths=[],nbp=False):
        self.f4=f4 #nb of 4-faces
        self.f5=f5 #nb of 5-faces
        self.f6=f6 #nb of 6-faces
        self.c=2*f4+f5 #curvature
        self.f=f #the list of faces
        self.v=v #the list of vertices
        self.nb=nb #patch number
        self.boundary=boundary #boundary description
        self.nbOuterFaces=nbOuterFaces #nb of incomplete faces
        self.type=t #ODD, ID_EVEN or CY_EVEN
        self.meta=meta #metapost declaration of vertices and faces
        self.success=success #found a solution for even and odd Q-paths
        self.initialAstFaces=initialAstFaces #initial AST faces
        self.Qpaths=Qpaths #Q-paths
        self.needBothParities=nbp #whether both parities are needed or just one

    def calculateType(self):
        if self.c!=6:
            self.nanoType=None
        else:
            vector=[]
            for face in self.f[-1].n:
                vector.append(self.f[face].s-3)
            length=self.f[-1].s
            reducedVector=[]
            for i in range(length):
                if vector[i]!=2:
                    reducedVector.append(i)
            nanoType=[0,0]
            if reducedVector==[]:
                nanoType=[length,0]
            else:
                for i in range(len(reducedVector)):
                    nanoType[i%2]+=(reducedVector[i]-reducedVector[i-1])%length
                if nanoType[0]<nanoType[1]:
                    temp=nanoType[0]
                    nanoType[0]=nanoType[1]
                    nanoType[1]=temp
            self.nanoType=nanoType
                
            
    
    def show(self):
        print(self.f4,self.f5,self.f6,self.nb)
        print(self.boundary)
        for face in self.f:
            face.show()
        for vr in self.v:
            vr.show()

    def calculateOuterFaces(self):
        
        nbOuterFaces=self.nbOuterFaces
        boundary=self.boundary
        #print(boundary)
        firstOuter=len(self.f)
        self.outer=firstOuter+nbOuterFaces
        lastOuter=self.outer-1
        while len(boundary[0])<=1:
            aux=boundary[0]
            del(boundary[0])
            boundary.append(aux)
        
        realFace=boundary[0][0]
        self.f.append(Face(firstOuter,len(boundary[0])+3,[]))
        whereIs=whereIsLast(None,self.f[realFace].n)
        self.f[realFace].n[whereIs]=firstOuter
        self.f[firstOuter].n.append(realFace)
        for j in range(1,len(boundary[0])):
            realFace=boundary[0][j]
            whereIs=whereIsFirst(None,self.f[realFace].n)
            self.f[realFace].n[whereIs]=firstOuter
            self.f[firstOuter].n.insert(0,realFace)
        self.f[firstOuter].n.append(lastOuter)
        self.f[firstOuter].n.append(self.outer)
        self.f[firstOuter].n.insert(0,firstOuter+1)
        del(boundary[0])
        newOuter=firstOuter+1
        while len(boundary)>1:
            realFace=boundary[0][0]
            self.f.append(Face(newOuter,len(boundary[0])+3,[]))
            for j in range(len(boundary[0])):
                   realFace=boundary[0][j]
                   whereIs=whereIsFirst(None,self.f[realFace].n)
                   self.f[realFace].n[whereIs]=newOuter
                   self.f[newOuter].n.insert(0,realFace)
            self.f[newOuter].n.append(newOuter-1)
            self.f[newOuter].n.append(self.outer)
            self.f[newOuter].n.insert(0,newOuter+1)
            del(boundary[0])
            newOuter=newOuter+1
        realFace=boundary[0][0]
        self.f.append(Face(newOuter,len(boundary[0])+3,[]))
        for j in range(len(boundary[0])):
                   realFace=boundary[0][j]
                   whereIs=whereIsFirst(None,self.f[realFace].n)
                   self.f[realFace].n[whereIs]=newOuter
                   self.f[newOuter].n.insert(0,realFace)
        self.f[newOuter].n.append(newOuter-1)
        self.f[newOuter].n.append(self.outer)
        self.f[newOuter].n.insert(0,firstOuter)
        del(boundary[0])
        self.f.append(Face(self.outer,nbOuterFaces,[]))
        for i in range(firstOuter,self.outer):
            self.f[self.outer].n.insert(0,i)
            
    def calculateVertices(self):
        for face in self.f:
            face.w = [whereIsFirst(face.nb,self.f[face.n[i]].n)
                                for i in range(face.s)]
        cv=0 
        AllDone=False
        maxFaceNb=len(self.f)-1
        for face in self.f:
            face.a=[None for i in range(face.s)]
        for whichFace in range(len(self.f)):
         for where in range(self.f[whichFace].s):
          if self.f[whichFace].a[where]==None:
            self.v.append(Vertex(cv,[],[],[None,None,None]))
            vr=self.v[cv]
            secondFace=self.f[whichFace].n[where]
            thirdFace=self.f[whichFace].n[(where+1)%self.f[whichFace].s]
            vr.a=[whichFace,secondFace,thirdFace]
            self.f[whichFace].a[where]=cv
            self.f[secondFace].a[whereIsFirst(thirdFace,self.f[secondFace].n)]=cv
            self.f[thirdFace].a[whereIsFirst(whichFace,self.f[thirdFace].n)]=cv
            cv+=1
        for vr in self.f[-1].a:
            while self.v[vr].a[1]!=maxFaceNb:
                self.v[vr].a.append(self.v[vr].a.pop(0))
        for vr in self.v:
            for i in range(3):
                whichFace=vr.a[i]
                where=whereIsFirst(vr.nb,self.f[whichFace].a)
                vr.n.append(self.f[whichFace].a[(where+1)%self.f[whichFace].s])

        for vr in self.v:
            vr.w=[whereIsFirst(vr.nb,self.v[vr.n[i]].n) for i in range(3)]

        for face in self.f:
            face.sn=[self.f[face.n[i]].n[face.w[i]-2]
                 for i in range(face.s)]
        for face in self.f:
            face.sw=[whereIsFirst(face.n[(i+1)%face.s],self.f[face.sn[i]].n) for i in range(face.s)]
        
        L=[maxFaceNb]
        self.f[maxFaceNb].d=0
        while L!=[]:
            currentFace=self.f[L.pop(0)]
            for i in currentFace.n:
                if self.f[i].d==None:
                    L.append(i)
                    self.f[i].d=currentFace.d+1
        L=[]
        for i in self.f[maxFaceNb].a:
            self.v[i].d=0
            L.append(i)
        while L!=[]:
            currentVertex=self.v[L.pop(0)]
            for i in currentVertex.n:
                if self.v[i].d==None:
                    L.append(i)
                    self.v[i].d=currentVertex.d+1

    def startingEdges(self):
        maxFaceNb=len(self.f)-1
        startingEdges=[]
        astFaces=[]
        astFace=self.f[maxFaceNb-1]
        di = 0
        while astFace!=None:
            left=astFace.n[di]
            right=astFace.n[di+1]
            stE=[(astFace,di)]
            astF=[astFace.nb]
            while len(stE)<=1 or (astFace,di)!=stE[0]:
                if astFace.d==0:
                    while self.f[astFace.n[(di+1)%astFace.s]].s==6:
                        di+=1
                    di=di%astFace.s
                    stE.append((astFace,di))
                    (astFace,di)=(self.f[astFace.sn[di]],astFace.sw[di])
                    astF.append(astFace.nb)
                if astFace.d==1:
                    di+=1
                    while self.f[astFace.n[(di+1)%astFace.s]].d>0 and self.f[astFace.n[(di+1)%astFace.s]].s>4:
                        stE.append((astFace,di))
                        di+=1
                    di-=1
                    (astFace,di)=(self.f[astFace.sn[di]],astFace.sw[di])
                    astF.append(astFace.nb)
                elif astFace.d<=3:
                    while self.f[astFace.sn[di-1]].d<2:
                        di-=1
                        stE.append((self.f[astFace.sn[di]],astFace.sw[di]))
                    (astFace,di)=(self.f[astFace.sn[di]],astFace.sw[di])
                    astF.append(astFace.nb)
            del(stE[-1])
            del(astF[-1])
            startingEdges.append(stE)
            astFaces.append(astF)

            astFace=None
            maybeAstFace=self.f[maxFaceNb-1]
            while astFace==None and maybeAstFace.d==1:
                for dire in range(maybeAstFace.s):
                    if astFace==None:
                        if self.f[maybeAstFace.sn[dire]].d>1:
                            found=False
                            for stE in startingEdges:
                                if (maybeAstFace,dire) in stE:
                                    found=True
                            if not found:
                                astFace=maybeAstFace
                                di=dire
                maybeAstFace=self.f[maybeAstFace.nb-1]
        return startingEdges,astFaces

    def calculateTimesEdges(self,Qpaths):
        timesEdges=[]
        for Qpath in Qpaths:
          qpath=Qpath.timesFaces
          for i in range(1,len(qpath)):
            first=self.f[qpath[i-1]]
            second=self.f[qpath[i]]
            v1=Qpath.forVer[2*i-2]
            v2=Qpath.forVer[2*i-1]
            di=whereIsFirst(second.nb,first.sn)
            di2=whereIsLast(second.nb,first.sn)
            timesEdges.append((first.nb,v1,v2,second.nb))

        return timesEdges

    def calculateCircEdges(self):
        foundEdge=[[None for i in face.n] for face in self.f]
        maxFaceNb=len(self.f)-1
        circEdges=[]
        for face in self.f:
          if face.nb<maxFaceNb:  
           if face.label==CIRC:  
            for di in range(face.s):
              if face.n[di]<maxFaceNb:  
                if foundEdge[face.nb][di]==None:
                    if self.f[face.n[di]].label==AST:
                        foundEdge[face.nb][di]=False
                    elif self.f[face.n[di]].label==CIRC:
                        circEdges.append((face.nb,face.n[di],(face.a[di],face.a[di-1])))
                        foundEdge[face.n[di]][face.w[di]]=True
                    else: #the label is TIMES (cannot be None, it is excluded)
                        outer=False
                        whereTo=face.n[di]
                        dirFrom=face.w[di]
                        traversing=[(face.a[di],face.a[di-1])]
                        prev=face.nb
                        while self.f[whereTo].label!=CIRC and not outer:
                            if whereTo==maxFaceNb:
                                outer=True
                            dirFrom-=1
                            while self.f[self.f[whereTo].n[dirFrom]].label==AST or self.f[self.f[whereTo].n[dirFrom]].label==None:
                                dirFrom-=1
                            traversing.append((self.f[whereTo].a[dirFrom],self.f[whereTo].a[(dirFrom-1)%self.f[whereTo].s]))
                            (prev,whereTo,dirFrom)=(whereTo,self.f[whereTo].n[dirFrom],self.f[whereTo].w[dirFrom])
                            if traversing[-1][0]==traversing[-2][1] and traversing[-1][1]==traversing[-2][0]:
                                outer=True
                        foundEdge[whereTo][dirFrom]=True
                        if not outer:
                            circEdges.append((face.nb,whereTo)+tuple(traversing))
                        else:
                            circEdges.append((face.nb,prev)+tuple(traversing[:-1]))
        hasEvolved=True
        while hasEvolved:
            hasEvolved=False
            for circEdge in circEdges:
                if not hasEvolved and ((self.f[circEdge[1]].label!=CIRC and self.f[circEdge[1]].d>1) or (
                    self.f[circEdge[0]].label!=CIRC and self.f[circEdge[0]].d>1)):
                    hasEvolved=True
                    if self.f[circEdge[1]].label!=CIRC:                                       
                        erasedCirc=circEdge[0]
                    elif self.f[circEdge[0]].label!=CIRC:
                        erasedCirc=circEdge[1]
                    if self.f[erasedCirc].label!=CIRC:
                        return []
                    else:
                        self.f[erasedCirc].label=TIMES
                    containErasedCirc=[]
                    for otherCircEdge in circEdges:
                        if erasedCirc in otherCircEdge and otherCircEdge!=circEdge:
                            containErasedCirc.append(otherCircEdge)
                    foundFirst=False
                    if len(containErasedCirc)==2:
                        newCircEdge=[]
                        for otherCircEdge in containErasedCirc:
                          if not foundFirst:  
                            if otherCircEdge[0]==erasedCirc:
                                foundFirst=True
                                newCircEdge.append(otherCircEdge[1])
                                newCircEdge+=list(reversed(otherCircEdge[2:]))
                                firstToRemove=otherCircEdge
                            elif otherCircEdge[1]==erasedCirc:
                                foundFirst=True
                                newCircEdge.append(otherCircEdge[0])
                                newCircEdge+=list(otherCircEdge[2:])
                                firstToRemove=otherCircEdge
                          else:
                            if otherCircEdge[0]==erasedCirc:
                                foundSecond=True
                                newCircEdge.insert(1,otherCircEdge[1])
                                newCircEdge+=list(otherCircEdge[2:])
                                secondToRemove=otherCircEdge
                            elif otherCircEdge[1]==erasedCirc:
                                foundSecond=True
                                newCircEdge.insert(1,otherCircEdge[0])
                                newCircEdge+=list(reversed(otherCircEdge[2:]))
                                secondToRemove=otherCircEdge
                        circEdges.remove(circEdge)
                        circEdges.remove(firstToRemove)
                        circEdges.remove(secondToRemove)
                        circEdges.append(tuple(newCircEdge))
                    elif len(containErasedCirc)==1:
                        circEdges.remove(circEdge)
        return circEdges

    def isTriangle(self,circEdges):
        adj={}
        for face in self.f:
            if face.label==CIRC:
                adj[face.nb]=[]
        for edge in circEdges:
            if self.f[edge[0]].label==CIRC and self.f[edge[1]].label==CIRC:
                if edge[0]==edge[1]:
                    return -1
                else:
                    adj[edge[0]].append(edge[1])
                    adj[edge[1]].append(edge[0])
        for f in adj:
            for n1 in adj[f]:
                if adj[f].count(n1)>1:
                    return 2
                for n2 in adj[f]:
                    if n1!=n2:
                        if n1 in adj[n2]:
                            if n1 in self.f[f].n and n2 in self.f[f].n and n1 in self.f[n2].n:
                                return -3
        for f in adj:
            for n1 in adj[f]:
                if adj[f].count(n1)>1:
                    return 2
                for n2 in adj[f]:
                    if n1!=n2:
                        if n1 in adj[n2]:
                            if n1 in self.f[f].n and n2 in self.f[f].n and n1 in self.f[n2].n:
                                return -3
                            else:
                                return 3
        return 4
                        
    def completeLabels(self,astFaces,timesFaces,Qpaths):
        maxFaceNb=len(self.f)-1
        NbOuterFaces=self.f[maxFaceNb].s
        for face in self.f:
            face.label=None
        circFaces=[]
        for nb in self.f[maxFaceNb].n:
            if True not in [nb in x for x in astFaces] and True not in [nb in x for x in timesFaces]:
                circFaces.append(nb)
        astFaces.append([])
        for nb in range(maxFaceNb-NbOuterFaces,-1,-1):
            if True not in [nb in x for x in astFaces] and True not in [nb in x for x in timesFaces]:
                if [i for i in self.f[nb].n if True in [i in x for x in astFaces]]==[
                    ] and [i for i in self.f[nb].sn if True in [i in x for x in astFaces]]!=[]:
                    astFaces[-1].append(nb)
                elif [i for i in self.f[nb].n if True in [i in x for x in astFaces]]!=[]:
                    circFaces.append(nb)
                else:
                    if self.f[nb].s==4:
                        circFaces.append(nb)
                    else:
                        return False
        for x in astFaces:
            for faceNb in x:
                self.f[faceNb].label=AST
        for qpath in timesFaces:
            for faceNb in qpath:
                self.f[faceNb].label=TIMES
        for faceNb in circFaces:
            self.f[faceNb].label=CIRC
        k=0
        for faceNb in range(len(self.f)-1):
            if self.f[faceNb].label==AST:
                for nei in self.f[faceNb].n:
                  if nei<len(self.f)-1  :
                    if self.f[nei].label==AST:
                        k+=1
        self.f[-1].label=None
        l=0
        for qpath in Qpaths:
                l+=max(0,len(qpath.timesFaces)-1)
        if k//2!=l:
            return False
        for ver in self.v:
            if len(self.f)-1 not in ver.a:
             if len([1 for inc in ver.a if self.f[inc].label!=AST])==3:
                 return False
        return True

    def drawBadCase(self):
        for face in self.f:
            face.label=None
        for face in self.initialAstFaces:
            self.f[face].label=AST            
        self.drawFigure([],[],0,[])
        
    def drawFigure(self,timesEdges,circEdges,parity,Qpaths):
        global figNb
        global patchNb
        maxFaceNb=len(self.f)-1
        output=str(self.f4)+'.'+str(self.f5)+'.'+str(self.f6)+'.'+str(patchNb)
        metapostFile=open("./output/"+output+'.mp','a')
        metapostFile.write("beginfig("+str(0*parity+figNb)+")\n")
        if circEdges==[]:
            print('drawing bad case',figNb)
        for face in self.f[:-1]:
            if face.label==AST:
                metapostFile.write("fill ")
                for v in face.a:
                    metapostFile.write("v"+str(v)+"--")
                metapostFile.write("cycle withcolor "+str(0.85)+"white;\n")        
        metapostFile.write("draw underlyingGraph withcolor .5white;\n")
        metapostFile.write("pickup pencircle scaled .3mm;\n");
        for (f1,v1,v2,f2) in timesEdges:
            if f1<maxFaceNb and f2<maxFaceNb:
                metapostFile.write("draw f"+str(f1)+"..v"+str(v1)+"..v"+str(v2)+"..f"+str(f2)+"dashed withdots scaled .5;\n")
            elif f1==maxFaceNb:
                metapostFile.write("draw v"+str(v1)+"..v"+str(v2)+"..f"+str(f2)+"dashed withdots scaled .5;\n")
            elif f2==maxFaceNb:
                metapostFile.write("draw f"+str(f1)+"..v"+str(v1)+"..v"+str(v2)+"dashed withdots scaled .5;\n")
        for edge in circEdges:
            f1=edge[0]
            f2=edge[1]
            metapostFile.write("draw f"+str(edge[0]))
            for pair in edge[2:]:
                metapostFile.write("..1/2[v"+str(pair[0])+",v"+str(pair[1])+"]")
            metapostFile.write("..f"+str(edge[1])+";\n")

        for face in self.f:
            if face.label==CIRC:
                metapostFile.write("draw circ shifted f"+str(face.nb)+";\n");
        metapostFile.write("endfig;\n")
        metapostFile.close()
        texFile=open("./output/"+output+'.tex','a')
        texFile.write("\\includegraphics{"+output+"."+str(0*parity+figNb)+"}\n")
        #print('writing down figure',figNb)
        texFile.close()
        figNb+=1

    def setMetapostDefinitions(self):
        meta="u:=10mm;\n"
        meta+="draw (0,0) withpen pencircle scaled (2pt+.6mm);\n"
        meta+="undraw (0,0) withpen pencircle scaled 2pt;\n"
        meta+="picture circ;\n"
        meta+="circ:=currentpicture;\n"
        meta+="currentpicture:=blankpicture;\n"
        maxFaceNb=len(self.f)-1
        nbOuterFaces=self.f[maxFaceNb].s
        meta+="pair v[];\n"
        for i in range(nbOuterFaces):
            meta+="v"+str(self.f[maxFaceNb].a[i])+"=(0,"+str(self.c)+"u/2) rotated ("+str(i)+"*360/"+str(nbOuterFaces)+");\n"
        for i in range(len(self.v)-1,-1,-1):
            if i not in self.f[maxFaceNb].a:
                vr=self.v[i]
                n0=self.v[vr.n[0]]
                n1=self.v[vr.n[1]]
                n2=self.v[vr.n[2]]
                f0=self.f[vr.a[0]]
                f1=self.f[vr.a[1]]
                f2=self.f[vr.a[2]]
                c0=0
                c1=0
                c2=0
                if vr.d>4:
                    cc=2
                    c0=(f0.s-6+f2.s-6)/cc
                    c1=(f1.s-6+f0.s-6)/cc
                    c2=(f2.s-6+f1.s-6)/cc
                corr=1.5*(-2+max(2,vr.d))
                meta+=str(2*(n0.d+n1.d+n2.d)-3*corr+c0+c1+c2)+"v"+str(vr.nb)+"="
                meta+=str(n1.d+n2.d-corr+c0)+"v"+str(n0.nb)+"+"
                meta+=str(n0.d+n2.d-corr+c1)+"v"+str(n1.nb)+"+"
                meta+=str(n0.d+n1.d-corr+c2)+"v"+str(n2.nb)+";\n"
        meta+="pair f[];\n"
        for face in self.f:
            meta+=str(face.s)+"f"+str(face.nb)+"=v"+str(face.a[0])
            for i in range(1,face.s):
                meta+="+v"+str(face.a[i])
            meta+=";\n"
        meta+="pickup pencircle scaled .3mm;\n"
        for i in range(len(self.v)-1,-1,-1):
            if i not in self.f[maxFaceNb].a:
                vr=self.v[i]
                for ii in range(3):
                    ni=self.v[vr.n[ii]]
                    if ni.nb>vr.nb:
                        meta+="draw v"+str(vr.nb)+"--v"+str(ni.nb)+";\n"
        meta+="pickup pencircle scaled 2pt;\n"
        realVertices=[vr.nb for vr in self.v if vr.nb not in self.f[maxFaceNb].a]
        meta+="for i:="+str(realVertices[0])
        for nb in realVertices[1:]:
            meta+=","+str(nb)
        meta+=": draw v[i]; endfor \n"
        meta+="picture underlyingGraph;\n"
        meta+="underlyingGraph:=currentpicture;\n"
        self.meta=meta

    def setInitialAstFacesOneActiveSegment(self,face,di,aroundFaces):
        astFaces=[]
        leftNb=face.n[di]
        rightNb=face.n[(di+1)%face.s]
        leftIndex=aroundFaces.index(leftNb)
        rightIndex=aroundFaces.index(rightNb)
        if rightIndex<leftIndex:
            for i in range(rightIndex,leftIndex+1):
                astFaces.append(aroundFaces[i])
        else:
            for i in range(rightIndex,len(aroundFaces)):
                astFaces.append(aroundFaces[i])
                
            for i in range(0,leftIndex+1):
                astFaces.append(aroundFaces[i])
        if len(self.f)-1 in astFaces:
            astFaces.remove(len(self.f)-1)
        self.initialAstFaces=astFaces

    def setOddInitialAstFacesOneActiveSegment(self,face,di,aroundFaces):
        astFaces=[]
        leftNb=face.n[di]
        rightNb=face.n[(di+1)%face.s]
        leftIndex=aroundFaces.index(leftNb)
        rightIndex=aroundFaces.index(rightNb)
        if rightIndex<leftIndex:
            for i in range(rightIndex,leftIndex+1):
                astFaces.append(aroundFaces[i])
        else:
            for i in range(rightIndex,len(aroundFaces)):
                astFaces.append(aroundFaces[i])
                
            for i in range(0,leftIndex+1):
                astFaces.append(aroundFaces[i])
        if len(self.f)-1 in astFaces:
            astFaces.remove(len(self.f)-1)
        self.initialAstFaces=astFaces

    def setInitialAstFacesTwoActiveSegments(self,inFace,inDi,outFace,outDi,aroundFaces):
        astFaces=[]
        inLeftNb=inFace.n[inDi]
        inRightNb=inFace.n[(inDi+1)%inFace.s]
        inLeftIndex=aroundFaces.index(inLeftNb)
        inRightIndex=aroundFaces.index(inRightNb)
        outLeftNb=outFace.n[outDi]
        outRightNb=outFace.n[(outDi+1)%outFace.s]
        outLeftIndex=aroundFaces.index(outLeftNb)
        outRightIndex=aroundFaces.index(outRightNb)
        if inRightIndex<=outLeftIndex and (outLeftIndex-inRightIndex)<len(aroundFaces)//2:
            for i in range(inRightIndex,outLeftIndex+1):
                astFaces.append(aroundFaces[i])
        else:
            for i in range(inRightIndex,len(aroundFaces)):
                astFaces.append(aroundFaces[i])
                
            for i in range(0,outLeftIndex+1):
                astFaces.append(aroundFaces[i])
        if outRightIndex<=inLeftIndex and (inLeftIndex-outRightIndex)<len(aroundFaces)//2:
            for i in range(outRightIndex,inLeftIndex+1):
                astFaces.append(aroundFaces[i])
        else:
            for i in range(outRightIndex,len(aroundFaces)):
                astFaces.append(aroundFaces[i])
                
            for i in range(0,inLeftIndex+1):
                astFaces.append(aroundFaces[i])
        while len(self.f)-1 in astFaces:
            astFaces.remove(len(self.f)-1)
        self.initialAstFaces=astFaces

    def setInitialAstFacesTwoActiveAccordedSegments(self,inFace,inDi,outFace,outDi,aroundFaces):
        astFaces=[]
        inLeftNb=inFace.n[inDi]
        inRightNb=inFace.n[(inDi+1)%inFace.s]
        outLeftNb=outFace.n[outDi]
        outRightNb=outFace.n[(outDi+1)%outFace.s]
        for ii in range(3):
            if inRightNb in aroundFaces[ii]:
                inRightIndex=aroundFaces[ii].index(inRightNb)
                outLeftIndex=aroundFaces[ii].index(outLeftNb)
                if inRightIndex<=outLeftIndex:
                    astFaces+=aroundFaces[ii][inRightIndex:outLeftIndex+1]
                
                else:
                    astFaces+=aroundFaces[ii][inRightIndex:]
                    astFaces+=aroundFaces[ii][:outLeftIndex+1]
            
            if outRightNb in aroundFaces[ii]:
                outRightIndex=aroundFaces[ii].index(outRightNb)
                inLeftIndex=aroundFaces[ii].index(inLeftNb)
                if outRightIndex<=inLeftIndex:
                    astFaces+=aroundFaces[ii][outRightIndex:inLeftIndex+1]
                else:
                    astFaces+=aroundFaces[ii][outRightIndex:]
                    astFaces+=aroundFaces[ii][:inLeftIndex+1]
                
        if len(self.f)-1 in astFaces:
            astFaces.remove(len(self.f)-1)
        self.initialAstFaces=astFaces

    def setOddInitialAstFacesTwoActiveSegments(self,inFace,inDi,outFace,outDi,aroundFaces):
        astFaces=[]
        inLeftNb=inFace.n[inDi]
        inRightNb=inFace.n[(inDi+1)%inFace.s]
        outLeftNb=outFace.n[outDi]
        outRightNb=outFace.n[(outDi+1)%outFace.s]
        for i in range(2):
            if inLeftNb in aroundFaces[i]:
                inLeftIndex=aroundFaces[i].index(inLeftNb)
                outRightIndex=aroundFaces[i].index(outRightNb)
                if outRightIndex<=inLeftIndex:
                    astFaces+=aroundFaces[i][outRightIndex:inLeftIndex+1]
                else:
                    astFaces+=aroundFaces[i][outRightIndex:]+aroundFaces[i][:inLeftIndex+1]
            if inRightNb in aroundFaces[i]:
                outLeftIndex=aroundFaces[i].index(outLeftNb)
                inRightIndex=aroundFaces[i].index(inRightNb)
                if inRightIndex<=outLeftIndex:
                    astFaces+=aroundFaces[i][inRightIndex:outLeftIndex+1]
                else:
                    astFaces+=aroundFaces[i][inRightIndex:]+aroundFaces[i][:outLeftIndex+1]
        self.initialAstFaces=astFaces

        
    def searchFrom(self,initialDirections):

        maxFaceNb=len(self.f)-1
        L=[(0,mode,[],face,di,[],[face.nb],[],targets) for (mode,face,di,targets) in initialDirections]
        #0 : total number of times edges
        #mode : 0 for inner, 1 for one active segment, 2 for two active segments, -1 for parity switching cycle
        #Qpaths : definitive qpaths
        #face : starting face
        #di : starting direction of the next timesEdge
        #forVer : actual vertices passed by the actual xPath
        #xFaces : actual xFaces
        #astFaces : actual astFaces
        #targets: possible ends of the xFace
        ## if mode = 0 then some pentagons
        ## if mode = 1 then some pentagons
        ## if mode = 2 then some pentagons plus a hexagon last but one
        ## if mode = -1 then a single face of whichever size
        global figNb
        while L!=[] and not self.success==[True,True]:
          (nbTimesEdges,mode,Qpaths,face,di,forVer,xFaces,astFaces,targets)=L.pop(0)
          newface=self.f[face.sn[di]]
          if True:
            incoming=face.sw[di]
            newpa=incoming%2
            v1=face.a[di]
            v2=newface.a[incoming]
            f1=face.n[di]
            f2=newface.n[incoming]
            if newface.nb<maxFaceNb:
              if newface.nb not in self.initialAstFaces and newface.nb not in astFaces and True not in [newface.nb in qpath.astFaces for qpath in Qpaths]:
               if v1 not in forVer and True not in [v1 in qpath.forVer for qpath in Qpaths] and v2 not in forVer and True not in [v2 in qpath.forVer for qpath in Qpaths]:
                if f1 not in xFaces and True not in [f1 in qpath.timesFaces for qpath in Qpaths] and f2 not in xFaces and True not in [f2 in qpath.timesFaces for qpath in Qpaths]:
                 if (newface.nb not in xFaces and True not in [newface.nb in qpath.timesFaces for qpath in Qpaths]) or newface.nb in targets:
                    if newface.nb in targets:
                        #create new Qpath
                        newqpath=qpath(xFaces+[newface.nb],astFaces+[f1,f2],forVer+[v1,v2])
                        newMode=None
                        works=True
                        if newqpath.timesFaces[0]==newqpath.timesFaces[-1]:
                            if len(newqpath.timesFaces)==4:
                                works=False
                        elif self.outSegment!=(None,None) and newface.nb not in self.pentagons:
                            (outFace,outDi)=self.outSegment
                            (inFace,inDi)=self.inSegment
                            
                            if outFace.sn[outDi]==newface.nb and newqpath.timesFaces[0]==inFace.nb:
                                whereIs=outFace.sw[outDi]
                                vbis1=newface.a[whereIs]
                                vbis2=outFace.a[outDi]
                                fbis1=newface.n[whereIs]
                                fbis2=outFace.n[outDi]
                                newqpath.timesFaces.append(outFace.nb)
                                newqpath.astFaces+=[fbis1,fbis2]
                                newqpath.forVer+=[vbis1,vbis2]
                            elif inFace.sn[inDi]==newface.nb and newqpath.timesFaces[0]==outFace.nb:  
                                whereIs=inFace.sw[inDi]
                                vbis1=newface.a[whereIs]
                                vbis2=inFace.a[inDi]
                                fbis1=newface.n[whereIs]
                                fbis2=inFace.n[inDi]
                                newqpath.timesFaces.append(inFace.nb)
                                newqpath.astFaces+=[fbis1,fbis2]
                                newqpath.forVer+=[vbis1,vbis2]                        
                            else:
                                works=False
                        if works:
                            nbTimesEdges+=1
                            newMode=0
                            if mode==2 and newface.nb in self.pentagons :
                                newMode=1
                            newQpaths=Qpaths+[newqpath]
                            self.completeSolution(newQpaths)

                            if newMode==1:
                                newStart=None
                                newTargets=self.findFreePentagons(newQpaths)
                                (outFace,outDi)=self.outSegment
                                (inFace,inDi)=self.inSegment
                                if newqpath.timesFaces[0:2]==[outFace.nb,outFace.sn[outDi]]:
                                    newStart=(nbTimesEdges+1,1,newQpaths,inFace,inDi,[],[inFace.nb],[],newTargets)
                                elif newqpath.timesFaces[0:2]==[inFace.nb,inFace.sn[inDi]]:
                                    newStart=(nbTimesEdges+1,1,newQpaths,outFace,outDi,[],[outFace.nb],[],newTargets)
                                L.insert(0,newStart)
                            else:
                                newInitialDirections=self.callForNewInitialDirections(newQpaths)

                                for (Mode,Face,Di,Targets) in newInitialDirections:
                                    newStart=(nbTimesEdges+1,Mode,newQpaths,Face,Di,[],[Face.nb],[],Targets)
                                    if Targets!=[]:
                                        L.insert(0,newStart)
                    elif newface.s==6:
                        for i in [3,1,5]:
                          if self.f[newface.sn[incoming-i]].d>2 or (self.f[newface.sn[incoming-i]].d>1 and (self.c<=5 or self.f6<28+2*self.c)) or newface.sn[incoming-i] in targets:
                            L.append((nbTimesEdges+1,mode,Qpaths,newface,incoming-i,forVer+[v1,v2],xFaces+[newface.nb],astFaces+[f1,f2],targets))
                    elif newface.s==4:
                        for i in [3,1]:
                          if self.f[newface.sn[incoming-i]].d>1 or newface.sn[incoming-i] in targets:
                            L.append((nbTimesEdges+1,mode,Qpaths,newface,incoming-i,forVer+[v1,v2],xFaces+[newface.nb],astFaces+[f1,f2],targets))
                    elif newface.d==1:
                        for i in [1,-1]:
                          if newface.n[(incoming+i)%newface.s]!=maxFaceNb:
                           if newface.n[(incoming+i+1)%newface.s]!=maxFaceNb:
                            L.append((nbTimesEdges+1,mode,Qpaths,newface,(incoming+i)%newface.s,forVer+[v1,v2],xFaces+[newface.nb],astFaces+[f1,f2],targets))
                 elif True in [newface.nb in qpath.timesFaces for qpath in Qpaths] and newface.d>=2:
                     existingTimesEdges=self.existingTimesEdges(newface,Qpaths)
                     if len(existingTimesEdges)==newface.s-4:
                         if newface.s==5:
                             existing=existingTimesEdges[0]
                             new=[]
                             if (incoming-existing)%5==2:
                                 new.append((incoming-1)%5)
                             elif (incoming-existing)%5==3:
                                 new.append((incoming+1)%5)
                             elif (incoming-existing)%5==1:
                                 new.append((incoming+1)%5)
                                 new.append((incoming+3)%5)
                             elif (incoming-existing)%5==4:
                                 new.append((incoming-1)%5)
                                 new.append((incoming-3)%5)
                             for i in new:
                               if self.f[newface.sn[i]].d>1 or newface.sn[incoming-i] in targets:
                                 L.append((nbTimesEdges+1,mode,Qpaths,newface,i,forVer+[v1,v2],xFaces+[newface.nb],astFaces+[f1,f2],targets))
                         elif newface.s==6:
                             new=[]
                             if (existingTimesEdges[0]-existingTimesEdges[1])%6==3:
                                 for i in [-1,1]:
                                     if (incoming-i)%6 not in existingTimesEdges:
                                         new.append((incoming-i)%6)
                             else:
                                for i in [1,3,5]:
                                  if self.f[newface.sn[incoming-i]].d>1 or newface.sn[incoming-i] in targets:
                                    if (incoming-i)%6 not in existingTimesEdges:
                                        new.append((incoming-i)%6)
                             for i in new:
                               if self.f[newface.sn[i]].d>1 or newface.sn[incoming-i] in targets:
                                 L.append((nbTimesEdges+1,mode,Qpaths,newface,i,forVer+[v1,v2],xFaces+[newface.nb],astFaces+[f1,f2],targets))
                             
    def findFreePentagons(self,Qpaths):
        freePentagons=[]
        for p in self.pentagons:
            isFree=True
            for path in Qpaths:
                if p in path.astFaces:
                    isFree=False
                if p in path.timesFaces:
                    isFree=False
            if isFree:
                freePentagons.append(p)
        return freePentagons
                                    
    def existingTimesEdges(self,face,Qpaths):
        timesEdges=[]
        for qpath in Qpaths:
            for i in range(len(qpath.timesFaces)):
                if qpath.timesFaces[i]==face.nb:
                    if i>0:
                        timesEdges.append(whereIsFirst(qpath.timesFaces[i-1],face.sn))
                    if i<len(qpath.timesFaces)-1:
                        timesEdges.append(whereIsFirst(qpath.timesFaces[i+1],face.sn))
        return timesEdges

    def isTooComplicated(self,Qpaths):
        for face in self.f:
          if face.label==AST:  
            labels=[]
            for nei in face.n:
                labels.append(self.f[nei].label)
            if labels==[TIMES,AST,TIMES,AST,TIMES,AST]:
                trigon=[face.n[0],face.n[2],face.n[4]]
                found=False
                for qpath in Qpaths:
                    isin=True
                    for tr in trigon:
                        if tr not in qpath.timesFaces:
                            isin=False
                    if isin:
                        found=True
                if not found:
                    return True
            elif labels==[AST,TIMES,AST,TIMES,AST,TIMES]:
                trigon=[face.n[1],face.n[3],face.n[5]]
                found=False
                for qpath in Qpaths:
                    isin=True
                    for tr in trigon:
                        if tr not in qpath.timesFaces:
                            isin=False
                    if isin:
                        found=True
                if not found:
                    return True
        return False

    def removeComplicatedTriangles(self):
        for face in self.f:
          if face.label==AST:  
            labels=[]
            for nei in face.n:
                labels.append(self.f[nei].label)
            if labels==[TIMES,AST,TIMES,AST,TIMES,AST]:
                face.label=CIRC
            elif labels==[AST,TIMES,AST,TIMES,AST,TIMES]:
                face.label=CIRC
        

    def eliminate2vertices(self,circEdges):
        for face in self.f:
            if face.s==4 and face.d>1 and face.label==CIRC:
                #find the two incident circEdges and join them
                erasedCirc=face.nb
                face.label=TIMES
                containErasedCirc=[]
                for edge in circEdges:
                        if erasedCirc in edge:
                            containErasedCirc.append(edge)
                foundFirst=False
                if len(containErasedCirc)==2:
                        newCircEdge=[]
                        for otherCircEdge in containErasedCirc:
                          if not foundFirst:  
                            if otherCircEdge[0]==erasedCirc:
                                foundFirst=True
                                newCircEdge.append(otherCircEdge[1])
                                newCircEdge+=list(reversed(otherCircEdge[2:]))
                                firstToRemove=otherCircEdge
                            elif otherCircEdge[1]==erasedCirc:
                                foundFirst=True
                                newCircEdge.append(otherCircEdge[0])
                                newCircEdge+=list(otherCircEdge[2:])
                                firstToRemove=otherCircEdge
                          else:
                            if otherCircEdge[0]==erasedCirc:
                                foundSecond=True
                                newCircEdge.insert(1,otherCircEdge[1])
                                newCircEdge+=list(otherCircEdge[2:])
                                secondToRemove=otherCircEdge
                            elif otherCircEdge[1]==erasedCirc:
                                foundSecond=True
                                newCircEdge.insert(1,otherCircEdge[0])
                                newCircEdge+=list(reversed(otherCircEdge[2:]))
                                secondToRemove=otherCircEdge
                        circEdges.remove(firstToRemove)
                        circEdges.remove(secondToRemove)
                        circEdges.append(tuple(newCircEdge))
        return circEdges
    def dfs(self,face,resFaceNb):
        for nei in face.n:
            if self.f[nei].label==AST:
                if self.f[nei].resFace==-1:
                    self.f[nei].resFace=resFaceNb
                    self.f[nei].father=face.nb
                    self.dfs(self.f[nei],resFaceNb)
                elif self.f[nei].resFace!=resFaceNb:
                    self.isWrong=True
                    return
                elif self.f[nei].resFace==resFaceNb:
                    if nei!=face.father:
                        self.isWrong=True
                        return   
        
    def calculateResidualFaces(self):
        self.isWrong=False
        for face in self.f:
            face.resFace=-1
        resFaceNb=0
        for face in self.f:
            if face.label==AST:
                if face.resFace==-1:
                    if not self.isWrong:
                        face.resFace=resFaceNb
                        face.father=None
                        self.dfs(face,resFaceNb)
                    resFaceNb+=1
        if not self.isWrong:
            for ver in self.v:
                ver.resFace=-1
            for face in self.f:
                if face.label==AST:
                    for ver in face.a:
                        self.v[ver].resFace=face.resFace
            newResFaceNb=-2
            peri=self.f[-1].s
            for i in range(peri):
                ver=self.f[-1].a[i]
                if self.v[ver].resFace==-1:
                    prec=self.f[-1].a[i-1]
                    succ=self.f[-1].a[(i+1)%peri]
                    precFace=self.f[self.v[ver].a[2]]
                    succFace=self.f[self.v[ver].a[0]]
                    if self.v[prec].resFace!=-1 and (precFace.s==6 or (precFace.s==5 and ((self.inSegment[0]==precFace or self.outSegment[0]==precFace) and not (self.inSegment[0]==precFace and self.outSegment[0]==precFace)))):
                        self.v[ver].resFace=self.v[prec].resFace
                    elif self.v[succ].resFace!=-1 and (succFace.s==6 or (succFace.s==5 and ((self.inSegment[0]==succFace or self.outSegment[0]==succFace) and not (self.inSegment[0]==succFace and self.outSegment[0]==succFace)))):
                        self.v[ver].resFace=self.v[succ].resFace
                    else:
                        self.v[ver].resFace=newResFaceNb
                        newResFaceNb-=1
            first = self.f[-1].a[0]
            last = self.f[-1].a[-1]
            precFace=self.f[self.f[-1].n[0]]
            firstResFace = self.v[first].resFace
            lastResFace = self.v[last].resFace
            if precFace.s==6 or (precFace.s==5 and ((self.inSegment[0]==precFace or self.outSegment[0]==precFace) and not (self.inSegment[0]==precFace and self.outSegment[0]==precFace))):
               if firstResFace <-1:
                   if lastResFace <-1:
                       if firstResFace != lastResFace:
                           for ver in self.v:
                               if ver.resFace==lastResFace:
                                   ver.resFace=firstResFace

    def calculateResidualAdjacencies(self):
        direction=None
        length=self.f[-1].s
        self.resGraphFaces={}
        for ver in self.v:
            if ver.resFace>-1:
                if ver.resFace not in self.resGraphFaces:
                    self.resGraphFaces[ver.resFace]=[]
                    first=ver.nb
                    whereTo=0
                    #find the edge that is boundary of a residual face
                    while not (self.f[ver.a[whereTo]].label==AST and self.f[ver.a[whereTo-1]].label!=AST):
                        whereTo+=1
                    loop=True
                    while ver.nb!=first or loop:
                        loop=False
                        #if there is a outgoing edge, look at the resFAce
                        if self.f[ver.a[whereTo-2]].label!=AST:
                            other=self.v[ver.n[whereTo-1]].resFace
                            if other!=ver.resFace:
                                if self.resGraphFaces[ver.resFace]==[]:
                                    self.resGraphFaces[ver.resFace].append(other)
                                elif other!=self.resGraphFaces[ver.resFace][-1]:
                                    self.resGraphFaces[ver.resFace].append(other)
                            elif ver.d==0 and self.v[ver.n[whereTo-1]].d==0:
                                whereIs = whereIsFirst(ver.nb,self.f[-1].a)
                                whereIsOther = whereIsFirst(ver.n[whereTo-1],self.f[-1].a)

                                if (whereIsOther-whereIs)%length == 1:
                                    direction = 1
                                else:
                                    direction = -1
                                if direction==1:    
                                    whereIs+=direction
                                    whereIs=whereIs%length
                                    newOther = self.v[self.v[self.f[-1].a[whereIs]].n[0]].resFace
                                    while self.v[self.f[-1].a[whereIs]].resFace==ver.resFace and newOther!=ver.resFace:
                                        if self.resGraphFaces[ver.resFace]==[]:
                                            self.resGraphFaces[ver.resFace].append(newOther)
                                        elif newOther!=self.resGraphFaces[ver.resFace][-1]:
                                            self.resGraphFaces[ver.resFace].append(newOther)
                                        whereIs+=direction
                                        whereIs=whereIs%length
                                        newOther = self.v[self.v[self.f[-1].a[whereIs]].n[0]].resFace
                                    newOther = self.v[self.f[-1].a[whereIs]].resFace
                                    if newOther!=ver.resFace:
                                        if self.resGraphFaces[ver.resFace]==[]:
                                            self.resGraphFaces[ver.resFace].append(newOther)
                                        elif newOther!=self.resGraphFaces[ver.resFace][-1]:
                                            self.resGraphFaces[ver.resFace].append(newOther)
                                else:
                                    oldWhereIs=whereIs
                                    whereIs+=direction
                                    whereIs=whereIs%length
                                    newOther = self.v[self.v[self.f[-1].a[whereIs]].n[0]].resFace
                                    while self.v[self.f[-1].a[whereIs]].resFace==ver.resFace and newOther!=ver.resFace:
                                        whereIs+=direction
                                        whereIs=whereIs%length
                                        newOther = self.v[self.v[self.f[-1].a[whereIs]].n[0]].resFace
                                    newOther = self.v[self.f[-1].a[whereIs]].resFace
                                    if newOther!=ver.resFace:
                                        if self.resGraphFaces[ver.resFace]==[]:
                                            self.resGraphFaces[ver.resFace].append(newOther)
                                        elif newOther!=self.resGraphFaces[ver.resFace][-1]:
                                            self.resGraphFaces[ver.resFace].append(newOther)
                                    whereIs-=direction
                                    whereIs=whereIs%length
                                    while whereIs!=oldWhereIs:
                                        newOther = self.v[self.v[self.f[-1].a[whereIs]].n[0]].resFace
                                        if self.resGraphFaces[ver.resFace]==[]:
                                            self.resGraphFaces[ver.resFace].append(newOther)
                                        elif newOther!=self.resGraphFaces[ver.resFace][-1]:
                                            self.resGraphFaces[ver.resFace].append(newOther)
                                        whereIs-=direction
                                        whereIs=whereIs%length
                                        
                        if ver.d==0 and self.v[ver.n[whereTo]].d==0:
                            if self.resGraphFaces[ver.resFace]==[] or self.resGraphFaces[ver.resFace][-1]!=-1:
                                self.resGraphFaces[ver.resFace].append(-1)
                        ver=self.v[ver.n[whereTo]]
                        whereTo=0
                        while not (self.f[ver.a[whereTo]].label==AST and self.f[ver.a[whereTo-1]].label!=AST):
                            whereTo+=1
            elif ver.resFace<-1:
                if ver.resFace not in self.resGraphFaces:
                    self.resGraphFaces[ver.resFace]=[]
                    whereIs = whereIsFirst(ver.nb,self.f[-1].a)
                    while self.v[self.f[-1].a[whereIs-1]].resFace ==  ver.resFace:
                        whereIs-=1
                    newOther = self.v[self.f[-1].a[whereIs-1]].resFace
                    if newOther!=ver.resFace:
                        if self.resGraphFaces[ver.resFace]==[]:
                            self.resGraphFaces[ver.resFace].append(newOther)
                        elif newOther!=self.resGraphFaces[ver.resFace][-1]:
                            self.resGraphFaces[ver.resFace].append(newOther)
                    newOther = self.v[self.v[self.f[-1].a[whereIs]].n[0]].resFace
                    while self.v[self.f[-1].a[whereIs]].resFace==ver.resFace and newOther!=ver.resFace:
                        if self.resGraphFaces[ver.resFace]==[]:
                            self.resGraphFaces[ver.resFace].append(newOther)
                        elif newOther!=self.resGraphFaces[ver.resFace][-1]:
                            self.resGraphFaces[ver.resFace].append(newOther)
                        whereIs+=1
                        whereIs=whereIs%length
                        newOther = self.v[self.v[self.f[-1].a[whereIs]].n[0]].resFace
                    newOther = self.v[self.f[-1].a[whereIs]].resFace
                    if newOther!=ver.resFace:
                        if self.resGraphFaces[ver.resFace]==[]:
                            self.resGraphFaces[ver.resFace].append(newOther)
                        elif newOther!=self.resGraphFaces[ver.resFace][-1]:
                            self.resGraphFaces[ver.resFace].append(newOther)
                    self.resGraphFaces[ver.resFace].append(-1)                    
        self.resGraphFaces[-1]=[]
        for ver in self.f[-1].a:
            if self.resGraphFaces[-1]==[]:
                self.resGraphFaces[-1].append(self.v[ver].resFace)
            elif self.v[ver].resFace!=self.resGraphFaces[-1][-1]:
                self.resGraphFaces[-1].append(self.v[ver].resFace)
        for rf in self.resGraphFaces:
            if len(self.resGraphFaces[rf])==1:
                self.isWrong=True
            elif self.resGraphFaces[rf][0]==self.resGraphFaces[rf][-1]:
                del(self.resGraphFaces[rf][-1])
##        for i in self.resGraphFaces:
##            for j in self.resGraphFaces[i]:
##                if i not in self.resGraphFaces[j]:
##                    print('problematic resGraphFaces',i,j,self.resGraphFaces,[self.v[ver].resFace for ver in self.f[-1].a])
    def isNontrivial3cut(self):
        checked={}
        changed=True
        checked[-1]=True
        for resFaceNb in self.resGraphFaces:
            checked[resFaceNb]=True
            resFace=self.resGraphFaces[resFaceNb]
            deg=len(resFace)
            for i in range(deg):
                ii=resFace[i]
                if ii not in checked:
                    for j in range(i+2-deg,i-1):
                        jj=resFace[j]
                        if jj not in checked:
                            if ii in self.resGraphFaces[jj]:
                                degi=len(self.resGraphFaces[ii])
                                whereji=self.resGraphFaces[ii].index(jj)
                                wheredi=self.resGraphFaces[ii].index(resFaceNb)
                                difi=whereji-wheredi
                                if difi<0:
                                    difi*=-1
                                if 2<=difi and difi <= degi - 2:
                                    degj=len(self.resGraphFaces[jj])
                                    whereij=self.resGraphFaces[jj].index(ii)
                                    wheredj=self.resGraphFaces[jj].index(resFaceNb)
                                    difj=whereij-wheredj
                                    if difj<0:
                                        difj*=-1
                                    if 2<=difj and difj<=degj-2:
                                        if not ((2==difi or difi==degi-2) and (2==difj or difj==degj-2) and -1 in [resFaceNb,ii,jj]):
                                            return True
                                
        return False
    def completeSolution(self,Qpaths):
        if self.completeLabels([self.initialAstFaces]+[qpath.astFaces for qpath in Qpaths],[qpath.timesFaces for qpath in Qpaths],Qpaths):
            self.completeTheRest(Qpaths)

    def completeTheRest(self,Qpaths):
            qua=[face.nb for face in self.f if (face.s==4 and face.d>1)]
            parity = (
                  len([q for q in qua if self.f[q].label!=AST])
                + len(Qpaths)
                - len([
                        1 for qpath in Qpaths if
                       ( qpath.timesFaces[0]==qpath.timesFaces[-1] and not (self.inSegment[0]!=None and self.outSegment[0]!=None and qpath.timesFaces[0]==self.inSegment[0].nb ))
                        ])
            )%2
            if self.isTooComplicated(Qpaths):
                return
            self.calculateResidualFaces()
            if self.isWrong:            
                return
            self.calculateResidualAdjacencies()
            for rf in self.resGraphFaces:
                if len(self.resGraphFaces[rf])==1:
                    return
            digons = [rf for rf in self.resGraphFaces if len(self.resGraphFaces[rf])==2]
            trigons = [rf for rf in self.resGraphFaces if (len(self.resGraphFaces[rf])==3 and -1 not in self.resGraphFaces[rf])]
            isUgly=False
            if len(digons)+len(trigons)>1:
                isUgly=True
            if len(digons)==1:
                digon=digons[0]
                nei1=self.resGraphFaces[digon][0]
                nei2=self.resGraphFaces[digon][1]
                done=False
                for face in self.f:
                    if face.label!=AST and face.s==6 and not done:
                        whatISee=[self.v[ver].resFace for ver in face.a]
                        if digon in whatISee and nei1 in whatISee and nei2 in whatISee:
                            done=True
                            face.label=AST
                            for fn in face.n:
                                if self.f[fn].label==CIRC:
                                    self.f[fn].label=TIMES
                            for ff in self.f:
                                if ff.resFace==nei1 or ff.resFace==nei2:
                                    ff.resFace=digon
                            for vv in self.v:
                                if vv.resFace==nei1 or vv.resFace==nei2:
                                    vv.resFace=digon
                if not done:
                    isUgly=True
            elif len(trigons)==1:
                trigon=trigons[0]
                neis=[self.resGraphFaces[trigon][i] for i in range(3)]
                isAvailable=[None,None,None]
                for i in range(3):
                    previous = self.resGraphFaces[trigon][i-1]
                    nextt = self.resGraphFaces[trigon][i-2]
                    whereIs = whereIsFirst(nextt,self.resGraphFaces[previous])
                    if whereIs==None:
                        print(self.resGraphFaces)
                        print(trigon)
                        print([path.timesFaces for path in Qpaths])
                    opposite = self.resGraphFaces[previous][(whereIs+1)%len(self.resGraphFaces[previous])]
                    if len(self.resGraphFaces[opposite])>=5 or opposite<-1:
                        isAvailable[i]=True
                    else:
                        isAvailable[i]=False
                lengths=[len(self.resGraphFaces[neis[i]]) for i in range(3)]
                longest=max(lengths)
                if lengths.count(4)>=2:
                    isUgly=True
                if longest<6:
                    isUgly=True
                if lengths.count(longest)==1:
                    other=lengths.index(longest)
                elif lengths.count(longest)==2:
                    other=None
                    for i in range(3):
                        if isAvailable[i]:
                            if lengths[i]==longest:
                                other=i
                    if other==None:
                        other=lengths.index(longest)
                elif lengths.count(longest)==3:
                    other=None
                    for i in range(3):
                        if isAvailable[i]:
                            if lengths[i]==longest:
                                other=i
                    if other==None:
                        other=lengths.index(longest)
                others=[0,1,2]
                del(others[other])
                second=neis[others[0]]
                third=neis[others[1]]
                for face in self.f:
                    if face.label!=AST and face.s==6:
                        whatISee=[self.v[ver].resFace for ver in face.a]
                        if trigon in whatISee and second in whatISee and third in whatISee:
                            auxList=[nei for nei in face.n if self.f[nei].label==TIMES and self.f[nei].d==1]
                            
                            if False and auxList!=[]:
                                isUgly=True
                                
                            else:
                                if not isUgly:
                                    face.label=AST
                                    for fn in face.n:
                                        if self.f[fn].label==CIRC:
                                            self.f[fn].label=TIMES
                                    for ff in self.f:
                                        if ff.resFace==second or ff.resFace==third:
                                            ff.resFace=trigon
                                    for vv in self.v:
                                        if vv.resFace==second or vv.resFace==third:
                                            vv.resFace=trigon
            self.calculateResidualFaces()
            if self.isWrong:            
                return
            
            self.calculateResidualAdjacencies()
            if self.isNontrivial3cut():
                isUgly=True
            timesEdges=self.calculateTimesEdges(Qpaths)
            circEdges=self.calculateCircEdges()
            if circEdges==[]:
                return
            circEdges=self.eliminate2vertices(circEdges)
            isTri=self.isTriangle(circEdges)
            if self.success[parity]==False:
              if not isUgly:  
                if isTri>=2:
                    self.success[parity]=True
                    if self.needBothParities==False:
                        self.success[1-parity]=True
                    self.drawFigure(timesEdges,circEdges,parity,Qpaths)
        
        
    def callForNewInitialDirections(self,Qpaths):
        astPentagons=[]
        timesPentagons=[]
        d={}
        for p in self.pentagons:
            if True in [p in qpath.astFaces for qpath in Qpaths]:
                astPentagons.append(p)    
            elif True in [p in qpath.timesFaces for qpath in Qpaths]:
                timesPentagons.append(p)
            else:
                foundAst=False
                L=[p]
                dist={}
                dist[p]=0
                while not foundAst:
                    nf=L.pop(0)
                    for i in self.f[nf].n:
                        if i not in dist:
                            dist[i]=dist[nf]+1
                            L.append(i)
                            if True in [i in qpath.astFaces for qpath in Qpaths] or i in self.initialAstFaces:
                                foundAst=True
                                d[p]=dist[i]
        self.completeSolution(Qpaths)
        if d=={}:
          if self.success!=[True,True]:  
            initialDirections=[]
            quad = [face.nb for face in self.f if face.s==4 and face.d>1]        
            for where in quad:
                face=self.f[where]
                if where not in timesPentagons:
                 if where not in astPentagons:   
                  for i in range(face.s):
                    if face.n[i] not in astPentagons:
                        if face.n[i-2] not in astPentagons:
                            if face.n[i-1] not in timesPentagons:
                                whereFrom=face.n[i]
                                newDi=face.w[i]
                                initialDirections+=[(0,self.f[whereFrom],newDi,[whereFrom])]
            return initialDirections
        if self.success!=[True,True]:
            initialDirections=[]
            for where in d:
                    face=self.f[where]
                    initialDirections+=[(0,face,di,[p for p in d if p>where]) for di in range(face.s)]
            for where in d:
                face=self.f[where]
                for i in range(face.s):
                    if face.n[i] not in astPentagons:
                        if face.n[i-2] not in astPentagons:
                            if face.n[i-1] not in timesPentagons:
                                whereFrom=face.n[i]
                                newDi=face.w[i]
                                initialDirections+=[(0,self.f[whereFrom],newDi,[whereFrom])]
            quad = [face.nb for face in self.f if face.s==4 and face.d>1]        
            for where in quad:
                face=self.f[where]
                if where not in timesPentagons:
                 if where not in astPentagons:   
                  for i in range(face.s):
                    if face.n[i] not in astPentagons:
                        if face.n[i-2] not in astPentagons:
                            if face.n[i-1] not in timesPentagons:
                                whereFrom=face.n[i]
                                newDi=face.w[i]
                                initialDirections+=[(0,self.f[whereFrom],newDi,[whereFrom])]
            return initialDirections
        else:
            return []



    def regularizeAstFaces(self):
        toRemove=[]
        for astFace in self.initialAstFaces:
            if self.f[astFace].d>2:
                toRemove.append(astFace)
        for face in toRemove:
            while face in self.initialAstFaces:
                self.initialAstFaces.remove(face)
    def checkInactiveEverywhere(self):
        if self.completeLabels([self.initialAstFaces],[],[]):
            self.completeTheRest([])

    def isDanger(self,face,di):
        mayContinue = []
        size=face.s
        for i in [-1,1,-3]:
            newDi=(di+i)%size
            nextFace = self.f[face.sn[newDi]]
            if nextFace.d>=2:
                mayContinue.append((newDi,nextFace))
        if len(mayContinue)>=2:
            return (False,None)
        elif len(mayContinue)==0:
            print('Error, cannot continue at all!')
            return (True,None)
        else:
            return (True,mayContinue[0])

    def check(self,pNb):
        global patchNb
        patchNb=pNb
        global figNb
        figNb=0
        self.setMetapostDefinitions()
        output=str(self.f4)+'.'+str(self.f5)+'.'+str(self.f6)+'.'+str(patchNb)
        metapostFile=open("./output/"+output+'.mp','w')
        print(output)
        metapostFile.write(self.meta)
        metapostFile.close()
        texFile=open("./output/"+output+'.tex','w')
        texFile.write("\\documentclass{article}\n")
        texFile.write("\\usepackage{graphicx}\n")
        texFile.write("\\begin{document}\n")
        texFile.close()
        pentagons = [face.nb for face in self.f if face.s==5 and face.d>1]
        self.pentagons=[face.nb for face in self.f if face.s==5 and face.d>1]
        maxFaceNb=len(self.f)-1


        (startingEdges,aroundFaces)=self.startingEdges()
        if self.c%2==1:
            if len(aroundFaces[0])>len(aroundFaces[1]):
                (aroundFaces[0],aroundFaces[1])=(aroundFaces[1],aroundFaces[0])
                (startingEdges[0],startingEdges[1])=(startingEdges[1],startingEdges[0])
            
            aroundFacesThird=aroundFaces[0]
            tobeRemoved=[]
            for astFace in aroundFacesThird:
                if self.f[astFace].d==3:
                    tobeRemoved.append(astFace)
            for astFace in tobeRemoved:
                aroundFacesThird.remove(astFace)
            incomplete=0
            
            self.outSegment=(None,None)
            self.needBothParities=True
            texFile=open("./output/"+output+'.tex','a')
            texFile.write("\n")
            texFile.close()
     
            self.success=[False,False]
            self.initialAstFaces=aroundFaces[0]
            #print(self.initialAstFaces)
            self.Qpaths=[]
            self.inSegment=(None,None)
            self.outSegment=(None,None)
            self.checkInactiveEverywhere()
            newInitialDirections=self.callForNewInitialDirections([])
            self.searchFrom(newInitialDirections)
            if self.success==[False,False]:
                print('Cannot find any solution for 0 active segments !!!')
                self.drawBadCase()
            elif self.success==[True,True]:
                self.needBothParities=False
            else:
                if self.c>=7:
                    print('Cannot change parity!')
    ##            else:
    ##                print('Success')
    #        print([(face.nb,face.sn[di]) for (face,di) in twoActiveSegmentsStartingEdges])
            if self.c<=5:
                texFile=open("./output/"+output+'.tex','a')
                texFile.write("\n")
                texFile.close()
                if self.needBothParities:
                    for face in self.f:
                        face.bothParities=False

                oneActiveSegmentStartingEdges = startingEdges[0]
                twoActiveSegmentsStartingEdges = startingEdges[1]
                self.outSegment=(None,None)
                oneActiveSegmentStartingPoints=[(face,di%2,di) for (face,di) in (oneActiveSegmentStartingEdges[::2]+oneActiveSegmentStartingEdges[1::2])]
                #self.show()
                for (face,pa,di) in oneActiveSegmentStartingPoints:
                   #print(oneActiveSegmentStartingPoints.index((face,pa,di))*2+1)
        #           if oneActiveSegmentStartingPoints.index((face,pa,di))*2+1==9:
##                    texFile=open("./output/"+output+'.tex','a')
##                    texFile.write("\n")
##                    texFile.close()
         
                    self.success=[False,False]
                    self.setOddInitialAstFacesOneActiveSegment(face,di,aroundFaces[1])
        #            print(self.initialAstFaces)
                    self.Qpaths=[]
                    self.inSegment=(face,di)
                    self.outSegment=(None,None)
                    initialDirections=[(1,face,di,pentagons)]
                    self.searchFrom(initialDirections)
                    if self.success==[False,False]:
                        print('Cannot find any solution for',oneActiveSegmentStartingPoints.index((face,pa,di))*2+1,'!!!')
                        self.drawBadCase()
                    else:
                        if self.needBothParities:
                            if self.success==[True,True]:
                                newface=self.f[face.sn[di]]
                                incoming=face.sw[di]
                                f1=face.n[di]
                                f2=newface.n[incoming]
                                face.bothParities=True
                                self.f[f1].bothParities=True
                                self.f[f2].bothParities=True
                                newface.bothParities=True
                if self.needBothParities:
                    AllBothParities=True
                    for faceDist1 in self.f[maxFaceNb].n:
                        if self.f[faceDist1].bothParities==False:
                            nbNotBothParities=0
                            for nei in self.f[faceDist1].n:
                                if nei<maxFaceNb:
                                    if self.f[nei].bothParities==False:
                                        nbNotBothParities+=1
                            if nbNotBothParities>1:
                                AllBothParities=False
                                #print('face',faceDist1,'does not have both parities')
                    if not AllBothParities:
                        print('cannot guarantee both parities for one active segment...')
                    else:
                        self.needBothParities=False
                redStartingEdges = startingEdges[1][::2]
                blueStartingEdges = startingEdges[1][1::2]
                for (inFace,inDi) in redStartingEdges:
                    texFile=open("./output/"+output+'.tex','a')
                    texFile.write("\n")
                    texFile.close()
                    incoming=inFace.sw[inDi]
                    inNewFace=self.f[inFace.sn[inDi]]
                    v1=inFace.a[inDi]
                    v2=inNewFace.a[incoming]
                    f1=inFace.n[inDi]
                    f2=inNewFace.n[incoming]
                    inDanger = self.isDanger(inNewFace,incoming)                      
                    for (outFace,outDi) in blueStartingEdges:
                        outcoming=outFace.sw[outDi]
                        outNewFace=self.f[outFace.sn[outDi]]
                        v3=outFace.a[outDi]
                        v4=outNewFace.a[outcoming]
                        f3=outFace.n[outDi]
                        f4=outNewFace.n[outcoming]
                        outDanger = self.isDanger(outNewFace,outcoming)
                        danger=False
                        if inDanger[0] and outDanger[0]:
                            (inNewDi,inNextFace) = inDanger[1]
                            (outNewDi,outNextFace) = outDanger[1]
                            w1=inNewFace.a[inNewDi]
                            w2=inNextFace.a[inNewFace.sw[inNewDi]]
                            w3=outNewFace.a[outNewDi]
                            w4=outNextFace.a[outNewFace.sw[outNewDi]]
                            if not disjoint([w1,w2],[w3,w4]):
                                danger=True
                        if not danger:
                            self.success=[False,False]
                            self.setOddInitialAstFacesTwoActiveSegments(inFace,inDi,outFace,outDi,aroundFaces)
                            while maxFaceNb in self.initialAstFaces:
                                self.initialAstFaces.remove(maxFaceNb)
                            self.regularizeAstFaces()
                            countPairs=0
                            pairs=[]
                            for faceNb in self.initialAstFaces:
                                for i in range(self.f[faceNb].s):
                                    if self.f[faceNb].n[i] in self.initialAstFaces:
                                        countPairs+=1
                                        pairs.append((faceNb,self.f[faceNb].n[i]))
                            
                            astAdj={}
                            for (i,j) in pairs:
                                if i not in astAdj:
                                    astAdj[i]=[j]
                                else:
                                    astAdj[i]+=[j]
                            possible=True
                            for i in astAdj:
                                if len(astAdj[i])==2:
                                    if astAdj[i][0] in astAdj[astAdj[i][1]]:
                                        possible=False
                            if possible:
                              if countPairs==4:
                                self.Qpaths=[]
                                initialDirections=[(2,inFace,inDi,pentagons+[outFace.sn[outDi]]),(2,outFace,outDi,pentagons+[inFace.sn[inDi]])]
                                self.inSegment=(inFace,inDi)
                                self.outSegment=(outFace,outDi)
                                self.searchFrom(initialDirections)
                                if self.success==[False,False]:
                                    print('Cannot find any solution for',inFace.nb,outFace.nb,'!!!')
                                    self.drawBadCase()
                
        if self.c%2==0 and len(aroundFaces)==1:
            for aroundFacesThird in aroundFaces:
                tobeRemoved=[]
                for astFace in aroundFacesThird:
                    if self.f[astFace].d==3:
                        tobeRemoved.append(astFace)
                for astFace in tobeRemoved:
                    aroundFacesThird.remove(astFace)

            for face in self.f:
                face.bothParities=False
            startingEdges=startingEdges[0]
            aroundFaces=aroundFaces[0]                
            firstLeftNb=startingEdges[0][0].n[startingEdges[0][1]]
            firstRightNb=startingEdges[0][0].n[startingEdges[0][1]+1]
            if aroundFaces.index(firstLeftNb)>aroundFaces.index(firstRightNb):
                oneActiveSegmentStartingEdges = startingEdges[::2]
                twoActiveSegmentsStartingEdges = startingEdges[1::2]
            else:
                oneActiveSegmentStartingEdges = startingEdges[1::2]
                twoActiveSegmentsStartingEdges = startingEdges[::2]
            self.outSegment=(None,None)
            oneActiveSegmentStartingPoints=[(face,di%2,di) for (face,di) in oneActiveSegmentStartingEdges]
            self.needBothParities=True
            for (face,pa,di) in oneActiveSegmentStartingPoints:
                texFile=open("./output/"+output+'.tex','a')
                texFile.write("\n")
                texFile.close()
     
                self.success=[False,False]
                self.setInitialAstFacesOneActiveSegment(face,di,aroundFaces)
                self.Qpaths=[]
                self.inSegment=(face,di)
                self.outSegment=(None,None)
                initialDirections=[(1,face,di,pentagons)]
                self.searchFrom(initialDirections)
                if self.success==[False,False]:
                    print('Cannot find any solution for',oneActiveSegmentStartingPoints.index((face,pa,di))*2+1,'!!!')
                    self.drawBadCase()
                elif self.success!=[True,True]:
                    True
                else:
                    newface=self.f[face.sn[di]]
                    incoming=face.sw[di]
                    f1=face.n[di]
                    f2=newface.n[incoming]
                    if face.d in [1,2]:
                        face.bothParities=True
                    if self.f[f1].d in [1,2]:
                        self.f[f1].bothParities=True
                    if self.f[f2].d in [1,2]:
                        self.f[f2].bothParities=True
                    if newface.d in [1,2]:
                        newface.bothParities=True
            AllBothParities=True
            for faceDist1 in self.f[-1].n:
                if self.f[faceDist1].s==4:
                  if not self.f[faceDist1].bothParities:  
                    nb=0
                    for faceNb in self.f[faceDist1].n:
                        if self.f[faceNb].bothParities:
                            nb+=1
                    if nb>=3:
                        self.f[faceDist1].bothParities=True
                            
            for faceDist1 in self.f[maxFaceNb].n:
                if self.f[faceDist1].bothParities==False:
                    AllBothParities=False
                    print('face',faceDist1,'does not have both parities')

            if not AllBothParities:
                print('cannot guarantee both parities for one active segment')
                self.needBothParities=True
            else:
                self.needBothParities=False
                        
            if self.c<6 or (self.c==6 and self.nanoType in [[8,0],[6,2]]) :
                for inSegmentNb in range(len(twoActiveSegmentsStartingEdges)):
                    (inFace,inDi)=twoActiveSegmentsStartingEdges[inSegmentNb]
                    incoming=inFace.sw[inDi]
                    inNewFace=self.f[inFace.sn[inDi]]
                    v1=inFace.a[inDi]
                    v2=inNewFace.a[incoming]
                    f1=inFace.n[inDi]
                    f2=inNewFace.n[incoming]
                    inDanger = self.isDanger(inNewFace,incoming)                      

                    outSegmentNb=inSegmentNb-(len(twoActiveSegmentsStartingEdges)//2)
                    texFile=open("./output/"+output+'.tex','a')
                    texFile.write("\n")
                    texFile.close()
                    continues=True
                    while continues:
                        (outFace,outDi)=twoActiveSegmentsStartingEdges[outSegmentNb]
                        outcoming=outFace.sw[outDi]
                        outNewFace=self.f[outFace.sn[outDi]]
                        v3=outFace.a[outDi]
                        v4=outNewFace.a[outcoming]
                        f3=outFace.n[outDi]
                        f4=outNewFace.n[outcoming]
                        outDanger = self.isDanger(outNewFace,outcoming)
                        danger=False
                        if inDanger[0] and outDanger[0]:
                            (inNewDi,inNextFace) = inDanger[1]
                            (outNewDi,outNextFace) = outDanger[1]
                            w1=inNewFace.a[inNewDi]
                            w2=inNextFace.a[inNewFace.sw[inNewDi]]
                            w3=outNewFace.a[outNewDi]
                            w4=outNextFace.a[outNewFace.sw[outNewDi]]
                            if not disjoint([w1,w2],[w3,w4]):
                                danger=True
                        if not danger:
                            self.success=[False,False]
                            self.success=[False,False]
                            self.setInitialAstFacesTwoActiveSegments(inFace,inDi,outFace,outDi,aroundFaces)
                            self.Qpaths=[]
                            initialDirections=[(2,inFace,inDi,pentagons+[outFace.sn[outDi]]),(2,outFace,outDi,pentagons+[inFace.sn[inDi]])]
                            self.inSegment=(inFace,inDi)
                            self.outSegment=(outFace,outDi)
                            self.searchFrom(initialDirections)
                            if self.success==[False,False]:
                                print('Cannot find any solution for',inFace.nb,outFace.nb,'!!!')
                                self.drawBadCase()
                        outSegmentNb+=1
                        (outFace,outDi)=twoActiveSegmentsStartingEdges[outSegmentNb]
                        outcoming=outFace.sw[outDi]
                        v3=outFace.a[outDi]
                        v4=self.f[outFace.sn[outDi]].a[outcoming]
                        f3=outFace.n[outDi]
                        f4=self.f[outFace.sn[outDi]].n[outcoming]


                        if (not disjoint([v1,v2],[v3,v4])) or inFace.sn[inDi] in [f3,f4] or outFace.sn[outDi] in [f1,f2]:
                            continues=False

        elif self.c%2==0 and len(aroundFaces)>1:
            if len(aroundFaces)==2:
                aroundFaces.append(self.f[-1].sn)
            for aroundFacesThird in aroundFaces:
                tobeRemoved=[]
                for astFace in aroundFacesThird:
                    if self.f[astFace].d==3:
                        tobeRemoved.append(astFace)
                for astFace in tobeRemoved:
                    aroundFacesThird.remove(astFace)
            incomplete=0
            for i in range(3):
            
                self.inSegment=(None,None)
                self.outSegment=(None,None)
                self.needBothParities=True
                texFile=open("./output/"+output+'.tex','a')
                texFile.write("\n")
                texFile.close()
     
                self.success=[False,False]
                self.initialAstFaces=aroundFaces[i]
                self.Qpaths=[]

                newInitialDirections=self.callForNewInitialDirections([])
                self.searchFrom(newInitialDirections)

                if self.success==[False,False]:
                    print('Cannot find any solution for',i,'!!!')
                    self.drawBadCase()
                elif self.success!=[True,True]:
                    incomplete+=1
            if incomplete==3:
                print('Cannot change parity for any choice!')
            if self.c<6:
                self.needBothParities=False
                for i in range(3):
                    redStartingEdges = startingEdges[i][::2]
                    blueStartingEdges = startingEdges[i][1::2]
                    for (inFace,inDi) in redStartingEdges:
                        texFile=open("./output/"+output+'.tex','a')
                        texFile.write("\n")
                        texFile.close()
                        for (outFace,outDi) in blueStartingEdges:
                            self.success=[False,False]
                            self.setInitialAstFacesTwoActiveAccordedSegments(inFace,inDi,outFace,outDi,aroundFaces)
                            self.Qpaths=[]
                            initialDirections=[(2,inFace,inDi,pentagons+[outFace.sn[outDi]]),(2,outFace,outDi,pentagons+[inFace.sn[inDi]])]
                            self.outSegment=(outFace,outDi)
                            self.inSegment=(inFace,inDi)
                            self.searchFrom(initialDirections)
                            if self.success==[False,False]:
                                print('Cannot find any solution for',inFace.nb,outFace.nb,'!!!')
                                self.drawBadCase()
                            

        metapostFile=open("./output/"+output+'.mp','a')
        metapostFile.write("end.\n")
        metapostFile.close()
        texFile=open("./output/"+output+'.tex','a')
        texFile.write("\\end{document}\n")
        texFile.close()
    

        
