function [Instability, alpha, beta, gamma, a, b1, b2, c] = Check_Sub_Osc(dIup_dt, dIdn_dt, U_SL, R_IS)


% dIup_dt = 4; 
% dIdn_dt = 7;
% U_SL = 0.092;
% R_IS = 0.02;


dt = 1;

dIup = dIup_dt * dt;
dIdn = dIdn_dt * dt;

dUup = dIup * R_IS;
dUdn = dIdn * R_IS;

alpha = pi/2 - atan2(dUup, dt); % * 180 / pi
beta  = pi/2 - atan2(dUdn, dt); % * 180 / pi

gamma = atan2(U_SL, dt); 

%[alpha, beta, gamma] * 180 / pi

[Instability, a, b1, b2, c] = Sub_osc(alpha, beta, gamma);