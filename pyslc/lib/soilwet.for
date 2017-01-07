C Programm berechnet feuchtes Spektrum aus trockenen und speichert es ab
C
C Berechnung von EffektivitÑt EFFEKT  aus empirischen Ansatz heraus
C EFFEKT = -1.2 * EXP(-18.53 * X) + 1.2
C X = optisch aktive (halbe) Schichtdicke in mm
C
C SCHMAX= Schichtdicke in doppelte Schicht und cm
c
c soilref,soilrefwet und soilmoisture sind dimensionslos
C
      subroutine soilwet(soilref,soilrefwet,soilmoisture,
     +				H2Orefr,H2Oabs)
C
C
      REAL soilref,SCHMAX,EFFEKT,ZBRECH,BBRECH,H2Orefr,H2Oabs
     +     soilrefwet,ZZHELP,soilmoisture

	integer bandnr

	schmax=((soilmoisture*100)-5)/60*0.028		! nach Abb.5.18 Diss

	EFFEKT = -1.2 * EXP(-18.53 * (SCHMAX * 5.) ) + 1.2 
	IF (EFFEKT.GT.1.) EFFEKT = 1.
C
C Brechungsindex des Bodens (kann variiert werden)
C     
      BBRECH = 2.
C
C ZBRECH = Brechungsindex
C
	ZBRECH = H2Orefr
C
C Brechung berechnen
C
c nach Lekner inclusive BerÅcksichtigung von EFFEKT:
c ZBRECH = Brechungsindex Wasser
c BBRECH = Brechungsindex Boden
c SOILREF = Reflexionswert dimensionlos Eingabe
c ZZHELP = Ergebnisreflexionswert nach BerÅcksichtigung der internen Reflexion
c EFFEKT   = Gewichtungsfaktor fÅr die Wirksamkeit der internen Reflexion 

	CALL BRECHL(ZBRECH,BBRECH,SOILREF,ZZHELP,EFFEKT)
C
C
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
C Absorption berechnen
C
C ZZHELP = Durch Brechung reduzierte Reflexion
C H2O_ABKO = Absorptionskoeffizient a
C SCHMAX = doppelte Schichtdicke s in cm
C Soilrefwet = Reflexion nach Absorption durch Wasser
C R(feucht)= R(Trocken) * Transmission T
C T = Transmission bei Wasserabsorpt. mit Schichtdicke s
C T = EXP (-a * s)
C
      soilrefwet = ZZHELP * (EXP((-1)*(H2Oabs*SCHMAX)) )
C	
c      WRITE(*,'(F8.2,I4,2F8.2)') soilmoisture,bandnr,soilref,soilrefwet
C
	RETURN
C
99	END
