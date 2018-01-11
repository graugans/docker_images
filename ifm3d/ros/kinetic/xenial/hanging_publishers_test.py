#!/usr/bin/env python
import roslaunch
import rospy
import os
import signal
import time
from sensor_msgs.msg import Image
from multiprocessing import Lock


hostname = "192.168.0.69"
port = 80
base_topic = "ifm_left"


class Atom(object):
    # Don't trust assignment thread safety.
    def __init__(self, v):
        self._lock = Lock()
        self._value = v

    def reset(self, v):
        with self._lock:
            self._value = v

    def deref(self):
        with self._lock:
            return self._value


def kill_nodes(launcher, nodes):
    for node in nodes:
        os.kill(node.pid, signal.SIGKILL)
    time.sleep(2.0)


def await_pred(pred, timeout):
    start_time = time.time()
    while True:
        if pred():
            return True
        dt = time.time() - start_time
        if dt > timeout:
            return False


def receive_one(topic, msg_class, timeout):
    """
    Creates a subscriber, waits to receive a message from the given topic/msg_class,
    then unregisters the subscriber. Returns the received message.
    """
    container = Atom(None)
    sub = rospy.Subscriber(topic, Image, container.reset)
    assert await_pred(container.deref, timeout=timeout), "Never received msg from %s after %s seconds" % (topic, timeout)
    sub.unregister()
    return container.deref()


def gen_msgs(topic, msg_class):
    while True:
        yield receive_one(topic, msg_class, 10.0)


def launch_ifm(launcher, base_topic):

    rospy.set_param(os.path.join(base_topic, base_topic),
                    {"frame_id_base": base_topic,
                     "ip": hostname,
                     "password": "",
                     "publish_viz_images": False,
                     "schema_mask": 15,
                     "timeout_millis": 500,
                     "timoute_tolerance_secs": 5.0,
                     "xmlrpc_port": port,
                     "assume_sw_triggered": False})

    node = roslaunch.core.Node(
        package="ifm3d",
        node_type="ifm3d_node",
        name=base_topic,
        namespace=base_topic,
        output="screen",
        respawn=False,
        required=False,
        remap_args=[['distance', "/%s/depth_with_confidence" % base_topic]]
    )

    return launcher.launch(node)


def receive_depth_image_test(base_topic):
    """
    1. Create a ros launcher instance.
    2. Repeatedly:
         - Launch ifm node.
         - Create subscriber, receive one depth message, then unsubscribe.
         - kill ros node.

    This test will eventually fail with a timeout error waiting for the
    depth message on my machine.
    """
    launcher = roslaunch.scriptapi.ROSLaunch()
    launcher.start()
    # Launch the ros node.
    node = launch_ifm(launcher, base_topic)
    topic = os.path.join(base_topic, "depth_with_confidence")
    depth_msgs = gen_msgs(topic, Image)
    msg = next(depth_msgs)
    while True:
        # Note: the first couple depth messages received after registering a
        # subscriber are empty. This is another, probably separate, issue.
        print "Received depth message. Shape: ", msg.height, msg.width
        kill_nodes(launcher, [node])
        node = launch_ifm(launcher, base_topic)
        msg = next(depth_msgs)


if __name__ == "__main__":
    rospy.init_node("UnitVectorsTest")
    receive_depth_image_test(base_topic)
