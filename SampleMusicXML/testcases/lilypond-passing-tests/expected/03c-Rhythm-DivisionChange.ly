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
\clef treble \key c \major \time 4/4 c''4 c''4 c''4 c''4  | 

 % measure 2
c''2 c''2  \bar "|."

 }

<<\ponestaffone>>