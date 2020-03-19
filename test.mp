prologues:=0;
vv:=7pt;
ww:=5pt;
c:=.25;
picture ver;
draw (0,0) withpen pencircle scaled vv;
undraw (0,0) withpen pencircle scaled (vv-.8mm);
ver:=currentpicture;
currentpicture:=blankpicture;
picture pl,mi,pls,mis;
draw (0,0) withpen pencircle scaled ww;
undraw (0,0) withpen pencircle scaled (ww-.4mm);
pickup pencircle scaled .3mm;
draw (-c*ww,0)--(c*ww,0);
mi:=currentpicture;
draw (0,-c*ww)--(0,c*ww);
pl:=currentpicture;
draw (0,0) withpen pencircle scaled ww withcolor .3white;
undraw (0,0) withpen pencircle scaled (ww-.4mm);
pickup pencircle scaled .3mm;
draw (-c*ww,0)--(c*ww,0) withcolor .3white;
mis:=currentpicture;
draw (0,-c*ww)--(0,c*ww) withcolor .3white;
pls:=currentpicture;
currentpicture:=blankpicture;


qq:=1.5mm;
rr:=14pt;
draw (-qq,0)--(qq,0) withpen pencircle scaled rr;
picture kk;
kk:=currentpicture;
currentpicture:=blankpicture;

draw (0,0) withpen pencircle scaled (5pt+.6mm);
draw (0,0) withpen pencircle scaled (5pt) withcolor white;
picture k;
k:=currentpicture;
currentpicture:=blankpicture;
picture cely;
u:=10mm;
beginfig(0)
z0=(6u,6u);
z1=z0+(5u,0);
z2=z1 rotatedabout(z0,60);
z3=z2 rotatedabout(z0,60);
z4=z3 rotatedabout(z0,60);
z5=z4 rotatedabout(z0,60);
z6=z5 rotatedabout(z0,60);


fill z1--z2--z3--cycle withcolor .7white;

pickup pencircle scaled .3mm;

draw z1--z2;
draw z2--z3;
draw z3--z1;

endfig;
end.