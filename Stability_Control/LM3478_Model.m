%LM3478_Model

clear all; close all; clc;

f = (0: 1: 1e6);

twopi = 3.14159265358979 * 2;

s = f * twopi;

V_FB = 1.26; 
%----------------------

V_in = 5;
V_out = 12;
I_out = 1.5;

R_Load = V_out / I_out;
R_SN = 0.02;

L = 10.e-6;

fs = 1.0e6;



%------------------------

V_SL = 0.083; % 0.092

Se = V_SL * fs / R_SN;
Sn = V_in / L;

% n = 1 + 2 * Se / Sn;
% w_c_L_e = w_s * L / (D^3 * pi * n );
% A_cm = D * w_c_L_e * (R_Load / 2) / (w_c_L_e + R_Load / 2);

D = (V_out - V_in) / V_out;
D_ = 1 - D;

A_cm = D_ * R_Load / (2 * R_SN);

C_out = 150e-6;
R_ESR = 0.05;


% Error Amplifier
R_out = 50000;
gm = 800e-6;

C_C1 = 100e-9;
R_C1 = 4700;

figure(1);
subplot(121);
semilogx([0]);
subplot(122);
semilogx([0]);

for k = -9: 1: 3

C_out = 10^(k);

w_z1 = 1 / (C_out * R_ESR);
w_z2 = R_Load * ((V_in / V_out)^2) / L;
w_p1 = 2 / (C_out * R_Load);

w_s = 2 * pi * fs;


Q = 1 / (pi * (D_ * Se / Sn + 0.5 - D));


% R_fb1 = 440;
% R_fb2 = 0.1;
%A_FB = R_fb2 / (R_fb2 + R_fb1);
A_FB = V_FB / V_out;

A_EA = gm * R_out;

w_z3 = 1 / (C_C1 * R_C1);
w_p2 = 1 / (C_C1 * R_out);


T1 = A_cm * A_EA * A_FB * ...
    (1 + s * 1i / w_z1) .* (1 - s * 1i / w_z2)  ./   ...
    (        (1 + s * 1i / w_p1) .* (   1 + s * 1i / (Q * (w_s / 2)) + (s * 1i).^2 / (w_s^2 / 4)   )        );


log_T1 = 20 * log10(abs(T1));

subplot(121)
hold on;
semilogx(f, log_T1, 'm')
hold off;

subplot(122)
hold on;
semilogx(f, atan2(imag(T1), real(T1)) * 180 / pi, 'r');
hold off;


T2 = A_cm * A_EA * A_FB * ...
    (1 + s *1i / w_z1) .* (1 - s * 1i / w_z2) .* (1 + s * 1i / w_z3) ./ ...
(         (1 + s * 1i / w_p1) .* (1 + s * 1i / w_p2) .* (   1 + s * 1i / (Q * (w_s / 2)) + (s*1i).^2 / (w_s^2 / 4)    )           );

log_T2 = 20 * log10(abs(T2));

subplot(121)
hold on;
semilogx(f, log_T2, 'g');
hold off;
grid on;

subplot(122)
hold on;
semilogx(f, atan2(imag(T2), real(T2)) * 180 / pi, 'b');
hold off;
grid on;
%legend('Power + Load loop', 'Power + Load + Control loop')

end
