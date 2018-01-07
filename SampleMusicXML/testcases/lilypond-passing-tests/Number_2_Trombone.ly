\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Trombone" 
 } 
 } 
 } 
shortInstrumentName = \markup { 
 \column { 
 \line { "Trb." 
 } 
 } 
 } 
 }{\autoBeamOff % measure 1
\clef bass \key c \major \time 4/4 ees8 r2 r8 r8 ees8  | 

 % measure 2
d4 ees4 g8 r8 ees8 r8  | 

 % measure 3
d8 c4 r8 c4 g8[ ees8]~  | 

 % measure 4
ees4. c4. c4  | 

 % measure 5
g,8 ees,4. aes,4. bes,8  | 

 % measure 6
ees,1  | 

 % measure 7
\break d8[ d8 d8 d8] r8 f16[ f16] r8 bes,16[ bes,16]  | 

 % measure 8
r1  | 

 % measure 9
r1  | 

 % measure 10
r8 c8[ c8 c8] r8 g,8[ g,8 g,8]  | 

 % measure 11
r8 c8[ c8 c8] r8 g,8[ g,8 g,8]  | 

 % measure 12
r8 c8[ c8 c8] r8 g,8[ g,8 g,8]  | 

 % measure 13
\break r8 c8[ c8 c8] r8 g8[ g8 g8]  | 

 % measure 14
g,8 ees,4. aes,4. bes,8  | 

 % measure 15
ees,1  | 

 % measure 16
d8[ d8 d8 d8] r8 f16[ f16] r8 bes,16[ bes,16]  | 

 % measure 17
c1  | 

 % measure 18
c1  | 

 % measure 19
r1  | 

 % measure 20
r1  | 

 % measure 21
r1  \bar "|."

 }


\header {
title = "Number 2"
composer = "Daniel Turner"

}\markuplist {
\vspace #0.5

\general-align #Y #UP
 \abs-fontsize #12.0 "Trombone"  }<<\ponestaffone>>