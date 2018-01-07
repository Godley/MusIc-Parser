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
 }{\autoBeamOff % measure 1
\clef treble \key c \major \time 4/4 \once \override TupletBracket.bracket-visibility = ##t
\tuplet 2/2 {c''2 c''2}}  | 

 % measure 2
\once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {b'4 b'4 a'4} \once \override TupletBracket.bracket-visibility = ##f
\tuplet 4/4 {b'16[ b'16 b'16 b'16]} \once \override TupletBracket.bracket-visibility = ##f
\tuplet 5/4 {b'64[ b'64 b'64 b'64 a'64]}} r16 r8  | 

 % measure 3
\once \override TupletBracket.bracket-visibility = ##t
\tuplet 6/4 {a'4 c''4 b'4 b'4 b'4 b'4}}  | 

 % measure 4
\once \override TupletBracket.bracket-visibility = ##t
\tuplet 7/4 {c''4 g'4 c''4 e''4 c''4 c''4 a'4}}  | 

 % measure 5
\once \override TupletBracket.bracket-visibility = ##f
\tuplet 8/8 {b'8[ b'8 c''8 d''8 e''8 d''8 c''8 b'8]}}  | 

 % measure 6
\break \once \override TupletBracket.bracket-visibility = ##f
\tuplet 9/8 {d''8[ b'8 d''8 c''8 e''8 c''8 b'8 a'8 a'8]}}  | 

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
r1  | 

 % measure 18
r1  | 

 % measure 19
r1  | 

 % measure 20
r1  | 

 % measure 21
r1  | 

 % measure 22
\break r1  | 

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