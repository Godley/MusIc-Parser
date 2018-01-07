\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Clarinet in Eb" 
 } 
 } 
 } 
shortInstrumentName = \markup { 
 \column { 
 \line { "Eb Cl." 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key e \major \time 4/4 a'1  \bar "|."

 }

ptwostaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Clarinet in Bb" 
 } 
 } 
 } 
shortInstrumentName = \markup { 
 \column { 
 \line { "Bb Cl." 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key a \major \time 4/4 d''1  \bar "|."

 }

pthreestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Clarinet in A" 
 } 
 } 
 } 
shortInstrumentName = \markup { 
 \column { 
 \line { "A Cl." 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key bes \major \time 4/4 ees''1  \bar "|."

 }

pfourstaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Horn in F" 
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
\clef treble \key d \major \time 4/4 g''1  \bar "|."

 }

pfivestaffone = \new Staff \with {
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
\clef treble \key e \major \time 4/4 a''1  \bar "|."

 }

psixstaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "" }
 \line { "Piccolo Tr" }
 } 
 } 
shortInstrumentName = \markup { 
 \column { 
 \line { "Picc.Tpt." 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key bes \major \time 4/4 ees'1  \bar "|."

 }

psevenstaffone = \new Staff \with {
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
\clef treble \key a \major \time 4/4 d''1  \bar "|."

 }

peightstaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Trumpet in C" 
 } 
 } 
 } 
shortInstrumentName = \markup { 
 \column { 
 \line { "C Tpt." 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key g \major \time 4/4 c''1  \bar "|."

 }

pninestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Trumpet in D" 
 } 
 } 
 } 
shortInstrumentName = \markup { 
 \column { 
 \line { "D Tpt." 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key f \major \time 4/4 bes'1  \bar "|."

 }

ponezerostaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "displayed c'=fis'''" 
 } 
 } 
 } 
 }{ % measure 1
\clef "bass_8" \key cis \major \time 4/4 fis,,1  \bar "|."

 }

poneonestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "MusicXML Part" 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key g \major \time 4/4 c''1  \bar "|."

 }

<<\ponestaffone\ptwostaffone\pthreestaffone\pfourstaffone\pfivestaffone\psixstaffone\psevenstaffone\peightstaffone\pninestaffone\ponezerostaffone\poneonestaffone>>