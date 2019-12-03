<<INTRO>>

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
}

system BandGeneral
numberer RCM
constraints Transformation
<<INTEGRATOR>>
<<ALGORITHM>>
<<TEST>>
analysis Static

<<RECORDERS>>

# Array of each element's ID.
set l [list <<ELEM_IDS>>]
# Write internal forces to file.
set outfile [open "<<FORCES_OUT_FILE>>" w]

foreach i $l {
	# https://opensees.berkeley.edu/community/viewtopic.php?f=2&t=64527&p=110182&hilit=shellMITC4#p110182
	# [Nxx, Nyy, Nxy, Mxx, Myy, Mxy, Vxz, Vyz]
	set internal_force [eleResponse $i stresses]
	puts $outfile $internal_force
}
close $outfile

analyze 1
