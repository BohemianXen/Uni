close all; 
%clear all; 

source = im2double(imread('window.jpg'));
target = zeros(size(source)); target2 = zeros(size(source));

calib_params = [474.53 0 405.96; 0 474.53 217.81; 0 0 1];
distortion_coefficients = [-0.27194, 0.11517 -0.029859];

for row = 1:size(source, 1)
    for col = 1:size(source, 2)
        [u, v] = undistort(calib_params, distortion_coefficients, row, col);
        if (floor(u)>0 && floor(v)>0 && ceil(u)<=size(source,1) && ceil(v)<=size(source,2))  
            target(row, col, :) = bilinear_interpolation(source, v, u);
%             target2(row, col, :) = source(round(u), round(v),:);
        else
            disp([x y u v])
        end
    end
end

imshow([source target])% target2])

function [u_prime,v_prime] = undistort(K, coefficients,u,v)
fx = K(1,1); fy = K(2,2);
px = K(1,3); py = K(2,3);
k1 = coefficients(1); k2 = coefficients(2); k3 = coefficients(3);
x = (u - px) / fx;
y = (v - py) / fy;
r_sq = x^2 + y^2;
x_prime = x*(1+(k1*r_sq)+(k2*(r_sq^2))+(k3*(r_sq^3)));
y_prime = y*(1+(k1*r_sq)+(k2*(r_sq^2))+(k3*(r_sq^3)));
u_prime = (x_prime*fx) + px;
v_prime = (y_prime*fy) + py;
end

function [pixel_val] = bilinear_interpolation(source_img, u_prime, v_prime)

% Obtain neighbouring pixel coordinates 
f1_vu = [floor(v_prime) floor(u_prime)];
f2_vu = [floor(v_prime) ceil(u_prime)];
f3_vu = [ceil(v_prime) floor(u_prime)];
f4_vu = [ceil(v_prime) ceil(u_prime)];

% Obtain neighbouring pixel values
f1 = source_img(f1_vu(1), f1_vu(2), :);
f2 = source_img(f2_vu(1), f2_vu(2), :);
f3 = source_img(f3_vu(1), f3_vu(2), :);
f4 = source_img(f4_vu(1), f4_vu(2), :);

alpha = -1; beta = -1;

% Edge cases
if (f1_vu(1)<1) % Top edge
    f1 = 0; f2 = 0; beta = 0; 
end

if (f1_vu(2)<1) % Left edge
    f1 = 0; f3 = 0; alpha=0;
end

if (f2_vu(2)>size(source_img,2)) % Right Edge
    f2 = 0; f4 = 0; alpha = 1;
end

if (f3_vu(1)>size(source_img,1)) % Bottom Edge
    f3 = 0; f4 = 0; beta= 1;
end

if (beta==-1)
    beta = v_prime - f1_vu(1);
end

if (alpha==-1)
    alpha = u_prime - f1_vu(2);
end

pixel_val = ((1-alpha)*(1-beta)*f1) + (alpha*(1-beta)*f2) + ...
            ((1-alpha)*beta*f3) + (alpha*beta*f4);
       
end