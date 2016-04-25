//KD_BZ-3D_magnet_holder.scad
//09/02/2016    Kevin Donkers, Cronin Group, University of Glasgow
//OpenSCAD file creating a 3D model of a holder for two magnets to be attached at the end of a motor shaft
//All values in mm.

//Motor shaft paramters
shtshape = "cylinder";  //shaft shape
shtd=0.8;       //shaft diameter
shtl=4.5;       //shaft length

//Magnet parameters
magshape = "cylinder";  //magnet shape
magd = 2.1;       //magnet diameter (cylinder)
magh = 2;       //magnet height (cylinder)
magx = 1;       //magnet width (cube)
magy = 1;       //magnet length (cube)
magz = 1;       //magnet depth (cube)
mags = 1.5;       //magnet spacing

//Holder parameters
hldshape = "cylinder";  //holder shape
hldd = 7;           //holder diameter (cylinder)
hldh = 2.5;           //holder height (cylinder)
hldx = 4;           //holder width (cube)
hldy = 7;           //holder length (cube)
hldz = 2.5;           //holder depth (cube)

//Set translation parameters
x= hldshape=="cube" ? hldx : hldd;
y= hldshape=="cube" ? hldy : hldd;
z= hldshape=="cube" ? hldz : hldh;

//Construct 
difference(){
    //Holder
    if (hldshape=="cylinder"){
        translate([hldd/2,hldd/2,0])
        cylinder(h=hldh,d=hldd,center=false,$fn=100);
    }
    else if (hldshape=="cube"){
        cube([hldx,hldy,hldz],center=false);
    }
    //Magnets
    if (magshape=="cylinder"){
        translate([x/2,y/2-magd/2-mags/2,z-magh+0.1])
        cylinder(h=magh,d=magd,center=false,$fn=50);
        translate([x/2,y/2+magd/2+mags/2,z-magh+0.1])
        cylinder(h=magh,d=magd,center=false,$fn=50);
    }
    else if (magshape=="cube"){
        translate([x/2,y/2-magy/2-mags/2,z-magz/2+0.1])
        cube([magx,magy,magz],center=true);
        translate([x/2,y/2+magy/2+mags/2,z-magz/2+0.1])
        cube([magx,magy,magz],center=true);
    }
    //Shaft
    if (shtshape=="cylinder"){
        translate([x/2,y/2,-shtl+z+0.1])
        cylinder(h=shtl,d=shtd,center=false,$fn=50);
    }
}