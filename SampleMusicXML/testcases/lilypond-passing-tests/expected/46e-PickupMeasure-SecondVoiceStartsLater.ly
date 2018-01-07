\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff{ % measure 0
\partial 4 c''4  | 

 % measure 1
<< % voice 1
\new Voice = "one"
{\voiceOne c''4 a'4 f'4 c''4 } % voice 2
\new Voice = "two"
{\voiceTwo r4 c'4 }>> | 

 }

<<\ponestaffone>>