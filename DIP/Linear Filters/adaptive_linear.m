function output_val = adaptive_linear(window, dimensions, k)

center_val = window(ceil(dimensions(1)/2), ceil(dimensions(2)/2));
std_dev = std2(window);
avg = mean(window,'all');
snr = avg/std_dev;

if (k < 0 || k > 1 )
    k = 1 / snr;
%     disp(k)
end

output_val = avg + (k*(center_val-avg));

end