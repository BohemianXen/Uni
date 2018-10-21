function [kernel, normalisation] = gaussian_blur_kernel(sigma, rows, cols)
%creates a rows x cols sized gaussain kernel (with sd of value sigma) along
%with the sum of all the elements 

kernel = zeros(rows, cols);
variance = sigma^2;

%offsets from center of image
row_center = floor(rows/2);
col_center = floor(cols/2);

%gaussian equation in 2D - TODO: Only generate top half then mirror to save
%time and also compare with fspecial
for row=-row_center:row_center
    for col=-col_center:col_center
        val = (1/(2*pi*variance))*exp(-(col^2 + row^2)/(2*variance));
        kernel(row+row_center+1, col+col_center+1) = val;
    end
end

kernel = kernel * 1/sum(kernel(:));
normalisation = sum(kernel(:));
end