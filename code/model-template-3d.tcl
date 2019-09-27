wipe

model basic -ndm 3 -ndf 6

<<NODES>>

<<FIX>>

<<SUPPORTS>>

<<SECTIONS>>

<<ELEMENTS>>

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
