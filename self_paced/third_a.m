% Problem 3A: Walking or not walking (Part A: Preliminary processing)

% Load the data file which contains a variable called mat_data 
load acc_data
% The matrix mat_data has 51635 rows and 4 columns 
% 
% Column 1: The time at which the acceleration is measured 
% Column 2: Acceleration in x-axis
% Column 3: Acceleration in y-axis
% Column 4: Acceleration in z-axis

% YOUR TASK: 
% Create a column vector vec_time which contains the first column of the 
% the matrix mat_data
% Note that you will only be using the vector vec_time for plotting, 
% you won't be using this vector for calculations  
% You must call your variable vec_time because the test looks for this
% variable name. 
vec_time = mat_data(1:end,1:1)

% YOUR TASK: 
% Create a matrix called mat_acc_3axes which contains columns 2-4 of 
% the matrix mat_data.
% The matrix mat_acc_3axes must have the same number of rows as the matrix
% mat_data and 3 columns.
% You must call your variable mat_acc_3axes because the test looks for 
% this variable name. 
mat_acc_3axes = mat_data(:,2:4)

% Recommended but optional task: Plot the accelerations in the three axes
% Uncomment the following 5 lines to see a plot of the acceleration
% figure(1)
% plot(vec_time,mat_acc_3axes)
% xlabel('time')
% ylabel('Acceleration')
% legend('x','y','z')
figure(1)
plot(vec_time,mat_acc_3axes)
xlabel('time')
ylabel('Acceleration')
legend('x','y','z')
% YOUR TASK: 
% Use the matrix mat_acc_3axes to calculate the total acceleration 
% You must assign the results to a column vector called vec_acc_total 
% This column vector has the same number of rows as mat_acc_3axes
% You must call your variable vec_acc_total because the test looks for 
% this variable name.
% Prohibition: You must NOT use any loops. 
vec_acc_total = sqrt(sum(mat_acc_3axes.^2,2))

% Recommended but optional task: Plot the total acceleration 
% Uncomment the following 5 lines to see a plot of the total acceleration
% figure(2)
% plot(vec_time,vec_acc_total)
% xlabel('time')
% ylabel('Acceleration')
% legend('total acceleration')
