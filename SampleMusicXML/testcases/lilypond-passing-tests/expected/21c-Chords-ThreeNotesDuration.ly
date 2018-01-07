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
\clef treble \time 4/4 <f' a' c''>4. <a' g''>8 <a' f' c''>4 <a' f' c''>4  | 

 % measure 2
<a' f' e''>4 <a' f' f''>4 <a' f' d''>2  | 

 }

<<\pzerostaffone>>