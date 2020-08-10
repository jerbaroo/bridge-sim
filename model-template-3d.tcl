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

<<DECK_NODES>>

<<SUPPORT_NODES>>

<<FIX_DECK>>

<<FIX_SUPPORTS>>

<<DECK_SECTIONS>>

<<PIER_SECTIONS>>

<<DECK_ELEMENTS>>

<<PIER_ELEMENTS>>

<<SUPPORTS>>

timeSeries Linear 1

pattern Plain 1 1 {
<<LOAD>>
<<THERMAL_AXIAL_LOAD_DECK>>
<<THERMAL_MOMENT_LOAD_DECK>>
<<SELF_WEIGHT>>
}

<<FORCES>>

<<TRANS_RECORDERS>>

<<STRAIN_RECORDERS>>

system BandGeneral
numberer RCM
constraints Plain
<<INTEGRATOR>>
<<ALGORITHM>>
<<TEST>>
analysis Static

analyze 1

# Array of each element's ID.
set l [list <<ELEM_IDS>>]
# Write internal forces to file.
set outfile [open "<<FORCES_OUT_FILE>>" w]

foreach i $l {
	# https://opensees.berkeley.edu/community/viewtopic.php?f=2&t=64527&p=110182&hilit=shellMITC4#p110182
	# [Nxx, Nyy, Nxy, Mxx, Myy, Mxy, Vxz, Vyz]
	set internal_force [eleResponse $i stresses]
	puts $outfile $internal_force
	puts $outfile "\n"
}
close $outfile
