#!/bin/bash
echo "Kurulum başlıyor..."

mkdir -p ~/.gazebo/models
mkdir -p ~/.gazebo/worlds

cp -r map_models/siyahlar ~/.gazebo/models/
cp -r map_models/beyazlar ~/.gazebo/models/
cp -r map_models/maviler ~/.gazebo/models/
cp -r map_models/yesil ~/.gazebo/models/
cp map_worlds/map_world.world ~/.gazebo/worlds/

# Eksik klasörleri oluştur
mkdir -p Arac_Ws/src/bee1_description/config
mkdir -p Arac_Ws/src/bee1_description/meshes
mkdir -p Arac_Ws/src/bee1_description/rviz

# Build et
cd Arac_Ws
rm -rf build install log
colcon build --packages-select bee1_description
source install/setup.bash

echo "Kurulum tamamlandı!"
echo "Çalıştırmak için:"
echo "source /opt/ros/foxy/setup.bash"
echo "source Arac_Ws/install/setup.bash"
echo "ros2 launch bee1_description map_and_bee1.launch.py"
