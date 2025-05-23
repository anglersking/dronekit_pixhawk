#!/usr/bin/env python
# -*- coding: utf-8-*-
"""© Copyright2015-2016, 3D Robotics.simple_goto.py:GUIDED mode "simple goto" example (Copter Only)Demonstrates how toarm and takeoff in Copter and how to navigate to points usingVehicle.simple_goto.
""" 
from __future__ import print_function 
import time 
from dronekit import connect, VehicleMode, LocationGlobalRelative 
# 改为当前连接的pixhawk飞控的端口 
connection_string ='/dev/ttyUSB0' 
print('Connectingto vehicle on: %s' % connection_string) 
# connect函数将会返回一个Vehicle类型的对象，即此处的vehicle 
# 即可认为是无人机的主体，通过vehicle对象，我们可以直接控制无人机 
vehicle =connect(connection_string, wait_ready=True,baud=57600) 
# 定义arm_and_takeoff函数，使无人机解锁并起飞到目标高度 
# 参数aTargetAltitude即为目标高度，单位为米 
vehicle.armed = True 
def arm_and_takeoff(aTargetAltitude):     
	# 进行起飞前检查     
	print("Basic pre-armchecks")     
	# vehicle.is_armable会检查飞控是否启动完成、有无GPS fix、卡曼滤波器     
	# 是否初始化完毕。若以上检查通过，则会返回True    
	while not vehicle.is_armable:         
		print(" Waiting for vehicle toinitialise...")
         	
		time.sleep(1)     
	# 解锁无人机（电机将开始旋转）     
	print("Arming motors")     
	# 将无人机的飞行模式切换成"GUIDED"（一般建议在GUIDED模式下控制无人机）     
	vehicle.mode =VehicleMode("GUIDED")     
	# 通过设置vehicle.armed状态变量为True，解锁无人机     
	vehicle.armed = True     
	# 在无人机起飞之前，确认电机已经解锁     
	while not vehicle.armed:         
		print(" Waiting forarming...")         
		time.sleep(1)     
	# 发送起飞指令     
	print("Taking off!")     
	# simple_takeoff将发送指令，使无人机起飞并上升到目标高度    
	vehicle.simple_takeoff(aTargetAltitude)     # 在无人机上升到目标高度之前，阻塞程序     
	while True:        
		 print(" Altitude: ",vehicle.location.global_relative_frame.alt)         
		# 当高度上升到目标高度的0.95倍时，即认为达到了目标高度，退出循环        
		#vehicle.location.global_relative_frame.alt为相对于home点的高度         
		 if vehicle.location.global_relative_frame.alt>= aTargetAltitude * 0.95:             
			print("Reached targetaltitude")             
			break         
		# 等待1s         
		 time.sleep(1) 
# 调用上面声明的arm_and_takeoff函数，目标高度10m 
arm_and_takeoff(10) 
# 设置在运动时，默认的空速为3m/s 
print("Setdefault/target airspeed to 3") 
# vehicle.airspeed变量可读可写，且读、写时的含义不同。 
# 读取时，为无人机的当前空速；写入时，设定无人机在执行航点任务时的默认速度 
vehicle.airspeed =3 
# 发送指令，让无人机前往第一个航点 
print("Goingtowards first point for 30 seconds ...") 
#LocationGlobalRelative是一个类，它由经纬度(WGS84)和相对于home点的高度组成 
# 这条语句将创建一个位于南纬35.361354，东经149.165218，相对home点高20m的位置 .注意：如要实际测试，此处的经纬度需要改成你当前测试位置的经纬度，不然飞机飞跑了！！！
point1 =LocationGlobalRelative(-35.361354, 149.165218, 20) 
# simple_goto函数将位置发送给无人机，生成一个目标航点 
vehicle.simple_goto(point1) 
# simple_goto函数只发送指令，不判断有没有到达目标航点 
# 它可以被其他后续指令打断，此处延时30s，即让无人机朝向point1飞行30s 
time.sleep(30) # 发送指令，让无人机前往第二个航点 
print("Goingtowards second point for 30 seconds (groundspeed set to 10 m/s) ...") 
# 与之前类似，这条语句创建了另一个相对home高20m的点。 注意：同理，如要实际测试，此处的经纬度也需要改成你当前测试位置的经纬度！！！
point2 =LocationGlobalRelative(-35.363244, 149.168801, 20) 
# simple_goto将目标航点发送给无人机，groundspeed=10设置飞行时的地速为10m/s 
vehicle.simple_goto(point2,groundspeed=10) 
# 与之前一样，延时30s 
time.sleep(30) 
# 发送"返航"指令 
print("Returningto Launch") 
# 返航，只需将无人机的飞行模式切换成"RTL(Return to Launch)" 
# 无人机会自动返回home点的正上方，之后自动降落 
vehicle.mode =VehicleMode("RTL") 
# 退出之前，清除vehicle对象 
print("Closevehicle object") 
vehicle.close()
