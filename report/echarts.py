from pyecharts import Bar,Pie

#### 统计表业绩
def eply_kpi_bar(data):
    bar = Bar("制造工效比",title_pos="10%",title_top='1%',width='100%')
    bar.add('',data['用户'],round(data['工效比'],2),legend_pos='38%',legend_top='7%',mark_line_raw=[{'yAxis': 1.2}],is_label_show=True,
        is_datazoom_show=True,datazoom_type='both',is_toolbox_show =False,xaxis_rotate=30)


    return bar.render_embed()
def eply_eff_bar(data):
    bar = Bar("工时有效率",title_pos="10%",title_top='1%',width='100%')
    bar.add('',data['用户'],round(data['工时有效率'],2),label_color=['#2f4554'],legend_pos='38%',legend_top='7%',mark_line_raw=[{'yAxis': 0.75}],is_label_show=True,
        is_datazoom_show=True,datazoom_type='both',is_toolbox_show =False,xaxis_rotate=30)

    return bar.render_embed()
#### 统计表工步
def op_bar(data):
    bar = Bar("工步统计",title_pos="10%",title_top='1%',width='100%')
    name = []
    qty = []
    for i in range(len(data)):
        name.append(data[i]['op_name'])
        qty.append(data[i]['qty'])
    bar.add('工步',name,qty,legend_pos='38%',legend_top='7%',label_color=['#FFB90F'],is_label_show=True,is_toolbox_show =False,xaxis_rotate=30)
    return bar.render_embed()

def support_bar(data,month):

    # for i in range(len(data)):

    bar = Bar(title='辅助工时',title_pos='10%',title_top='1%',width='100%')
        # bar.add('',data.columns,data['休息'],label_color=['#2f4554'])
    # month_list=[]
    # month_list.append(str(month))
    # if month !=0:
    bar.add('1月',data[0].columns, [ '%.2f' % eli for eli in data[0].iloc[0]],is_legend_show=True,is_label_show=True,legend_orient='vertical',legend_pos='right',
           is_toolbox_show=False,is_stack=True,label_color='red')
    bar.add('2月',data[1].columns,[ '%.2f' % eli for eli in data[1].iloc[0]],is_stack=True)
    bar.add('3月',data[2].columns,[ '%.2f' % eli for eli in data[2].iloc[0]],is_stack=True)
    bar.add('4月',data[3].columns,[ '%.2f' % eli for eli in data[3].iloc[0]],is_stack=True)
    bar.add('5月',data[4].columns,[ '%.2f' % eli for eli in data[4].iloc[0]],is_stack=True)
    bar.add('6月',data[5].columns,[ '%.2f' % eli for eli in data[5].iloc[0]],is_stack=True)

    bar.add('7月',data[6].columns,[ '%.2f' % eli for eli in data[6].iloc[0]],is_stack=True)
    bar.add('8月',data[7].columns,[ '%.2f' % eli for eli in data[7].iloc[0]],is_stack=True)
    bar.add('9月',data[8].columns,[ '%.2f' % eli for eli in data[8].iloc[0]],is_stack=True)
    bar.add('10月',data[9].columns,[ '%.2f' % eli for eli in data[9].iloc[0]],is_stack=True)
    bar.add('11月',data[10].columns,[ '%.2f' % eli for eli in data[10].iloc[0]],is_stack=True)
    bar.add('12月',data[11].columns,[ '%.2f' % eli for eli in data[11].iloc[0]],is_stack=True,label_color=['green','yellow','red','brown','orange',
        'grey','violet','#2f4554','gold','purple','blue','#FFB90F'],xaxis_rotate=30)

    #     return bar.render_embed()
    # else:
    #     bar.add('',month_list, data.iloc[0],is_legend_show=True,is_label_show=True,legend_orient='vertical',legend_pos='right',
    #         is_toolbox_show=False)
    return bar.render_embed()
    