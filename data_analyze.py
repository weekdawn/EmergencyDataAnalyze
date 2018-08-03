import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl


class EmergencyAnalyze:
    def __init__(self):
        self.csv_file = "test_tb_ato_event_final_his.csv"
        self.csv_data = pd.read_csv(self.csv_file, low_memory = False)
        self.total_emg_df = pd.DataFrame(self.csv_data)#, columns = ['UNIT_ID','KPI_ID', 'GENERANT_TIME','CLEAR_TIME ']
        pd.set_option('display.max_columns', None)#print显示所有列
        self.origin_meg = [["10-11-37-20:BILLING_DATA-db03","PM-10-11-037-15"],
                      ["10-10-24-14:ismp01_96_171-//","PM-00-01-004-03"],
                      ["10.243.34.32","PM-00-01-004-03"],
                      ["10.243.73.27","PM-00-01-002-01"],
                      ["10.243.73.17","PM-00-01-002-02"]
                      ]

    # 清洗数据
    def clearData(self, df):
        df = df[df['GENERANT_TIME'] < df['CLEAR_TIME']]
        # 对明显违反事实的异常数据进行过滤操作（如消失时间在产生时间之前）
        return df

    #1&2 计算总告警和告警元数量
    def emergencyNum(self):
        unit_num_norepeat_df = pd.DataFrame(self.csv_data, columns=['UNIT_ID', 'KPI_ID','GENERANT_TIME','CLEAR_TIME'])
        unit_num_norepeat_df = unit_num_norepeat_df.drop_duplicates(subset=['UNIT_ID', 'KPI_ID'], keep='first')
        #去掉UNIT_ID和KPI_ID列中重复的行，并保留第一次出现的行
        #补充：
        # 当keep=False时，就是去掉所有的重复行
        # 当keep=‘first'时，就是保留第一次出现的重复行
        # 当keep='last'时就是保留最后一次出现的重复行。（注意，这里的参数是字符串）

        unit_num_norepeat_df = self.clearData(unit_num_norepeat_df)


        print("1.总告警数量：")
        print (self.total_emg_df.shape[0])
        print("\n2.总告警元数量：")
        print(unit_num_norepeat_df.shape[0])

    #3 计算告警时间跨度
    def time(self):
        emg_time_df = pd.DataFrame(self.csv_data, columns = ['GENERANT_TIME'])#,'CLEAR_TIME'
        emg_time_norepeat_df = emg_time_df.drop_duplicates(subset=['GENERANT_TIME'], keep='first')
        print("\n3.告警时间跨度：")
        print(emg_time_norepeat_df.iloc[1,:])
        print(emg_time_norepeat_df.iloc[-1:])

    #4 所有告警元的告警量分布
    def emergencyDistrbution(self):
        pass
        # emg_df = self.total_emg_df.groupby("UNIT_ID")
        # print(emg_df.size().values)


    #5 对那五个告警根源，分别统计各个告警元的告警量 & 8 对那五个告警根源，统计每一个的平均持续时间
    def countEmergency(self):
        count_df = pd.DataFrame(self.csv_data, columns=['UNIT_ID','KPI_ID','GENERANT_TIME','CLEAR_TIME'])

        #告警元由两个id决定

        #求每个告警元的告警量
        count1 = count_df.query('UNIT_ID == "10-11-37-20:BILLING_DATA-db03"').query('KPI_ID == "PM-10-11-037-15"')
        count2 = count_df.query('UNIT_ID == "10-10-24-14:ismp01_96_171-//"').query('KPI_ID == "PM-00-01-004-03"')
        count3 = count_df.query('UNIT_ID == "10-10-24-14:hfwxapp01_34_32-/apacheserver"').query('KPI_ID == "PM-00-01-004-03"')
        count4 = count_df.query('UNIT_ID == "10-10-24-12:HN2_104_H02_07Rs-memory"').query('KPI_ID == "PM-00-01-002-01"')
        count5 = count_df.query('UNIT_ID == "10-10-24-12:HN2_104_H01_09Rs-memory"').query('KPI_ID == "PM-00-01-002-02"')
        print("\n5.\n1号告警元有%s个\n2号告警元有%s个\n3号告警元有%s个\n4号告警元有%s个"
              "\n5号告警元有%s个\n"%(count1.shape[0],count2.shape[0],count3.shape[0],count4.shape[0],count5.shape[0]))

        mean_time1 = pd.DataFrame(pd.to_datetime(count1['CLEAR_TIME']) - pd.to_datetime(count1['GENERANT_TIME']))
        mean_time2 = pd.DataFrame(pd.to_datetime(count2['CLEAR_TIME']) - pd.to_datetime(count2['GENERANT_TIME']))
        mean_time3 = pd.DataFrame(pd.to_datetime(count3['CLEAR_TIME']) - pd.to_datetime(count3['GENERANT_TIME']))
        mean_time4 = pd.DataFrame(pd.to_datetime(count4['CLEAR_TIME']) - pd.to_datetime(count4['GENERANT_TIME']))
        mean_time5 = pd.DataFrame(pd.to_datetime(count5['CLEAR_TIME']) - pd.to_datetime(count5['GENERANT_TIME']))
        print("\n8.\n1号告警元平均持续  %s\n2号告警元平均持续  %s\n3号告警元平均持续  %s"
              "\n4号告警元平均持续  %s\n5号告警元平均持续  %s\n"%(mean_time1.mean(),mean_time2.mean(),mean_time3.mean(),mean_time4.mean(),mean_time5.mean()))

    #6 所有告警的平均持续时间
    def meanEmergency(self):
        mean_time_df = pd.DataFrame(self.csv_data, columns=['GENERANT_TIME', 'CLEAR_TIME'])
        mean_time_df = mean_time_df.dropna(axis=0,how='any')
        # 删除表中全部为NaN的行
        # 删除行，使用参数axis = 0，删除列的参数axis = 1
        # df.dropna(axis=0, how='all')
        # 删除表中含有任何NaN的行
        # df.dropna(axis=0, how='any')  # drop all rows that have any NaN values
        mean_time_df = self.clearData(mean_time_df)

        #转换成时间格式后再相减
        mean_time = pd.DataFrame(pd.to_datetime(mean_time_df['CLEAR_TIME']) - pd.to_datetime(mean_time_df['GENERANT_TIME']))
        return mean_time


    #7 告警持续时间分布（图形）
    def timeDistribution(self):
        time_df = self.meanEmergency()
        #超过5分钟的告警数
        # temp_time = pd.to_datetime('00:30:00', format='%H:%M:%S')
        # temp_time2 = pd.to_datetime('00:00:00', format='%H:%M:%S')
        # sub_time = temp_time - temp_time2
        # over_five_time = time_df[pd.to_datetime(time_df[0]) > sub_time]
        #

        time_num = time_df.groupby(0)
        #总共14371组
        time = time_num.size()
        #横坐标  持续时间（分钟
        x = time.index.seconds / 60
        y = time.values / self.total_emg_df.shape[0]

        #前5分钟的数据
        plt.xlim(0, 5)
        #占比
        plt.ylim(0,0.1)
        plot1 = plt.plot(x,y)
        plt.setp(plot1, color='r')#, linewidth=2.0
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.title("告警持续时间分布")
        plt.xlabel("告警持续时间(天)")
        plt.ylabel("告警数占总告警数的比例")
        plt.show()

        # plot1 = pl.plot(x, y)
        #
        # pl.title("告警持续时间分布")  # give plot a title
        # pl.xlabel("告警持续时间")  # make axis labels
        # pl.ylabel("告警数量")
        #
        # # pl.xlim(0.0, 9.0)  # set axis limits
        # # pl.ylim(0.0, 30.)
        #
        # pl.legend(plot1,  numpoints = 1)  # make legend
        # pl.show()  # show the plot on the screen


if __name__ == '__main__':
    e = EmergencyAnalyze()

    e.emergencyDistrbution()

    e.emergencyNum()
    e.time()
    e.countEmergency()
    print("\n6.所有告警的平均持续时间：")
    print(e.meanEmergency().mean())
    # e.timeDistribution()
    e.emergencyDistrbution()

