// BZ platform pumps clip
// This is a 3D printed devide that will be attached to the BZ grid
// In order to create 4 inputs to connect 4 pumps.

//Cell dimensions

nx = 7;     //number of cells in x
ny = 7;     //number of cells in y
cx = 16;     //cell width
cy = 16;     //cell length
cz = 11;     //cell depth

//Base and edge thicknesses

base = 1.5;
edge = 15;

//Calculate arena dimensions

ax = nx*cx;
ay = ny*cy;
az = cz;
bz = az + base;     //depth

//Bolt hole paramters

boltd = 5.2;  //bolt diameter
bolte = 5;  //distance from edge


module clip(){
    side = ax+edge;
    hs = side/2;
    difference(){
        #cube([side, (edge/2)+8, 27]);
        translate([0,0,15])cube([side, (edge/2)+2, 15]);
        translate([0,-5,15])cube([30, 50, 15]);
        translate([97,-5,15])cube([30, 50, 15]);
        translate([hs-9,30,12])rotate([65,0,0])cylinder(h=50,d=6, $fn=20);
        translate([hs-25,30,12])rotate([65,0,0])cylinder(h=50,d=6, $fn=20);
        translate([hs+9,30,12])rotate([65,0,0])cylinder(h=50,d=6, $fn=20);
        translate([hs+25,30,12])rotate([65,0,0])cylinder(h=50,d=6, $fn=20);
        //translate([4,9,-12])rotate([0,0,0])cylinder(h=50,d=5, $fn=20);
        //translate([56,9,-12])rotate([0,0,0])cylinder(h=50,d=5, $fn=20);
    }
}

module base(){
    union(){
        translate([-edge/2,-edge/2,0])cube([ax+edge,ay+edge,bz+1]);
        translate([-edge/2+bolte,-edge/2+bolte,-9])
        cylinder(h=bz+20,d=boltd,$fn=50);
        translate([ax+edge/2-bolte,-edge/2+bolte,-9])
        cylinder(h=bz+20,d=boltd,$fn=50);     
        translate([-edge/2+bolte,ay+edge/2-bolte,-9])
        cylinder(h=bz+20,d=boltd,$fn=50);
        translate([ax+edge/2-bolte,ay+edge/2-bolte,-9])
        cylinder(h=bz+20,d=boltd,$fn=50);
    }
}

difference() {
    translate([-edge/2,(-edge/2)-3, -0.75])
    clip();
    base();
    
}
