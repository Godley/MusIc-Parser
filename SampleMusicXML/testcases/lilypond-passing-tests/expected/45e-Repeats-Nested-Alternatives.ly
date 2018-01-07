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
\clef treble \key c \major \time 4/4 r1 }

 % measure 2
\alternative {
{r1  \bar ":|."}

 % measure 3
{r1 }
}

 % measure 4
r1  | 

 % measure 5
 \repeat volta 2 {r1 }

 % measure 6
r1 }

 % measure 7
\alternative {
{r1  \bar ":|."}
}

 % measure 8
 \repeat volta 2 {r1  | 

 % measure 9
r1 }

 % measure 10
r1  \bar "|."

 }

<<\ponestaffone>>