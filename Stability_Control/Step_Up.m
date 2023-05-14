clear all; close all; clc;

U_in = 5: 0.01: 35;
U_out = 36;
I_out = 1;

U_SL = 0.092;
R_IS = 0.02;


N = length(U_in);

I_ramp_max = zeros(1, N);
I_L_max = zeros(1, N);
I_DC = zeros(1, N);
Mode = zeros(1, N);
t_cyc = zeros(1, N);
I_DC  = zeros(1, N);
P_in_S = zeros(1, N);
Instability = zeros(1, N);
D_k = zeros(1, N);
alpha = zeros(1, N);
beta = zeros(1, N);
gamma = zeros(1, N);
a = zeros(1, N);
b1 = zeros(1, N);
b2 = zeros(1, N);
c = zeros(1, N);
t_dn_k = zeros(1, N);
t_up_k = zeros(1, N);

fs = 1000 * 1e3; dt = 1 / fs;
L = 2.2 * 1e-6;

for k = 1: N
U_L = U_out - U_in(k);

t_dn = ( 2 * L * dt * I_out / U_L )^0.5;
I_dn_start = t_dn * U_L / L;
I_up_stop = I_dn_start;
t_up = L * I_up_stop / U_in(k);
t_cycle = t_up + t_dn;

t_dn_k(k) = t_dn;
t_up_k(k) = t_up;

t_cyc(k) = t_cycle * 1e6;

if  t_cycle > dt
    TYPE = 'CCM'
    Mode(k) = 1;
    
    D = 1 - (U_in(k) / (U_in(k) + U_L));
    D_k(k) = D;
    
    t_up_CCM = D * dt;
    t_dn_CCM = (1 - D) * dt;
    
    I_up_stop_CCM = t_up_CCM * U_in(k) / L;
    I_dn_strt_CCM = t_dn_CCM *  U_L / L;
    
    I_out_Ramp = I_dn_strt_CCM * t_dn_CCM / dt / 2;
    I_in_Ramp  = I_up_stop_CCM * t_up_CCM / dt / 2
    
    I_out_DC = (I_out - I_out_Ramp) / t_dn_CCM * dt;
    I_DC(k) = I_out_DC;
    
    I_ramp_max(k) = I_dn_strt_CCM;
    
    [Instability(k), alpha(k), beta(k), gamma(k), a(k), b1(k), b2(k), c(k)] = Check_Sub_Osc(dt * U_in(k) / L, dt * U_L / L, U_SL, R_IS);
    
    
    I_in_S(k) = I_DC(k) + I_up_stop_CCM / 2;
    
    P_in_S(k) = I_DC(k) * U_in(k) + I_up_stop_CCM / 2 * U_in(k) * t_up / dt + I_dn_strt_CCM / 2 * U_in(k) * t_dn / dt;
    
    P_in_S(k) = I_up_stop_CCM / 2 * U_in(k) * t_up_CCM / dt + I_dn_strt_CCM / 2 * U_in(k) * t_dn_CCM / dt;
    
    P_in_S(k) = I_DC(k) * U_in(k) + I_up_stop_CCM / 2 * U_in(k) ;
    
else
    TYPE = 'DCM'
    Mode(k) = 2;    
    I_ramp_max(k) = I_dn_start;
    
    I_out_Ramp = I_ramp_max(k) * t_dn / dt / 2;
    
    
    I_in_S(k) = I_DC(k) + I_dn_start / 2 * t_up / dt + I_dn_start / 2 * t_dn / dt;
    
    P_in_S(k) = I_DC(k) * U_in(k) + I_dn_start / 2 * U_in(k) * t_up / dt + I_dn_start / 2 * U_in(k) * t_dn / dt;
end



I_L_max(k) = I_ramp_max(k) + I_DC(k);
end

figure(1001);
%plot(U_in, I_DC .* U_in, U_in, P_in_S)



%plot(U_in, I_ramp_max, U_in, I_L_max, U_in, Mode - 1, U_in, t_cyc, U_in, I_DC, U_in, P_in_S, U_in)
plot(U_in, I_ramp_max, U_in, I_L_max, U_in, Mode - 1, U_in, t_cyc, U_in, I_DC, U_in, I_in_S)
grid on
legend('I_{ramp_{max}}', 'I_{L_{max}}', 'Mode', 't_{cyc}', 'I_{DC}', 'I_{in_{total}}')
xlabel('U_{in}, B');
ylabel('I, A  t, us')

figure(2001);
plot(U_in, t_up_k * 1e6, U_in, t_dn_k * 1e6, U_in, t_cyc)
legend('t_{up}', 't_{dn}', 't_{cyc}')
xlabel('U_{in}, B');
ylabel('t, us')
title('Rising, Falling times, total time')
return

figure(1002);
plot(U_in, Instability, U_in, D_k)
grid on
figure(1003);
plot(U_in, 90 - alpha * 180 / pi, U_in, 90 - beta * 180 / pi, U_in, gamma * 180 / pi)
legend('alpha', 'beta', 'gamma')
grid on

figure(1004);
plot(U_in, a, U_in, b1, U_in, b2, U_in, c);
legend('a', 'b1', 'b2', 'c')
grid on
grid on
