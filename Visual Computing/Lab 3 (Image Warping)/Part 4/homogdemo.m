close all;
clear all;

% Read in two photos of the library.
left  = im2double(imread('parade1.bmp'));
right = im2double(imread('parade2.bmp'));

% Draw the left image.
figure(1);
image(left);
axis equal;
axis off;
title('Left image');
hold on;

% Draw the right image.
figure(2);
image(right);
axis equal;
axis off;
title('Right image');
hold on;

% Get 4 points on the left image.
figure(1);
[x, y] = ginput(4);
leftpts = [x'; y'];
% Plot left points on the left image.
figure(1)
plot(leftpts(1,:), leftpts(2,:), 'rx');

% Get 4 points on the right image.
figure(2);
[x, y] = ginput(4);
rightpts = [x'; y'];
% Plot the right points on the right image
figure(2)
plot(rightpts(1,:), rightpts(2,:), 'gx');

% Make leftpts and rightpts (clicked points) homogeneous.
leftpts(3,:) = 1;
rightpts(3,:) = 1;

%% TODO: compute the homography between the left and right points.

H = calchomography(leftpts, rightpts);

%% TODO: have user click on left image, and plot their click. Then estimate
%        point in right image using the homography and draw that point.

figure(3);
image(left)
axis equal;
axis off;
title('Left image');
hold on;
[x, y] = ginput(4);
leftpts_2 = [x'; y'];
leftpts_2(3,:) = 1;
plot(leftpts_2(1,:), leftpts_2(2,:), 'rx');
figure(4);
image(right);
rightpts_2 = H * leftpts_2; 
rightpts_2(1,:) = rightpts_2(1,:)./rightpts_2(3,:);
rightpts_2(2,:) = rightpts_2(2,:)./rightpts_2(3,:);
% Plot left points on the right image.
axis equal;
axis off;
title('Right image');
hold on;
plot(rightpts_2(1,:), rightpts_2(2,:), 'rx');
