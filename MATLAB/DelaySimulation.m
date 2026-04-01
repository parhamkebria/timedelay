%%
clc
clear
close all
%%
Stime=100;  % Sec
Npack=5000 ;% Packet
PackSend.Time= sort(randperm(1.5*Npack,Npack))*Stime/(1.5*Npack);
%% Simulated Delay
s='0';
while(s~='l'&& s~='L'&& s~='s'&& s~='S')
    s=input('L=LongDistance  S=ShortDistance    : ','s'); 
end
%% Simulated delay
if (s=='l' | s=='L')
    mn= 1.52;
    sd= 0.38;
    Simdelay=mn+sd*randn(1,Npack);

elseif (s=='s' | s=='S')
    Min=.002
    lambda=.002
    Simdelay=Min+exprnd(lambda, 2,Npack);
end
%%
k=1;
nT(1)=0;
V(1)=0;
for i=1:Npack
    k=k+1;
    V(k)=0;
    nT(k)=PackSend.Time(i);
    
    k=k+1;
    V(k)=1;
    nT(k)=PackSend.Time(i)+0.00001;
    
    k=k+1;
    V(k)=1;
    nT(k)=PackSend.Time(i)+Simdelay(i);  
    
    k=k+1;
    V(k)=0;
    nT(k)=PackSend.Time(i)+Simdelay(i)+0.00001;
end 
figure (1)
subplot(221)
plot(nT,V)
title('5000 packets with random send time and random delay time')
axis([0 nT(end) -2 5])
hold on 
plot(nT(1000:1100),V(1000:1100),'r')
subplot(222)
plot(nT(1000:1100),V(1000:1100),'r')
title('zoom on the read segment/delay is the width of each pulse')
axis([nT(1000) nT(1100) -2 5])
%%
subplot(223)
hist(Simdelay,100);
title('Frequency distribution')
[nelement centres]=hist(Simdelay,100);
sum(nelement);

if (s=='l' | s=='L')
    MinDelay=min(Simdelay);
    MeanDelay=mean(Simdelay);
    stdDealy= std(Simdelay);
elseif (s=='s' | s=='S')
    MinDelay=min(Simdelay);
    MeanDelay=mean(Simdelay-MinDelay);
    stdDealy= std(Simdelay-MinDelay);
end


%% Probability fit
subplot(224)
plot(centres,nelement/1);
hold on
if (s=='l' | s=='L')
    pd = fitdist(Simdelay','Normal');
    x=linspace(0.005,0.015,100);
    dx=0.010/100;
    Pdf = pdf(pd,x)*dx;
    Pdf=Pdf/sum(Pdf);
    sum(Pdf)
    plot(x,Pdf,'LineWidth',2);
    legend(strcat('Measured','mean =',num2str(pd.mu),' std=', num2str(pd.sigma)),strcat('Distribution Fit ','mean =',num2str(pd.mu),' std=', num2str(pd.sigma)))
elseif (s=='s' | s=='S')
    pd = fitdist(Simdelay'-MinDelay,'Exponential');
    x=linspace(0,0.020,100);
    dx=0.020/100;
    Pdf = pdf(pd,x)*dx/1.039;
    Pdf=Pdf/sum(Pdf);
    sum(Pdf);
    plot(MinDelay+x,Pdf,'LineWidth',2);
    legend(strcat('Measured','mean =',num2str(pd.mu)),strcat('Distribution Fit ','mean =',num2str(pd.mu)))
end
title('Distribution fit')
%%
% run 'DelayModel1.slx'
figure(2)
subplot(1,3,3)
h=histogram(Simdelay,100);
h.FaceColor = [0 0 1];
h.EdgeColor = 'b';
[nelement centres]=hist(Simdelay,100);
sum(nelement);
if (s=='l' | s=='L')
    MinDelay=min(Simdelay);
    MeanDelay=mean(Simdelay);
    stdDealy= std(Simdelay);
elseif (s=='s' | s=='S')
    MinDelay=min(Simdelay);
    MeanDelay=mean(Simdelay-MinDelay);
    stdDealy= std(Simdelay-MinDelay);
end
hold on
plot(centres,nelement/1,'r','LineWidth',2);
legend(strcat('Frequency distribution'),strcat('Distribution mean =',num2str(pd.mu),' std=', num2str(pd.sigma)))

subplot(1,3,[1 2])
% plot(Delay)
%%
SimDelay.time=PackSend.Time'
SimDelay.signals.values=Simdelay'