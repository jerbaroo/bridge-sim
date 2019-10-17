# Minimal shell model for testing.
#
# Units:
#  length [m]
#  force  [N]
#
#
#  ^ y
#  |
#  |
#  0---> x
#
#
#	 7     8     9
#    o-----o-----o
#    |     |     |
#    |     |     |
#    o-----o-----o
#    |4    |5    |6
#    |     |     |
#    o-----o-----o 
#    1     2     3


wipe


model BasicBuilder -ndm 3 -ndf 6


# Nodes
<<NODE>>


# Supports
<<SUPPORT>>


# Material
# nDMaterial ElasticIsotropic $matTag $E $v <$rho>
# nDMaterial ElasticIsotropic 1 1.00000e+6 0.2

# Cross-sections
# section ElasticMembranePlateSection $secTag $E $nu $h $rho
section ElasticMembranePlateSection 1 1.00000e+6 0.2 0.1 0
# section PlateFiber $secTag $matTag $h
# section PlateFiber 1 1 0.1


# Shell elements
# ShellMITC4 Elements Definition: element ShellMITC4 $eleTag $iNode $jNode $kNode $lNode $secTag
<<ELEMENT>>


# Loading
timeSeries Linear 1


pattern Plain 1 Linear {
<<LOAD>>
}


# Recorder
# Recorder
recorder Node -file <<MODEL_NAME>>_transl_x.out -nodeRange 1 <<TOT_NODE_NR>> -dof 1 disp
recorder Node -file <<MODEL_NAME>>_transl_y.out -nodeRange 1 <<TOT_NODE_NR>> -dof 2 disp
recorder Node -file <<MODEL_NAME>>_transl_z.out -nodeRange 1 <<TOT_NODE_NR>> -dof 3 disp
# the line below does not work for me (produces only zeros) that's why the eleResponse approach at the bottom of this file
recorder Element -file <<MODEL_NAME>>_internal_force1.out -eleRange 1 <<TOT_ELEM_NR>> stresses

# are these the forces between nodes?
recorder Element -file <<MODEL_NAME>>_force.out -eleRange 1 <<TOT_ELEM_NR>> forces

# https://opensees.berkeley.edu/community/viewtopic.php?f=2&t=64252&p=109351&hilit=ShellMITC4#p109351
# [eps11, eps22, gamma12, theta11, theta22, theta33, gamma13, gamma23]
recorder Element -file <<MODEL_NAME>>_strain_integrationpoint=1.out -eleRange 1 <<TOT_ELEM_NR>> material 1 deformation
recorder Element -file <<MODEL_NAME>>_strain_integrationpoint=2.out -eleRange 1 <<TOT_ELEM_NR>> material 2 deformation
recorder Element -file <<MODEL_NAME>>_strain_integrationpoint=3.out -eleRange 1 <<TOT_ELEM_NR>> material 3 deformation
recorder Element -file <<MODEL_NAME>>_strain_integrationpoint=4.out -eleRange 1 <<TOT_ELEM_NR>> material 4 deformation

system BandGeneral
numberer RCM
constraints Plain
integrator LoadControl 1
algorithm Linear
analysis Static

analyze 1


print node 7
print node 8


# Write internal forces to file
set outfile [open "<<MODEL_NAME>>_internal_force.out" w]
for {set i 1} {$i <= <<TOT_ELEM_NR>>} {incr i}  {
	# https://opensees.berkeley.edu/community/viewtopic.php?f=2&t=64527&p=110182&hilit=shellMITC4#p110182
	# [Nxx, Nyy, Nxy, Mxx, Myy, Mxy, Vxz, Vyz]
	set internal_force [eleResponse $i stresses]
	puts $outfile $internal_force
}
close $outfile






