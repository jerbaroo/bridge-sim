# Programatically generated file.
#
# Units:
# - dimension: metre
# - force: newton
#
# Dimension order is
# - x: longitudinal
# - y: vertical
# - z: transverse

wipe

model basic -ndm 3 -ndf 6

# node nodeTag x y z
# Begin deck nodes
node 100 0 0 -16.6
node 101 11.575 0 -16.6
node 102 14.675 0 -16.6
node 103 26.875 0 -16.6
node 104 29.975 0 -16.6
node 105 35.0 0 -16.6
node 106 42.175 0 -16.6

node 200 0 0 -16.0
node 201 11.575 0 -16.0
node 202 14.675 0 -16.0
node 203 26.875 0 -16.0
node 204 29.975 0 -16.0
node 205 35.0 0 -16.0
node 206 42.175 0 -16.0

# fix nodeTag x y z rx ry rz
# Begin fixed deck nodes
fix 100 1 1 1 0 0 0
fix 106 1 1 1 0 0 0
fix 200 1 1 1 0 0 0
fix 206 1 1 1 0 0 0

# section ElasticMembranePlateSection secTag youngs_modulus poisson_ratio depth mass_density
# Begin deck sections
section ElasticMembranePlateSection 1 38400000000.0 0.2 0.75 0.002724

# element ShellMITC4 eleTag iNode jNode kNode lNode secTag
# Begin deck shell elements
element ShellMITC4 1 100 101 201 200 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2 101 102 202 201 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3 102 103 203 202 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 4 103 104 204 203 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 5 104 105 205 204 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 6 105 106 206 205 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2

timeSeries Linear 1

pattern Plain 1 1 {
# load nodeTag N_x N_y N_z N_rx N_ry N_rz
# Begin loads
load 104 0 100000 0 0 0 0
# End loads
}

# recorder Node -file out/node-y.out -node 100 101 102 103 104 105 -dof 2 disp

recorder Element -file out/forces.out -eleRange 100 105 forces

# recorder Node -file path -node nodeTags -dof direction disp
# Begin translation recorders
# End translation recorders

recorder Element -file out/strain1.out -eleRange 100 105 material 1 deformation
recorder Element -file out/strain2.out -eleRange 100 105 material 2 deformation
recorder Element -file out/strain3.out -eleRange 100 105 material 3 deformation
recorder Element -file out/strain4.out -eleRange 100 105 material 4 deformation

system BandGeneral
numberer RCM
constraints Plain
integrator LoadControl 1
algorithm Linear

analysis Static

analyze 1

print node 104