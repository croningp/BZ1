//cube([10,10,30]);
//translate([5,5,30])cylinder(h=50, d=4.5, $fn=20);

difference() {
    cube([10,10,13]);
    translate([5,5,-1])cylinder(h=15, d=6, $fn=20);
}