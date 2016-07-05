%initializing and running fcm on log rms values of muscles
%code can be run in MATLAB/octave

%change filename if needed
X = csvread('test.csv',2);
%second number changes clusters (goes up to 6 thus far)
%can add more in for loop
[A,B,C] = fcm(X,4);

[~,maxindex] = max(B,[],1);
maxindex = maxindex(:);

%plotting all the values on one figure
for i = 1:size(X,1),
    figure(2);
    plot(X(i,1),X(i,2),'blacko');
    hold on;
end

%plotting the values grouped by their highest membership value
for i = 1:size(maxindex,1),
    if maxindex(i,1)==1,
        figure(1);
        plot(X(i,1), X(i,2), 'go');
    elseif maxindex(i,1)==2,
        figure(1);
        plot(X(i,1), X(i,2), 'yo');
    elseif maxindex(i,1)==3,
        figure(1);
        plot(X(i,1), X(i,2), 'ro');
    elseif maxindex(i,1)==4,
        figure(1);
        plot(X(i,1), X(i,2), 'bo');
    elseif maxindex(i,1)==5,
        figure(1);
        plot(X(i,1), X(i,2), 'mo');
    elseif maxindex(i,1)==6,
        figure(1);
        plot(X(i,1), X(i,2), 'co');
    else
        figure(1);
        plot(X(i,1), X(i,2), 'blacko');
    end
    hold on;
end


%plotting centroids
A
figure(1);
x = A(:,1);
y = A(:,2);
plot(x,y,'.black', 'MarkerSize', 10);
hold on;

