% 
clear all
figure(1)
text=load('plotdata.log');
num=[4 8 16 32 64 128 256];

plot(num,text(2,:),'ko-','LineWidth',1)
hold on
plot(num,text(3,:),'ks-','LineWidth',1)
grid on
legend('二进制指数退避','自适应退避')
xlabel('节点数')
ylabel('成功率')
axis([4 256 0 1.5])
figure(1)


clear all
figure(2)
text=load('plotdata.log');
num=[4 8 16 32 64 128 256];
plot(num,text(5,:),'ko-','LineWidth',1)
hold on
plot(num,text(6,:),'ks-','LineWidth',1)
grid on
legend('二进制指数退避','自适应退避')
xlabel('节点数')
ylabel('发起时延')
axis([4 256 0.0 2.3])


clear all
figure(3)
text=load('plotdata.log');
num=[4 8 16 32 64 128 256];

plot(num,text(8,:)/10000,'ko-','LineWidth',1)
hold on
plot(num,text(9,:)/10000,'ks-','LineWidth',1)
grid on
legend('二进制指数退避','自适应退避')
xlabel('节点数')
ylabel('公平性')
axis([4 256 0.70 1.2])

clear all
figure(4)
text=load('plotdata.log');
num=[4 8 16 32 64 128 256];

plot(num,text(11,:)*3./3600,'ko-','LineWidth',1)
hold on
plot(num,text(12,:)*3./3600,'ks-','LineWidth',1)
grid on
legend('二进制指数退避','自适应退避')
xlabel('节点数')
ylabel('话务量')
axis([4 256 0 1.2])

