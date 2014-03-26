#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define N 100
#define L 5
#define R 1.0
#define V 0.03
#define ETA 1.0
#define STEP 1000
#define PI 3.14159265358979323846
#define random() rand()/(RAND_MAX+1.0)

int simulation(double xcor[], double ycor[], double xdir[], double ydir[], double omega);
double distance(double x, double y);

int main(int argc, char *argv[])
{
/*begin of decleration*/
    double xcor[N], ycor[N], xdir[N], ydir[N];
    /*xcor,ycor for agents' position; xdir, ydir for agents' direction*/
    int i,k ;
    /*iterator*/
    double denominator;
    /*denominator*/
    double omega;
    FILE *fp;
    char filename[100];
/*end of decleration*/

/*begin of initializing*/
    srand((unsigned int)time(NULL));
    /*initializing the random seed*/

    omega = cos((3./2.)*PI/2.);

    printf("%f",omega);
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

        denominator = distance(xdir[i], ydir[i]);
        xdir[i] /= denominator;
        ydir[i] /= denominator;
        /*renormalizaiton*/
    }
/*end of initializing*/

/*begin of simulation*/
    for(k=0; k<STEP; k++)
    {
        simulation(xcor, ycor, xdir, ydir, omega);
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

int simulation(double xcor[], double ycor[], double xdir[], double ydir[], double omega){

    double xcor_e1[N], ycor_e1[N], xcor_e2[N], ycor_e2[N], xdir_e1[N], ydir_e1[N], xdir_e2[N], ydir_e2[N];
    /*perodic boudry*/
    double xcort[N], ycort[N], xdirt[N], ydirt[N];
    /*temps for simulation*/
    int i, j;
    double denominator;
    /*denominator*/
    double sumx, sumy;
    /*the sum of neighbors' directions*/
    double x, y;
    /*temps for perturbation*/
    double dx, dy, dis;
    /*temps for differences between xcors and ycors*/
    double theta;
    /*for perturbation*/
 
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
        if(xcor[i] < R)
        {
            if ( ycor[i] < R ) {
                xcor_e2[i] = xcor[i] + L;
                ycor_e2[i] = ycor[i] + L;
                xdir_e2[i] = xdir[i];
                ydir_e2[i] = ydir[i];
            }                               /* left buttom */
            else if(ycor[i] > (L - R) ){
                xcor_e2[i] = xcor[i] + L;
                ycor_e2[i] = ycor[i] - L;
                xdir_e2[i] = xdir[i];
                ydir_e2[i] = ydir[i];
            }                               /* left top */
            else {
                xcor_e1[i] = xcor[i] + L;
                ycor_e1[i] = ycor[i] ;
                xdir_e1[i] = xdir[i];
                ydir_e1[i] = ydir[i];
            }                               /* left */
        }
        else if(xcor[i] > (L - R))
        {
            if (ycor[i] < R  ) {
                xcor_e2[i] = xcor[i] - L;
                ycor_e2[i] = ycor[i] + L;
                xdir_e2[i] = xdir[i];
                ydir_e2[i] = ydir[i];
            }                               /* right buttom */
            else if(ycor[i] > (L - R)){
                xcor_e2[i] = xcor[i] - L;
                ycor_e2[i] = ycor[i] - L;
                xdir_e2[i] = xdir[i];
                ydir_e2[i] = ydir[i];
            }                               /* right top */
            else{
                xcor_e1[i] = xcor[i] - L;
                ycor_e1[i] = ycor[i] ;
                xdir_e1[i] = xdir[i];
                ydir_e1[i] = ydir[i];
            }                               /* right */
        }
        else
        {

            if(ycor[i] < R){
                xcor_e1[i] = xcor[i] ;
                ycor_e1[i] = ycor[i] + L;
                xdir_e1[i] = xdir[i];
                ydir_e1[i] = ydir[i];
            }                               /* buttom */
            else if(ycor[i] > (L - R)){
                xcor_e1[i] = xcor[i] ;
                ycor_e1[i] = ycor[i] - L;
                xdir_e1[i] = xdir[i];
                ydir_e1[i] = ydir[i];
            }                               /* top */
        }
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
            dx = xcor[j] - xcor[i];
            dy = ycor[j] - ycor[i];
            if(abs(dx) < R && abs(dy) < R){
                dis = distance(dx, dy);
                if(dis ==0 || (dis < R && (dx*xdir[i]+dy*ydir[i])/dis > omega))
                {
                    sumx += xdir[j];
                    sumy += ydir[j];
                }
            }

            if(xcor_e1[j] > 0 && ycor_e1[j] > 0){
                dx = xcor_e1[j] - xcor[i];
                dy = ycor_e1[j] - ycor[i];
                if(abs(dx) < R && abs(dy) < R){
                    dis = distance(dx, dy);
                    if(dis == 0 || (dis < R && (dx*xdir[i]+dy*ydir[i])/dis > omega))
                    {
                        sumx += xdir_e1[j];
                        sumy += ydir_e1[j];
                    } 
                }
            }

            if(xcor_e2[j] > 0 && ycor_e2[j] > 0){
                dx = xcor_e2[j] - xcor[i];
                dy = ycor_e2[j] - ycor[i];
                if(abs(dx) < R && abs(dy) < R){
                    dis = distance(dx, dy);
                    if(dis == 0 || (dis < R && (dx*xdir[i]+dy*ydir[i])/dis > omega))
                    {
                        sumx += xdir_e2[j];
                        sumy += ydir_e2[j];
                    } 
                }
            }

        }

        xdirt[i] = sumx;
        ydirt[i] = sumy;
        denominator = distance(xdirt[i], ydirt[i]);
        xdirt[i] /= denominator;
        ydirt[i] /= denominator;
        /*end of direction*/

        /*begin of perturbation*/
        x = xdirt[i];
        y = ydirt[i];
        theta = random() * ETA - ETA/2.0; 
        xdirt[i] = x * cos(theta) + y * sin(theta);
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
double distance(double x, double y)
{
    return sqrt(pow(x,2)+pow(y,2));
}
