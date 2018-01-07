\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Flute" 
 } 
 } 
 } 
shortInstrumentName = \markup { 
 \column { 
 \line { "Fl." 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key c \major \time 4/4 g'1\<   | 

 % measure 2
a'1\>   | 

 % measure 3
\alternative {
{c''1 }

 % measure 4
{g'1 }

 % measure 5
{a'1 }
}

 % measure 6

\ottava #1
 c'''1   | 

 % measure 7

\ottava #2
 b'''1   | 

 % measure 8

\ottava #-1
 a1   | 

 % measure 9

\ottava #-2
 g,1   | 

 % measure 10
f'1  | 

 % measure 11
e'1\trill\startTrillSpan
  | 

 % measure 12
d'1\sustainOn
   | 

 % measure 13
c'1\sustainOn
   | 

 % measure 14
\override TextSpanner.dash-fraction = 1.0 
r1
\startTextSpan
 
\stopTextSpan
 | 

 % measure 15
r1  | 

 % measure 16
r1  | 

 % measure 17
r1  | 

 % measure 18
r1  | 

 % measure 19
\break r1  | 

 % measure 20
r1  | 

 % measure 21
r1  | 

 % measure 22
r1  | 

 % measure 23
r1  | 

 % measure 24
\override TextSpanner.dash-fraction = 1.0 
r1
\startTextSpan
 
\stopTextSpan
 | 

 % measure 25
r1  | 

 % measure 26
r1  | 

 % measure 27
r1  | 

 % measure 28
r1  | 

 % measure 29
r1  | 

 % measure 30
r1  | 

 % measure 31
r1  | 

 % measure 32
r1  \bar "|."

 }

<<\ponestaffone>>