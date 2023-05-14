%LM3478_Model

% http://tera.yonsei.ac.kr/class/2017_1_1/lecture/Lect%2010%20Pole,%20Zero,%20and%20Bode%20Plot.pdf

clear all; close all; clc;

f = (0: 1: 1e6);

twopi = 3.14159265358979 * 2;

s = f * twopi;


C_C1 = 100e-9;
R_C1 = 4.700;

figure(1);
subplot(121);
semilogx([0]);
subplot(122);
semilogx([0]);

for k = -9: 1: 3

    C_C1 = 10^k;
    
    w_z3 = 1 / (C_C1 * R_C1);

    
    T2 =  1 ./ (1 + s * 1i / w_z3);
    
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