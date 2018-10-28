close all;
clear all;

% 2D polygon for Earth: square of 2 by 2 units, in homogeneous coordinates.
earth = [-1 1 1 -1 -1; -1 -1 1 1 -1; 1 1 1 1 1];

% Another 2D polygon for the Moon, made by scaling the earth to 1/4 size
S = [0.25 0 0; 0 0.25 0; 0 0 1];
moon = S * earth;

% Set up axes for plotting our animation.
figure;
hold on;
axis equal;
axis([-14 14 -14 14]); % Extended axes for third moon


for a = 0:0.01:2 * pi

	% Moon a and c will spin 5 times as fast as the Earth.
    % Moon b will spin 10 times as fast as the Earth.
	a_moon = 5 * a;
    b_moon = 10 * a;
    c_moon = 5 * a;

	% Rotation matrix for Earth.
	R_earth = [cos(a) -sin(a) 0; sin(a) cos(a) 0; 0 0 1];

	% Rotation matrix for the Moons.
	R_a_moon = [cos(a_moon) -sin(a_moon) 0; sin(a_moon) cos(a_moon) 0; 0 0 1];
    R_b_moon = [cos(b_moon) -sin(b_moon) 0; sin(b_moon) cos(b_moon) 0; 0 0 1];
    R_c_moon = [cos(c_moon) -sin(c_moon) 0; sin(c_moon) cos(c_moon) 0; 0 0 1];

	% Translation matrix to move the Moons away from Earth
    % ( A orbits at a distance of 5 units, 
    %   B orbits at a distance of 10 units and
    %   C orbits at a distance of 2 units but this will be taken relative to
    %   the Moon B
    % ) 
	T_a_moon = [1 0 5; 0 1 0; 0 0 1];
    T_b_moon = [1 0 10; 0 1 0; 0 0 1];
    T_c_moon = [1 0 4; 0 1 0; 0 0 1];

	% Rotate the Earth.
	p_earth = R_earth * earth;

	% Rotate the moons, then move them away from their relative origins.
	p_a_moon = T_a_moon * R_a_moon * moon;
    p_b_moon = T_b_moon * R_b_moon * moon;
    p_c_moon = T_c_moon * R_c_moon * moon;

	% Place A and B moons in the Earth's reference frame (which is R)
    % then place moon C in the B's reference and translate it relative to 
    % moon B's current coordinates. 
	p_a_moon = R_earth * p_a_moon;
    p_b_moon = R_earth * p_b_moon;
    
    b_moon_current_x = mean(p_b_moon(1,:)); % Need to divide this by homogenous coordinates to get exact center?
    b_moon_current_y = mean(p_b_moon(2,:));
    p_c_moon = [1 0 b_moon_current_x; 0 1 b_moon_current_y; 0 0 1] * R_b_moon * p_c_moon ; 
       

	% Draw the earth in blue and the moons in black, red and green respectively.
	cla;
	plot(p_earth(1,:), p_earth(2,:), 'b', 'LineWidth', 2);
	plot(p_a_moon(1,:),  p_a_moon(2,:),  'k', 'LineWidth', 2);
    plot(p_b_moon(1,:),  p_b_moon(2,:),  'r', 'LineWidth', 2);
    plot(p_c_moon(1,:),  p_c_moon(2,:),  'g', 'LineWidth', 2);
	drawnow;

end