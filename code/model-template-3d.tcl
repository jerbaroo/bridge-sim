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

analyze 1
