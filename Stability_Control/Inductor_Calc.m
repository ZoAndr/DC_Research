clear all; close all; clc;

%U_in = 12;
U_in = [8: 0.1: 33];
U_out = 36;
I_out = 1;

U_q = 0.07;
U_D = 0.6;

L = 2.2 * 1e-6;
%L = [2.2, 3.3, 4.7, 6.8, 8.2, 10] * 10e-6;

Fs = 1 * 1e6;

I_in = I_out .* (U_out + U_D) ./ (U_in - U_q);

D = 1 - ( (U_in - U_q) ./ (U_out + U_D) );

dt = 1 / Fs;
t_ON = dt * D;
t_OFF = dt * (1 - D);

dI = U_in .* t_ON ./ L;

I_L_avr = ( (1 + D) .* I_in ) .* ones(1, max(length(L), length(U_in)) );

I_L_max = I_L_avr + 0.5 * dI;

figure(1001); plot(U_in, dI,   U_in, D,   U_in, I_in,   U_in, I_L_avr,   U_in, I_L_max,   U_in, dI / 2); legend('dI', 'D', 'I_{in}', 'I_{L avr}', 'I_{max}', 'dI/2'); xlabel('U_{in}, B'); ylabel('I, A;  D, [0-1]'); grid on;
figure(1002); plot(L * 1e6, dI,   L * 1e6, I_L_avr,   L * 1e6, I_L_max,   L * 1e6, dI / 2); legend('dI', 'I_{L avr}', 'I_{L max}', 'dI/2'); xlabel('L, uH'); ylabel('I, A'); grid on;