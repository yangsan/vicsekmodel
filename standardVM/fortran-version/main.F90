module agents
	implicit none

	type agent
		real::x
		real::y
		real::sinf
		real::cosf
	end type

end module


program SVM01
use agents
implicit none

	real::L
	real::t

	real::denominator

	integer::pattern(234,234)

	integer,parameter::N=300
	real,parameter::r=1.0
	real::nn

	real,parameter::v=0.03
	real::eta
	real::theta

	integer::i
	integer::j
	integer::k

	integer::time

	integer::cx
	integer::cy


	real::sinf
	real::cosf
	real::distance
	
	real::sumsinf
	real::sumcosf
	real::va



	type(agent)::fore(N)
	type(agent)::las(N)
	type(agent)::extra1(N)
	type(agent)::extra2(N)

	open(unit=10,file='SVM01.txt')
	call random_seed()


	L=7
    eta=2.0
	time=400


	nn=N

	pattern=0
	
	sumsinf=0
	sumcosf=0
	


	!give an initial configeration
	do i=1,N
		call random_number(t)
		fore(i)%x=t*L
		call random_number(t)
		fore(i)%y=t*L
		call random_number(t)
		fore(i)%sinf=t
		call random_number(t)
		fore(i)%cosf=t
		
		call random_number(t)
		if(t<0.5)then
			fore(i)%sinf=(-1)*fore(i)%sinf
		end if
		
		call random_number(t)
		if(t<0.5)then
			fore(i)%cosf=(-1)*fore(i)%cosf
		end if	

		denominator=sqrt(fore(i)%sinf**2+fore(i)%cosf**2)
		fore(i)%sinf=fore(i)%sinf/denominator
		fore(i)%cosf=fore(i)%cosf/denominator


	end do
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	!the simulation
	do k=1,time

		!the periodic boundary
		do i=1,N
			extra1(i)%x=-10
			extra1(i)%y=-10
			extra1(i)%sinf=0
			extra1(i)%cosf=0

			extra2(i)%x=-10
			extra2(i)%y=-10
			extra2(i)%sinf=0
			extra2(i)%cosf=0

			if(fore(i)%x<r .and. fore(i)%y<r)then
				extra2(i)%x=fore(i)%x+L
				extra2(i)%y=fore(i)%y+L
				extra2(i)%cosf=fore(i)%cosf
				extra2(i)%sinf=fore(i)%sinf
			end if

			if(fore(i)%x<r .and. fore(i)%y>(L-r))then
				extra2(i)%x=fore(i)%x+L
				extra2(i)%y=fore(i)%y-L
				extra2(i)%cosf=fore(i)%cosf
				extra2(i)%sinf=fore(i)%sinf
			end if

			if(fore(i)%y<r .and. fore(i)%x>(L-r))then
				extra2(i)%x=fore(i)%x-L
				extra2(i)%y=fore(i)%y+L
				extra2(i)%cosf=fore(i)%cosf
				extra2(i)%sinf=fore(i)%sinf
			end if

			if(fore(i)%x>(L-r) .and. fore(i)%y>(L-r))then
				extra2(i)%x=fore(i)%x-L
				extra2(i)%y=fore(i)%y-L
				extra2(i)%cosf=fore(i)%cosf
				extra2(i)%sinf=fore(i)%sinf
			end if

			if(fore(i)%x<r)then
				extra1(i)%x=fore(i)%x+L
				extra1(i)%y=fore(i)%y
				extra1(i)%cosf=fore(i)%cosf
				extra1(i)%sinf=fore(i)%sinf
			end if

			if(fore(i)%x>(L-r))then
				extra1(i)%x=fore(i)%x-L
				extra1(i)%y=fore(i)%y
				extra1(i)%cosf=fore(i)%cosf
				extra1(i)%sinf=fore(i)%sinf
			end if

			if(fore(i)%y<r)then
				extra1(i)%y=fore(i)%y+L
				extra1(i)%x=fore(i)%x
				extra1(i)%cosf=fore(i)%cosf
				extra1(i)%sinf=fore(i)%sinf
			end if

			if(fore(i)%y>(L-r))then
				extra1(i)%y=fore(i)%y-L
				extra1(i)%x=fore(i)%x
				extra1(i)%cosf=fore(i)%cosf
				extra1(i)%sinf=fore(i)%sinf
			end if

		end do
		!!!!!!!!!!!!!!


		!the simulation
		do i=1,N

			!the displacement
			las(i)%x=fore(i)%x+v*fore(i)%cosf
			las(i)%y=fore(i)%y+v*fore(i)%sinf
			!!!!!!!!!!!!!!!!!

			!the periodic boundary
			if(las(i)%x>L)then
				las(i)%x=las(i)%x-L
			end if
			if(las(i)%x<0)then
				las(i)%x=las(i)%x+L
			end if
			if(las(i)%y>L)then
				las(i)%y=las(i)%y-L
			end if
			if(las(i)%y<0)then
				las(i)%y=las(i)%y+L
			end if
			!!!!!!!!!!!!!!!!!!!!



			!the direction

			las(i)%sinf=0
			las(i)%cosf=0

			do j=1,N !periodic boundary???
				distance=sqrt((fore(i)%x-fore(j)%x)**2+(fore(i)%y-fore(j)%y)**2)
				if(distance<r)then
					las(i)%cosf=las(i)%cosf+fore(j)%cosf
					las(i)%sinf=las(i)%sinf+fore(j)%sinf
				end if

				distance=sqrt((fore(i)%x-extra1(j)%x)**2+(fore(i)%y-extra1(j)%y)**2)
				if(distance<r)then
					las(i)%cosf=las(i)%cosf+extra1(j)%cosf
					las(i)%sinf=las(i)%sinf+extra1(j)%sinf
				end if

				distance=sqrt((fore(i)%x-extra2(j)%x)**2+(fore(i)%y-extra2(j)%y)**2)
				if(distance<r)then
					las(i)%cosf=las(i)%cosf+extra2(j)%cosf
					las(i)%sinf=las(i)%sinf+extra2(j)%sinf
				end if

			end do

			denominator=sqrt(las(i)%sinf**2+las(i)%cosf**2)
			las(i)%sinf=las(i)%sinf/denominator
			las(i)%cosf=las(i)%cosf/denominator



			!!!!the perturbation
			sinf=las(i)%sinf
			cosf=las(i)%cosf

			call random_number(t)

			theta=t*eta-eta/2.

			las(i)%sinf=sinf*cos(theta)+cosf*sin(theta)
			las(i)%cosf=cosf*cos(theta)-sinf*sin(theta)
			!!!!!!!!!!!!!!!!!

		end do
		!!!!!!!!!!!!!!!!!!!!!!
        
        sumsinf=0
        sumcosf=0
        
        !the abusolute average velocity
        do i=1,N
            sumsinf=sumsinf+las(i)%sinf
            sumcosf=sumcosf+las(i)%cosf
        end do
        
        va=sqrt(sumsinf**2+sumcosf**2)/nn
        
        write(10,*)k,va
        !!!!!!!!!!!!!!!!!!!!!!!!!

		!draw the pic
!		if(k>(time-10))then
!			do i=1,N
!				cx=int(33*las(i)%x)+1
!				cy=int(33*las(i)%y)+1
!
!				pattern(cx,cy)=1
!			end do
!		end if
		!!!!!!!!!!!!!!!!!!!!!!

		!the replacement
		do i=1,N
			fore(i)%x=las(i)%x
			fore(i)%y=las(i)%y
			fore(i)%sinf=las(i)%sinf
			fore(i)%cosf=las(i)%cosf
		end do
		!!!!!!!!!!!!!!!!!!!!!


	end do
	!!!!!!!!!!!!!!!!


!	write(10,"(234I2)")((pattern(i,j),i=1,234),j=234,1,-1)



end program
