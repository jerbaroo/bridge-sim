# Minimal shell model for testing.
#
# Units:
# 
#    1     2
#    o-----o
#    |     |
#    |     |
#  3 o-----o 4


wipe

model BasicBuilder -ndm 3 -ndf 6

node 1 0.0 0.0 0.0
node 2 1.0 0.0 0.0
node 3 0.0 1.0 0.0
node 4 1.0 1.0 0.0

# Supports
fix 3 1 1 1 1 1 1
fix 4 1 1 1 1 1 1


#geomTransf Linear 1 0 0 -1
#geomTransf Linear 2 0 1 0

# Cross-sections
section ElasticMembranePlateSection 1 2.00000e+8 0.2 0.1 0


# Shell elements
# ShellMITC4 Elements Definition: element ShellMITC4 $eleTag $iNode $jNode $kNode $lNode $secTag
element ShellMITC4 1 1 2 4 3 1


# Loading
timeSeries Linear 1

pattern Plain 1 1 {
load 2 0 0 1e3 0 0 0
}

system BandGeneral
numberer RCM
constraints Plain
integrator LoadControl 1
algorithm Linear
analysis Static

# Recorder
recorder Node -file shell_model_minimal_transl_z.out -node 1 2 3 4 -dof 3 disp

analyze 1

puts "Analysis done!"
print node 1
print node 2