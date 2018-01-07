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
\clef treble \key c \major \time 4/4 r1  | 

 % measure 2
r1  | 

 % measure 3
r1  | 

 % measure 4
r2 r4 r8 r16 r32 r64 r128 r128  | 

 % measure 5
r2. r4  | 

 % measure 6
r4. r8. r16. r32. r64. r128.  \bar "|."

 }


\header {
title = "Rest unit test"

}<<\ponestaffone>>