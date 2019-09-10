# Minimal rigid link model for testing.
#
# 
#    2     3
#    o------o
#    ||    ||
#    ||    ||
#  1 o     o 4

wipe

model BasicBuilder -ndm 2 -ndf 3

node 1 0.0 0.0 0.0
node 2 0.0 1.0 0.0
node 3 1.0 1.0 0.0
node 4 1.0 0.0 0.0


# Supports
fix 1 1 1 0
fix 4 1 1 0


# Geometric Transformation

geomTransf Linear 1

# Elastic Beam Column Definition
# element elasticBeamColumn $eleTag $iNode $jNode $A $E $Iz $transfTag <-mass $massDens> <-cMass>
element elasticBeamColumn    1    2    3    1e-2      3e+07   8.3333e-06    1   -mass        0

# Rigid link
# rigidLink $type $masterNodeTag $slaveNodeTag
rigidLink beam 1 2
rigidLink beam 4 3

# Loading
timeSeries Linear 1

pattern Plain 1 1 {
	load 2 1e3 0 0
}

system BandGeneral
numberer RCM
# constraints Plain
constraints Transformation
integrator LoadControl 1
algorithm Linear
analysis Static

# Recorder
recorder Node -file rigid_link_minimal_transl_x.out -node 1 2 3 4 -dof 1 disp

analyze 1

puts "Analysis done!"
print node 1
print node 2