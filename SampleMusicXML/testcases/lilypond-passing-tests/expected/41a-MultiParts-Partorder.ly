\version "2.18.2" 
\version "2.18.2" 
pzerostaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Part 1" 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key g \major \time 4/4 c'4 r4 r2  | 

 }

ponestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Part 2" 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key g \major \time 4/4 e'4 r4 r2  | 

 }

ptwostaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Part 3" 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key g \major \time 4/4 g'4 r4 r2  | 

 }

pthreestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Part 4" 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key g \major \time 4/4 b'4 r4 r2  | 

 }

<<\pzerostaffone\ponestaffone\ptwostaffone\pthreestaffone>>