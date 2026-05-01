#!/bin/bash
echo "Kurulum başlıyor..."

mkdir -p ~/.gazebo/models
mkdir -p ~/.gazebo/worlds

cp -r map_models/siyahlar ~/.gazebo/models/
cp -r map_models/beyazlar ~/.gazebo/models/
cp -r map_models/maviler ~/.gazebo/models/
cp -r map_models/yesil ~/.gazebo/models/
cp map_worlds/map_world.world ~/.gazebo/worlds/

cd Arac_Ws
colcon build --packages-select bee1_description
source install/setup.bash

echo "Kurulum tamamlandı!"
echo "Çalıştırmak için:"
echo "ros2 launch bee1_description map_and_bee1.launch.py"
