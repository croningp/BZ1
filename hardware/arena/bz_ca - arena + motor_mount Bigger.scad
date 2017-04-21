//KD_BZ-3D_square_in_square+grid+channels+stirrer_grid.scad
//08/02/2016    Kevin Donkers, Cronin Group, University of Glasgow
//OpenSCAD file creating a 3D model of a square arena for conducting reaction-diffusion chemistry as part of the BZ-3D workshop in BUCT, Beijing, China.
//Arena contains cells divided by walls with channels
//A holder for a matrix of motors can be modelled too (optional)
//All values in mm.

//What are we printing? #
// 0 = show everything ;)
// 1 = base only
// 2 = grid only, no channels
// 3 = grid only, with tapered channels
// 4 = show none of the base

baseprint = 0;

//Stirrer matrix?
// 0 = hide stirrer matrix
// 1 = show stirrer matrix
// 2 = show stirrer matrix new size holes

stirrer = 0;

//Cell dimensions

nx = 7;     //number of cells in x
ny = 7;     //number of cells in y
cx = 16;     //cell width
cy = 16;     //cell length
cz = 11;     //cell depth

//Arena total size is (nx*cx)x(ny*cy) 
//Cells are (cx-0.5gw)x(cy-0.5gw)

//Base and edge thicknesses

base = 1.5;
edge = 15;

//Equidistant groove depth and width

gw = 2;     //width
gz = 0;     //depth
gh = 0;     //height above cell edge

shim = 0.0;     //narrowing wrt grooves
extend = 0;   //extension of grooves into sides
raise = 3;      //height of channels from bottom of cell [mm]
prop = 0.5;     //propoprtion of cell wall to have open as channel

//Stirrer motor parameters

md = 4;     //motor top sleeve diameter
mx = 12.05; //motor x width
my = 10.05; //motor y width
mz = 24;    //motor length

//Bolt hole paramters

boltd = 5.2;  //bolt diameter
bolte = 5;  //distance from edge

//Calculate arena dimensions

ax = nx*cx;
ay = ny*cy;
az = cz + gz;

//Calculate block dimensions

bd = sqrt((ax*ax+ay*ay))+edge;   //diameter
bz = az + base;     //depth

//Base
if (baseprint==1 || baseprint==0) {
difference() {
    //Create block
    translate([-edge/2,-edge/2,0])
    cube([ax+edge,ay+edge,bz],false);
    //Subtract arena
    translate([(0.5*gw),(0.5*gw),base])
    cube([(ax-gw),(ay-gw),(az+1)],false);
    //Subtract bolt holes
    if (stirrer==1||stirrer==0||stirrer==2){
        translate([-edge/2+bolte,-edge/2+bolte,-1])
        cylinder(h=bz+2,d=boltd,$fn=50);
        translate([ax+edge/2-bolte,-edge/2+bolte,-1])
        cylinder(h=bz+2,d=boltd,$fn=50);     
        translate([-edge/2+bolte,ay+edge/2-bolte,-1])
        cylinder(h=bz+2,d=boltd,$fn=50);
        translate([ax+edge/2-bolte,ay+edge/2-bolte,-1])
        cylinder(h=bz+2,d=boltd,$fn=50);
        }
}
} 


//Walls
/*
if (baseprint==2 || baseprint==3  ||baseprint==0) {
union() {
    //Build X grid walls
    if (nx>1) {
        translate([cx-(gw*0.5)+shim,-(extend-shim),(base)])
        cube([gw-(2*shim),ay+((extend-shim)*2),(cz/2)])  ;
    for (i=[2:(nx-1)]) {
        if (i<nx) {
        translate([(i*cx)-(gw*0.5)+(shim),-(extend-shim),(base)])
        cube([gw-(2*shim),ay+((extend-shim)*2),(cz/2)]);
    }}};
    //Build Y grid walls 
    if (ny>1) { 
        translate([-(extend-shim),cy-(gw*0.5)+shim,(base)])
        cube([ax+((extend-shim)*2),gw-(2*shim),(cz/2)]);
    for (i=[2:(ny-1)]) {
        if (i<ny) {
        translate([-(extend-shim),(i*cy)-(gw*0.5)+(shim),(base)])
        cube([ax+((extend-shim)*2),gw-(2*shim),(cz/2)]);
    }}};        
}
} */


//Walls and Channels
difference() { 
//Walls
if (baseprint==2 || baseprint==3  ||baseprint==0) {
union() {
    //Build X grid walls
    if (nx>1) {
        translate([cx-(gw*0.5)+shim,-(extend-shim),(base)])
        cube([gw-(2*shim),ay+((extend-shim)*2),(az+gh-(gz*2))])  ;
    for (i=[2:(nx-1)]) {
        if (i<nx) {
        translate([(i*cx)-(gw*0.5)+(shim),-(extend-shim),(base)])
        cube([gw-(2*shim),ay+((extend-shim)*2),(az+gh-(gz*2))]);
    }}};
    //Build Y grid walls 
    if (ny>1) { 
        translate([-(extend-shim),cy-(gw*0.5)+shim,(base)])
        cube([ax+((extend-shim)*2),gw-(2*shim),(az+gh-(gz*2))]);
    for (i=[2:(ny-1)]) {
        if (i<ny) {
        translate([-(extend-shim),(i*cy)-(gw*0.5)+(shim),(base)])
        cube([ax+((extend-shim)*2),gw-(2*shim),(az+gh-(gz*2))]);
    }}};        
}
} 

//Channels 

if (baseprint==3 || baseprint==0) {
union() {
    //Cut X grid wall channels
    if (nx>1) {
    //subtracts a vertical stack of 4 hexagonal prisms half a diameter apart
    for (m=[1:(ceil(1/prop)*2)]){
    //channels (gaps) in x as single long triangular prisms
    for (l=[1:nx]){
        translate([(l-0.5)*cx,0,(m*prop*cx*0.5)+gz+base+raise])
        rotate([-90,90,0])
        cylinder(h=ay,d=(prop*cy),$fn=6);        
            }
        }
    }
    if (ny>1) {
    //subtracts a vertical stack of 4 hexagonal prisms half a diameter apart
    for (m=[1:(ceil(1/prop)*2)]){
    //channels (gaps) in x as single long triangular prisms
    for (l=[1:ny]){
        translate([0,(l-0.5)*cy,(m*prop*cy*0.5)+gz+base+raise])
        rotate([0,90,0])
        cylinder(h=ax,d=(prop*cx),$fn=6);        
            }
        }
    }
}
} 
/*
//Channels
if (baseprint==3 || baseprint==0) {
union() {
    //Cut X grid wall channels
    if (nx>1) {
    //subtracts a vertical stack of 4 hexagonal prisms half a diameter apart

    //channels (gaps) in x as single long triangular prisms
    for (l=[1:nx]){
        translate([(l-0.5)*cx,0,(prop*cx*0.5)+gz+base+raise])
        rotate([-90,90,0])
        #cylinder(h=ay,d=(prop*cy),$fn=6);        
            }

    }
    if (ny>1) {
    //subtracts a vertical stack of 4 hexagonal prisms half a diameter apart

    //channels (gaps) in x as single long triangular prisms
    for (l=[1:ny]){
        translate([0,(l-0.5)*cy,(prop*cx*0.5)+gz+base+raise])
        rotate([0,90,0])
        #cylinder(h=ax,d=(prop*cx),$fn=6);        
            }

    }
}
}*/


}
//Stirrer grid round
if (stirrer==1){
difference(){
    //Create block
    translate([-edge/2,-edge/2,bz*5])
    cube([ax+edge,ay+edge,mz],false);
    //Subtract bolt holes
    translate([-edge/2+bolte,-edge/2+bolte,bz*5-1])
    cylinder(h=mz+2,d=boltd,$fn=50);
    translate([ax+edge/2-bolte,-edge/2+bolte,bz*5-1])
    cylinder(h=mz+2,d=boltd,$fn=50);     
    translate([-edge/2+bolte,ay+edge/2-bolte,bz*5-1])
    cylinder(h=mz+2,d=boltd,$fn=50);
    translate([ax+edge/2-bolte,ay+edge/2-bolte,bz*5-1])
    cylinder(h=mz+2,d=boltd,$fn=50);
    //Subtract motor holes
    for (i=[1:nx]){
        for (j=[1:ny]){
            translate([(i-0.5)*cx,(j-0.5)*cy,bz*5-1])
            cylinder(h=mz+2,d=md,$fn=50);
        }
    }    
}
}
//Stirrer grid round
if (stirrer==2){
difference(){
    //Create block
    translate([-edge/2,-edge/2,bz*5])
    cube([ax+edge,ay+edge,mz],false);
    //Subtract bolt holes
    translate([-edge/2+bolte,-edge/2+bolte,bz*5-1])
    cylinder(h=mz+2,d=boltd,$fn=50);
    translate([ax+edge/2-bolte,-edge/2+bolte,bz*5-1])
    cylinder(h=mz+2,d=boltd,$fn=50);     
    translate([-edge/2+bolte,ay+edge/2-bolte,bz*5-1])
    cylinder(h=mz+2,d=boltd,$fn=50);
    translate([ax+edge/2-bolte,ay+edge/2-bolte,bz*5-1])
    cylinder(h=mz+2,d=boltd,$fn=50);
    //Subtract motor holes
    for (i=[1:nx]){
        for (j=[1:ny]){
            translate([(i-0.5)*cx,(j-0.5)*cy,bz*6-1
           ])
            cube([mx,my,mz],true);
            //cylinder(h=mz+2,d=md,$fn=50);
        }
    }  
    for (i=[1:nx]){
        for (j=[1:ny]){
            translate([(i-0.5)*cx,(j-0.5)*cy,bz*5-1])
            cylinder(h=mz+2,d=md,$fn=50);
        }
    }   
}
}