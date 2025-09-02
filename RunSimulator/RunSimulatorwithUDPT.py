import random
import subprocess
import math
from bursty_traffic_generation import generate_flow_packet_sizes

integer_array = [i for i in range(6)] * 100 #5ms - packets generation time
FairnessIndex = []
# 初始化总和
total_sum = 0
TotaltransmittedPacketsize = []
# 进行100次随机选择和运行
a = 2
AverageThroughput = []
AverageFI = []
AverageEF = []
FairnessIndexofBigandSmallGroupALL = []
AverageProgramRunningTimeforDifferentNumUsers = []
AverageRvalue = []

while a < 101:  # Maximum of users+ 1
    QueuingTime = [0] * a
    FI = []
    Efficiency1 = []
    total_sum = 0
    TotaltransmittedPacketsize = []
    c = 0
    AverageEFF = []
    TotalQueueingTime = [0] * a
    while c < 1001:
        my_list = generate_flow_packet_sizes(simulation_time=20, pg_duration=18)
        FairnessIndexofBigandSmallGroup = []
        FairnessIndex1 = []
        QueuingTime = [0] * a
        AverageProgramRunningTimeInAPeriod = []
        R_value = []
        arr = [random.randint(1, 10) for _ in range(a)]
        Totalnumberofpackets = sum(arr)
        for _ in range(10):               #number of ru allocation interval in a period of fairness control period
            # 随机选择n个元素
            random_numbers = list(range(1, 101))
            selected_average_packet_size = random.choices(random_numbers, k=Totalnumberofpackets)
            selected_elements = random.sample(my_list, a)
            FairnessIndex1 = []
            ProgramRunningTime = []
            ProgramRunningTimeValue = []
            b = 0
            while b < len(selected_elements):
                selected_elements[b] = math.ceil(selected_elements[b] * selected_average_packet_size[b] / 5)     #every user has different average packet size
                b = b + 1
            with open("UpdatedDynamicProgrammingCombinedwithTimsort.py", "r") as file:
                content = file.read()
                # 替换DynamicProgramming0retransmission.py中的PacketSize数组
                new_content = content.replace("GeneratedPacketSize = []", f"GeneratedPacketSize = {selected_elements}")
            with open("UpdatedDynamicProgrammingCombinedwithTimsort_temp.py", "w") as file:
                file.write(new_content)

            with open("UpdatedDynamicProgrammingCombinedwithTimsort_temp.py", "r") as file:
                content = file.read()
                # 替换DynamicProgramming0retransmission.py中的PacketSize数组
                new_content2 = content.replace("QueuingTime = []", f"QueuingTime = {QueuingTime}")
            with open("UpdatedDynamicProgrammingCombinedwithTimsort_temp2.py", "w") as file:
                file.write(new_content2)

            # 运行 DynamicProgramming0retransmission_temp.py
            process = subprocess.Popen(['python', 'UpdatedDynamicProgrammingCombinedwithTimsort_temp2.py'], stdout=subprocess.PIPE,
                                       universal_newlines=True)
            # 从程序的输出中提取 TotalTransmittedPacketSize 的值
            for line in process.stdout:
                if 'Total transmitted packet size:' in line:
                    value = int(line.split(':')[1].strip())
                    TotaltransmittedPacketsize.append(value)
                if 'Efficiency:' in line:
                    Efficiency = float(line.split(':')[1].strip())
                    Efficiency1.append(Efficiency)
                if 'Queuing time:' in line:
                    QueuingTime = str(line.split(':')[1].strip())
                if 'Program running time:' in line:
                    ProgramRunningTime = str(line.split(':')[1].strip())
                if 'Average R-value for ordered packets:' in line:
                    AverageR = str(line.split(':')[1].strip())
            # 等待程序执行完成
            process.communicate()
            # 删除临时文件
            subprocess.run(["rm", "UpdatedDynamicProgrammingCombinedwithTimsort_temp.py"])
            subprocess.run(["rm", "UpdatedDynamicProgrammingCombinedwithTimsort_temp2.py"])
            # 将选择的元素的总和累加
        num_QueuingTime = eval(QueuingTime)
        num_ProgramRunningTime = eval(ProgramRunningTime)
        ProgramRunningTimeValue.append(num_ProgramRunningTime)
        AverageProgramRunningTime = sum(ProgramRunningTimeValue) / len(ProgramRunningTimeValue)
        AverageProgramRunningTimeInAPeriod.append(AverageProgramRunningTime)
        num_averageR = eval(AverageR)
        R_value.append(num_averageR)
        y = 0
        while y < a:
            remainder = y % 50
            num_QueuingTime[y] = num_QueuingTime[y] + remainder * (5000 + remainder * 500)
            y = y + 1
        int_QueuingTime = [math.floor(x) for x in num_QueuingTime]
        QueuingTime2 = []
        l = 0
        while l < len(int_QueuingTime):
            QT2 = int_QueuingTime[l] * int_QueuingTime[l]
            QueuingTime2.append(QT2)
            l = l + 1
        l = 0
        while l < len(TotalQueueingTime):
            TotalQueueingTime[l] = TotalQueueingTime[l] + int_QueuingTime[l]
            l = l + 1
        FI = math.floor(
            10000 * (sum(int_QueuingTime) * sum(int_QueuingTime)) / (len(int_QueuingTime) * sum(QueuingTime2)))
        FairnessIndex1.append(FI)
        total_sum += sum(selected_elements)
        NumberofSmallPacketsGroup = math.floor(len(int_QueuingTime) / 2)
        QueuingTimeofSmallPacketsGroup = my_list[:NumberofSmallPacketsGroup]
        QueuingTimeofBigPacketsGroup = my_list[NumberofSmallPacketsGroup:]
        AverageQueuingTimeofSmallPacketsGroup = math.floor(sum(QueuingTimeofSmallPacketsGroup) / len(QueuingTimeofSmallPacketsGroup))
        AverageQueuingTimeofBigPacketsGroup = math.floor(sum(QueuingTimeofBigPacketsGroup) / len(QueuingTimeofBigPacketsGroup))
        FairnessIndexofBigandSmallGroup1 = math.floor(10000*((AverageQueuingTimeofSmallPacketsGroup+AverageQueuingTimeofSmallPacketsGroup)*(AverageQueuingTimeofBigPacketsGroup+AverageQueuingTimeofBigPacketsGroup))/(2 * ((AverageQueuingTimeofSmallPacketsGroup*AverageQueuingTimeofSmallPacketsGroup)+(AverageQueuingTimeofBigPacketsGroup*AverageQueuingTimeofBigPacketsGroup))))
        FairnessIndexofBigandSmallGroup.append(FairnessIndexofBigandSmallGroup1)
        l = 0
        AverageFairnessIndex = sum(FairnessIndex1) / len(FairnessIndex1)
        FairnessIndex.append(AverageFairnessIndex)
        Averagethroughput = sum(TotaltransmittedPacketsize) * 8 / (1048576 * 5)
        AverageEfficiency = sum(Efficiency1) / len(Efficiency1)
        AverageEFF.append(AverageEfficiency)
        AverageThroughput.append(Averagethroughput)
        c = c + 1
    a = a + 5
    Average_R = sum(R_value) / len(R_value)
    AverageEF1 = sum(AverageEFF) / len(AverageEFF)
    AverageFI1 = sum(FairnessIndex) / len(FairnessIndex)
    AverageProgramRunningTimeforDifferentNumUser1 = sum(AverageProgramRunningTimeInAPeriod) / len(AverageProgramRunningTimeInAPeriod)
    AvrageFIofBigandSmallGroup = sum(FairnessIndexofBigandSmallGroup) / len(FairnessIndexofBigandSmallGroup)
    AverageProgramRunningTimeforDifferentNumUsers.append(AverageProgramRunningTimeforDifferentNumUser1)
    FairnessIndexofBigandSmallGroupALL.append(AvrageFIofBigandSmallGroup)
    AverageFI.append(AverageFI1)
    AverageEF.append(AverageEF1)
    AverageRvalue.append(Average_R)
    print('Average Efficiency: ', AverageEF)
    print('Average Fairness Index: ', AverageFI)
    print('Average Fairness Index of big and small group: ', FairnessIndexofBigandSmallGroupALL)
    print('Average program running time for different number of users: ',AverageProgramRunningTimeforDifferentNumUsers )
    print('Average R-value: ', AverageRvalue)
exit(0)