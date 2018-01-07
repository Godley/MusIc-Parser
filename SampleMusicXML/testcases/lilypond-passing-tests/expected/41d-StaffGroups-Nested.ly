\version "2.18.2" 
\version "2.18.2" 
ptwostaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "MusicXML Part" 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key c \major \time 4/4 a'1  | 

 % measure 2
a'1  | 

 % measure 3
r1  \bar "|."

 }

pfourstaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "MusicXML Part" 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key c \major \time 4/4 f'1  | 

 % measure 2
b'1  | 

 % measure 3
r1  \bar "|."

 }

pthreestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "MusicXML Part" 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key c \major \time 4/4 a'1  | 

 % measure 2
a'1  | 

 % measure 3
r1  \bar "|."

 }

pfourstaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "MusicXML Part" 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key c \major \time 4/4 f'1  | 

 % measure 2
b'1  | 

 % measure 3
r1  \bar "|."

 }

ponestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "MusicXML Part" 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key c \major \time 4/4 b'1  | 

 % measure 2
a'1  | 

 % measure 3
r1  \bar "|."

 }

pfivestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "MusicXML Part" 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key c \major \time 4/4 d''1  | 

 % measure 2
f'1  | 

 % measure 3
r1  \bar "|."

 }

<<\new StaffGroup <<\ptwostaffone\pfourstaffone\new StaffGroup <<\pthreestaffone\pfourstaffone>>>>\new StaffGroup <<>>\ponestaffone\pfivestaffone>>