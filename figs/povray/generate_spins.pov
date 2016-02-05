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
    // so the film plane is in the XZ plane now (with a left
    // handed system)
    location <7, -8, 5>
    look_at <0, 5, 5>
    // Change the aspect ratio
    up        1 * y
    right     2 * x

    // The angle keyword followed by a float expression specifies the
    // (horizontal) viewing angle in degrees of the camera used 
    // (from Povray Documentation)
    angle 60
}
light_source { <15, 0.5, 0.5> 
               color White
               spotlight
               point_at <0, 5, 5>
               tightness 20 
               radius 15
               falloff 30 
             }

#declare scalesize=0.35;
// Load the "spins" from the include file at the end:
// 3 coordinates, 3 spin directions, and rgb colour values
// from every row
#macro spins(cx, cy, cz, sx, sy, sz, rr, gg, bb)
union{
cone {<cx + 0.5 * sx * scalesize, 
      cy + 0.5 * sy * scalesize,
      cz + 0.5 * sz * scalesize
      >, 
      scalesize * 0.5,
      <cx - 0.5 * sx * scalesize,
       cy - 0.5 * sy * scalesize,
       cz - 0.5 * sz * scalesize
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
      // normal {bumps 0.1 scalesize 0.01}
      }

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
