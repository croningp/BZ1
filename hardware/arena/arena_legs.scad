leg();
translate([20,0,0])leg();
translate([20,20,0])leg();
translate([0,20,0])leg();

translate([0,40,0])spacers();
translate([20,40,0])spacers();
translate([20,60,0])spacers();
translate([0,60,0])spacers();


module leg() {
    cube([10,10,30]);
    translate([5,5,30])cylinder(h=60, d=4.5, $fn=20);
}

module spacers() {

    difference() {
        cube([10,10,13.5]);
        translate([5,5,-1])cylinder(h=20, d=7, $fn=20);
    }
}