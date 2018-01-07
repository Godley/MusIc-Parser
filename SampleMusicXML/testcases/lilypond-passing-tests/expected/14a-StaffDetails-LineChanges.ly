\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Part 1" 
 } 
 } 
 } 
 }{ % measure 1
\key c \major d''1  | 

 % measure 2
d''1  | 

 % measure 3
d''1  | 

 }

ptwostaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Part 2" 
 } 
 } 
 } 
 }{ % measure 1
\key c \major g'1  | 

 % measure 2
g'2 g'2  | 

 % measure 3
g'2 g'2  | 

 }

<<\new StaffGroup <<\ponestaffone\ptwostaffone>>>>