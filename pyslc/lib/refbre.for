C Berechnet Reflexion einer isotropisch beleuchteten OberflÑche aus 
C dem bekannten Realteil des Brechungsindex der OberflÑche;
C Gilt fÅr Brechungsindexe grî·er 1;
C Formel (8) aus Lekner, 1988
C
C Åbergeben werden mu· der Brechungsindex,
C zurÅckgegeben wird die Reflexion (dimensionslos)
C
	SUBROUTINE REFBRE(X,Y)

	IF(X.LT.1.) THEN
	  WRITE(*,12) 
12	  FORMAT(5x,'** FEHLER - au·erhalb Definitionsbereich **')
	  Y = 0.
	  RETURN
	ELSEIF(X.EQ.1) THEN
	  Y = 0.
	  RETURN
	ENDIF	

	Y1 = ( 3*X*X + 2*X + 1 )     / ( 3*(X+1)*(X+1) )
	Y2 = ( 2*X*X*X*(X*X+2*X-1) ) / ( (X*X+1)**2*(X*X-1) )
	Y3 = ( X*X*(X*X+1) )         / ( (X*X-1)**2 ) * LOG(X) 
	Y4 = ( X*X*(X*X-1)**2 )      / ( (X*X+1)**3 )
	Y5 = LOG ( ( X*(X+1) ) / ( X-1 ) )
	
	Y = Y1 - Y2 + Y3 - Y4 * Y5

	RETURN
	END
	