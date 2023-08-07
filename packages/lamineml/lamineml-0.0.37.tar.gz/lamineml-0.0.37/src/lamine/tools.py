import time
from jnius import autoclass
import platform
context=autoclass("android.content.Context")
from  plyer.platforms.android import activity
Context = autoclass('android.content.Context')
from kivy.app import App
from jnius import autoclass ,cast
def Secure(): 
    x=cast ("android.app.KeyguardManager",activity.getSystemService(Context.KEYGUARD_SERVICE)  )
    h=x.isKeyguardSecure()
    if(h):
        return True
    else:
        return False
    
            
