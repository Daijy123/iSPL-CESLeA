function [Window_data, window_labels] = cutData_v2(X, Labels, window_length, overlap)
%CUTDATA_V2 cuts the data X into windows and labels those windows with the
%corresponding activities.
%   [window_data, window_label] = CUTDATA_V2(X, Label, window_length, overlap) 
%   - window_length is the length of each window
%   - X is a matrix where each row contains the acceleration and gyroscope
%   data of 1 time step
%   - overlap = (window_length - step length) is the overlap  between 2 adjacent windows.
%   - Label is a matrix with 5 columns: 
%           1st column: experiment ID, 
%           2nd column: user ID,
%           3rd column: activity ID (label)
%           4th column: starting point of that activity
%           5th column: ending point of that activity
%   Window_data is a cell with size of (number of windows) x 1:
%           each row is a windowed data (size: window_length x 6...no. Acc and Gyro)
%   window_label is column vector contains labels of the corresponding windows
%
% This version is the version 2 of cutData. CUTDATA_V2 deals with the
% gaps when it cuts and labels the windows
%
% The idea here is using the matrix Label to create a new matrix named 
% Lab_X which has the same length with the labelled data in Label 
% (because some parts of the signal X were not labelled).
% Lab_X will contain the data and label of activity along
% time. 
% Then we cut data into windows and label that window.
% For the case that there are more than 1 types of activities in a window,
% we will label the acitivity that has the most data points in that window
%
% The data was not labelled continuously. There are some GAPS between
% activities so it is better to take them into account when we do the
% window cutting. Here, I use a flag to mark those gaps. While cutting
% a window, if we meet a flag, we will skip the data from the beginning of
% that window to the flag; and then re-start at the data point right after
% the flag. For the flag, I use label = -1


Lab_X = [];
labels = [];

for i = 1 : size(Labels,1)
    start_point = Labels(i, 4);
    end_point = Labels(i, 5);
    
    labels = [labels; Labels(i, 3) * ones(end_point - start_point + 1, 1)];
    
    Lab_X = [Lab_X; X(start_point : end_point, :)];
    
    % check whether there is a gap or not
    if (i < size(Labels,1)) && (end_point + 1 ~= Labels(i+1, 4))

        % add a new data point as a flag
        labels = [labels; -1];
        Lab_X = [Lab_X; [0 0 0 0 0 0]];
    end
end


%% WINDOWING and LABELLING %%%%%%%%%


Window_data = {}; % type: cell
window_labels = [];

win_idx = 0; % window's index
i = 1;

while i <= (size(Lab_X, 1) - window_length)
    is_flag = false;
    flag_idx = 0;
    for i2 = i : (i + window_length - 1)
        if labels(i2) == -1 % have a gap in this window
            is_flag = true;
            flag_idx = i2;
            break
        end
    end
    if is_flag == true
        i = flag_idx + 1;
    else 
        win_idx = win_idx + 1;
        Window_data{win_idx} = Lab_X(i : i+window_length-1, :);
        window_labels(win_idx) = mode(labels(i : i+window_length-1)); % finding the most common label in the window
        i = i + (window_length - overlap);
    end        
end

%%

Window_data = Window_data';
window_labels = window_labels';

% =========================================================================
end