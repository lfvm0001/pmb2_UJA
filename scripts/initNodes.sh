#!/bin/bash

rosnode kill /amcl 
rosnode kiil /compressed_map_publisher
rosnode kiil /joystick_relay
rosnode kiil /map_configuration_server
rosnode kiil /map_server
rosnode kiil /map_setup
rosnode kiil /joystick
rosnode kiil /pal_computer_monitor_node
rosnode kiil /pal_navigation_sm
rosnode kiil /pal_topic_monitor_node
rosnode kiil /move_base
rosnode kiil /pal_vo_server
rosnode kiil /mm11_prod
rosnode kiil /embedded_networking_supervisor
rosnode kiil /joy_teleop
rosnode kiil /pose_saver
rosnode kiil /pal_diagnostic_aggregator 
rosnode kiil /pal_supervisor_node
rosnode kiil /pal_webcommander_node
