clc; close all;
x = input('Enter the first sequence');
h = input('Enter the second sequence');
y = xcorr(x,h);
figure;
subplot(3,1,1);
stem(x); 
ylabel('Amplitude');
subplot(3,1,2);
stem(h);
ylabel('Amplitude');
subplot(3,1,3);
stem(fliplr(y));
ylabel('Amplitude');
disp('The reultant signal is'); fliplr(y)