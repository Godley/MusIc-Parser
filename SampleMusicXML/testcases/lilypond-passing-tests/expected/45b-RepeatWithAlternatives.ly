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
 \repeat volta 2 {\clef treble \key c \major \time 4/4 c''1 }

 % measure 2
\alternative {
{c''1  \bar ":|."}

 % measure 3
{c''1 }
}

 % measure 4
c''1  \bar "|."

 }

<<\ponestaffone>>