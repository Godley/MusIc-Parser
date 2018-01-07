\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "MusicXML Part" 
 } 
 } 
 } 
 }{ % measure 0
\clef treble \key c \major \time 4/4 \partial 4. e'4 e'8  | 

 % measure 1
f'4 g'4  \bar ""

 % measure X1
\partial 2 a'4 b'4  | 

 % measure 2
c''4 d''4 r4  \bar "|."

 }

<<\ponestaffone>>