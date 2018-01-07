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
\clef treble \key c \major \time 4/4 \repeat tremolo 2 a'8 \repeat tremolo 4 c''16 \repeat tremolo 8 e''32 g''4  | 

 % measure 2
\once \override TupletBracket.bracket-visibility = ##f
\omit TupletNumber
\tuplet 2/1 {\repeat tremolo 4 {g''16 a'16}} e''4 e''4  | 

 % measure 3
r1  | 

 % measure 4
r1  | 

 % measure 5
r1  | 

 % measure 6
r1  | 

 % measure 7
r1  | 

 % measure 8
r1  | 

 % measure 9
r1  | 

 % measure 10
r1  | 

 % measure 11
r1  | 

 % measure 12
r1  | 

 % measure 13
r1  | 

 % measure 14
r1  | 

 % measure 15
r1  | 

 % measure 16
r1  | 

 % measure 17
\break r1  | 

 % measure 18
\break r1  | 

 % measure 19
r1  | 

 % measure 20
r1  | 

 % measure 21
r1  | 

 % measure 22
r1  | 

 % measure 23
r1  | 

 % measure 24
r1  | 

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