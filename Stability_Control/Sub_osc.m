function [I_np1_Q, a, b1, b2, c] = Sub_osc(alpha, beta, gamma)

% alpha = 63 * pi / 180; beta = 33 * pi / 180; gamma = 10 * pi / 180;

I_n = 1;

delta = pi/2 + gamma - alpha;

a = I_n * sin(alpha) / sin(delta);

b1 = a * sin(pi/2 - gamma - beta) / sin(pi/2 + beta);

if b1 < 0
    disp('fd')
end

b2 = I_n * tan(alpha) - b1;

c = b2 / tan(beta);

I_np1 = I_n * tan(alpha) / tan(beta);

I_np1_Q = I_np1 - c;