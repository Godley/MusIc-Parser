\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff{\autoBeamOff % measure 1
\clef treble  \time 4/4 << % voice 1
\new Voice = "one"
{\voiceOne c'4 c'4 } % voice 2
\new Voice = "two"
{\voiceTwo a4 a4 }>> | 

 }

<<\ponestaffone>>