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
\clef treble \key c \major \time 4/4 <e'' 
\tweak #'style #'triangle
 c'' 
\tweak #'style #'slash
 a'>4 
\tweak #'style #'cross
 <e'' 
\tweak #'style #'square
 c'' a'>4\harmonic 
 <e'' 
\tweak #'style #'xcircle
 c'' \xNote a'>4 
 <e'' 
 c'' 
 a'>4  \bar "|."

 }

<<\ponestaffone>>