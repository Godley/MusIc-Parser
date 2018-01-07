\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Trumpet in Bb" 
 } 
 } 
 } 
shortInstrumentName = \markup { 
 \column { 
 \line { "Bb Tpt." 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key d \major \time 4/4 d'4 e'4 fis'4 g'4  | 

 % measure 2
a'4 b'4 cis''4 d''4  \bar "|."

 }

ptwostaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Horn in Eb" 
 } 
 } 
 } 
shortInstrumentName = \markup { 
 \column { 
 \line { "Hn." 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key a \major \time 4/4 a'4 b'4 cis''4 d''4  | 

 % measure 2
e''4 fis''4 gis''4 a''4  \bar "|."

 }

pthreestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Piano" 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key c \major \time 4/4 c'4 d'4 e'4 f'4  | 

 % measure 2
g'4 a'4 b'4 c''4  \bar "|."

 }

<<\ponestaffone\ptwostaffone\pthreestaffone>>