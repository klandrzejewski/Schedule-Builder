% Read in the data
x = csvread('x.csv');
y = csvread('y.csv');

% Make predictions using the neural network function
predicted_z = neuralNetworkFunction([x ; y]);

% Save the predicted values to a CSV file
csvwrite('z-predicted.csv', predicted_z);