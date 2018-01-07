\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff{ % measure 25
\clef treble \grace { e''2   g''16(} e''2)  | 

 }

ponestafftwo = \new Staff{ % measure 25
\key c \major \time 4/4  | 

 }

<<\new StaffGroup \with {
instrumentName = \markup { 
 \column { 
 \line { "MusicXML Part" 
 } 
 } 
 } 
 }<<\ponestaffone
\ponestafftwo>>>>