% Estimate the homography from a set of point correspondences.
function H = calchomography(points1, points2)

    if size(points1, 2) < 4 || size(points2, 2) < 4
        error('Need at least 4 points for a homography.');
    end

    A = [];

    for point = 1:size(points1, 2)
      x = points1(1, point);
      y = points1(2, point);
      u = points2(1, point);
      v = points2(2, point);

      A = [A; ...
           -x   -y   -1    0    0    0   x * u   y * u   u; ...
            0    0    0   -x   -y   -1   x * v   y * v   v];

    end

    % Solve A * h = 0 for h.
    [U, S, V] = svd(A);
    h = V(:,end);

    % Reshape vectorised result back into matrix shape.
    H = reshape(h, 3, 3)';

    % Homogeneous normalisation.
    H = H ./ H(3,3);
