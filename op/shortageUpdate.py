import pandas as pd 
from shortageConf.models import Supplier, Overdue, DeliveredTotal, ReasonAnalysis
from pyecharts import Bar, Pie



def getAllRdata():
    # supplier = read_excel('../excel/按供应商分类.xlsx')
    # overdue = read_excel('../excel/超期分类汇总.xlsx')
    # shortage = read_excel('../excel/发货缺件数量汇总.xlsx')
    # reason = read_excel('../excel/原因分析汇总.xlsx')

    
    supplierObj = Supplier.objects.all().values()
    supplier = pd.DataFrame(list(supplierObj),columns=['id','supplier_name','quantity'])
    del supplier['id']

    overdueObj = Overdue.objects.all().values()
    overdue = pd.DataFrame(list(overdueObj),columns=['id','category','quantity'])
    del overdue['id']
   
    deliveredObj = DeliveredTotal.objects.all().values()
    delivered = pd.DataFrame(list(deliveredObj),columns=['id','Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    del delivered['id']

    reasonObj = ReasonAnalysis.objects.all().values()
    reason = pd.DataFrame(list(reasonObj),columns=['id','reason_category','quantity'])
    del reason['id']

    return supplier, overdue, delivered, reason




def supplierBar(supplier):
    names = supplier['supplier_name']
    bar = Bar(title='按供应商分类',title_pos='center')
    bar.add('', names,supplier['quantity'],is_label_show=True, is_legend_show=True,legend_pos='center',legend_top='6%',
        is_toolbox_show=False,xaxis_rotate=30)
    bar.render('templates/op/supplier.html')



def overduePie(overdue):
    names = overdue['category']
    pie = Pie(title='超期分类汇总',title_pos='center')
    pie.add('',names, overdue['quantity'],is_legend_show=True,is_label_show=True,legend_orient='vertical',legend_pos='right',
        is_toolbox_show=False)
    pie.render('templates/op/overdue.html')


def deliveredBar(delivered):
    names = delivered.columns[1:]
    bar = Bar(title='发货缺件数量汇总',title_pos="center")
    bar.add(delivered['Year'][-2:-1], names, delivered.iloc[-2][1:],legend_top='6%',is_label_show=True)
    bar.add(delivered['Year'][-1:], names, delivered.iloc[-1][1:], legend_top='6%',is_label_show=True, is_legend_show=True, is_toolbox_show=False)
    bar.render('templates/op/shortage.html')


def reasonPie(reason):
    pie = Pie(title='原因分析汇总',title_pos="center")
    pie.add('',reason['reason_category'],reason['quantity'],is_label_show=True,is_legend_show=True,legend_orient='vertical',legend_pos='right',
        is_toolbox_show=False)
    pie.render('templates/op/reason.html')


def update_shortage():   
    results = []  
    try:
        supplier, overdue, delivered, reason = getAllRdata()
        results.append('Geting Data is successful')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        results.append('Error of getting data ' + message)


    try:
        deliveredBar(delivered)
        results.append('Shortage is successful')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        results.append('Shortage cannot be executed '+ message)

    try:
        supplierBar(supplier)
        results.append('Supplier is successful')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        results.append('Supplier cannot be executed ' + message)

    try:
        overduePie(overdue)
        results.append('Overdue is successful')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        results.append('Overdue cannot be executed ' + message)

    try:
        reasonPie(reason)
        results.append('Reason is successful')
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        results.append('Reason cannot be executed ' + message)
    return results


