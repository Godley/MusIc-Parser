\version "2.18.2" 
\version "2.18.2" 
ponestaffone = \new Staff{ % measure 1
\clef treble \key c \major \time 4/4 c''4 \tempo 4=100 c''4 c''4 \tempo "Adagio" \longa=100 c''4  | 

 % measure 2
c''4 \tempo \markup {
	\concat {
		
			\smaller \general-align #Y #DOWN \note #"4" #1
				" = "
				\smaller \general-align #Y #DOWN \note #"2" #1
		
	}
} c''4 c''4 \tempo \markup {
	\concat {
		
			\smaller \general-align #Y #DOWN \note #"longa" #1
				" = "
				\smaller \general-align #Y #DOWN \note #"32" #1
		
	}
} c''4  | 

 % measure 3
c''4 \tempo \markup {
	\concat {
		(
			\smaller \general-align #Y #DOWN \note #"4" #1
				" = "
				\smaller \general-align #Y #DOWN \note #"2" #1
		)
	}
} c''4 c''4 \tempo "" 4=77 c''4  \bar "|."

 }

<<\ponestaffone>>