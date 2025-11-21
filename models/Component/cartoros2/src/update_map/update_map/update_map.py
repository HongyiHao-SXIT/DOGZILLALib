import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
import threading

map_msg = OccupancyGrid()
class MapSubscriberPublisher(Node):
    def __init__(self):
        super().__init__('map_subscriber_publisher')
        self.subscription = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.map_callback,
            10)
        #self.map_msg = OccupancyGrid()
        

    def map_callback(self, msg):
        #print("******************************")
        #print(msg)
        global map_msg
        #print(map_msg)
        map_msg = msg
        

async def publish_map(publisher):
        while True:
            #print(map_msg)
            publisher.publish(map_msg)

def main(args=None):
    rclpy.init(args=args)
    
    
    node = MapSubscriberPublisher()
    publisher = node.create_publisher(
            OccupancyGrid,
            'nwe_map',
            100)
    
    executor = rclpy.executors.MultiThreadedExecutor(num_threads=2)
    
    executor.add_node(node)
    async_map_pub  = publish_map(publisher)
    executor.create_task(async_map_pub)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    executor.shutdown()
    node.destroy_node()
    #rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

