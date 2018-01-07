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
 \repeat volta 2 {\clef treble \key c \major \time 4/4 r1 }

 % measure 2
\alternative {
{r1  \bar ":|."}

 % measure 3
{r1  | 

 % measure 4
r1  | 

 % measure 5
r1 }

 % measure 6
{r1 }
}

 % measure 7
r1  | 

 % measure 8
r1  | 

 % measure 9
r1 }

 % measure 10
\alternative {
{r1 }

 % measure 11
{r1 }
}

 % measure 12
r1  \bar "|."

 }

<<\ponestaffone>>