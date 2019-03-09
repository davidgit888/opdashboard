import calendar
from datetime import date
from .models import Report, SupportiveTime,GroupPerform
import pandas as pd

class valReport:
    """test the Report data"""
    def report():
        global date
        global Report
        global SupportiveTime
        global GroupPerform

        year = int(input('Enter Year: '))
        month = int(input('Enter Month: '))
        group = input('Enter Group: ')

        days = calendar.monthrange(year,month)[1]
        today = date.today()
        
        for i in range(1,days+1):
            cdate = today.replace(year=year,month=month,day=i)
            dataReport = Report.objects.filter(date=cdate,groups=group).values()
            dataGroup = GroupPerform.objects.filter(date=cdate,work_group=group).values()

            # print(dataGroup)
            if(len(dataReport)!=0 and len(dataGroup)!=0):
               
            
                reportItems = pd.DataFrame(list(dataReport),columns=['user_id','real_time'])
                groupItems = pd.DataFrame(list(dataGroup),columns=['user','username','real_time'])
                
                reportTotal = reportItems.sum()
                groupTotal = groupItems.sum()

                if reportTotal['real_time'] == groupTotal['real_time']:
                    pass
    
                else:
                    print('No',cdate)
                    reportPivot = reportItems.groupby(['user_id']).sum()
                    print('report: ',reportPivot)
                    print('---')
                    print('group: ',groupItems)
            else:
                print('one is empty %s' %(cdate))

                