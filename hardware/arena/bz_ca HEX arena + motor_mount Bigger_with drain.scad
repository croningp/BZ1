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

//Drain outlet?
// 0 = print without a drain oulet
// 1 = print with a drain outlet
drain = 1;

// clip = 0 no tubbing clip, clip = 1 yes
clip = 1;

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
raise = -2;      //height of channels from bottom of cell [mm]
prop = 0.3;     //propoprtion of cell wall to have open as channel
roundness = 6;  //arena units - 6=hexagon. 50= circle etc

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

//clip attachment for tubing
module clip(){
    side = ax+edge;
    hs = side/2;
    difference() {
        translate([20,6,0])cube([side-40, (edge/2)-0.5, 15]);
        translate([hs-32,30,-2])rotate([65,0,0])cylinder(h=50,d=6, $fn=20);
        translate([hs,30,-2])rotate([65,0,0])cylinder(h=50,d=6, $fn=20);
        translate([hs-16,30,-2])rotate([65,0,0])cylinder(h=50,d=6, $fn=20);
        translate([hs+16,30,-2])rotate([65,0,0])cylinder(h=50,d=6, $fn=20);
        translate([hs+32,30,-2])rotate([65,0,0])cylinder(h=50,d=6, $fn=20);
    }
}

if (clip==1){
rotate([0,0,-90])translate([-20+edge/2-(ax+edge)+20, -6+(-edge/2)+1.5, bz])clip();
}

//Base
if (baseprint==1 || baseprint==0) {
    difference() {
        //Create block
        union() { 
            translate([-edge/2,-edge/2,0])
            cube([ax+edge,ay+edge,bz],false);
                
            if(drain==1) {
                translate([-base-1,ax/2,0])
                cube([10,10,4],true);
            }
        }
        
        if (baseprint==3 || baseprint==0) {
            union() {
        
               for (x=[0:(nx-1)], y=[0:(nx-1)]) {
                        translate([(x+0.5)*cx,(y+0.5)*cy,(base)])
                        cylinder(h=20,r=cx/2,$fn=roundness);
                };
        
                //Cut X grid wall channels
                if (nx>1) {
                    //subtracts a vertical stack of 4 hexagonal prisms 
                    // half a diameter apart

                    //channels (gaps) in x as single long triangular prisms
                    for (l=[1:nx]){
                        translate([(l-0.5)*cx,(ax/2),(base+6)])
                        cube([(prop*cy),ax-gw-cx,12],true);              
                    }
                }
                
                if (ny>1) {
                //channels (gaps) in x as single long triangular prisms
                    for (l=[1:ny]){
                        translate([(ay/2),(l-0.5)*cy,(base+6)])
                        cube([ay-gw-cy,(prop*cy),12],true);        
                    }    
                }
            }
        } 
            
            
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
        
        // DRAIN OUTLET
        if (drain==1) {
            rotate([0,90,0])
            translate([-base-1,ax/2,-(0.5+edge/2)])
            cylinder(h=2+(edge/2), r1=3, r2=2,$fn=50);
        }   
    }
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