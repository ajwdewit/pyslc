        subroutine SLC2lib(option, nwl, optipar, soilspec, soilpar,
     +                     leafgreen,leafbrown,vegpar,ang,Rsoil,RTleaf,
     +                     Rcan,fvc)
c
c	Integrated Soil-Leaf-Canopy reflectance model with 2 layers	
c
c	Lib-version of the combined radiative transfer models 4SOIL, FLUSPECT
c	and 4SAIL2 for simulating the top-of-canopy BRDF in the optical 
c	spectral region (400 - 2400 nm).
c	The soil model is extended with the darkening effect due to moisture
c	after Heike Bach (1995) 
c
c	Wout Verhoef & Heike Bach
c
c	February 2004: First version
c
c	June 2004:		Add canopy absorption, fractional cover & conservative scattering
c
c	August 2004:	Support for 3 processing options, swap array dimensions
c						of 2D input and output arrays. Make spectral dimension variable
c
c    FORMAL PARAMETERS:  (I=input,O=output,C=control,IN=init,T=time)
c    name      type dimension meaning                                                 units  class
c    ----      ---- --------- -------                                                 -----  -----
c    OPTION     I4  (1)       Decimal mask, see comments line 108                       -      I
c    NWL        I4  (1)       Number of wavelengths                                     -      I
c    OPTIPAR    R4  (7,NWL)   Leaf optical parameters for each wavelength, see below           I
c                             * nr:    Refraction index of leaf tissue                  -
c                             * Kdm:   Specific absorption coeff. dry matter          cm2/g
c                             * Kab:   Specific absorption coeff. chlorophyll a+b     cm2/microgr.
c                             * Kw:    Specific absorption coeff. water                cm-1
c                             * Ks:    Specific absorption coeff. brown pigments        -
c                             * nrW:   Refraction index water in soil moisture model    -
c                             * H2Oabs Absorption coeff. water soil moisture model     cm-1
c    SOILSPEC   R4  (NWL)     Dry soil reflectance for each wavelength                  -      I
c                             or dry soil particle single scattering albedo
c    SOILPAR    R4  (5)       Soil parameters, see below                                       I
c                             * H_b:  b - Coefficient of phase function Legendre pol.  sr-1
c                             * H_c:  c - Coefficient of the Lengendre polynomial      sr-1
c                             * H_B0: Relative magnitude of the hotspot peak            -
c                             * H_h: Half width of the hotspot peak                     -
c                             * SM: Soil moisture content [0-1]                       cm3/cm3
c    LEAFGREEN  R4  (5)       Green leaf biochemical parameters, see below                     I
c                             * Cab: Chlorophyll AB content                          microgr/cm2
c                             * Cw:  Water content (EWT)                                cm
c                             * Cdm: Dry matter content                                g/cm2
c                             * Cs:  Senescent material                                 -
c                             * N:   Mesophyll structure                                -
c    LEAFBROWN  R4  (5)       Brown leaf biochemical parameters, see below                     I
c                             * Cab: Chlorophyll AB content                          microgr/cm2
c                             * Cw:  Water content (EWT)                                cm
c                             * Cdm: Dry matter content                                g/cm2
c                             * Cs:  Senescent material                                 -
c                             * N:   Mesophyll structure                                -
c    VEGPAR     R4  (8)       Vegetation Canopy parameters, see below                          I
c                             * LAI:    Total Leaf Area Index, brown+green              -
c                             * LIDFa:  Average leaf slope indicator [-1,+1]            -
c                             * LIDFb:  Bimodality parameter of lidf [-1,+1]            -
c                             * hot:    Hot spot effect parameter, estimated as ratio   
c                               of average leaf width and canopy height                 -
c                             * fB:     Fraction brown LAI [0,1]                        -
c                             * diss:   Dissociation factor [0,1]                       -
c                             * Cv:     Vertical crown coverage [0,1]                   -
c                             * zeta:   Tree shape factor (diameter/height)             -
c    ANG        R4  (3)       Angular Geometry                                                 I
c                             * tts: Solar zenith angle in degrees [0-90]               º
c                             * tto: Viewing zenith angle in degrees [0-90]             º
c                             * psi: Sun-view azimuth difference in degrees             º
c                               (relative azimuth difference absolute [0-180])
c    RSOIL      R4  (4,NWL)   Soil BRDF Outputs for each NWL, see below                        O
c                             * rddsoil: Bi-hemispherical reflectance                   -
c                               (should be equal to Rin)
c                             * rsdsoil: Diffuse reflectance for direct solar           -
c                               incidence
c                             * rdosoil: Directional reflectance for diffuse            -
c                               incidence                                          
c                             * rsosoil: Bidirectional reflectance                      -
c    RTLEAF     R4  (4,NWL)   Leaf BRDF outputs for each NWL, see below                        O
c                             * green leaf reflectance                                  -
c                             * green leaf transmittance                                -
c                             * brown leaf reflectance                                  -
c                             * brown leaf transmittance                                -
c    RCAN       R4  (6,NWL)	 Canopy BRDF output                                            O
c                             * rddt: diffuse reflectance for diffuse incidence         - 
c                             * rsdt: diffuse reflectance for direct solar incidence    -
c                             * rdot: directional reflectance for diffuse incidence     -
c                             * rsot: bidirectional reflectance                         -
c                             * alfadt: canopy absorption for sky radiation             -
c                             * alfast: canopy absorption for solar radiation           -
c    FVC        R4  (1)     Fractional vegetation cover (viewing direction)             -      O
c                                                              
c F2py compiler directives
Cf2py intent(hide), depend(soilspec) :: nwl = len(soilspec) 
Cf2py intent (in) option,optipar,soilspec,soilpar,leafgreen
Cf2py intent (in) leafbrown,vegpar,ang
Cf2py intent (out) Rsoil,RTleaf,Rcan,fvc

	integer*4 option,nwl,N
	real Kab,Kw,Kdm,Ks
	real optipar(7,nwl),soilspec(nwl),soilpar(5),leafgreen(5),
     +	  leafbrown(5),vegpar(8),ang(3)
	real Rsoil(4,nwl),RTleaf(4,nwl),Rcan(6,nwl),
     +	  refl(nwl),tran(nwl)
	logical YN(9)
c
	include 'SLC.h'
c
c	Determine selected options from decimal mask. Any non-zero digit selects 
c	the corresponding option. Currently three options are available.
c
c	Digit 1 (rightmost): If <> 0 then no Hapke BRDF model for the soil is applied
c				     (soilspec array contains Lambertian reflectances)
c	Digit 2		   : If <> 0 then no soil moisture effect modelling is applied
c	Digit 3		   : If <> 0 then skip leaf and canopy model (equivalent to LAI = 0)
c
	do i=1,9
		YN(i)=.false.
	end do
c
	N=option
	i=1
c
	do while (N.gt.0)
		YN(i)=(mod(N,10).gt.0)
		N=N/10
		i=i+1
	end do
c
c	Constants
c
	pi=datan(1.d0)*4.
	rd=pi/180. 
c
c	Reflectance and transmittance of green and brown leaf
c
	if (.not.YN(3)) then
c
		call fluspect(nwl,leafgreen,optipar,refl,tran)
c
		do iwl=1,nwl
			RTleaf(1,iwl)=refl(iwl)
			RTleaf(2,iwl)=tran(iwl)
		end do
c
		call fluspect(nwl,leafbrown,optipar,refl,tran)
c
		do iwl=1,nwl
			RTleaf(3,iwl)=refl(iwl)
			RTleaf(4,iwl)=tran(iwl)
		end do
c
	end if
c
c	Soil parameters (except omega)
c
	H_b =soilpar(1)
	H_c =soilpar(2)
	H_B0=soilpar(3)
	H_h =soilpar(4)
	SM  =soilpar(5)
c
c	Canopy parameters		
c
	LAI  =vegpar(1)
	LIDFa=vegpar(2)
	LIDFb=vegpar(3)
	hot  =vegpar(4)
	fB   =vegpar(5)
	diss =vegpar(6)
	Cv   =vegpar(7)
	zeta =vegpar(8)
c
c	Angular geometry	
c
	tts=ang(1)
	tto=ang(2)
	psi=ang(3)
c
c	Default cover = 0 requires canopy transmittance tooc = 1
c
	tooc=1.
c
c	Spectral loop
c
	do iwl=1,nwl
c
		H2Orefr=optipar(6,iwl)
		H2Oabs =optipar(7,iwl)
c
		if (YN(1)) then
c
c			Input was Lambertian reflectance
c
			rsdry=soilspec(iwl)
			rswet=rsdry
c
c			Soil moisture effect after Bach
c
			if (.not.YN(2)) then 
c			
				call soilwet(rsdry,rswet,SM,H2Orefr,H2Oabs)
c
			end if
c
			rddsoil=rswet
			rsdsoil=rswet
			rdosoil=rswet
			rsosoil=rswet
c
		else
c
c			Input was soil single scattering albedo
c
			omg=soilspec(iwl)
			hsqrt=sqrt( (1-omg) / (1+0.25*omg*H_b))
			rdd_dry = (1-hsqrt) / (1+hsqrt)
			omg_wet = omg	     
c
c			Soil moisture effect after Bach
c
	      if (.not.YN(2)) then
c			 
				call soilwet(rdd_dry,rdd_wet,SM,H2Orefr,H2Oabs)
c
				x=(1-rdd_wet)/(1+rdd_wet)
				x2=x*x
				omg_wet=(1-x2)/(1+.25*H_b*x2)
	
			end if
c
			call FourSoil(omg_wet,H_b,H_c,H_B0,H_h)
c
         endif
c
c		Collect soil BRDF outputs
c
		Rsoil(1,iwl)=rddsoil
		Rsoil(2,iwl)=rsdsoil
		Rsoil(3,iwl)=rdosoil
		Rsoil(4,iwl)=rsosoil
c
		rddt=rddsoil
		rsdt=rsdsoil
		rdot=rdosoil
		rsot=rsosoil
		alfadt=0
		alfast=0
c
		if (.not.YN(3)) then
c
			rg=RTleaf(1,iwl)
			tg=RTleaf(2,iwl)
			rb=RTleaf(3,iwl)
			tb=RTleaf(4,iwl)
c
c			Canopy reflectance
c
			call FourSAIL2
c
c			Collect canopy BRDF outputs
c
		end if
c
		Rcan(1,iwl)=rddt
		Rcan(2,iwl)=rsdt
		Rcan(3,iwl)=rdot
		Rcan(4,iwl)=rsot
		Rcan(5,iwl)=alfadt
		Rcan(6,iwl)=alfast
c										
	end do	
c
	fvc=1.-tooc
c
	return
	end 
