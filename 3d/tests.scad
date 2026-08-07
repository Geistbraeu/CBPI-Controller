
$fn = 100;

cube([90,145,1], center=true);

    color("Silver")
    linear_extrude(height = 2.5 )
        resize([0, 140, 0], auto=true)
            import("text_testss_contr.svg", center=true);