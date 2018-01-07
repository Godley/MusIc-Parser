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
\clef treble \key c \major \time 2/4 \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {b'8[ b'8] \once \override TupletBracket.bracket-visibility = ##t
\tuplet 15/4 {b'8[ b'8 b'8 b'8  b'8]} b'8[  b'8]}  \bar "|."

 }

<<\ponestaffone>>