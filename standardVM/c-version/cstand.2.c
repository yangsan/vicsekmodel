#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define N 100
#define L 15
#define R 1.0
#define V 0.03
#define ETA 1.0
#define STEP 10000

#define random() rand()/(RAND_MAX+1.0)

double distance(double x1, double x2, double y1, double y2);

int main(int argc, char *argv[])
{
/*begin of decleration*/
    double xcor[N], ycor[N], xdir[N], ydir[N];
    /*xcor,ycor for agents' position; xdir, ydir for agents' direction*/
    double xcor_e1[N], ycor_e1[N], xcor_e2[N], ycor_e2[N], xdir_e1[N], ydir_e1[N], xdir_e2[N], ydir_e2[N];
    /*perodic boudry*/
    double xcort[N], ycort[N], xdirt[N], ydirt[N];
    /*temps for simulation*/
    int i, k, j;
    /*iterators*/
    double denominator;
    /*denominator*/
    double sumx, sumy;
    /*the sum of neighbors' directions*/
    double theta;
    /*for the perturbation*/
    double x, y;
    /*temps for perturbation*/
    FILE *fp;
    char filename[100];
/*end of decleration*/

/*begin of initializing*/
    srand((unsigned int)time(NULL));
    /*initializing the random seed*/

    for(i=0; i<N; i++)
    {
        xcor[i] = random()*L;
        ycor[i] = random()*L;

        if(random()>0.5)
        {
            xdir[i] = random();
        }
        else
        {
            xdir[i] = -random();
        }

        if(random()>0.5)
        {
            ydir[i] = random();
        }
        else
        {
            ydir[i] = -random();
        }

        denominator = sqrt(xdir[i] * xdir[i] + ydir[i] * ydir[i]);
        xdir[i] /= denominator;
        ydir[i] /= denominator;
        /*renormalizaiton*/
    }
/*end of initializing*/

/*begin of simulation*/
    for(k=0; k<STEP; k++)
    {
       /*begin of initializing for everytime step simulation*/
       for(i=0; i<N; i++) 
       {
           xcor_e1[i] = -10;
           ycor_e1[i] = -10;
           xdir_e1[i] = 0;
           ydir_e1[i] = 0;

           xcor_e2[i] = -10;
           ycor_e2[i] = -10;
           xdir_e2[i] = 0;
           ydir_e2[i] = 0;
           /*perodic boundry*/
           
           xcort[i] = 0;
           ycort[i] = 0;
           xdirt[i] = 0;
           ydirt[i] = 0;
           /*temps*/
        }
       /*end of initializing for everytime step simulation*/

       /*begin of dealing with the perodic boundry, move ones near boundry aside*/
        for(i=0; i<N; i++)
        {
            if(xcor[i]< R && ycor[i]<R) 
            {
                xcor_e2[i] = xcor[i] + L;
                ycor_e2[i] = ycor[i] + L;
                xdir_e2[i] = xdir[i];
                ydir_e2[i] = ydir[i];
            }
            /*left buttom*/

            if(xcor[i] < R && ycor[i]>(L - R))
            {
                xcor_e2[i] = xcor[i] + L;
                ycor_e2[i] = ycor[i] - L;
                xdir_e2[i] = xdir[i];
                ydir_e2[i] = ydir[i];
            }
            /*left top*/

            if(xcor[i]>(L - R) && ycor[i]<R)
            {
                xcor_e2[i] = xcor[i] - L;
                ycor_e2[i] = ycor[i] + L;
                xdir_e2[i] = xdir[i];
                ydir_e2[i] = ydir[i];
            }
            /*right buttom*/
            if(xcor[i]>(L - R) && ycor[i]>(L-R))
            {
                xcor_e2[i] = xcor[i] - L;
                ycor_e2[i] = ycor[i] - L;
                xdir_e2[i] = xdir[i];
                ydir_e2[i] = ydir[i];
            }
            /*right top*/

            if(xcor[i] < R)
            {
                xcor_e1[i] = xcor[i] + L;
                ycor_e1[i] = ycor[i] ;
                xdir_e1[i] = xdir[i];
                ydir_e1[i] = ydir[i];
            }
            /*left*/

            if(ycor[i] < R)
            {
                xcor_e1[i] = xcor[i] ;
                ycor_e1[i] = ycor[i] + L;
                xdir_e1[i] = xdir[i];
                ydir_e1[i] = ydir[i];
            }
            /*buttom*/

            if(xcor[i] > (L -R))
            {
                xcor_e1[i] = xcor[i] - L;
                ycor_e1[i] = ycor[i] ;
                xdir_e1[i] = xdir[i];
                ydir_e1[i] = ydir[i];
            }
            /*right*/

            if(ycor[i] > (L - R))
            {
                xcor_e1[i] = xcor[i] ;
                ycor_e1[i] = ycor[i] - L;
                xdir_e1[i] = xdir[i];
                ydir_e1[i] = ydir[i];
            }
            /*top*/
        }
       /*end of dealing with the perodic boundry*/

        /*begin of simulation*/
        for(i=0; i<N; i++)
        {
            /*begin of moving agents*/
            xcort[i] = xcor[i] + V * xdir[i];
            if(xcort[i] > L) xcort[i] -= L;
            if(xcort[i] < 0) xcort[i] += L;
            ycort[i] = ycor[i] + V * ydir[i];
            if(ycort[i] > L) ycort[i] -= L;
            if(ycort[i] < 0) ycort[i] += L;
            /*end of moving agents*/

            /*begin of direction*/
            sumx = 0;
            sumy = 0;
            for(j=0; j<N; j++)
            {
                if(distance(xcor[i], xcor[j], ycor[i], ycor[j]) < R)
                {
                    sumx += xdir[j];
                    sumy += ydir[j];
                }

                if(distance(xcor[i] , xcor_e1[j], ycor[i] , ycor_e1[j]) < R)
                {
                    sumx += xdir_e1[j];
                    sumy += ydir_e1[j];
                } 

                
                if(distance(xcor[i] , xcor_e2[j], ycor[i] , ycor_e2[j]) < R)
                {
                    sumx += xdir_e2[j];
                    sumy += ydir_e2[j];
                } 
 
            }

            xdirt[i] = sumx;
            ydirt[i] = sumy;
            denominator = sqrt(xdirt[i] * xdirt[i] + ydirt[i] * ydirt[i]);
            xdirt[i] /= denominator;
            ydirt[i] /= denominator;
            /*end of direction*/

            /*begin of perturbation*/
            x = xdirt[i];
            y = ydirt[i];
            theta = random() * ETA - ETA/2.0; 
            xdirt[i] = x * cos(theta) + y * sin(theta);
            theta = random() * ETA - ETA/2.0; 
            ydirt[i] = y * cos(theta) - x * sin(theta);
            /*end of perturbation*/
        }
        /*end of simulation*/

        /*begin of copy temps to the originals*/
        for(i=0; i<N; i++)
        {
            xcor[i] = xcort[i];
            ycor[i] = ycort[i];
            xdir[i] = xdirt[i];
            ydir[i] = ydirt[i];
        }
        /*end of copy temps to the originals*/

        sprintf(filename, "./data/%i.out", k);
        fp = fopen(filename,"w");
        for(i = 0;i<N;i++)
        {
            fprintf(fp,"%.18e %.18e %.18e %.18e\n",xcor[i],ycor[i],xdir[i],ydir[i]);
        }
        fclose(fp);

    }
/*end of simulation*/

    return 0;
/*begin of cleanup*/
/*end of cleanup*/
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  distance
 *  Description:  return the distance of the two points passed in
 * =====================================================================================
 */
double distance(double x1, double x2, double y1, double y2)
{
    return sqrt(pow(x1-x2,2)+pow(y1-y2,2));
}
