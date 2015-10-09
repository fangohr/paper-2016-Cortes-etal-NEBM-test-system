#include "colors.inc"
#include "metals.inc"
#include "screen.inc"
#include "textures.inc"
global_settings { assumed_gamma 1.6 }
background { color Black }
camera {
    // The center is at <0.5, 5, 5>
    // We transformed the coordinates as:
    // x --> -z , y --> x, x --> y
    location <7, -8, 5>
    look_at <0, 5, 5>
    // Change the aspect ratio
    // right 9./16. * image_width / image_height
    up        1 * y
    right     2 * x
    // Angle is necessary for correcting the view
    angle 60
}
// Set_Camera(<CX,CY,CZ>, <LX,LY,LZ>, 15)
// Set_Camera_Aspect(4,3)
// Set_Camera_Sky(<0,10,0>)
light_source { <15, 0.5, 0.5> 
               color White
               spotlight
               point_at <0, 5, 5>
               tightness 20 
               radius 15
               falloff 30 
             }

#declare sscale0=0.35;
#declare rscale0=1.2;
#declare cscale0=3.54;
#declare cones0=1;
#declare spincolors0=0;
#declare spincolor0=pigment {color rgb < 0.1 0.1 0.1 >};
// Load the "spins" from the include file at the end:
// 3 coordinates, 3 spin directions, and rgb colour values
// from every row
#macro spins(cx, cy, cz, sx, sy, sz, rr, gg, bb)
union{
#if(cones0) cone {<cx + 0.5 * sx * sscale0, 
                   cy + 0.5 * sy * sscale0,
                   cz + 0.5 * sz * sscale0
                   >, 
                  sscale0 * 0.5,
                  <cx - 0.5 * sx * sscale0,
                   cy - 0.5 * sy * sscale0,
                   cz - 0.5 * sz * sscale0
                   >,
                  0.0
                  texture{ 
                        // Load the color giving rgb values
                        pigment { color rgb < rr, gg, bb > }
                        // We will make the cones to look like plastic
                        finish { specular 1 roughness 0.001 
                                 reflection{0 0.83 fresnel on metallic 0}
                                 ambient 0 diffuse 0.6 conserve_energy }  
                  }
                  interior{ ior 1.3 }
                  // normal {bumps 0.1 scale 0.01}
              }
    #end
}
#end

#if (SK)
    #include "skyrmion.inc"
#end
#if (FM)
    #include "ferromagnetic.inc"
#end
#if (DS)
    #include "destruction.inc"
#end
