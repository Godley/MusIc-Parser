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
\clef treble \key c \major \time 4/4 g'4( c''4)( a'4)( g'4)  | 

 % measure 2
g'4( c''4( a'4) g'4)  \bar "|."

 }

<<\ponestaffone>>