\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "MusicXML Part" 
 } 
 } 
 } 
 }{ % measure 1
 \repeat volta 5 {\clef treble \key c \major \time 4/4 r1 }

 % measure 2
r1  \bar "|."

 }

<<\ponestaffone>>