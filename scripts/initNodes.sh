#!/bin/bash

rosnode kill /amcl &> /dev/null 
rosnode kill /compressed_map_publisher &> /dev/null
rosnode kill /map_configuration_server &> /dev/null
rosnode kill /map_server &> /dev/null
rosnode kill /map_setup &> /dev/null 
rosnode kill /pal_computer_monitor_node &> /dev/null
rosnode kill /pal_navigation_sm &> /dev/null 
rosnode kill /pal_topic_monitor_node &> /dev/null 
rosnode kill /move_base &> /dev/null 
rosnode kill /pal_vo_server &> /dev/null
rosnode kill /mm11_prod &> /dev/null
rosnode kill /embedded_networking_supervisor &> /dev/null
rosnode kill /pose_saver &> /dev/null
rosnode kill /pal_diagnostic_aggregator &> /dev/null
rosnode kill /pal_supervisor_node &> /dev/null
rosnode kill /pal_webcommander_node &> /dev/null
