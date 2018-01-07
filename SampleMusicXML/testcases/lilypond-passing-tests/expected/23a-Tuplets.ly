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
\clef treble \key c \major \time 14/4 \tuplet 3/2 {c'4 d'4  e'4} \tuplet 3/2 {f'4 g'4  a'4} \tuplet 3/2 {b'4 c''4  d''4} \tuplet 4/2 {e''4 f''4 g''4  a''4} \tuplet 4/1 {b''4 c'''4 c'''4  b''4} \tuplet 7/3 {a''4 g''4 f''4 e''4 d''4 c''4  b'4} \tuplet 6/2 {a'4 g'4 f'4 e'4 d'4  c'4}  \bar "|."

 }

<<\ponestaffone>>