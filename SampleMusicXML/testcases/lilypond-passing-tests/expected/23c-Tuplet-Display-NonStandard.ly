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
\clef treble \key c \major \time 4/4 \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''4. c''4.  c''4.}  | 

 % measure 2
\once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''4. c''4.  c''4.}  | 

 % measure 3
\once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''4. c''4.  c''4.}  | 

 % measure 4
\once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''4. c''4.  c''4.}  | 

 % measure 5
\once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''8 c''8  c''8} \once \override TupletBracket.bracket-visibility = ##t
\tuplet 3/2 {c''4. c''4.  c''4.}  \bar "|."

 }

<<\ponestaffone>>