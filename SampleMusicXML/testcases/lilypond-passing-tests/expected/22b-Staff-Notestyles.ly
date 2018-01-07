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
\clef treble \key c \major \time 4/4 a'4 a'4 c''4 a'4  | 

 % measure 2
c''4 
\hideNotes
a'4
\unHideNotes 
\hideNotes
c''4
\unHideNotes 
\hideNotes
c'4
\unHideNotes  | 

 % measure 3

\hideNotes
d'2
\unHideNotes g'2  \bar "|."

 }

<<\ponestaffone>>