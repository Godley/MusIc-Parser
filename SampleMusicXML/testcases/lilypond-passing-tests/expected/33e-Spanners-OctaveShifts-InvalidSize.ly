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
\clef treble \key c \major \time 3/4 a'4 
\ottava #0
 a''''4 
\ottava #0
\ottava #-0
 c4   \bar "|."

 }

<<\ponestaffone>>