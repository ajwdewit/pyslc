	subroutine Foursoil (omeg,back,c,B0,h)
c
c	Four-stream soil reflectance computation based on Hapke's (1981) model
c
c	The multiple scattering contributions of Hapke's model have been modified in 
c	order to obtain outputs that are consistent with the assumed phase
c	function. This gives results that are different from Hapke's if parameter b is
c	not equal to zero. 
c
c	Inputs
c
c	omeg	: Soil single scattering albedo
c	back	: Phase function parameter b (controls backscatter/forescatter ratio)
c	c		: Phase function parameter c (controls depth of side scattering dip)
c	B0		: Hot spot relative amplitude (i.e. 0.2 gives 20% increase of reflectance)
c	h		: Half width of the hot spot peak
c	tts	: Solar zenith angle (deg)
c	tto	: Observation zenith angle	(deg)
c	psi	: Relative azimuth angle (deg)
c
c	Outputs
c
c	rddsoil	: Bi-hemispherical reflectance (should be equal to Rin)
c	rsdsoil	: Diffuse reflectance for direct solar incidence
c	rdosoil	: Directional reflectance for diffuse incidence
c	rsosoil	: Bidirectional reflectance
c
c	Wout Verhoef 
c	NLR	
c	July 2003
c		
	implicit integer (i-n), real (a-h,o-z)
c
	real ks,ko,m
c
	include 'SLC.h'
c
c	Angular geometry
c
	cts=cos(rd*tts)
	cto=cos(rd*tto)
	sts=sin(rd*tts)
	sto=sin(rd*tto)
	cps=cos(rd*psi)
	csd=cts*cto+sts*sto*cps
	if (csd.gt.1.) csd=1.
	del=acos(csd)
c
c	Phase function
c
	p=1.+back*csd+.5*c*(3*csd*csd-1)
c
c	Extinction and scattering coeffcients
c
	ks=1/cts
	ko=1/cto
	sigb=omeg*(1+.25*back)
	sigf=omeg*(1-.25*back)
	att=2.-sigf
	m=sqrt(att*att-sigb*sigb)
	rinf=0.
	if (omeg>0) rinf=(att-m)/sigb
c
	sb=omeg*(.5*ks+.25*back)
	sf=omeg*(.5*ks-.25*back)
	vb=omeg*(.5*ko+.25*back)
	vf=omeg*(.5*ko-.25*back)
c
c	Diffuse reflectances
c
	rddsoil=rinf	
	rsdsoil=(sb+sf*rinf)/(ks+m)
	rdosoil=(vb+vf*rinf)/(ko+m)
c
	w=omeg*p/(4*cts*cto)
c
c	Single and multiple contributions to bidirectional reflectance
c
	cor=B0/(1+tan(.5*del)/h)	
	rsosoils=w*(1+cor)/(ks+ko)
c
	rsosoild=((rdosoil*(sf+sb*rinf)+rsdsoil*(vf+vb*rinf))
     +        /(ks+ko)-rdosoil*rsdsoil*rinf)
     +		/(1-rinf*rinf)
c
	rsosoil=rsosoils+rsosoild
c
	return
	end