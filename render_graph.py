class graph_renderer():
    def __init__(self,adj_list_dual):
        self.dual = adj_list_dual
    
    def draw_dual(self):
        ext_vertex = 31
        file = open("dual.mp","w+")
        file.write("prologues:=0;\nvv:=7pt;\nww:=5pt;\nc:=.25;\npicture ver;\ndraw (0,0) withpen pencircle scaled vv;\nundraw (0,0) withpen pencircle scaled (vv-.8mm);\nver:=currentpicture;\ncurrentpicture:=blankpicture;\npicture pl,mi,pls,mis;\ndraw (0,0) withpen pencircle scaled ww;\nundraw (0,0) withpen pencircle scaled (ww-.4mm);\npickup pencircle scaled .3mm;\ndraw (-c*ww,0)--(c*ww,0);\nmi:=currentpicture;\ndraw (0,-c*ww)--(0,c*ww);\npl:=currentpicture;\ndraw (0,0) withpen pencircle scaled ww withcolor .3white;\nundraw (0,0) withpen pencircle scaled (ww-.4mm);\npickup pencircle scaled .3mm;\ndraw (-c*ww,0)--(c*ww,0) withcolor .3white;\nmis:=currentpicture;\ndraw (0,-c*ww)--(0,c*ww) withcolor .3white;\npls:=currentpicture;\ncurrentpicture:=blankpicture;\nqq:=1.5mm;\nrr:=14pt;\ndraw (-qq,0)--(qq,0) withpen pencircle scaled rr;\npicture kk;\nkk:=currentpicture;\ncurrentpicture:=blankpicture;\ndraw (0,0) withpen pencircle scaled (5pt+.6mm);\ndraw (0,0) withpen pencircle scaled (5pt) withcolor white;\npicture k;\nk:=currentpicture;\ncurrentpicture:=blankpicture;\npicture cely;\nu:=10mm;\nbeginfig(0)\n")
        if len(self.dual[ext_vertex]) == 6:
            file.write("z0=(6u,6u);\nz"+str(self.dual[ext_vertex][0])+"=z0+(5u,0);\nz"+ str(self.dual[ext_vertex][1])+"=z"+str(self.dual[ext_vertex][0])+" rotatedabout(z0,60);\nz"+ str(self.dual[ext_vertex][2])+ "=z"+str(self.dual[ext_vertex][1])+" rotatedabout(z0,60);\nz"+ str(self.dual[ext_vertex][3])+ "=z"+ str(self.dual[ext_vertex][2])+ " rotatedabout(z0,60);\nz"+ str(self.dual[ext_vertex][4])+ "=z"+ str(self.dual[ext_vertex][3])+ " rotatedabout(z0,60);\n"+ str(self.dual[ext_vertex][5])+"=z"+ str(self.dual[ext_vertex][4])+" rotatedabout(z0,60);\n")
        else:
            file.write("z0=(6u,6u);\nz"+str(self.dual[ext_vertex][0])+"=z0+(5u,0);\nz"+ str(self.dual[ext_vertex][1])+"=z"+str(self.dual[ext_vertex][0])+" rotatedabout(z0,72);\nz"+ str(self.dual[ext_vertex][2])+ "=z"+str(self.dual[ext_vertex][1])+" rotatedabout(z0,72);\nz"+ str(self.dual[ext_vertex][3])+ "=z"+ str(self.dual[ext_vertex][2])+ " rotatedabout(z0,72);\nz"+ str(self.dual[ext_vertex][4])+ "=z"+ str(self.dual[ext_vertex][3])+ " rotatedabout(z0,72);\n")
        ext_vertex +=1
        for index in range(len(self.dual)):
            try:
                self.dual[index].remove(ext_vertex)
            except:
                pass
            if index+1 not in self.dual[ext_vertex-1]:
                if index+1!=ext_vertex:
                    bary_equ = "z" + str(index+1) +"="
                    for neighbor in self.dual[index]:
                        if neighbor!=ext_vertex:
                            bary_equ += "z" + str(neighbor)
                            if neighbor!=self.dual[index][len(self.dual[index])-1]:
                                bary_equ += "+"
                            else:
                                bary_equ += ";"
                    file.write(bary_equ+"\n")
        
        for index in range(len(self.dual)):
                for neighbor in self.dual[index]:
                    if index+1!=ext_vertex and neighbor!=ext_vertex:
                        file.write("draw z"+str(index+1)+"--z"+str(neighbor)+";\n")
        file.write("endfig;\nend.")
        return 


exDual = [[2,3,4,5,6],[1,3,6,7,8,16],[1,2,4,8,9,10],[1,3,5,10,11,12],[1,4,6,12,13,14],[1,2,5,14,15,16],[2,8,16,17,18,26],[2,3,7,9,18],[3,8,10,18,19,20],[3,4,9,11,20],[4,10,12,20,21,22],[4,5,11,13,22],[5,12,14,22,23,24],[5,6,13,15,24],[6,14,16,24,25,26],[2,6,7,15,26],[7,18,26,27,31],[7,8,9,17,19,27],[9,18,20,27,28],[9,10,11,19,21,28],[11,20,22,28,29],[11,12,13,21,23,29],[13,22,24,29,30],[13,14,15,23,25,30],[15,24,26,30,31],[7,15,16,17,25,31],[17,18,19,28,31,32],[19,20,21,27,29,32],[21,22,23,28,30,32],[23,24,25,29,31,32],[17,25,26,27,30,32],[27,28,29,30,31]]
gr = graph_renderer(exDual)
gr.draw_dual()