\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Flute" 
 } 
 } 
 } 
shortInstrumentName = \markup { 
 \column { 
 \line { "Fl." 
 } 
 } 
 } 
 }{ % measure 1
\clef treble \key c \major \time 4/4 a'1  | 

 % measure 2
c''1 ^\markup { "blablabla"  }  | 

 % measure 3
d'1  | 

 % measure 4
b'1  | 

 % measure 5
d''1 \mark #2  | 

 % measure 6
b''1  | 

 % measure 7
b'1  | 

 % measure 8
r1  | 

 % measure 9
r1  | 

 % measure 10
r1  | 

 % measure 11
r1  | 

 % measure 12
r1  | 

 % measure 13
r1  | 

 % measure 14
r1  | 

 % measure 15
r1  | 

 % measure 16
r1  | 

 % measure 17
r1  | 

 % measure 18
r1  | 

 % measure 19
r1  | 

 % measure 20
\break r1  | 

 % measure 21
r1  | 

 % measure 22
r1  | 

 % measure 23
r1  | 

 % measure 24
r1  | 

 % measure 25
r1  | 

 % measure 26
r1  | 

 % measure 27
r1  | 

 % measure 28
r1  | 

 % measure 29
r1  | 

 % measure 30
r1  | 

 % measure 31
r1  | 

 % measure 32
r1  \bar "|."

 }


\header {
title = "Hello Friends"
composer = "Charlotte Godley"

}\markuplist {
\vspace #0.5

\general-align #Y #UP
 \abs-fontsize #12.0 "Charlotte Godley"  }<<\ponestaffone>>