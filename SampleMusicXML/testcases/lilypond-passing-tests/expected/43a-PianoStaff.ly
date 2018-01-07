\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff{ % measure 1
\clef treble \key c \major \time 4/4 f'1  | 

 }

ponestafftwo = \new Staff{ % measure 1
\clef bass b,1  | 

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