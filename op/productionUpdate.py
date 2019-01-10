from pyecharts import Bar,Line, Overlap
import pandas as pd
import plotly.offline as off
import plotly.graph_objs as go

from .models import InstalledCmm, DeliveredCmm, NewOrder, WaitingOrderAndInventory,InstalledEachYear



#######################1 first 3 bar chart and 3 lines together ##################
def waitingOrderInventory(waiting):
    

    dfOrder = waiting.iloc[0]
    dfShip = waiting.iloc[1]
    dfAss = waiting.iloc[2]
    dfBack = waiting.iloc[6]
    dfExcue = waiting.iloc[7]
    dfNet = waiting.iloc[8]
    months = waiting.columns
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
    # conn = sqlite3.connect('db.sqlite3')
    # installed = pd.read_sql('select * from op_installedcmm ORDER BY Year desc LIMIT 3',conn)
    # del installed['id']
    
    # installed = installed.sort_values('Year')
    # installed = installed.set_index('Year')
    # installed = installed.T
    
    # delivered = pd.read_sql('select * from op_deliveredcmm ORDER BY Year desc LIMIT 3',conn)
    # del delivered['id']
    # delivered = delivered.sort_values('Year')
    # delivered = delivered.set_index('Year')
    # delivered = delivered.T

    # produced = pd.read_sql('select * from op_neworder ORDER BY Year desc LIMIT 3',conn)
    # del produced['id']
    # produced = produced.sort_values('Year')
    # produced = produced.set_index('Year')
    # produced = produced.T

    inLen=InstalledCmm.objects.all().count()
    installedObj = InstalledCmm.objects.all().values()[inLen-3:inLen]
    installed = pd.DataFrame(list(installedObj),columns=['id','Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    del installed['id']
    installed = installed.set_index('Year')
    installed = round(installed,0)
    installed = installed.T
    # print(installed)
    inLen2=DeliveredCmm.objects.all().count()
    deliveredObj = DeliveredCmm.objects.all().values()[inLen2-3:inLen2]
    delivered = pd.DataFrame(list(deliveredObj),columns=['id','Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    del delivered['id']
    delivered = delivered.set_index('Year')
    delivered = round(delivered,0)
    delivered = delivered.T

    inLen3=NewOrder.objects.all().count()
    producedObj = NewOrder.objects.all().values()[inLen3-3:inLen3]
    produced = pd.DataFrame(list(producedObj),columns=['id','Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    del produced['id']
    produced = produced.set_index('Year')
    produced = round(produced,0)
    produced = produced.T

    
    wObj = WaitingOrderAndInventory.objects.all().values()
    waiting = pd.DataFrame(list(wObj),columns=['id','YearAndMonth','OrderQty','ShipmentQty','AuctalAssemblyQty','ToBeExcutedTendency','BackLogTendency','NetAvailableTendency','Backlog','ToBeExcutedOrder','NetAvailable'])
    waiting.sort_values('id')
    del waiting['id']
    waiting = waiting.set_index('YearAndMonth')
    waiting = round(waiting,0)
    waiting = waiting.T
    

    eObj = InstalledEachYear.objects.all().values()
    eachYear = pd.DataFrame(list(eObj),columns=['id','Year','Global_A','Global_B','Global_C','Global_D','Global_EF','Explorer','Inspector_Pioneer_InspectorP_GlobalP','MH3D_Inspector454_Explorer454','Optive_Vision','Toro_ToroImage','Micro_Plus','Alpha_Apollo','Function_Pluse','Zoo_ZC','Stinger_ll','Global_Mini','Auctual_Build_Qty'])
    eachYear.sort_values('id')
    del eachYear['id']
    eachYear = eachYear.set_index('Year')
    eachYear = round(eachYear,0)
    eachYear = eachYear.T
    eachYear = eachYear.fillna('-')
    return installed,delivered,produced,waiting,eachYear


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
def installedEachYear(eachYear):
    
    date_b = eachYear.columns
    bar_build = Bar(title='历年生产装机量汇总', title_pos="46%",title_top='1%',width='100%',height=600)

    bar_build.add("Global A",date_b, eachYear.iloc[0],legend_top='8%',label_color=['#FFB90F'],is_label_show=True,is_toolbox_show =False,)
    bar_build.add("Global B",date_b, eachYear.iloc[1],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add("Global C",date_b, eachYear.iloc[2],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add("Global D",date_b, eachYear.iloc[3],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add("Global E/F", date_b, eachYear.iloc[4],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add("Explorer",date_b, eachYear.iloc[5],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add("Inspector /Pioneer /Inspector+ /Global+",date_b, eachYear.iloc[6],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add("MH3D /Inspector454 /Explorer454", date_b, eachYear.iloc[7],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add("Optiv/Vision",date_b, eachYear.iloc[8],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add("Toro /Toro Image",date_b, eachYear.iloc[9],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add("Micro Plus",date_b, eachYear.iloc[10],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add("Alpha/Apollo",date_b, eachYear.iloc[11],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add("Function Plus",date_b, eachYear.iloc[12],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add("Zoo/ZC",date_b, eachYear.iloc[13],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add("Stinger II",date_b, eachYear.iloc[14],legend_top='8%',is_label_show=True,legend_selectedmode='multiple')
    bar_build.add("Global Mini",date_b, eachYear.iloc[15],yaxis_max="1000",legend_orient='horizontal',legend_pos='center',legend_top='8%',
        visual_pos='20%',is_label_show=True,is_datazoom_show=True,datazoom_type='both',legend_selectedmode='multiple',xaxis_type='category',
        tooltip_trigger = 'axis')

    str_date = [str(i) for i in date_b]
    line_build = Line(width='100%')
    line_build.add("Actual Build Qty",str_date, eachYear.iloc[16], label_color=['#FFB90F'],
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

    columns = eachYear.columns
    eachYear=eachYear.fillna(0)
    trace = go.Table(
        header=dict(values=['Year'] + list(eachYear.columns),
                    fill = dict(color='#C2D4FF'),
                    
                    align = ['center']),
        cells=dict(values=[list(eachYear.index)]+[list(eachYear[columns[i]]) for i in range(len(columns))],
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
    off.plot(fig1,filename='templates/op/Installed_each_year_bar.html',show_link=False,auto_open=False)


# path = '../excel/'
# fileName = 'dashboard.xlsx'
# path1 = "../excel/"
# fileName1 = 'history.xlsx'


def updateProduction():
    results = []
    try:
        installed, delivered,produced,waiting, eachYear = getIdpData()
        # # global g_installed
        # global g_delivered
        # global g_produced
        # global g_waiting
        # # g_installed = installed
        # g_delivered = delivered
        # g_produced = produced 
        # g_waiting = waiting

        #results.append("Get data successfully")
    except Exception as ex:
        template = " An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)

        results.append('Cannot get Data'+message)

    try:
        installedCmm(installed)
        # print("Installed CMM is successful")
        results.append('Successful')
    except Exception as ex:
        template = " An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        results.append("Error in Installed CMM" + message)

    try:
        deliveredCmm(delivered)
        
        results.append('Successful')
    except Exception as ex:
        template = " An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        # print("Error in Delivered CMM", message)
        results.append("Error in Delivered CMM" + message)
    try:
        newOrder(produced)
        # print('New Order is successful')
        results.append('Successful')
    except Exception as ex:
        template = " An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        # print("Error in New Order", message)
        results.append("Error in New Order" + message)

    try:
        waitingOrderInventory(waiting)
        results.append('Successful')
    except Exception as ex:
        template = " An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        results.append("Error in Waiting Order" + message)

    
    try:
        installedEachYear(eachYear)
        results.append('Successful')
    except Exception as ex:
        template = " An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        results.append('Installed CMM Each Year cannot be executed' + message)

    results = list(set(results))
    if len(results) == 1 and results[0] == 'Successful':
        message = "全部更新成功"

    if len(results) > 1:
        if "Successful" in results:
            results.remove('Successful')
        message = '错误: ' + ' '.join(results)
    return message
# input("Press enter key to exit ")
