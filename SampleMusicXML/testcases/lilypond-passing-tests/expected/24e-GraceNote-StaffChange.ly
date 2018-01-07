\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff{\autoBeamOff % measure 25
\clef treble \key c \major \time 4/4 e''2 \grace { g''16[ a''16] }  e''2  | 

 }

ponestafftwo = \new Staff{\autoBeamOff % measure 25
\time 4/4  | 

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