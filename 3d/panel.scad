hight = 367;
width = 262;
base_thick = 3;
corner_D =18;
base_circ_device_d = 22 + 1;
button_r = 3.5;

window_h = 70;
window_w = 38;

therm_d = 48;
therm_h = 29;

pwm_h = 57;
pwm_w = 90;

main_disp_hight = 41;
main_disp_width = 97;

va_hight = 37;
va_width = 70;

axe1 = hight / 2 - 35;
axe2 = - hight / 2 + 30;
main_buttons_axe = axe1 - main_disp_hight / 2 - 20;

axe_displays = main_buttons_axe - window_h / 2 - 20 - therm_h / 2 ;

axe_left = main_disp_width / 2 + 10;
axe_right = - axe_left;

module helper_axesX(length = 1000, thickness = 0.5) {
    // Знак '%' делает всё содержимое модуля вспомогательным фоном

        // Ось X (Красная)
       % color("red") 
        translate([-length /2 , 0 , base_thick / 2])
            rotate([0, 90, 0]) 
                cylinder(h = length, r = thickness, $fn = 12);
}

module helper_axesY(length = 1000, thickness = 0.5) {
    // Знак '%' делает всё содержимое модуля вспомогательным фоном
       
        // Ось Y (Зеленая)
        % color("green") 
            translate([0, -length /2, base_thick / 2 ])
            rotate([-90, 0, 0]) 
            cylinder(h = length, r = thickness, $fn = 12);
}

module base( $fn=100) {
    
    color("gray")
    difference() {
        cube([hight, width, base_thick], center = true);
        translate([hight / 2, width/2, 0])
            cylinder( h = base_thick + 1, r = corner_D /2,  center = true);
        translate([ -hight / 2, -width/2, 0])
            cylinder( h = base_thick + 1, r = corner_D /2,  center = true);
        translate([ hight / 2, - width/2, 0])
            cylinder( h = base_thick + 1, r = corner_D /2,  center = true);
        translate([-hight / 2, width/2 ,0])
            cylinder( h = base_thick + 1, r = corner_D /2,  center = true);
    }
}

module keys() {
    up = 85;
    d = 26;
    right = 16;
    translate([hight / 2 - up, - width/2 + right, 0])
            cylinder( h = base_thick + 1, r = d /2,  center = true);
    
    translate([-hight / 2 + up, - width/2 + right, 0])
            cylinder( h = base_thick + 1, r = d /2,  center = true);
    
    translate([hight / 2 - up, - width/2 + right / 2, 0])
            cube( [d, right +1, base_thick + 1],  center = true);
    
    translate([- hight / 2 + up, - width/2 + right / 2, 0])
            cube( [d, right +1, base_thick + 1],  center = true);
}

module base_circ_device($fn=100) {
    cylinder( h = base_thick + 1, r = base_circ_device_d / 2, center = true );
}

module PhaseAlarms() {
    right = 50;
    translate([main_buttons_axe , - width/2 + right, 0])
            base_circ_device();
    
    translate([axe2, - width/2 + 28, 0])
            base_circ_device();
}


module main_display() {

    color("red")
        translate([ axe1, axe_left, 0])
            cube( [ main_disp_hight, main_disp_width, 4 ], center = true );
}

module VoltAmper_display_base() {

    cube( [ va_hight, va_width, 4 ], center = true );
}

module VoltAmper_displays () {
    left = 20;
    translate([ axe1, -va_width /2 - 10, 0])
        VoltAmper_display_base();
    
    translate([axe2, -va_width /2 - 10, 0])
        VoltAmper_display_base();
}

module mainKey() {
    down = 11 + 7;
    right = 28;
    translate([axe1 , - width / 2+ right, 0])
            base_circ_device();   
}

module termometer() {

    translate([main_buttons_axe, -therm_d / 2 - 10, 0])
        cube( [therm_h, therm_d ,4 ], center = true);
}

module basic_button($fn=200) {
    cylinder( h = base_thick + 1, r = button_r, center = true );
}

module main_buttons()  {
    diff = 22;
    start = 10 + 4;
    for ( a = [ 0 : 1 : 2] ) {
        translate( [main_buttons_axe, axe_left + a * diff, 0])
            basic_button();
        
        translate( [main_buttons_axe, axe_left - a * diff, 0])
            basic_button();
    }
}



module display_windowBase() {
    cube([window_h, window_w, 4], center = true);
}

module displays() {
    diff = 4;
    translate([axe_displays, axe_right - window_w / 2- 4, 0])
        display_windowBase();
    
    translate([axe_displays, axe_right + window_w / 2+ 4, 0])
        display_windowBase();
}

module KettleControls() {
    h1 = axe_displays - window_w - base_circ_device_d/ 2 - 9;
    translate([ h1 , axe_right - window_w / 2- 4,0])
        base_circ_device();
    
    translate([ h1 , axe_right + window_w / 2 + 4,0])
        base_circ_device();
    
    h2 = h1 - base_circ_device_d - 10;
    
    translate([ h2 , axe_right - window_w / 2- 4,0])
        base_circ_device();
    
    translate([ h2 , axe_right + window_w / 2 + 4,0])
        base_circ_device();
    
    h3 = h2 - base_circ_device_d;
    translate([ h3 , axe_right ,0])
        base_circ_device();
    
    h4 = h3 - base_circ_device_d - 10;
    translate([ h4 , axe_right ,0])
        base_circ_device();
        
    axebuttons = axe_displays - window_h / 4;
    axe_btn_left =  axe_right + window_w  + 4 + 8;
    axe_btn_right =  axe_right - window_w  - 4 - 8;
    $fn=200;
    translate([ axebuttons + button_r + 2,  axe_btn_left, 0])
        basic_button();
        
    translate([ axebuttons - button_r - 2, axe_btn_left, 0])
        basic_button();
        
    translate([ axebuttons + button_r + 2, axe_btn_right, 0])
        basic_button();
        
        translate([ axebuttons - button_r - 2, axe_btn_right, 0])
        basic_button();
}

module pwm() {
    translate( [axe_displays, axe_left, 0 ] )
        cube([pwm_h, pwm_w, 4], center = true );
    
    h_controls = axe_displays - pwm_h / 2 - 17;
    
    d_button = 11;
    
    $fn=200;
    translate( [h_controls, axe_left + 15, 0 ] )
        cylinder( h = 4, r = d_button / 2, center = true);
    
    d_control = 6;
    translate( [h_controls, axe_left - 15, 0 ] )
        cylinder( h = 4, r = d_control / 2, center = true);
    
}

module 7segment() {
    translate([main_buttons_axe - 20,axe_left, 0])
        cube([20,51,4], center = true);
}

module axes() {

translate([0 ,0, 0])
    helper_axesY();

translate([0 ,0, 0])
    helper_axesX();

translate([axe1,0, 0])
    helper_axesY();

translate([axe2,0, 0])
    helper_axesY();

translate([main_buttons_axe ,0, 0])
    helper_axesY();

translate([0 , axe_left, 0])
    helper_axesX();

translate([0 , axe_right, 0])
    helper_axesX();

translate([axe_displays, 0, 0])
    helper_axesY();
}

module logo() {

translate([ - hight/4 - 5  , axe_left , -0.49 ] )
    rotate([0,0,-90])
    {
        include<logo.scad>;
    }
}

module windows() {
    
translate([axe_displays, axe_right + window_w / 2 + 4, 1.5 ] )
    rotate([0,180,-90])
    {
        Window_Package("MT", 9, "Gold", $fn=200);
    }

translate([axe_displays, axe_right - window_w / 2 - 4, 1.5] )
    rotate([0,180,-90])
    {
        Window_Package("HLT", 3, $fn=200);
    }    
}

use<Window.scad>;



module panel() {
difference() {
    base();
    main_display($fn=200);
    keys();
    PhaseAlarms();
    VoltAmper_displays();
    mainKey();
    main_buttons();
    termometer();
    displays();
    KettleControls();
    pwm();
    7segment();
}

}
axes();
//projection() 
    panel();
//logo();
//windows();




