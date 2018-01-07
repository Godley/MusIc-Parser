\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff{ % measure 1
\clef treble \key c \major \time 4/4 c''4\ffff b'4 a'4 g'4\p  | 

 % measure 2
\key d \major a'4 b'4 cis''4 d''4  | 

 % measure 3
\clef mezzosoprano d''4 cis''4 b'4 a'4  | 

 % measure 4
r1  | 

 }

ponestafftwo = \new Staff{ % measure 1
\clef bass a,4\< b,4 c4 d4  | 

 % measure 2
\clef treble \key d \major fis'4 g'4 a'4 b'4  | 

 % measure 3
a'4 b'4 cis''4 d''4  | 

 % measure 4
r0  \bar "|."

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