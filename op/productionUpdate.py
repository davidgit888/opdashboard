from pyecharts import Bar,Line, Overlap
import pandas as pd
import plotly.offline as off
import plotly.graph_objs as go
import sqlite3



#######################1 first 3 bar chart and 3 lines together ##################
def waitingOrderInventory(path1,fileName1):
    data1 = pd.read_excel(path1+fileName1,sheet_name='backlog')

    dfOrder = data1.loc[0][2:]
    dfShip = data1.loc[1][2:]
    dfAss = data1.loc[2][2:]
    dfBack = data1.loc[6][2:]
    dfExcue = data1.loc[7][2:]
    dfNet = data1.loc[8][2:]
    months = data1.columns[2:]
    str_date_1 = [str(i) for i in months]
    bar_1 = Bar(title='整机“待执行订单” & “整机库存”数据汇总', title_pos="40%",title_top='1%',width='100%',height=700)

    bar_1.add('Order Qty', months, dfOrder, legend_pos='50%',legend_top='5%',label_color=['#2f4554'],is_label_show=True,is_toolbox_show =False)
    bar_1.add('Shipment Qty', months, dfShip,legend_top='5%',label_color=['#c23531'],is_label_show=True)
    bar_1.add('Actual Assembly Qty', months, dfAss,legend_top='5%',label_color=['#FFB90F'],is_label_show=True)


    line_1 = Line(width='100%')
    line_1.add('Backlog',str_date_1, dfBack, label_color=['#61a0a8'],
        line_width=3,
        is_label_show=True,
        is_toolbox_show =False)

    line_2 = Line(width='100%')
    line_2.add('To Be Excuted Order',str_date_1, dfExcue,
        line_width=3,
        label_color=['#d48265'],
        is_label_show=True,)

    line_3 = Line(width='100%')
    line_3.add('Net Available',str_date_1, dfNet, 
        line_width=3,
        label_color=['#749f83'],
        is_label_show=True,)

    overlap = Overlap(width='100%',height=600)
    overlap.add(bar_1)
    overlap.add(line_1)
    overlap.add(line_2)
    overlap.add(line_3)

    overlap.render('templates/op/Waiting_Order_and_Inventory.html')

##############Get Data#################
def getIdpData():
    conn = sqlite3.connect('db.sqlite3')
    installed = pd.read_sql('select * from op_installedcmm ORDER BY Year desc LIMIT 3',conn)
    del installed['id']
    
    installed = installed.sort_values('Year')
    installed = installed.set_index('Year')
    installed = installed.T
    
    delivered = pd.read_sql('select * from op_deliveredcmm ORDER BY Year desc LIMIT 3',conn)
    del delivered['id']
    delivered = delivered.sort_values('Year')
    delivered = delivered.set_index('Year')
    delivered = delivered.T

    produced = pd.read_sql('select * from op_neworder ORDER BY Year desc LIMIT 3',conn)
    del produced['id']
    produced = produced.sort_values('Year')
    produced = produced.set_index('Year')
    produced = produced.T
    return installed,delivered,produced


###############2 installed line and bar chart##########################   
def installedCmm(installed):

    installColumn=installed.columns

    attr = installed.index
    v1 = installed[installColumn[0]]
    v2 = installed[installColumn[1]]
    v3 = installed[installColumn[2]]
   



    barInstall = Bar(title="生产装机数量统计", title_pos="46%",title_top='1%',width='100%',height=600)

    barInstall.add(
        str(installColumn[0]), attr, v1, legend_pos='50%',legend_top='5%',label_color=['#c23531'],is_label_show=True,xaxis_name_gap=50,is_toolbox_show =False)

        # yaxis_formatter=" ml",
        # yaxis_max=250,
        # legend_pos="85%",
        # legend_orient="vertical",
        # legend_top="45%",

    barInstall.add(str(installColumn[1]), attr, v2,legend_top='5%',is_label_show=True,label_color=['grey'],xaxis_name_gap=50)
    barInstall.add(str(installColumn[2]), attr, v3,legend_top='5%',is_label_show=True,label_color=['blue'],xaxis_name_gap=50,
        yaxis_max="600")
    line = Line(width='100%')
    line.add(str(installColumn[0])+"年",attr,v1,label_color=['#c23531'],is_label_show=True,line_width=3,is_splitline_show=False,)
    line.add(str(installColumn[1])+"年",attr,v2,label_color=['#c23531'],is_label_show=True,line_width=3,is_splitline_show=False,)
    line.add(str(installColumn[2])+"年",attr,v3,label_color=['#c23531'],is_label_show=True,line_width=3,is_splitline_show=False,)
    overlap = Overlap(width='120%',height=600)
    overlap.add(barInstall)
    overlap.add(line,yaxis_index=1, is_add_yaxis=True)
    overlap.render('templates/op/Installed_CMM.html')


###########3 second delivered CMM chart##################
def deliveredCmm(delivered):

    deliveredColumn = delivered.columns
    attrDeliver = delivered.index
    dv1 = delivered[deliveredColumn[0]]
    dv2 = delivered[deliveredColumn[1]]
    dv3 = delivered[deliveredColumn[2]]
    
    barDelivered = Bar(title="生产发货量统计", title_pos='47%',title_top='1%',width='100%',height=600)

    barDelivered.add(str(deliveredColumn[0]), attrDeliver, dv1, legend_pos='50%',legend_top='5%',label_color=['#fab27b'], is_label_show=True,is_toolbox_show =False)
    barDelivered.add(str(deliveredColumn[1]), attrDeliver, dv2,legend_top='5%',is_label_show=True,label_color=['#2f4554'])
    barDelivered.add(str(deliveredColumn[2]), attrDeliver, dv3,legend_top='5%', is_label_show=True,label_color=['#f05b72'],yaxis_max="600")
    
   
    line = Line(width='100%')
    line.add(str(deliveredColumn[0])+"年",attrDeliver,dv1,label_color=['#fab27b'],is_label_show=True,line_width=3,is_splitline_show=False)
    line.add(str(deliveredColumn[1])+"年",attrDeliver,dv2,label_color=['#2f4554'],is_label_show=True,line_width=3,is_splitline_show=False)
    line.add(str(deliveredColumn[2])+"年",attrDeliver,dv3,label_color=['#f05b72'],is_label_show=True,line_width=3,is_splitline_show=False)
    overlap = Overlap(width='100%',height=600)
    overlap.add(barDelivered)
    overlap.add(line,yaxis_index=1, is_add_yaxis=True)
    overlap.render('templates/op/Delivered_CMM.html')



##########4 Third New Order line Chart###########
def newOrder(produced):
    
    producedColumn = produced.columns
    pattr= produced.index
    pv1 = produced[producedColumn[0]]
    pv2 = produced[producedColumn[1]]
    pv3 = produced[producedColumn[2]]
   

    pline = Line("新进生产订单数量汇总",title_pos='45%',title_top='1%',width='100%',height=600)

    pline.add(
        str(producedColumn[0]),
        pattr,
        pv1,
        mark_point=['max'],
        label_color=['#FFB90F'],
        line_width=3,
        is_label_show=True,
        is_toolbox_show =False,
        legend_top='5%',
    )
    pline.add(
        str(producedColumn[1]),
        pattr,
        pv2,
        mark_point=['max'],
        label_color=['grey'],
        is_label_show=True,
        line_width=3,
        legend_top='5%',
    )
    pline.add(
        str(producedColumn[2]),
        pattr,
        pv3,
        mark_point=['max'],
        label_color=['#D2691E'],
        is_label_show=True,
        line_width=3,
        legend_pos='center',
        legend_top='5%',
    )
    pline.render('templates/op/New_order.html')

###################5&6 Build Qty bar line chart and table############
def installedEachYear(path1, fileName1):
    dataBuild = pd.read_excel(path1+fileName1,sheet_name='Sheet1')
    date_b = dataBuild.columns[1:]
    bar_build = Bar(title='历年生产装机量汇总', title_pos="46%",title_top='1%',width='100%',height=600)

    bar_build.add(dataBuild['Model'][0],date_b, dataBuild.loc[0][1:],legend_top='8%',label_color=['#FFB90F'],is_label_show=True,is_toolbox_show =False,
    )
    bar_build.add(dataBuild['Model'][1],date_b, dataBuild.loc[1][1:],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add(dataBuild['Model'][2],date_b, dataBuild.loc[2][1:],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add(dataBuild['Model'][3],date_b, dataBuild.loc[3][1:],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add(dataBuild['Model'][4],date_b, dataBuild.loc[4][1:],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add(dataBuild['Model'][5],date_b, dataBuild.loc[5][1:],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add(dataBuild['Model'][6],date_b, dataBuild.loc[6][1:],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add(dataBuild['Model'][7],date_b, dataBuild.loc[7][1:],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add(dataBuild['Model'][8],date_b, dataBuild.loc[8][1:],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add(dataBuild['Model'][9],date_b, dataBuild.loc[9][1:],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add(dataBuild['Model'][10],date_b, dataBuild.loc[10][1:],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add(dataBuild['Model'][11],date_b, dataBuild.loc[11][1:],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add(dataBuild['Model'][12],date_b, dataBuild.loc[12][1:],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add(dataBuild['Model'][13],date_b, dataBuild.loc[13][1:],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add(dataBuild['Model'][14],date_b, dataBuild.loc[14][1:],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add(dataBuild['Model'][15],date_b, dataBuild.loc[15][1:],yaxis_max="1000",legend_orient='horizontal',legend_pos='center',legend_top='8%',
        visual_pos='20%',is_label_show=True,is_datazoom_show=True,datazoom_type='both',legend_selectedmode='multiple',xaxis_type='category',
        tooltip_trigger = 'axis')

    str_date = [str(i) for i in date_b]
    line_build = Line(width='100%')
    line_build.add(dataBuild['Model'][16],str_date, dataBuild.loc[16][1:], label_color=['#FFB90F'],
        line_width=3,
        is_label_show=True,
        legend_orient='horizontal',
        legend_pos='50%',
        legend_top='8%',
        is_splitline_show=False,
        is_toolbox_show =False)

    overlap = Overlap(width='100%',height=600)
    overlap.add(bar_build)
    overlap.add(line_build,yaxis_index=1, is_add_yaxis=True)
    overlap.render('templates/op/Installed_each_year.html')


    with open('templates/op/Installed_each_year.html', 'r',encoding='UTF-8') as myfile:
        data = myfile.read()


    index = data.find('"legend":')
    string1 = '''      "grid": {
    
            top:'20%',
            containLabel: true
        },'''
    dataGridTop = data[:index-1] + string1 + data[index:]
    Html_file= open('templates/op/Installed_each_year.html',"w",encoding='UTF-8')
    Html_file.write(dataGridTop)
    Html_file.close()

    ######################6, table 历年生产装机量汇总 #####################

    columns = dataBuild.columns
    dataBuild=dataBuild.fillna(0)
    trace = go.Table(
        header=dict(values=list(dataBuild.columns),
                    fill = dict(color='#C2D4FF'),
                    
                    align = ['center']),
        cells=dict(values=[list(dataBuild[columns[i]]) for i in range(len(columns))],
                fill = dict(color='#F5F8FF'),
                align = ['center']),
                    hoverinfo='all',
                    
                    )
    layout1 = dict(
        
        autosize=True,
        title='历年生产装机量汇总',
        
        showlegend=False,

    )

    data = [trace] 
    fig1 = dict(data=[trace], layout=layout1)
    off.plot(fig1,filename='templates/op/Installed each year bar.html',show_link=False,auto_open=False)


path = '../excel/'
fileName = 'dashboard.xlsx'
path1 = "../excel/"
fileName1 = 'history.xlsx'

# try:
#     waitingOrderInventory(path1,fileName1)
#     print("Waiting Order is successful")
# except Exception as ex:
#     template = "An exception of type {0} occurred. Arguments:\n{1!r}"
#     message = template.format(type(ex).__name__, ex.args)
#     print("Error in Waiting Order",message)
def updateProduction():
    results = []
    try:
        installed, delivered,produced = getIdpData()
        global g_installed
        global g_delivered
        global g_produced
        g_installed = installed
        g_delivered = delivered
        g_produced = produced 

        #results.append("Get data successfully")
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)

        results.append('Cannot get Data'+message)

    try:
        installedCmm(g_installed)
        # print("Installed CMM is successful")
        results.append('Installed CMM is successful')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        results.append("Error in Installed CMM" + message)

    try:
        deliveredCmm(g_delivered)
        print("Delivered CMM is successful")
        results.append('Delivered CMM is successful')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        # print("Error in Delivered CMM", message)
        results.append("Error in Delivered CMM" + message)
    try:
        newOrder(g_produced)
        # print('New Order is successful')
        results.append('New Order is successful')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        # print("Error in New Order", message)
        results.append("Error in New Order" + message)

    return results
# try:
#     installedEachYear(path,fileName1)
#     print('Installed CMM Each Year is successful')
# except Exception as ex:
#     template = "An exception of type {0} occurred. Arguments:\n{1!r}"
#     message = template.format(type(ex).__name__, ex.args)
#     print('Installed CMM Each Year cannot be executed',message)

# input("Press enter key to exit ")
