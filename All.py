import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

df = pd.read_excel("1_my_data.xlsx")
counter = 1
# 计算dQ/dV
def calculate_dQ_dV(capacity_col,df):
    df = df.dropna(subset=['总电压(V)'])  # 删除'总电压(V)'列中有缺失值的行
    capacity_col = capacity_col.dropna()  # 删除capacity_col中有缺失值的行
    dV = df['总电压(V)'].diff()
    dQ = capacity_col.diff()
    return dQ / dV
# 准备绘制dQ/dV曲线的函数
def plot_dQ_dV_curves(x_col, y_col, title, mode='lines', y_range=None):
    fig = go.Figure()

    # 分别绘制每个循环的充电和放电曲线
    for cycle, group in df.groupby('循环'):
        fig.add_trace(go.Scatter(
            x=group[x_col],
            y=group[y_col],
            mode=mode,
            name=f'循环 {cycle}',
            line=dict(width=2),  # 可以根据需要调整线宽
            customdata=group['循环']
        ))

    fig.update_layout(
        title=title,
        xaxis_title=x_col.replace('_', ' ').capitalize(),
        yaxis_title=y_col.replace('_', ' ').capitalize(),
        legend_title_text='循环次数',
        legend=dict(traceorder="normal"),
        yaxis=dict(range=y_range) if y_range else dict()  # 设置 y 轴范围
    )
    fig.write_image(f"static/img2/{counter}.png")


def generator_graph():  
    # 读取数据
    global counter
    # 数据预处理
    # 将字符串形式的时长转换为timedelta类型，以便进行时间运算和分析
    df['总运行时间'] = pd.to_timedelta(df['总运行时间'].str.replace('d', ' days'))
    df['单步时间'] = pd.to_timedelta(df['单步时间'].str.replace('d', ' days'))

    # 确保关键列如'充/放'、'循环'、'充电容量(AH)'、'放电容量(AH)'、'总电压(V)'等已经为正确的数据类型
    df['充/放'] = df['充/放'].astype(str)  # 确保充放电标记为字符串类型
    df['循环'] = df['循环'].astype(int)      # 确保循环次数为整型
    df['充电容量(AH)'] = df['充电容量(AH)'].astype(float)
    df['放电容量(AH)'] = df['放电容量(AH)'].astype(float)
    df['总电压(V)'] = df['总电压(V)'].astype(float)

    # 将字符串类型的循环次数转换为整数类型，以便进行数值计算和比较
    df['循环'] = df['循环'].astype(int)

    # 提取充放电结束时的容量数据
    df_charge_end = df[df['充/放'] == 'CH'].groupby('循环').agg({'充电容量(AH)': 'max'}).reset_index()
    df_discharge_end = df[df['充/放'] == 'DIS'].groupby('循环').agg({'放电容量(AH)': 'max'}).reset_index()


    # 将电流、电压和容量的字符串表示转换为相应的浮点数类型，以便进行精确的计算
    df['电流(A)'] = df['电流(A)'].astype(float)
    df['总电压(V)'] = df['总电压(V)'].astype(float)

    # 对每个电池的电压进行类型转换，以便进行电池性能的比较和分析
    for i in range(1, 7):
        df[f'电池{i}(V)'] = df[f'电池{i}(V)'].astype(float)

    # 将充电和放电容量的字符串表示转换为浮点数类型，以便计算和分析电池的容量表现
    df['充电容量(AH)'] = df['充电容量(AH)'].astype(float)
    df['放电容量(AH)'] = df['放电容量(AH)'].astype(float)

    # 将环境温度的字符串表示转换为浮点数类型，以便分析温度对电池性能的影响
    df['环境温度(°C)'] = df['环境温度(°C)'].astype(float)



    #电压：
    # 创建充电容量的线条图
    fig_current_capacity = go.Figure()

    # 循环遍历每个循环，创建充电容量的线条，自动分配颜色
    for cycle, group in df.groupby('循环'):
        fig_current_capacity.add_trace(go.Scatter(
            x=group['充电容量(AH)'],
            y=group['总电压(V)'],
            mode='lines',
            name=f'充电 - 循环 {cycle}',
            customdata=group['循环']
        ))

        # 添加放电容量的线条，自动分配颜色并设置为虚线
        fig_current_capacity.add_trace(go.Scatter(
            x=group['放电容量(AH)'],
            y=group['总电压(V)'],
            mode='lines',
            line=dict(dash='dash'),
            name=f'放电 - 循环 {cycle}',
            customdata=group['循环']
        ))

    # 更新图例，确保图例只显示一次
    fig_current_capacity.update_layout(legend=dict(traceorder="normal"),
                                    title="电压与容量的变化曲线",
                                    xaxis_title='充电/放电容量 (AH)',
                                    yaxis_title='总电压 (V)'
                                    )
    # 显示图表
    fig_current_capacity.write_image("static/img2/a.png")


    #电流：
    # 创建充电容量的线条图
    fig_current_capacity = go.Figure()

    # 循环遍历每个循环，创建充电容量的线条，自动分配颜色
    for cycle, group in df.groupby('循环'):
        fig_current_capacity.add_trace(go.Scatter(
            x=group['充电容量(AH)'],
            y=group['电流(A)'],
            mode='lines',
            name=f'充电 - 循环 {cycle}',
            customdata=group['循环']
        ))

        # 添加放电容量的线条，自动分配颜色并设置为虚线
        fig_current_capacity.add_trace(go.Scatter(
            x=group['放电容量(AH)'],
            y=group['电流(A)'],
            mode='lines',
            line=dict(dash='dash'),
            name=f'放电 - 循环 {cycle}',
            customdata=group['循环']
        ))

    # 更新图例，确保图例只显示一次
    fig_current_capacity.update_layout(legend=dict(traceorder="normal"),
                                    title="电流与容量的变化曲线",
                                    xaxis_title='充电/放电容量 (AH)',
                                    yaxis_title='电流(A)')

    # 显示图表
    fig_current_capacity.write_image("static/img2/b.png")



    #温度：
    # 创建充电容量的线条图
    fig_current_capacity = go.Figure()

    # 循环遍历每个循环，创建充电容量的线条，自动分配颜色
    for cycle, group in df.groupby('循环'):
        fig_current_capacity.add_trace(go.Scatter(
            x=group['充电容量(AH)'],
            y=group['环境温度(°C)'],
            mode='lines',
            name=f'充电 - 循环 {cycle}',
            customdata=group['循环']
        ))

        # 添加放电容量的线条，自动分配颜色并设置为虚线
        fig_current_capacity.add_trace(go.Scatter(
            x=group['放电容量(AH)'],
            y=group['环境温度(°C)'],
            mode='lines',
            line=dict(dash='dash'),
            name=f'放电 - 循环 {cycle}',
            customdata=group['循环']
        ))

    # 更新图例，确保图例只显示一次
    fig_current_capacity.update_layout(legend=dict(traceorder="normal"),
                                    title="环境温度与容量的变化曲线",
                                    xaxis_title='充电/放电容量 (AH)',
                                    yaxis_title='环境温度(°C)')
    # 显示图表
    fig_current_capacity.write_image("static/img2/c.png")


    # 绘制容量衰减曲线
    fig_capacity_decay = go.Figure()
    fig_capacity_decay.add_trace(go.Scatter(x=df_charge_end['循环'], y=df_charge_end['充电容量(AH)'], mode='lines+markers', name='充电容量'))
    fig_capacity_decay.add_trace(go.Scatter(x=df_discharge_end['循环'], y=df_discharge_end['放电容量(AH)'], mode='lines+markers', name='放电容量'))
    fig_capacity_decay.update_layout(title='容量衰减曲线', xaxis_title='循环次数', yaxis_title='容量(AH)')
    fig_capacity_decay.write_image("static/img2/d.png")


    fig_accumulated_capacity = go.Figure()

    for cycle in df['循环'].unique():
        cycle_data = df[df['循环'] == cycle]
        # 假设我们为每个点添加标签，标签内容为'循环X'，位置取每组数据的中位数以避免重叠
        text_labels = [f'循环 {cycle}' for _ in range(len(cycle_data))]
        fig_accumulated_capacity.add_trace(
            go.Scatter(
                x=cycle_data['充电容量(AH)'] - cycle_data['放电容量(AH)'],
                y=cycle_data['总电压(V)'],
                mode='lines+markers',
                name=f'循环 {cycle}',
                text=text_labels,  # 添加文本标签
                # 可选：为文本标签设置显示位置，这里假设在(0.5 * x_max, y_mean)处显示
                textposition="top center",  # 设置文本标签的位置
            )
        )

    fig_accumulated_capacity.update_layout(title='累积容量曲线', xaxis_title='容量(AH)', yaxis_title='总电压(V)')
    fig_accumulated_capacity.write_image("static/img2/e.png")

    # 提取充电和放电数据
    charging_data = df[df['充/放'] == 'CH']
    discharging_data = df[df['充/放'] == 'DIS']

    # df[df['充/放'] == 'CH'].groupby('循环').agg({'充电容量(AH)': 'max'}).reset_index()
    # df[df['充/放'] == 'DIS'].groupby('循环').agg({'放电容量(AH)': 'max'}).reset_index()

    # 计算累积容量
    charging_data['累积容量'] = charging_data['充电容量(AH)'].cumsum()
    discharging_data['累积容量'] = -discharging_data['放电容量(AH)'].cumsum()

    # 设置中文显示
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决坐标轴负号'-'显示为方块的问题


    # 使用Plotly绘制累积容量与总电压曲线
    fig_accumulated_voltage = go.Figure()

    # 绘制充电曲线
    fig_accumulated_voltage.add_trace(go.Scatter(x=charging_data['累积容量'], y=charging_data['总电压(V)'],
                                                mode='lines+markers', name='充电', line=dict(color='blue')))

    # 绘制放电曲线
    fig_accumulated_voltage.add_trace(go.Scatter(x=discharging_data['累积容量'], y=discharging_data['总电压(V)'],
                                                mode='lines+markers', name='放电', line=dict(color='red')))

    # 更新布局
    fig_accumulated_voltage.update_layout(
        title='累积容量与总电压曲线',
        xaxis_title='累积容量 (AH)',
        yaxis_title='总电压 (V)',
        legend=dict(orientation="h", xanchor="center", x=0.5, y=-0.2),
    )

    # 显示图形
    fig_accumulated_voltage.write_image("static/img2/f.png")




    # 假设df是包含充放电数据的DataFrame，至少包括'循环', '电压(V)', '充电容量(AH)', '放电容量(AH)'列





    # 对充电和放电数据分别计算dQ/dV
    df['dQ/dV_充电'] = calculate_dQ_dV(df['充电容量(AH)'],df)
    df['dQ/dV_放电'] = calculate_dQ_dV(df['放电容量(AH)'],df)


    


    # 绘制四幅dQ/dV曲线图
    plot_dQ_dV_curves('总电压(V)', 'dQ/dV_充电', "dQ/dV曲线 - 充电过程电压变化",y_range=[-325,3000])
    counter+=1
    plot_dQ_dV_curves('总电压(V)', 'dQ/dV_放电', "dQ/dV曲线 - 放电过程电压变化",y_range=[-250,5])
    counter+=1
    plot_dQ_dV_curves('充电容量(AH)', 'dQ/dV_充电', "dQ/dV曲线 - 充电过程容量变化",y_range=[-350,3000])
    counter+=1
    plot_dQ_dV_curves('放电容量(AH)', 'dQ/dV_放电', "dQ/dV曲线 - 放电过程容量变化", y_range=[-13,3])


    # 打印数据的基本信息
    print("数据的基本信息：")
    print(df.info())

    # 统计各个参数的描述性统计信息
    print("\n各个参数的描述性统计信息：")
    df.describe().to_csv('descriptive_stats.csv')
    #print(df.describe())

    # 设置中文显示
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决坐标轴负号'-'显示为方块的问题

    # 将字符串值替换为数值
    df['充/放'] = df['充/放'].replace({'DIS': 0, 'CH': 1})

    # 绘制各个参数之间的关系图
    # sns.pairplot(df[['充/放', '电流(A)', '总电压(V)', '环境温度(°C)', '充电容量(AH)', '放电容量(AH)']])
    # plt.savefig('last.png')
    # plt.show()
    # 使用修改后的数据绘制pairplot，其中0对应蓝色（放电），1对应红色（充电）
    sns.pairplot(df[['充/放', '电流(A)', '总电压(V)', '环境温度(°C)', '充电容量(AH)', '放电容量(AH)']],
                hue="充/放",
                palette=sns.color_palette(["blue", "red"]))  # 指定颜色：放电-蓝色，充电-红色

    plt.savefig('static/img2/g.png')  # 保存图表



    # 计算相关性矩阵
    correlation_matrix = df[['电流(A)', '总电压(V)', '充电容量(AH)', '放电容量(AH)', '环境温度(°C)', '循环']].corr()

    # 热图显示相关性矩阵
    plt.figure(figsize=(10, 8))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体字体显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 确保负号显示正常
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('参数相关性分析热图')

    plt.savefig('static/img2/h.png')  # 保存图表



