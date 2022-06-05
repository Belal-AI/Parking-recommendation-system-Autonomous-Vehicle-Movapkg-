#include <ros.h>
#include<geometry_msgs/Twist.h>

#define S0 0  //Speed 1
#define S1 70 //Speed 2
#define S2 90 //Speed 3
#define S3 100//Speed 4

#define LS 3  //Left Motor Speed
#define LD 2  //Left Motor Direction
#define RS 11 //Right Motor Speed
#define RD 8  //Right Motor Direction

double X=0;
double Z=0;

ros::NodeHandle  nh;
geometry_msgs::Twist Twist_msg;
ros::Subscriber<geometry_msgs::Twist> sub("/cmd_vel", callback);
void callback(const geometry_msgs::Twist& msg){
    X = msg.linear.x;    
    Z = msg.angular.z; 
/*-------------------------Stop-----------------------*/  
      if(X==0 && Z==0){
        digitalWrite(LS,S0);
        digitalWrite(RS,S0);
      }
/*-------------------------Forward-----------------------*/     
      else if(X>0 && X<=0.10 && Z==0){
        digitalWrite(LD,LOW);
        analogWrite(LS,S1);
        digitalWrite(RD,LOW);
        analogWrite(RS,S1+9);
      }
      else if(X>0.10 && X<0.17 && Z==0){
        digitalWrite(LD,LOW);
        analogWrite(LS,S2);
        digitalWrite(RD,LOW);
        analogWrite(RS,S2+9);
      }
      else if(X>=0.17 && X<0.23 && Z==0){
        digitalWrite(LD,LOW);
        analogWrite(LS,S3);
        digitalWrite(RD,LOW);
        analogWrite(RS,S3+9);
      }
      
/*-------------------------Backward-----------------------*/  
      else if(X<0 && X>=-0.10 && Z==0){
        digitalWrite(LD,HIGH);
        analogWrite(LS,S1);
        digitalWrite(RD,HIGH);
        analogWrite(RS,S1+9);
      }
      else if(X<-0.10 && X>-0.17 && Z==0){
        digitalWrite(LD,HIGH);
        analogWrite(LS,S2);
        digitalWrite(RD,HIGH);
        analogWrite(RS,S2+9);
      }
      else if(X<=-0.17 && X>-0.23 && Z==0){
        digitalWrite(LD,HIGH);
        analogWrite(LS,S3);
        digitalWrite(RD,HIGH);
        analogWrite(RS,S3+9);
      }
/*-------------------------Left-----------------------*/  
      else if(Z>=0.8 && X==0){
        digitalWrite(LD,HIGH);
        analogWrite(LS,S2);
        digitalWrite(RD,LOW);
        analogWrite(RS,S2+9);
      }
/*-------------------------Right-----------------------*/ 
      else if(Z<=-0.8 && X==0){
        digitalWrite(LD,LOW);
        analogWrite(LS,S2);
        digitalWrite(RD,HIGH);
        analogWrite(RS,S2+9);
      }
/*-------------------------ForwardLeft-----------------------*/
      else if(Z>=0.1 && Z<0.8 && X>0){
        digitalWrite(LD,LOW);
        analogWrite(LS,S2);
        digitalWrite(RD,LOW);
        analogWrite(RS,S2+9+10);
      }
/*-------------------------ForwardRight-----------------------*/
      else if(Z<=-0.1 && Z>-0.8 && X>0){
        digitalWrite(LD,LOW);
        analogWrite(LS,S2+10);
        digitalWrite(RD,LOW);
        analogWrite(RS,S2+9);
      }
/*-------------------------BackwardLeft-----------------------*/
      else if(Z>=0.1 && Z<0.8 && X<0){
        digitalWrite(LD,HIGH);
        analogWrite(LS,S2);
        digitalWrite(RD,HIGH);
        analogWrite(RS,S2+9+10);
      }
/*-------------------------BackwardRight-----------------------*/
      else if(Z<=-0.1 && Z>-0.8 && X<0){
        digitalWrite(LD,HIGH);
        analogWrite(LS,S2+10);
        digitalWrite(RD,HIGH);
        analogWrite(RS,S2+9);
      }
}

 void setup() 
{
      Serial.begin (57600);   
}

 void loop() {
    nh.subscribe(sub);
    nh.spinOnce(); 
    delay(10);
 }
