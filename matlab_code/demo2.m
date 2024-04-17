% By�������Ŀ����ճ�
% ����������ͼ

%% ������ɫ
% C = ColorPM(384:-1:1);
C = ColorPM(1:384);

%% ����׼��
N = size(C,1);
X = linspace(0,pi*3,1000);
Y = bsxfun(@(x,n)n*sin(x+2*n*pi/N), X(:), 1:N);

%% ͼƬ�ߴ����ã���λ�����ף�
figureUnits = 'centimeters';
figureWidth = 15;
figureHeight = 15;

%% ��������
figureHandle = figure('color','w');
set(gcf, 'Units', figureUnits, 'Position', [0 0 figureWidth figureHeight]); % define the new figure dimensions
hold on

%% ��ͼ
plot(X,Y, 'linewidth',0.8)

%% ��ɫ
colororder(C)

%% ����������
set(gca, 'Box', 'off', ...                                % �߿�
         'layer','bottom',...
         'LineWidth', 1, 'GridLineStyle', '-',...
         'XGrid', 'off', 'YGrid', 'on', ...               % ����
         'TickDir', 'out', 'TickLength', [.005 .005], ... % �̶�
         'XMinorTick', 'off', 'YMinorTick', 'off', ...    % С�̶�
         'XColor', [.1 .1 .1],  'YColor', [.1 .1 .1],...  % ��������ɫ
         'Xlim',[0 9])  

% �̶ȱ�ǩ������ֺ�
set(gca, 'FontName',  'Helvetica', 'FontSize', 11)

export_fig('test2.png','-r300')