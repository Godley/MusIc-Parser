\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff \with {
instrumentName = \markup { 

 \column { 


 \line { "MusicXML Part" 


 } 

 } 
 } 
 }{\autoBeamOff % measure 1
\clef treble \key c \major \time 5/4 \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8}  | 

 % measure 2
\once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8}  | 

 % measure 3
\once \override TupletBracket.bracket-visibility = ##f
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##f
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##f
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##f
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##f
\tuplet 3/2 {c''8 c''8  c''8}  | 

 % measure 4
\tuplet 4/3 {c''8 c''8 c''8  c''8} \tuplet 17/3 {c''8 c''8 c''8 c''8 c''8 c''8 c''8 c''8 c''8 c''8 c''8 c''8 c''8 c''8 c''8 c''8  c''8} c''8 c''8  \bar "|."

 }

<<\ponestaffone>>