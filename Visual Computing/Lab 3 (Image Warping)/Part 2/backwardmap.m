clear all;
close all;

source = im2double(imread('mona.jpg'));
target = zeros(size(source));
target2 = zeros(size(source));


T = [1 0 -size(source, 2) / 2; 0 1 -size(source, 1) / 2; 0 0 1];
t = pi / 4;
R = [cos(t) -sin(t) 0; sin(t) cos(t) 0; 0 0 1];
S = [4 0 0; 0 4 0; 0 0 1];

% The warping transformation (rotation + scale about an arbitrary point).
M = inv(T) * R * S * T;

% The forward mapping loop: iterate over every source pixel.
for y = 1:size(source, 1)
    for x = 1:size(source, 2)

        % Transform source pixel location (round to pixel grid).
        p = [x; y; 1];
        q = M \ p;
        u = q(1) / q(3); v = q(2) / q(3);
 
        % Sample the target pixel colour from the source pixel using
        % bilinear interpolation
         if (floor(u)>0 && floor(v)>0 && ceil(u)<=size(source,2) && ceil(v)<=size(source,1))  
            target(y, x, :) = bilinear_interpolation(source,u,v);
            target2(y, x, :) = source(round(v), round(u), :);
%          else if outside bounds use nearest pixel?
%             target(y, x, :) = source(round(v), round(u), :);
         end 
    end
end

% target uses bilinear interpolation, target2 uses nearest pixel 
imshow([source target2 target]);
ssd = sum((target(:) - target2(:)) .^ 2);
disp(["SSD: ",ssd])

% Returns weighted pixel value of neighbouring pixels
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

