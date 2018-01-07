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
\clef treble \key c \major \time 16/4 c''\longa  | 

 % measure 2
c''\breve c''1 c''2 c''4 c''8 c''16 c''32 c''64 c''128 c''128  | 

 % measure 4
\time 24/4 c''\longa.  | 

 % measure 5
c''\breve. c''1. c''2. c''4. c''8. c''16. c''32. c''64. c''128. c''128.  | 

 % measure 6
\time 28/4 c''\longa..  | 

 % measure 7
c''\breve.. c''1.. c''2.. c''4.. c''8.. c''16.. c''32.. c''64.. c''64..  \bar "|."

 }

<<\ponestaffone>>