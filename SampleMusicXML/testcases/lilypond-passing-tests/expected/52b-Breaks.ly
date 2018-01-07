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
\time 4/4 c''1  | 

 % measure 2
\break c''1  | 

 % measure 3
\pageBreak c''1  | 

 }

<<\ponestaffone>>