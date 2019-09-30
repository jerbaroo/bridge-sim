<<INTRO>>

wipe

model basic -ndm 3 -ndf 6

<<DECK_NODES>>

<<SUPPORT_NODES>>

<<FIX_DECK>>

<<FIX_SUPPORTS>>

<<SECTIONS>>

<<DECK_ELEMENTS>>

<<SUPPORT_ELEMENTS>>

<<SUPPORTS>>

timeSeries Linear 1

pattern Plain 1 1 {
<<LOAD>>
}

system BandGeneral
numberer RCM
constraints Transformation
integrator LoadControl 1
algorithm Linear
analysis Static

<<RECORDERS>>

analyze 1
