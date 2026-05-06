# Otonom Araç Gazebo Simülasyonu (bee1)

Bu depo, ROS 2 ve Gazebo ortamında **bee1** isimli otonom bir aracın simülasyonu, kontrolü ve çevre modellerini içermektedir. Proje; aracın fiziksel tanımlamalarından (URDF/Xacro), pist modellerine ve klavye ile kontrol edilmesini sağlayan teleop düğümlerine kadar tüm bileşenleri kapsar.

---

## 📁 Proje Yapısı ve Klasör Fonksiyonları

Aşağıdaki hiyerarşi, repodaki dosyaların rollerini ve teknik detaylarını açıklar:

### 1. Arac_Ws/ (ROS 2 Workspace)
Ana çalışma alanıdır. Robotun yazılımsal ve fiziksel tanımlamalarını barındırır.

* **src/bee1_description/**: Aracın tüm ROS 2 tanımlamalarını içeren ana pakettir.
    * **urdf/**: Aracın 3D iskelet ve fiziksel özelliklerini (kütle, atalet, sensör yerleşimi) tutan `.xacro` dosyalarını içerir.
    * **launch/**: Düğümleri ve Gazebo'yu başlatan Python tabanlı başlatma dosyalarıdır.
        * `map_and_bee1.launch.py`: Hem dünyayı hem de aracı tek seferde yükler.
        * `spawn_bee1.launch.py`: Sadece aracı mevcut bir dünyaya dahil eder.
    * **bee1_teleop.py**: Aracı klavye (WASD vb.) ile kontrol etmenizi sağlayan Python düğümüdür.
    * **CMakeLists.txt & package.xml**: Paket bağımlılıklarını ve derleme kurallarını belirleyen standart ROS 2 dosyalarıdır.

### 2. map_models/ (Gazebo Çevre Modelleri)
Simülasyon içerisindeki engellerin (mavi, siyah, beyaz, yeşil koniler) görsel ve fiziksel tanımlarıdır.

* Her model klasörü altında bir `.sdf` (Gazebo Model Formatı) ve mesh dosyaları (`.dae`) bulunur.
* **Önemli:** Bu klasörün yolu Gazebo'ya tanıtılmadan dünya modelleri (koniler vb.) düzgün yüklenmez.

### 3. map_worlds/ (Dünya Tanımları)
* **map_world.world**: Pistin genel yapısını, ışıklandırmayı ve `map_models` altındaki modellerin hangi koordinatlarda duracağını belirleyen ana sahne dosyasıdır.

### 4. setup.sh
Gerekli ortam değişkenlerini ayarlayan veya kurulum adımlarını otomatize eden yardımcı scripttir.

---

## 🚀 Sıfırdan Çalıştırma Rehberi

Bu adımlar, Ubuntu üzerinde **ROS 2 (Humble/Foxy)** yüklü olduğu varsayılarak hazırlanmıştır.

### 1. Hazırlık ve Bağımlılıklar
Gazebo'nun modelleri bulabilmesi için `GAZEBO_MODEL_PATH` değişkenini ayarlamalıyız. Deponun ana dizininde şu komutu çalıştırın:

```bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$(pwd)/map_models
```
## 2. Workspace DerlemeROS 2 çalışma alanına gidip paketleri derleyin:
```bash
cd Arac_Ws
colcon build --symlink-install
source install/setup.bash
```
## 3. Simülasyonu BaşlatmaDünyayı ve aracı aynı anda Gazebo ortamında açmak için ana launch dosyasını çalıştırın:
```bash
ros2 launch bee1_description map_and_bee1.launch.py
```
## 4. Aracı Hareket Ettirme (Teleop)Aracı klavye ile sürmek için yeni bir terminal açın, workspace'i tekrar kaynaklayın ve teleop düğümünü çalıştırın:
```bash
cd Arac_Ws
source install/setup.bash
ros2 run bee1_description bee1_teleop.py
```
🛠 Bilinmesi Gereken Teknik DetaylarÖzellikAçıklamaXacro Kullanımıbee1.xacro dosyası bir XML makrosudur. Model değişikliklerinde bu dosya çalışma anında URDF'e dönüştürülerek Gazebo'ya gönderilir.Mesh HatalarıEğer Gazebo açıldığında koniler görünmüyorsa, GAZEBO_MODEL_PATH değişkeninin map_models klasörünü gösterdiğinden emin olun.Topic İsimleriAraç varsayılan olarak /cmd_vel üzerinden komut alır. Kendi otonom algoritmanızı yazarsanız bu topice geometry_msgs/Twist mesajı göndermeniz gerekir.
