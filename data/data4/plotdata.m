% 
% clear all
% figure(1)
% text=load('plotdata.log');
% num=[4 8 16 32 64 128 256];
% 
% plot(num,text(2,:),'b')
% hold on
% plot(num,text(3,:),'b')
% grid on
% legend('BEB Backoff','Adaptive Backoff')
% xlabel('number of nodes')
% ylabel('success rate')
% axis([4 256 0 1.5])
% figure(1)

% 
% clear all
% figure(2)
% text=load('plotdata.log');
% num=[4 8 16 32 64 128 256];
% 
% plot(num,text(5,:),'g')
% hold on
% plot(num,text(6,:),'b')
% grid on
% legend('BEB Backoff','Adaptive Backoff')
% xlabel('number of nodes')
% ylabel('request delay(s)')
% axis([4 256 0.0 2.3])
% 

clear all
figure(3)
text=load('plotdata.log');
num=[4 8 16 32 64 128 256];

plot(num,text(8,:)/10000,'g')
hold on
plot(num,text(9,:)/10000,'b')
grid on
legend('BEB Backoff','Adaptive Backoff')
xlabel('number of nodes')
ylabel('fairness')
axis([4 256 0.80 1.3])
% 
% clear all
% figure(4)
% text=load('plotdata.log');
% num=[4 8 16 32 64 128 256];
% 
% plot(num,text(11,:)*3./3600,'g')
% hold on
% plot(num,text(12,:)*3./3600,'b')
% grid on
% legend('BEB Backoff','Adaptive Backoff')
% xlabel('number of nodes')
% ylabel('traffic')
% axis([4 256 0 1.2])

