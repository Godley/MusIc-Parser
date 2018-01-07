\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff{\autoBeamOff % measure 84
\clef treble \key c \major \time 6/8 f'8[\staccato  d'8\staccato  b8]\staccato  \clef bass g8( f4)  | 

 % measure 85
\clef treble e''8[\staccato  c''8\staccato  g'8]\staccato  g'8( f'4)  | 

 }

ponestafftwo = \new Staff{\autoBeamOff % measure 84
\clef bass r8 g,8[\staccato  g,8]\staccato  g,8[( a,16[ g,16 fis,16 g,16])  \bar "||"

 % measure 85
<c e g c'>4 r8 r4 g8\staccato   | 

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