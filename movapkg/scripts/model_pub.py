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
import requests

data_POINT = []


def build_feature(Hour, Temperature, Humidity, Wind_Speed, Visibility, Dew_Point, Solar_Radiation, Rainfall,IsHoliday, IsFunctioningDay, day,	month,year,Season_Autumn,Season_Spring,Season_Summer, Season_Winter):
    return Hour,Temperature, Humidity, Wind_Speed, Visibility, Dew_Point,Solar_Radiation, Rainfall,IsHoliday,IsFunctioningDay, day, month,	year,Season_Autumn, Season_Spring, Season_Summer,Season_Winter

def Api_func(complete_url):

    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        z = x["weather"]
        current_humidity = y["humidity"]
        return y["temp"]-273,y["humidity"]
    else:
        rospy.loginfo("cant reach")


    

parking=0
def movebase_client(x,y):
    rospy.loginfo(str(x))

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()


def talker():

    start_Hour = 0
    modell = load('clusterd.pkl')
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        api_key = "AAAAPPPPIIII_____KKKKEEEEYYYY"  # Enter the API key you got from the OpenWeatherMap website
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + 'd850f7f52bf19300a9eb4b0aa6b80f0d' + "&q=" + "alexandria"
        temp,humidity=Api_func(complete_url)
        now = datetime.datetime.now()
        start_Hour = now.hour

        current_day = now.day
        current_month = now.month
        current_year = now.year
        data_POINT = build_feature(start_Hour,temp,humidity, random.randint(1, 12), random.randint(1,1000), 11.0,	1.00,	0.0,	1,	1,current_day,current_month,current_year,	0,	1, 0,	0)
        data_POINT = np.array(list(data_POINT))
        prediction = modell.predict(data_POINT.reshape(1, -1))[0]
        parking=prediction
        if parking ==1:
            x=4.0
            y=3.0
        elif parking==2:
            x=-4.0
            y=-3.0
        else:
            x=0.0
            y=0.0
        

        rospy.loginfo(str(modell.predict(data_POINT.reshape(1, -1))[0]))
        result = movebase_client(x,y)
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
