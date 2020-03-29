file = ('29Mar_Test_1764.mat'); % uigetfile;
load(file);

% [total_samples, recording_length] = size(data);
% classes = unique(labels);
% total_classes = length(classes);
% samples_per_class = total_samples/(total_classes + 1);

labelled_data = cat(2, labels.', data);

standing = (data(labelled_data(:, 1) == 0, :) + 1.0) ./ 2.0;
walking = (data(labelled_data(:, 1) == 1, :) + 1.0) ./ 2.0;
lying_f = (data(labelled_data(:, 1) == 2, :) + 1.0) ./ 2.0;
lying_l = (data(labelled_data(:, 1) == 3, :) + 1.0) ./ 2.0;
lying_r = (data(labelled_data(:, 1) == 4, :) + 1.0) ./ 2.0;
falling_f = (data(labelled_data(:, 1) == 5, :) + 1.0) ./ 2.0;
falling_l = (data(labelled_data(:, 1) == 6, :) + 1.0) ./ 2.0;
falling_r = (data(labelled_data(:, 1) == 7, :) + 1.0) ./ 2.0;

% ---------------------------- Surface Plots ------------------------------

% figure(1) 
% surf(falling_f)
% figure(2)
% surf(falling_l)
% figure(3)
% surf(falling_r)

% ----------------------------- Colour Maps -------------------------------

map = jet(256);

figure(1)
subplot(2, 1, 1), imshow(standing), title('Standing');
subplot(2, 1, 2), imshow(walking), title('Walking');
colormap(map);

figure(2)
subplot(3, 1, 1), imshow(lying_f), title('Lying Forwards');
subplot(3, 1, 2), imshow(lying_l), title('Lying Left');
subplot(3, 1, 3), imshow(lying_r), title('Lying Right');
colormap(map);

figure(3)
subplot(3, 1, 1), imshow(falling_f), title('Falling Forwards');
subplot(3, 1, 2), imshow(falling_l), title('Falling Left');
subplot(3, 1, 3), imshow(falling_r), title('Falling Right');
colormap(map);

% -------------------------------- Montages -------------------------------

% fall_images = {falling_f, falling_l, falling_r};
% montage(fall_images, 'Size', [3, 1]);
% colormap(map);
