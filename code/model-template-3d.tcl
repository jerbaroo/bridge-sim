wipe

model basic -ndm 3 -ndf 6

<<NODES>>

<<SUPPORTS>>

geomTransf Linear 1

<<MATERIALS>>

<<SECTIONS>>

<<ELEMENTS>>

timeSeries Linear 1

pattern Plain 1 1 {
<<LOAD>>
}

system BandGeneral
numberer RCM
constraints Plain
<<TEST>>
<<ALGORITHM>>
<<INTEGRATOR>>
analysis Static

<<RECORDERS>>

analyze 1
