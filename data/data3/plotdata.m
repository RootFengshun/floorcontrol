
clear all
figure(1)
text=load('plotdata.log');
num=[5 10 15 20 25];
plot(num,text(1,:),'r')
hold on
plot(num,text(2,:),'g')
hold on
plot(num,text(3,:),'b')
legend('No Backoff','BEB Backoff','Adaptive Backoff')
xlabel('number of nodes')
ylabel('Wc')
axis([5 25 0.0 1.2])



clear all
figure(2)
text=load('plotdata.log');
num=[5 10 15 20 25];
plot(num,text(4,:),'r')
hold on
plot(num,text(5,:),'g')
hold on
plot(num,text(6,:),'b')
legend('No Backoff','BEB Backoff','Adaptive Backoff')
xlabel('number of nodes')
ylabel('establish delay(s)')
axis([5 25 0.0 25])


clear all
figure(3)
text=load('plotdata.log');
num=[5 10 15 20 25];
plot(num,text(7,:)./10000,'r')
hold on
plot(num,text(8,:)/10000,'g')
hold on
plot(num,text(9,:)/10000,'b')
legend('No Backoff','BEB Backoff','Adaptive Backoff')
xlabel('number of nodes')
ylabel('fairness)')
axis([5 25 0.50 1.5])

