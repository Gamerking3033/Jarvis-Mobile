from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.clock import Clock
import socket
import threading

class SplashScreen(Screen):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        layout = FloatLayout()
        # Telefon ekranında ortalanacak logo
        self.img = Image(source='ironman.png', size_hint=(.5, .5), pos_hint={'center_x': .5, 'center_y': .5})
        layout.add_widget(self.img)
        self.add_widget(layout)

    def on_enter(self):
        # 2 saniye bekle, 3 saniyede pürüzsüzce şeffaflaşarak kaybol
        anim = Animation(opacity=0, duration=3)
        anim.bind(on_complete=self.ana_ekrana_gec)
        Clock.schedule_once(lambda dt: anim.start(self.img), 2)

    def ana_ekrana_gec(self, *args):
        self.manager.current = 'jarvis_ui'

class JarvisUI(Screen):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.layout = FloatLayout()
        
        # J.A.R.V.İ.S. Çember Yazısı (Neon Mavi)
        self.label = Label(text="J.A.R.V.İ.S.", font_size='45sp', color=(0, 0.8, 1, 1))
        self.layout.add_widget(self.label)
        
        # Sürekli büyüme/küçülme (Nefes alma) efekti
        anim = Animation(font_size='50sp', duration=1.5) + Animation(font_size='45sp', duration=1.5)
        anim.repeat = True
        anim.start(self.label)
        
        self.add_widget(self.layout)

    def kucul(self):
        # Telefonda 'küçül' komutu geldiğinde sağ üst köşeye %55 şeffaflıkla yerleşir
        self.opacity = 0.45
        self.size_hint = (0.2, 0.15)
        self.pos_hint = {'top': 0.98, 'right': 0.98}

    def sunucuya_mesaj_gonder(self, mesaj):
        # Telefonun donmaması için arka planda thread ile çalıştırıyoruz
        threading.Thread(target=self._socket_gonder, args=(mesaj,)).start()

    def _socket_gonder(self, mesaj):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # NOT: Buraya daha sonra bilgisayarınızın yerel IP adresini yazacağız
            s.connect(('127.0.0.1', 5000)) 
            s.sendall(f"MOBIL|{mesaj}".encode('utf-8'))
            cevap = s.recv(4096).decode('utf-8')
            s.close()
            print(f"Jarvis'ten yanıt geldi: {cevap}")
        except Exception as e:
            print(f"Bağlantı başarısız: {e}")

class JarvisMobileApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(JarvisUI(name='jarvis_ui'))
        return sm

if _name_ == "_main_":
    JarvisMobileApp().run()