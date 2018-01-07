\version "2.18.2" 
\version "2.18.2" 
pzerostaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "MusicXML Part" 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \time 4/4 <a' fis' d'>4 r4\p \mark  \markup { \musicglyph #"scripts.segno" } r2  | 

 }

<<\pzerostaffone>>