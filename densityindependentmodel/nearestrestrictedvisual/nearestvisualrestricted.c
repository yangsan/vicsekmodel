#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define N 100
#define L 15
#define R 1.0
#define V 0.03
#define ETA 1.0
#define STEP 10000
#define NC 6

#define random() rand()/(RAND_MAX+1.0)

int simulation(double xcor[], double ycor[], double xdir[], double ydir[]);
double distance(double x1, double y1, double x2, double y2);

int main(int argc, char *argv[])
{
/*begin of decleration*/
    double xcor[N], ycor[N], xdir[N], ydir[N];
    /*xcor,ycor for agents' position; xdir, ydir for agents' direction*/
    int i,k ;
    /*iterator*/
    double denominator;
    /*denominator*/
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

        denominator = distance(xdir[i], ydir[i],0.0, 0.0);
        xdir[i] /= denominator;
        ydir[i] /= denominator;
        /*renormalizaiton*/
    }
/*end of initializing*/

/*begin of simulation*/
    for(k=0; k<STEP; k++)
    {
        simulation(xcor, ycor, xdir, ydir);
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
 *         Name:  simulation
 *  Description:  The core of the simualtion codes. Puts xcor, ycor, xdir, ydir in 
 *  and get them modified.
 * =====================================================================================
 */

int simulation(double xcor[], double ycor[], double xdir[], double ydir[]){

    double fordistance[N * 9];
    int forlabel[N * 9];
    double temp;
    int inttemp;
    double xcort[N], ycort[N], xdirt[N], ydirt[N];
    /*temps for simulation*/
    int i, j, k;
    double denominator;
    /*denominator*/
    double sumx, sumy;
    /*the sum of neighbors' directions*/
    double x, y;
    /*temps for perturbation*/
    double theta;
    /*for perturbation*/
 
   /*begin of initializing for everytime step simulation*/
    for(i=0; i<N; i++) 
    {
        xcort[i] = 0;
        ycort[i] = 0;
        xdirt[i] = 0;
        ydirt[i] = 0;
        /*temps*/
    }
    /*end of initializing for everytime step simulation*/

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
            fordistance[j] = distance(xcor[i], ycor[i], xcor[j], ycor[j]);
            forlabel[j] = j;

            fordistance[j + N] = distance(xcor[i], ycor[i], xcor[j]-L, ycor[j]+L);
            forlabel[j + N] = j;

            fordistance[j + 2*N] = distance(xcor[i], ycor[i], xcor[j], ycor[j]+L);
            forlabel[j + 2*N] = j;

            fordistance[j + 3*N] = distance(xcor[i], ycor[i], xcor[j]+L, ycor[j]+L);
            forlabel[j + 3*N] = j;

            fordistance[j + 4*N] = distance(xcor[i], ycor[i], xcor[j]-L, ycor[j]);
            forlabel[j + 4*N] = j;

            fordistance[j + 5*N] = distance(xcor[i], ycor[i], xcor[j]+L, ycor[j]);
            forlabel[j + 5*N] = j;

            fordistance[j + 6*N] = distance(xcor[i], ycor[i], xcor[j]- L, ycor[j] - L);
            forlabel[j + 6*N] = j;

            fordistance[j + 7*N] = distance(xcor[i], ycor[i], xcor[j], ycor[j] - L);
            forlabel[j + 7*N] = j;

            fordistance[j + 8*N] = distance(xcor[i], ycor[i], xcor[j] + L, ycor[j] - L);
            forlabel[j + 8*N] = j;
        }

        for(j=0 ; j< NC; j++){
            for(k = j; k< N*9; k++){
                if(fordistance[j] > fordistance[k]){
                   temp = fordistance[j];
                   fordistance[j] = fordistance[k];
                   fordistance[k] = temp;

                   inttemp = forlabel[j];
                   forlabel[j] = forlabel[k];
                   forlabel[k] = inttemp;
                }
            }
            sumx += xdir[forlabel[j]];
            sumy += ydir[forlabel[j]];
        }


        xdirt[i] = sumx;
        ydirt[i] = sumy;
        denominator = distance(xdirt[i], ydirt[i],0.0,0.0);
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

    return 0;
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  distance
 *  Description:  return the distance of the two points passed in
 * =====================================================================================
 */
double distance(double x1, double y1, double x2, double y2)
{
    return sqrt(pow(x1 - x2,2)+pow(y1 - y2,2));
}
