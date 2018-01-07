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
\clef treble \key c \major \time 3/4 \tuplet 3/2 {a'8[\staccato  a'8\staccato   a'8]\staccato } \tuplet 3/2 {a'8[\staccato  a'8\staccato   a'8]\staccato } \tuplet 3/2 {a'8[\staccato  a'8\staccato   a'8]\staccato }  | 

 % measure 2
 \tuplet 3/2 {\repeat tremolo 2 g'8.}  \tuplet 3/2 {\repeat tremolo 2 g'8.}  \tuplet 3/2 {\repeat tremolo 2 g'8.}  | 

 % measure 3
 \tuplet 6/4 {\repeat tremolo 2 g'4.}  \tuplet 3/2 {\repeat tremolo 2 g'8.}  | 

 % measure 4
\tuplet 3/2 {f'8[ a'8  a'8\fp]}  \tuplet 6/4 {\repeat tremolo 2 a'4.}  | 

 % measure 5
 \tuplet 6/4 {\repeat tremolo 2 g'4.}  \tuplet 3/2 {\repeat tremolo 2 g'8.}  \bar "|."

 }

<<\ponestaffone>>