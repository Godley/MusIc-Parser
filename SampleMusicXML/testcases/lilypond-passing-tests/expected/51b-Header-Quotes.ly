\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff \with {
instrumentName = \markup { 
 \column { 
 \line { "Staff "Test"" 
 } 
 } 
 } 
 }{ % measure 1
r1  \bar "|."

 }


\header {
title = "\"Quotes\" in header fields"
composer = "Some \"Tester\" Name"
tagline = "Free for anyone (\"Public Domain\") "
}<<\ponestaffone>>