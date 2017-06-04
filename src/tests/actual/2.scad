use <../../_fillygon.scad>
include <../../_settings.scad>

angle = 90;

render() intersection() {
    sector_3d(xmin=-side_length / 2);
    
    rotate([0, 0, -angle]) {
        sector_3d(xmin=-side_length / 2);
    }
    
    translate([-side_length, 0, 0]) {
        fillygon(
            angles=[angle],
            filled=false,
            filled_corners=false,
            gap=0.2,
            min_concave_angle=38.0,
            min_convex_angle=38.0,
            reversed_edges=[],
            $fn=8);
    }
}
