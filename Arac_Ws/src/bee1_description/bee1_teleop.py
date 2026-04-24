import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, select, termios, tty

msg = """
Bee 1 Gelişmiş Kontrol Paneli
----------------------------------
Hızlanma (İleri): YUKARI OK
Hızlanma (Geri) : AŞAĞI OK
Dönüş (Sol/Sağ): SOL-SAĞ OK
ANİ FREN      : BOŞLUK (SPACE)
Çıkış         : CTRL+C
----------------------------------
(Her basışta hız %10 artar)
"""

class Bee1Teleop(Node):
    def __init__(self):
        super().__init__('bee1_teleop')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.settings = termios.tcgetattr(sys.stdin)
        self.linear_vel = 0.0
        self.angular_vel = 0.0
        self.inc = 0.2  # Her basışta hız artış miktarı (m/s)

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
            if key == '\x1b':
                key += sys.stdin.read(2)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def run(self):
        print(msg)
        try:
            while True:
                key = self.get_key()
                
                if key == '\x1b[A': # YUKARI
                    self.linear_vel += self.inc
                elif key == '\x1b[B': # AŞAĞI
                    self.linear_vel -= self.inc
                elif key == '\x1b[D': # SOL
                    self.angular_vel += self.inc
                elif key == '\x1b[C': # SAĞ
                    self.angular_vel -= self.inc
                elif key == ' ':      # BOŞLUK (TAM DUR)
                    self.linear_vel = 0.0
                    self.angular_vel = 0.0
                
                # Sınırlandırma (Çok hızlı gitmemesi için)
                self.linear_vel = max(min(self.linear_vel, 5.0), -5.0)
                self.angular_vel = max(min(self.angular_vel, 3.0), -3.0)

                twist = Twist()
                twist.linear.x = self.linear_vel
                twist.angular.z = self.angular_vel
                self.publisher_.publish(twist)

                # Anlık hızı ekranda göster
                sys.stdout.write(f"\rMevcut Hız: İleri={self.linear_vel:.2f} | Dönüş={self.angular_vel:.2f}    ")
                sys.stdout.flush()

                if key == '\x03': break
        except Exception as e: print(e)

def main():
    rclpy.init()
    Bee1Teleop().run()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
