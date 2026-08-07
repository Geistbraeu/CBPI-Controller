module Window_Package(text, offset, color = "Silver") {

border_top = 5;
border_bottom = 4;

in_w = 36 + 0.5;
in_d = 34 * 2 + 0.5;

h= 1;
h2=4;

border_thin = 1;
overlap_thin = 2;
title = 10;
subtitle = 5;

w1= in_w + border_thin * 2;
d1= in_d + border_thin * 2;

d2 = d1 + overlap_thin*3  + title + subtitle ;
w2 = w1 + overlap_thin*2 ;

window_w = in_w;
window_d = 24;
window_h = 6;

module base( ) {
    color("black")
    {
        translate([0, title / 2, 0]) {
            cube([w2, d2, h], center = true);
        }
    
    

        translate([0,0,h2/2 + h/2])  {
            cube([w1,d1, h2 ],true);
        }
    }
    
    color(color)
        translate([w2/2 - offset , d2 / 2 - title - subtitle /2 - 1 , -h]) 
        {
           linear_extrude(height = 2, center = true)
            {
                rotate([0,180,0])
                text(text, direction="ltr", size=14, font = "Liberation Sans:style=Bold"); 
            }
        }
        
    color("yellow")
        translate([w2/2 - 1, -d2 / 2 + title / 2 + subtitle - 2 , -h]) 
        {
           linear_extrude(height = 2, center = true)
            {
                rotate([0,180,0])
                text("On", direction="ltr", font = "Liberation Sans:style=Bold", size = 5); 
            }
        }        
        
        color("yellow")
        translate([ -2, -d2 / 2 + title / 2 + subtitle - 2  , -h]) 
        {
           linear_extrude(height = 2, center = true)
            {
                rotate([0,180,0])
                text("Auto", direction="ltr", font = "Liberation Sans:style=Bold", size = 6); 
            }
        }        
}

module main() {
    
    difference() {
        base();
        color("blue")
        translate([0,0,h2/2 + h/2])   {
            cube([in_w,in_d, h2 + 1.01], true);
        }
    }
}

module window() {
    color("red")    
    cube([window_w,window_d,window_h], true);
}

difference() {
    main(); 
    translate([0, window_d /2 + border_bottom, 0]) {
        window();
    }
    translate([0, - window_d /2 - border_top, 0]) {
        window();
    }
    
}

}

Window_Package("MT", 9, "Gold");
//Window_Package("HLT", 3);