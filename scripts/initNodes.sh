#!/bin/bash

rosnode kill /amcl &> /dev/null
rosnode kiil /compressed_map_publisher &> /dev/null
rosnode kiil /joystick_relay &> /dev/null
rosnode kiil /map_configuration_server &> /dev/null
rosnode kiil /map_server &> /dev/null
rosnode kiil /map_setup &> /dev/null
rosnode kiil /joystick &> /dev/null
rosnode kiil /pal_computer_monitor_node &> /dev/null
rosnode kiil /pal_navigation_sm &> /dev/null
rosnode kiil /pal_topic_monitor_node &> /dev/null
rosnode kiil /move_base &> /dev/null
rosnode kiil /pal_vo_server &> /dev/null
rosnode kiil /mm11_prod &> /dev/null
rosnode kiil /embedded_networking_supervisor &> /dev/null
rosnode kiil /joy_teleop &> /dev/null
rosnode kiil /pose_saver &> /dev/null
rosnode kiil /pal_diagnostic_aggregator &> /dev/null 
rosnode kiil /pal_supervisor_node &> /dev/null
rosnode kiil /pal_webcommander_node &> /dev/null
