clear all;
close all;

source = im2double(imread('mona.jpg'));
target = zeros(size(source));
target_2 = zeros(size(source));
target_3 = zeros(size(source));

T = [1 0 -size(source, 2) / 2; 0 1 -size(source, 1) / 2; 0 0 1];
t = pi / 4; t2 = 3*pi/2;
R = [cos(t) -sin(t) 0; sin(t) cos(t) 0; 0 0 1];
R2 = [cos(t2) -sin(t2) 0; sin(t2) cos(t2) 0; 0 0 1];
S = [4 0 0; 0 4 0; 0 0 1]; S2 = [2 0 0; 0 2 0; 0 0 1];

% The warping transformation (rotation + scale about an arbitrary point).
M1 = inv(T) * R * S * T;
M2 = inv(T) * R * S2 * T;
M3 = inv(T) * R2 * S2 * T;

% The forward mapping loop: iterate over every source pixel.
for y = 1:size(source, 1)
    for x = 1:size(source, 2)

        % Transform source pixel location (round to pixel grid).
        p = [x; y; 1];
        q1 = M1 \ p; q2 = M2 \ p; q3 = M3 \ p;
        u1 = round(q1(1) / q1(3)); v1 = round(q1(2) / q1(3));
        u2 = round(q2(1) / q2(3)); v2 = round(q2(2) / q2(3));
        u3 = round(q3(1) / q3(3)); v3 = round(q3(2) / q3(3));

        % Check if target pixel falls inside the image domain.
        if (u1 > 0 && v1 > 0 && u1 <= size(source, 2) && v1 <= size(source, 1))
            % Sample the target pixel colour from the source pixel.
            target(y, x, :) = source(v1, u1, :);
        end
        
         if (u2 > 0 && v2 > 0 && u2 <= size(source, 2) && v2 <= size(source, 1))
            % Sample the target pixel colour from the source pixel.
            target2(y, x, :) = source(v2, u2, :);
         end
        
          if (u3 > 0 && v3 > 0 && u3 <= size(source, 2) && v3 <= size(source, 1))
            % Sample the target pixel colour from the source pixel.
            target3(y, x, :) = source(v3, u3, :);
        end

    end
end

imshow([source target target2 target3]);
