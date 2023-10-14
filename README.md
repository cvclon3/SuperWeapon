# SuperWeapon

A top secret weapon has been developed in a secret laboratory, which has only one function - it can shoot at a target. The laboratory in which this superweapon was created was super secret, and the tests of this weapon turned out to be no less secret. 

The target for shooting is set as a quadrilateral, with the coordinates of its vertices <b><i>M1(x1,y1), M2(x2,y2), M3(x3,y3), M4(x4, y4)</i></b>, and there is nothing particularly secret here.

But shooting from a super-secret weapon is conducted from a classified location on the polygon, which is defined as the intersection point of the lines <b><i>A1x+B1y+C1=0</i></b> and <b><i>A2x+B2y+C2=0</i></b>. 

The firing direction from a given launch point is carried out in the direction determined by the <b><i>a(m,n)</i></b>, which is rotated by the angle <b><i>α</i></b> using the rotation operator. 

It is known about the secret weapon that the velocity of the projectile flying out of its barrel is <b><i>v0</i></b>, and the angle of inclination of the barrel to the horizon <b><i>β</i></b>, the mass of the projectile is <b><i>q</i></b>. Shooting is carried out in an atmosphere having the following property – the resistance force of a moving projectile proportional to the cube of its velocity with a coefficient <b><i>k</i></b>. **If you forgot, we remind you that to solve this problem you will have to use a mathematical model of the movement of a body in the gravity field in the case of resistance of the medium (you will have to solve a differential equation).

Attention, question! It is necessary to determine whether the target will be hit under a given set of conditions (that is, whether the end point of the projectile trajectory will fall inside or on the boundary of the target). (This is a task marked "satisfactory").

The task is more complicated – to draw a graph with the trajectory of the projectile, a graph with its speed (depending on time), and also to make an illustration showing the location of the starting point, the target and the point of falling of the projectile. (this is for "good").

Superbonus on "excellent"

The developers of the superweapon are interested in how it will behave in real conditions, and they want to conduct a shooting simulation. To do this, we implement a random component – we assume that when pointing the barrel of a secret weapon fluctuates, while the direction of the barrel changes by a random value
<b><i>Δphi</i></b> from the interval <b><i>(-Δphi0, Δphi0)</i></b>, and the value <b><i>v0</i></b> changes by a random value the value of <b><i>Δv∈(-dv0,dv0)</i></b>. We collect information on the coordinates of the projectile hit in 100 experiments with a random shift of parameters, build a graph reflecting the dependence of the y coordinate of the point of incidence on the x coordinate of the point of incidence.
