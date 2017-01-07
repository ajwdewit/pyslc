c letzte énderungen : 21.11.97
c Brechnung der Abnahme der Reflexion einesr feuchten OberflÑche
c modifiziert nach Lekner, 1988 
c
	subroutine brechl(wbrech,bbrech,reftro,reffeu,step)
c
c uebergeben werden muss:
c wbrech = Brechungsindex Wasser
c bbrech = Brechungsindex Boden
c step = EffektivitÑt der internen Reflexion (0..1)
c reftro = Reflexion der trockenen BodenoberflÑche
c
c als Ergebnis zurÅckgegeben wird
c reffeu = Reflexion des feuchten Bodens
c
c Berechnung der mittleren isotropischen Reflexion der WasseroberflÑche
c Gleichung (8)
c
	call refbre(wbrech,rwquer)
c	write(*,*) 'wbrech, rwquer',wbrech,rwquer
c	
c
c bbrech = Brechungsindex des Bodens
c
	call refbre(bbrech,rbquer)
c	write(*,*) 'bbrech, rbquer',bbrech,rbquer
c
c
c hbrech = Hilfs-Brechungsindex 
c
	if (wbrech.ne.0) then
	  hbrech = bbrech / wbrech
	else
	  hbrech = bbrech
	endif
	call refbre(hbrech,rhquer)
c	write(*,*) 'hbrech, rhquer',hbrech,rhquer
c
c
c Berechnung von p unter BerÅcksichtigung des Korrekturgliedes 
c Gleichung (9)
c	
	p = 1 - ( (1 - rwquer) / (wbrech * wbrech) )	
c	write(*,*) 'p',p
c
c
c Berechnung der Reflexion der WasseroberflÑche bei senkrechten
C Einfallsstrahl vgl. Planet 
c	
	rl = (wbrech - 1) / (wbrech + 1)
	rl = rl * rl 
c	write(*,*) 'rl',rl
c
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
c
c
c a = Absorption der BodenoberflÑche
c
	  a = 1 - reftro
c
c Korrektur der Absorptions-Gleichung (11)
c
	  if (rbquer.eq.1.) then
	    write (*,*) '** FEHLER - Aw nicht korrigierbar **'
	    aw = a
	  else
	    yyhelp = (1-rhquer) / (1-rbquer)
	    zzhelp = ( (1-a) * yyhelp + a )
c
c mit step verÑndert
c
	    zzhelp = ( (zzhelp-1)*step + 1 ) 
c
	    aw =  zzhelp * a
c	    if (a.ne.0) write(*,*) ' ad, aw ',a,aw,aw/a
c	    write(*,*) step,yyhelp,a,aw
	  endif
c
c
c Berechnung von A/a (Gleichung (12))
c
c	  yy = ( 1 - p * (1-a) )**2
c	  if (yy.ne.0) z = ( (1-p) * (1-rl) ) / yy
c
c Gleichung (1)
c
c          aw
c z = -------------
c     1- p * (1-aw)
c
	  yy =  1 - p * (1-aw) 
c
c	  if (yy.ne.0) z = ( (1-rl) * aw)  / yy
c
c ohne BerÅcksichtigung des Faktors (1-rl)
c
	  if (yy.ne.0) z = aw / yy
c
c BerÅcksichtigung von STEP
c
	  z = ((z - a) * step) + a
c
c
c	
	reffeu = 1 - z
c	
	
	return
	end
	