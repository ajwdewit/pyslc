	subroutine fluspect(nwl,leafpar,optipar,refl,tran)
c
c	Modernised version of the PROSPECT leaf optics model of Jacquemoud & Baret.
c	This version was developed during the FLUMOD project (2003), in order to provide an extension 
c	to include leaf fluorescence. The version below does not include this, but it could easily
c	be inserted by means of a doubling routine.
c
c	Included here are a simplified calculation of the exponential integral (function expint1), 
c	the function "tav", and the treatment of the Stokes-equations. The present solution also
c	intercepts the case of zero absorption. 
c
c	Wout Verhoef
c	March 2004
c
         !DEC$ ATTRIBUTES DLLEXPORT :: fluspect
c
	implicit real*8 (a-z)
	integer*4 iwl,nwl
	real leafpar(5),optipar(7,nwl),refl(nwl),tran(nwl)
	real*8 expint1,tav
c
	Cab=leafpar(1)
	Cw =leafpar(2)
	Cdm=leafpar(3)
	Cs	=leafpar(4)
	N  =leafpar(5)
c
	do iwl=1,nwl
c
		nr	=optipar(1,iwl)
		Kdm=optipar(2,iwl)
		Kab=optipar(3,iwl)
		Kw =optipar(4,iwl)
		Ks =optipar(5,iwl)		
c
		Kall=(Cab*Kab+Cdm*Kdm+Cw*Kw+Cs*Ks)/N
		kChlrel=0.
		if (Kall>0) then kChlrel=Cab*Kab/(Kall*N)
c
		tau=1.
		if (Kall>0.) then 
			t1=(1.d0-Kall)*dexp(-Kall)
			t2=Kall*Kall*expint1(Kall)
			tau=t1+t2
		end if
c
c		Properties of the elementary layer
c
		talf=tav(59.d0,nr)
		ralf=1.-talf
		t12=tav(90.d0,nr)
		r12=1.-t12
		t21=t12/(nr*nr)
		r21=1.-t21
c
c		Top layer
c
		denom=1.-r21*r21*tau*tau
		Ta=talf*tau*t21/denom
		Ra=ralf+r21*tau*Ta
c
c		Deeper layers
c
		t=t12*tau*t21/denom
		r=r12+r21*tau*t
c
c		Stokes equations to compute properties of next N-1 layers (N real)
c
		if (r+t<1.) then
c
c			Normal case
c
			D=dsqrt((1+r+t)*(1+r-t)*(1-r+t)*(1-r-t))
			rq=r*r
			tq=t*t
			a=(1+rq-tq+D)/(2*r)
			b=(1-rq+tq+D)/(2*t)
c
			bNm1=b**(N-1)
			bN2=bNm1*bNm1
			a2=a*a
			denom=a2*bN2-1
			Rsub=a*(bN2-1)/denom
			Tsub=bNm1*(a2-1)/denom
c
		else
c
c			Case of zero absorption
c
			Tsub=t/(t+(1.-t)*(N-1))
			Rsub=1.-Tsub
c
		end if
c
c		Reflectance and transmittance of the leaf: combine top layer with next N-1 layers
c
		denom=1.-Rsub*r
c
		tran(iwl)=Ta*Tsub/denom
		refl(iwl)=Ra+Ta*Rsub*t/denom

c		Fluorescence calculation by doubling method (not activated yet)

c        eps = 2.**(-ndub)
c        do iex = 1,351
c			lamex = 400.+iex-1
c			j1 = float(iex)*nwl/2000.
c			ke = k(j1)
c			kC = kChl(j1)
c			se = s(j1)
c			te = 1.-(ke+se)*eps
c			re = se*eps
c			do ifl = 1,201
c				lamfl = 640.+ifl-1
c				j2 = float(ifl+240)*nwl/2000.
c				kf = k(j2)
c				sf = s(j2)
c				tf = 1.-(kf+sf)*eps
c				rf = sf*eps
        
c				Apply sigmoid function to suppress anti-Stokes fluorescence
        
c				sigmoid=1./(1.+exp((lamex-lamfl)/5.))
        
c				f=Phi(lamfl)*kC*eps*0.5*sigmoid				!Function to be provided elsewhere!
c				g=f
        
c				This is the doubling loop
        
c				do idub=1,ndub
c					xe=te/(1.-re*re)
c					tne=te*xe
c					rne=re*(1.+tne)
c					xf=tf/(1.-rf*rf)
c					tnf=tf*xf
c					rnf=rf*(1.+tnf)
c					fn=f*(xe+xf)+g*xe*xf*(re+rf)
c					gn=g*(1.+xe*xf*(1.+re*rf))+f*(xe*re+xf*rf)
c					te=tne
c					re=rne
c					tf=tnf
c					rf=rnf
c					f=fn
c					g=gn
c				end do
        
c				'Check ratio of numerical and analytical results for r & t
c				'(for debugging only)
        
c				rat1 = re / refl(j1)
c				rat2 = te / tran(j1)
        
c				'Store the results
         
c				fmat(iex,ifl)=f
c				gmat(iex,ifl)=g
c			end do

c		end do

	end do
c
	return
	end
	

	real*8 function expint1(u)
c
	implicit real*8 (a-z)
c
	u2=u*u
	u3=u2*u
	u4=u3*u
	u5=u4*u
c
	if (u<=1.) then
c
		expint1=-0.57721566+0.99999193*u-0.24991055*u2+0.05519968*u3
     +			  -0.00976004*u4+0.00107857*u5-dlog(u)
c
	else
c
		expint1=dexp(-u)*(u4+8.5773287401*u3+18.059016973*u2
     +		     +8.6347608925*u+0.2677737343)/(u4+9.5733223454*u3
     +			  +25.6329561486*u2+21.0996530827*u+3.9584969228)/u
     	end if
c
	return
	end		
	

	real*8 function tav(alfa,nr)
c
	implicit real*8 (a-z)
c
	pi=datan(1.d0)*4.0
	rd=pi/180.
c
	n2=nr*nr
	np=n2+1
	nm=n2-1
	a=(nr+1)*(nr+1)/2.
	k=-(n2-1)*(n2-1)/4.
	sa=dsin(alfa*rd)
c
	if (alfa==0) then
		f=4.*nr/((nr+1)*(nr+1))
	else
		if (alfa==90.) then
			b1=0.
		else
			b1=dsqrt((sa*sa-np/2)*(sa*sa-np/2)+k)
		end if
		b2=sa*sa-np/2
		b=b1-b2
		b3=b*b*b
		a3=a*a*a
		ts=(k*k/(6*b3)+k/b-b/2)-(k*k/(6*a3)+k/a-a/2)
		tp1=-2*n2*(b-a)/(np*np)
		tp2=-2*n2*np*dlog(b/a)/(nm*nm)
		tp3=n2*(1./b-1./a)/2
		tp4=16*n2*n2*(n2*n2+1)*dlog((2*np*b-nm*nm)/(2*np*a-nm*nm))
     +		 /(np*np*np*nm*nm)
         tp5=16*n2*n2*n2*(1./(2*np*b-nm*nm)-1./(2*np*a-nm*nm))
     +		 /(np*np*np)							 
		tp=tp1+tp2+tp3+tp4+tp5
		tav=(ts+tp)/(2*sa*sa)
	end if
c
	return
	end