#include <iostream>
#include <math.h>

double log_saturation(double x, double vmax, double log_slope){
	return log_slope*log((x-vmax)/log_slope + 1) + vmax;
}

extern "C" {
#if defined(_WIN32) 
__declspec( dllexport )
#endif
extern void update_velocity(int N, double *Pos, double *Vel, double *Pos1,
 double *Vel1, double centerx, double centery, double rflee, double rfollow, double rseek,
 double vmax, double log_slope){
	double posx, posy, velx, vely, vx, vy, nv, bv;
	for (int i = 0; i < N;i++) {
		posx = Pos[i];
		posy = Pos[N+i];
		velx = 0;
		vely = 0;
		for (int j = 0; j < N;j++) {
			vx = Pos[j] - posx;
			vy = Pos[N+j] - posy;
			nv = sqrt(vx*vx+vy*vy);
			if (nv > 0) {
				if (nv < rflee) {
					velx -= vx/nv;
					vely -= vy/nv;
				} else if (nv < rfollow) {
					vx = Vel[j];
					vy = Vel[N+j];
					nv = sqrt(vx*vx+vy*vy);
					velx += vx/nv*0.1;
					vely += vy/nv*0.1;					
				} else {
					velx += vx/nv*0.01;
					vely += vy/nv*0.01;					
				}
			}
		}
		nv = sqrt(velx*velx+vely*vely);
		if(nv > 0) {
			velx /= nv;
			vely /= nv;
		}
		// mass center
		vx = ((centerx*N-posx)/(N-1))-posx;
		vy = ((centery*N-posy)/(N-1))-posy;
		nv = sqrt(vx*vx+vy*vy);
		if(nv>0) {
			velx += vx/nv*0.1;
			vely += vy/nv*0.1;
			// velx -= vx/nv*0.1;
			// vely -= vy/nv*0.1;
		}
		Vel1[i] = Vel[i] + velx;
		Vel1[N+i] = Vel[N+i] + vely;
		nv = sqrt(Vel1[i]*Vel1[i] + Vel1[N+i]*Vel1[N+i]);
		if (nv > vmax) {
			nv = log_saturation(nv, vmax, log_slope)/nv;
			Vel1[i] *= nv;
			Vel1[i+N] *= nv;
		}
		if(posx > 980) Vel1[i] = -1;
		if(posx < 20) Vel1[i] = 1;
		if(posy > 980) Vel1[N+i] = -1;
		if(posy < 20) Vel1[N+i] = 1;
		Pos1[i] = Pos[i] + Vel1[i];
		Pos1[N+i] = Pos[N+i] + Vel1[N+i];
	}
}
}