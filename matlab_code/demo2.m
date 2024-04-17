% By：阿昆的科研日常
% 大批量折线图

%% 设置颜色
% C = ColorPM(384:-1:1);
C = ColorPM(1:384);

%% 数据准备
N = size(C,1);
X = linspace(0,pi*3,1000);
Y = bsxfun(@(x,n)n*sin(x+2*n*pi/N), X(:), 1:N);

%% 图片尺寸设置（单位：厘米）
figureUnits = 'centimeters';
figureWidth = 15;
figureHeight = 15;

%% 窗口设置
figureHandle = figure('color','w');
set(gcf, 'Units', figureUnits, 'Position', [0 0 figureWidth figureHeight]); % define the new figure dimensions
hold on

%% 绘图
plot(X,Y, 'linewidth',0.8)

%% 赋色
colororder(C)

%% 坐标区调整
set(gca, 'Box', 'off', ...                                % 边框
         'layer','bottom',...
         'LineWidth', 1, 'GridLineStyle', '-',...
         'XGrid', 'off', 'YGrid', 'on', ...               % 网格
         'TickDir', 'out', 'TickLength', [.005 .005], ... % 刻度
         'XMinorTick', 'off', 'YMinorTick', 'off', ...    % 小刻度
         'XColor', [.1 .1 .1],  'YColor', [.1 .1 .1],...  % 坐标轴颜色
         'Xlim',[0 9])  

% 刻度标签字体和字号
set(gca, 'FontName',  'Helvetica', 'FontSize', 11)

export_fig('test2.png','-r300')