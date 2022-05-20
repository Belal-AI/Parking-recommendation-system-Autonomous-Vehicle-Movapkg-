#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import String
from sklearn.naive_bayes import GaussianNB
from joblib import load
import pickle
import datetime
import random
import numpy as np
data_POINT=[]
def build_feature(start_Hour,start_min,end_Hour,end_Min,Date_Monday,Weather_rainy,Weather_sunny):
   return start_Hour,start_min,end_Hour,end_Min,Date_Monday,Weather_rainy,Weather_sunny
    
def talker():
    end_Min =0
    end_Hour=0
    start_Hour=0
    start_Min=0
    modell = load('tree_model.pkl')
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        now = datetime.datetime.now()
        start_Hour = now.hour
        start_Min = now.minute
        if start_Hour > 12:
            start_Hour=start_Hour-12

        if start_Min == 45:
            end_Min = 0
            end_Hour=start_Hour+1
        elif start_Min > 45:
            end_Min = start_Min-45
            end_Hour=start_Hour+1
        else:
            end_Hour=start_Hour
            end_Min = start_Min+15
       
        data_POINT=build_feature(start_Hour,start_Min,end_Hour,end_Min,random.randint(0,1),random.randint(0,1),random.randint(0,1))
        data_POINT=np.array(list(data_POINT))
        #prediction = modell.predict(data_POINT.reshape(1,-1))[0]
        rospy.loginfo(str(modell.predict(data_POINT.reshape(1,-1))[0]))
        pub.publish(str(modell.predict(data_POINT.reshape(1,-1))[0]))
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
