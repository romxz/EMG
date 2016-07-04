%initializing and running fcm on log rms values of muscles

%change filename if needed
X = csvread('g_forearm4.csv',2);
%second number changes clusters
[A,B] = kmeans(X,6);
maxindex = size(A,1);

%plotting all the values on one figure
for i = 1:size(X,1),
    figure(2);
    plot(X(i,1),X(i,2),'blacko');
    hold on;
end

%plotting the values grouped by their highest membership value
for i = 1:maxindex,
    if A(i,1)==1,
        figure(3);
        plot(X(i,1), X(i,2), 'go');
    elseif A(i,1)==2,
        figure(3);
        plot(X(i,1), X(i,2), 'yo');
    elseif A(i,1)==3,
        figure(3);
        plot(X(i,1), X(i,2), 'ro');
    elseif A(i,1)==4,
        figure(3);
        plot(X(i,1), X(i,2), 'blo');
    elseif A(i,1)==5,
        figure(3);
        plot(X(i,1), X(i,2), 'mo');
    elseif A(i,1)==6,
        figure(3);
        plot(X(i,1), X(i,2), 'co');
    else
        figure(3);
        plot(X(i,1), X(i,2), 'blacko');
    end
    hold on;
end


%plotting centroids
B
figure(3);
x = B(:,1);
y = B(:,2);
plot(x,y,'.black', 'MarkerSize', 10);
hold on;
