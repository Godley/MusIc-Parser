\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "MusicXML Part" 
 } 
 } 
 } 
 }{\autoBeamOff % measure 1
\clef treble \key c \major \time 4/4 a'8[ c''8 
\ottava #2
 a'''8 
\ottava #0
\ottava #-2
 c8] b,8[ 
\ottava #0
\ottava #1
 a''8] a''8[ 
\ottava #0
\ottava #-1
 b16[ c'16]   \bar "|."

 }

<<\ponestaffone>>