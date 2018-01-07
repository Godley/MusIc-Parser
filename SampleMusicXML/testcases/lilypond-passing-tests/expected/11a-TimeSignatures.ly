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
\clef treble \key c \major \time 2/2 c''1  | 

 % measure 2
\time 4/4 c''1  | 

 % measure 3
\time 2/2 c''1  | 

 % measure 4
\time 3/2 c''1.  | 

 % measure 5
\time 2/4 c''2  | 

 % measure 6
\time 3/4 c''2.  | 

 % measure 7
\time 4/4 c''1  | 

 % measure 8
\time 5/4 c''1~ c''4  | 

 % measure 9
\time 3/8 c''4.  | 

 % measure 10
\time 6/8 c''2.  | 

 % measure 11
\time 12/8 c''1.  \bar "|."

 }

<<\ponestaffone>>