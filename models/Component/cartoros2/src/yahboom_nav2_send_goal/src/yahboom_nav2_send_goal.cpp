#include <memory>
#include <chrono>
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "nav2_msgs/action/navigate_to_pose.hpp"
#include "rclcpp/time.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;
using std::placeholders::_1;
using std::placeholders::_2;

class Nav2Client : public rclcpp::Node
{
public:
  using NavigateToPose = nav2_msgs::action::NavigateToPose;
  using GoalHandleNavigateToPose = rclcpp_action::ClientGoalHandle<NavigateToPose>;
  rclcpp_action::Client<NavigateToPose>::SharedPtr client_ptr_;
  rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr subscription_goal;

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  std::vector<geometry_msgs::msg::PoseStamped> poses;
  float status;
  std_msgs::msg::String status_msg;



  explicit Nav2Client(): Node("nav2_send_goal")
  {

    this->client_ptr_  = rclcpp_action::create_client<NavigateToPose>(this, "navigate_to_pose");

    this->subscription_goal = this->create_subscription<geometry_msgs::msg::PoseStamped>(
              "/voice_command", 100, std::bind(&Nav2Client::lab_callback, this, _1));

    this->publisher_ = this->create_publisher<std_msgs::msg::String>(
              "/goal_status", 100);


  }

  void multGoal(){
      geometry_msgs::msg::PoseStamped pose1;
      pose1.header.frame_id = "map";
      pose1.pose.position.x = 0.0;
      pose1.pose.position.y = 0.0;
      pose1.pose.orientation.w = 1.0;
//      poses.push_back(pose1);
//      geometry_msgs::msg::PoseStamped pose2;
//      pose2.header.frame_id = "map";
//      pose2.pose.position.x = 1.0;
//      pose2.pose.position.y = 1.0;
//      pose2.pose.orientation.w = 1.0;
//      poses.push_back(pose2);
//      this->sendGoal();
  }

  void sendGoal(void) {

    while (!this->client_ptr_->wait_for_action_server()) {
      RCLCPP_INFO(get_logger(), "Waiting for action server...");
    }
    auto goal_msg = NavigateToPose::Goal();
    goal_msg.pose.header.stamp = this->now();
    goal_msg.pose.header.frame_id = "map";

    goal_msg.pose.pose.position.x = poses.at(0).pose.position.x;
    goal_msg.pose.pose.position.y = poses.at(0).pose.position.y;
    goal_msg.pose.pose.orientation.x = 0;
    goal_msg.pose.pose.orientation.y = 0;
    goal_msg.pose.pose.orientation.w = 0;
    goal_msg.pose.pose.orientation.z = 1;
    poses.erase(poses.begin());
    RCLCPP_INFO(get_logger(), "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%");
    RCLCPP_INFO(get_logger(), "mun:%d", poses.size());
    RCLCPP_INFO(get_logger(), "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%");
    auto send_goal_options = rclcpp_action::Client<NavigateToPose>::SendGoalOptions();
    send_goal_options.feedback_callback = std::bind(&Nav2Client::feedbackCallback, this, _1, _2);
    send_goal_options.result_callback = std::bind(&Nav2Client::resultCallback, this, _1);

    client_ptr_->async_send_goal(goal_msg, send_goal_options);
    RCLCPP_INFO(get_logger(), "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%");

  }
  //feedback
  void feedbackCallback(GoalHandleNavigateToPose::SharedPtr,const std::shared_ptr<const NavigateToPose::Feedback> feedback)
  {
    RCLCPP_INFO(get_logger(), "Distance remaininf = %f", feedback->distance_remaining);
//    RCLCPP_INFO(get_logger(), "mun:%d", rclcpp_action::ResultCode::SUCCEEDED);
  }
  //result
  void resultCallback(const GoalHandleNavigateToPose::WrappedResult & result)
  {
    switch (result.code) {
      case rclcpp_action::ResultCode::SUCCEEDED:
        RCLCPP_INFO(get_logger(), "Success!!!");
        RCLCPP_INFO(get_logger(), "mun:%d", rclcpp_action::ResultCode::SUCCEEDED);
        status_msg.data = "SUCCEEDED";
        publisher_->publish(status_msg);
        if(poses.size()!=0){
            this->sendGoal();
        }
        break;
      case rclcpp_action::ResultCode::ABORTED:
        RCLCPP_ERROR(get_logger(), "Goal was aborted");
        if(poses.size()!=0){
            this->sendGoal();
        }
        return;
      case rclcpp_action::ResultCode::CANCELED:
        RCLCPP_ERROR(get_logger(), "Goal was canceled");
        return;
      default:
        RCLCPP_ERROR(get_logger(), "Unknown result code");
        if(poses.size()!=0){
            this->sendGoal();
        }
        return;
    }
  }

  void lab_callback(const geometry_msgs::msg::PoseStamped::SharedPtr msg){

      geometry_msgs::msg::PoseStamped pose1;
      pose1.header.frame_id = "map";
      pose1.pose.position.x = msg->pose.position.x;
      pose1.pose.position.y = msg->pose.position.y;
      pose1.pose.orientation.w = msg->pose.orientation.w;
      poses.push_back(pose1);
      this->sendGoal();

  }


};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<Nav2Client>();
  node->multGoal();
  rclcpp::spin(node);

  rclcpp::shutdown();
  return 0;
}
