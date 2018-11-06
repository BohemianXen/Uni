close all;
clear all;

% Read in two photos of the library.
left  = im2double(imread('parade1.bmp'));
right = im2double(imread('parade2.bmp'));

% % Draw the left image.
% figure(1);
% image(left);
% axis equal;
% axis off;
% title('Left image');
% hold on;
% 
% % Draw the right image.
% figure(2);
% image(right);
% axis equal;
% axis off;
% title('Right image');
% hold on;
% 
% % Get 4 points on the left image.
% figure(1);
% [x, y] = ginput(4);
% leftpts = [x'; y'];
% % Plot left points on the left image.
% figure(1)
% plot(leftpts(1,:), leftpts(2,:), 'rx');
% 
% % Get 4 points on the right image.
% figure(2);
% [x, y] = ginput(4);
% rightpts = [x'; y'];
% % Plot the right points on the right image
% figure(2)
% plot(rightpts(1,:), rightpts(2,:), 'gx');
% 
% % Make leftpts and rightpts (clicked points) homogeneous.
% leftpts(3,:) = 1;
% rightpts(3,:) = 1;
% 
% %% TODO: compute the homography between the left and right points.
% 
% M = calchomography(leftpts, rightpts);
% save mymatrix M

%% TODO: have user click on left image, and plot their click. Then estimate
%        point in right image using the homography and draw that point.

load mymatrix
figure(1);

new_left = zeros(size(right)); new_left_merged = zeros(size(right));

for y=1:size(right,1)
    for x=1:size(right, 2)
        p = [x; y; 1];
        q = M \ p;
        u = q(1) / q(3); v = q(2) / q(3);
        if (floor(u)>0 && floor(v)>0 && ceil(u)<=size(right,2) && ceil(v)<=size(right,1))  
            % Sample the target pixel colour from the source pixel.
            new_left(y, x, :) = bilinear_interpolation(left, u, v);
            new_left_merged(y, x, :) = new_left(y, x, :);
        end
        if (new_left(y, x, :) == 0)
            new_left_merged(y, x, :) = right(y, x, :);
        end
    end
end

imshow([left new_left new_left_merged])

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
