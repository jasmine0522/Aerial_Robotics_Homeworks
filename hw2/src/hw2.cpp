// include ros library
#include "ros/ros.h"

// include msg library
#include <turtlesim/Pose.h>
#include <geometry_msgs/Twist.h>
#include <geometry_msgs/Point.h>

// include math 
#include <math.h>
#define PI acos(-1)
using namespace std;


turtlesim::Pose pose;
geometry_msgs::Twist vel_msg;
geometry_msgs::Point goal_point;
//Define a data structure to 3D
struct XYZ{
  float x;
  float y;
  float z;
};
//Declare a variable.Its name is pos_err with XYZ data type
struct XYZ pos_err;
float goal_degree;
float new_x;
float new_y;
// declare call back function(call back the pose of robot)
void pos_cb(const turtlesim::Pose::ConstPtr& msg)
{
  pose = *msg;
} 

int main(int argc, char **argv)
{
  ros::init(argc, argv, "tutorial_1");
  ros::NodeHandle n;

  // declare publisher & subscriber
  ros::Subscriber pos_sub = n.subscribe<turtlesim::Pose>("turtle1/pose", 10, pos_cb);
  ros::Publisher turtlesim_pub = n.advertise<geometry_msgs::Twist>("/turtle1/cmd_vel", 100);
  //input your desired position
  ROS_INFO("Please input (x,y). x>0,y>0");
  cout<<"desired_X:";
  cin>>goal_point.x;
  cout<<"desired_Y:";
  cin>>goal_point.y;
  // setting frequency as 10 Hz
  ros::Rate loop_rate(10);

  int count = 0;
  while (ros::ok()){

    printf("\ncount : %d\n",count);
    printf("goal x : %f \t y : %f\n",goal_point.x,goal_point.y);
    printf("pose x : %f \t y : %f\n",pose.x,pose.y);

    // Calculate position error(feedback term)
    pos_err.x = goal_point.x - pose.x;//vector
    pos_err.y = goal_point.y - pose.y;
    
    //Your error-driven controller design
    goal_degree=atan2(pos_err.y,pos_err.x)*180/PI;
    
    float new_x=pos_err.x*(cos(goal_degree))+pos_err.y*(sin(goal_degree));
    float new_y=(-1)*pos_err.x*(sin(goal_degree))+pos_err.y*(cos(goal_degree));
    
    printf("new_x: %f",new_x);
    printf("new_y: %f",new_y);
    printf("goal_theta: %f",goal_degree);
    printf("atan2(pos_err.y,pos_err.x): %f",atan2(pos_err.y,pos_err.x));

    vel_msg.linear.x = 1.2*sqrt(pow(new_x,2)+pow(new_y,2));
    vel_msg.angular.z = 4*(atan2(pos_err.y,pos_err.x)-pose.theta) ;
    turtlesim_pub.publish(vel_msg);

    count ++;
    ros::spinOnce();
    loop_rate.sleep();
  }
  return 0;
}



