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

module clip(){
    difference(){
        cube([60, (edge/2)+8, 25]);
        #translate([0,0,15])cube([60, (edge/2)+3, 15]);
        translate([0,-5,15])cube([10, 50, 15]);
        translate([50,-5,15])cube([10, 50, 15]);
        translate([25,30,10])rotate([60,0,0])cylinder(h=50,d=6, $fn=20);
        translate([35,30,10])rotate([60,0,0])cylinder(h=50,d=6, $fn=20);
        translate([45,30,10])rotate([60,0,0])cylinder(h=50,d=6, $fn=20);
        translate([15,30,10])rotate([60,0,0])cylinder(h=50,d=6, $fn=20);
        translate([4,9,-12])rotate([0,0,0])cylinder(h=50,d=5, $fn=20);
        translate([56,9,-12])rotate([0,0,0])cylinder(h=50,d=5, $fn=20);
    }
}

difference() {
    translate([(ax+edge)/2, -3, -0.75])
    clip();
    cube([ax+edge,ay+edge,bz+1]);
    
}