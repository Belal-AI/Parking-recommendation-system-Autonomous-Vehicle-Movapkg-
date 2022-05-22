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
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
data_POINT=[]
def build_feature(start_Hour,start_min,end_Hour,end_Min,Date_Monday,Weather_rainy,Weather_sunny):
   return start_Hour,start_min,end_Hour,end_Min,Date_Monday,Weather_rainy,Weather_sunny
def movebase_client():
    rospy.loginfo("allah eh da ana fe el movebase")
    
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 2.45
    goal.target_pose.pose.position.y = -1.45
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

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
        result = movebase_client()
        if result:
            rospy.loginfo("Goal execution done!")
        else:
            rospy.loginfo("Yaaarb")

        rate.sleep()
        

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
