\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff{ % measure 1
\clef treble \key c \major \time 4/4 f'4 g'4 a'4 b'4 c''4  | 

 }

ponestafftwo = \new Staff{\autoBeamOff % measure 1
\clef bass a,8[ b,8] \once \override TupletBracket.bracket-visibility = ##f
\omit TupletNumber
\tuplet 3/2 {c8[ d8 e8]} a,16[ b,16 c16 d16] \once \override TupletBracket.bracket-visibility = ##f
\omit TupletNumber
\tuplet 3/2 {e16[ f16 g16 a16 b16 c'16]}  | 

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