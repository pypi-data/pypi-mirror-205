import contextlib
from tkinter import simpledialog as log, messagebox as m
import socket as s
from datetime import*
import pickle
from _pickle import UnpicklingError

PORT = 5051
HEADER = 64
SERVER = '192.168.1.4'
FORMAT = 'utf-8'
GONE_MSG = '!GONE'
ADDR = (SERVER, PORT)

cl = s.socket(s.AF_INET, s.SOCK_STREAM)
try:
    cl.connect(ADDR)
except OSError:
    m.showerror('Error', 'Either your internet connection or TradChat is not working\nPlease check your Internet Connection\nIf TradChat is not working, we will fix it soon.')
    quit()

cl.send('iAmNotFrenchPotatoHead'.encode())
userinfo = cl.recv(4444)
userinfo = userinfo.decode(FORMAT)
chat = []
while True:
    recv = cl.recv(99999)
    decoded = recv.decode(FORMAT)
    if decoded == "DONE":
        break
    if decoded ==  "A$*<":
        continue
    if "A$*<" in decoded:
        messages = decoded.split("A$*<")
        for message in messages:
            try:
                Message = eval(message)
                chat.append(Message)
            except SyntaxError:
                continue
        continue
    message = eval(decoded)
    chat.append(message)

Userinfo = userinfo.split('?')
userinfo = {}
for i in Userinfo:
    username, password = i.split('!')
    userinfo[username] = password

truth_name = log.askstring('TradChat', 'type username:  ')
if truth_name not in userinfo:
    m.showerror('TradChat', f'No Username {truth_name}.\nWe will now exit you from the program.\nBut you still can just click on the app to start again.')
    cl.send('WrongUsernameError'.encode('utf-8'))
    quit()
truth_password = log.askstring('TradChat', 'Type Password: ')
if userinfo[truth_name].lower() == truth_password.lower():
    m.showinfo('TradChat', f'Welcome {truth_name} to TradChat')
else:
    m.showerror('TradChat', 'Incorrect password.\nWe will now exit you from the program.\nBut you still can just click on the app to start again.')
    cl.send('WrongPasswordError'.encode('utf-8'))
    quit()
cl.send(truth_name.encode(FORMAT))
day = date.today()
time = datetime.today()
message = ['Conn', f'{day.month}~{day.day}~{day.year} at {time.hour}:{time.minute}   New Connection {truth_name}>>> Hello TradChat']
cl.send(pickle.dumps(message))


from pyglet.window import key as k
from threading import Thread as T
import pyglet
import pymunk

board = k.KeyStateHandler()

filt = pymunk.ShapeFilter()

Scene = pymunk.Space()

size = 10

list_of_text = []

speed = 8

ls = [1, 1, 1]

listOfSendableStuff = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ |abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()[]{},./;'<>?:-=_+~`")
listOfSendableStuff.append('"')

pubpic1 = pyglet.image.load('graphics/p1.png')
pubpic1.anchor_x = pubpic1.width//2
pubpic1.anchor_y = pubpic1.height//2
pub2 = pyglet.sprite.Sprite(pubpic1, x=60, y=60)

pubpic2 = pyglet.image.load('graphics/p2.png')
pubpic2.anchor_x = pubpic2.width//2
pubpic2.anchor_y = pubpic2.height//2
pub1 = pyglet.sprite.Sprite(pubpic2, x=60, y=60)

pripic1 = pyglet.image.load('graphics/l1.png')
pripic1.anchor_x = pripic1.width//2
pripic1.anchor_y = pripic1.height//2
pri2 = pyglet.sprite.Sprite(pripic1, x=170, y=60)

pripic2 = pyglet.image.load('graphics/l2.png')
pripic2.anchor_x = pripic2.width//2
pripic2.anchor_y = pripic2.height//2
pri1 = pyglet.sprite.Sprite(pripic2, x=170, y=60)

uppic1 = pyglet.image.load('graphics/U1.png')
uppic1.anchor_y = uppic1.height//2
uppic1.anchor_x = uppic1.width//2
up2 = pyglet.sprite.Sprite(uppic1, x=60, y=180)

uppic2 = pyglet.image.load('graphics/U2.png')
uppic2.anchor_x = uppic2.width//2
uppic2.anchor_y = uppic2.height//2
up1 = pyglet.sprite.Sprite(uppic2, x=60, y=180)

leave = pyglet.media.load('graphics/leave.mp3')
join = pyglet.media.load('graphics/join.mp3')
pubsound = pyglet.media.load('graphics/public.mp3')
prisound = pyglet.media.load('graphics/private.mp3')
player = pyglet.media.Player()

public_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
public_body.position = 60, 60
public = pymunk.Circle(public_body, 50)
public.id = 'public'
Scene.add(public_body, public)

private_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
private_body.position = 170, 60
private = pymunk.Circle(private_body, 50)
private.id = 'private'
Scene.add(private_body, private)

update_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
update_body.position = 60, 180
update = pymunk.Circle(update_body, 50)
update.id = 'update'
Scene.add(update_body, update)

MESSAGE = ''
MESSAGELabel = pyglet.text.Label(MESSAGE, color=(0, 0, 0, 255), font_name='arial', font_size=20, x=15, y=15)

def sendpublic(msg):
    global chat
    day = date.today()
    time = datetime.today()
    message = ['Pub', f'{day.month}~{day.day}~{day.year} at {time.hour}:{time.minute}   {truth_name}>>> {msg}']
    cl.send(pickle.dumps(message))

def sendprivate(person, msg):
    global chat
    day = date.today()
    time = datetime.today()
    message = ['Pri', person, truth_name, f'{day.month}~{day.day}~{day.year} at {time.hour}:{time.minute}', f'   {msg}']
    cl.send(pickle.dumps(message))

NextText = []
You = False

def beforeText():
    for message in chat:
        with contextlib.suppress(TypeError):
            message = pickle.loads(message)
        if message[0] == 'Pub':
            NextText.append(('Pub', message[1]))
            pyglet.clock.schedule_once(Text, 1.0/60)

        elif message[0] == 'Conn':
            NextText.append(('Conn', message[1]))
            pyglet.clock.schedule_once(Text, 1.0 / 60)

        elif message[0] == 'Dis':
            NextText.append(('Dis', message[1]))
            pyglet.clock.schedule_once(Text, 1.0 / 60)

        elif message[0] == 'Pri':
            message.pop(0)
            recver = message.pop(0)
            sender = message.pop(0)
            time = message.pop(0)
            msg = message.pop(0)
            if recver == truth_name:
                NextText.append(('Pri', f'{time}    From {sender}>>> {msg}'))
                pyglet.clock.schedule_once(Text, 1.0 / 60)
            elif sender == truth_name:
                NextText.append(('Pri', f'{time}    To {recver}>>> {msg}'))
                pyglet.clock.schedule_once(Text, 1.0 / 60)
    update()

def Text(dt):
    global NextText
    for someText in NextText:
        try:
            y = list_of_text[-1].y - 30
            x = list_of_text[0].x
        except IndexError:
            y = 885
            x=0

        mode = someText[0]
        sometext = someText[1]
        if mode == 'Conn':
            text = pyglet.text.Label(sometext, y=y, x=x, font_name='arial', color=(255, 244, 0, 255), font_size=size)
            list_of_text.append(text)
        elif mode == 'Dis':
            text = pyglet.text.Label(sometext, y=y, x=x, font_name='arial', color=(87, 96, 255, 255), font_size=size)
            list_of_text.append(text)
        elif mode == 'Pri':
            text = pyglet.text.Label(sometext, y=y, x=x, color=(70, 255, 70, 255), font_size=size, font_name='arial')
            list_of_text.append(text)

        elif mode == 'Pub':
            text = pyglet.text.Label(sometext, y=y, x=x, color=(255, 255, 255, 255), font_size=size, font_name='arial')
            list_of_text.append(text)
    NextText = []

def update():
    while True:
        try:
            Message = cl.recv(65000)
        except ConnectionResetError:
            mainwin.close()
            cw.close()
            quit()
        with contextlib.suppress(UnpicklingError):
            message = pickle.loads(Message)
        if message[0] == 'Pub':
            player.queue(pubsound)
            player.play()
            NextText.append(('Pub', message[1]))
            pyglet.clock.schedule_once(Text, 1.0/60)

        elif message[0] == 'Conn':
            player.queue(join)
            player.play()
            NextText.append(('Conn', message[1]))
            pyglet.clock.schedule_once(Text, 1.0 / 60)

        elif message[0] == 'Dis':
            player.queue(leave)
            player.play()
            NextText.append(('Dis', message[1]))
            pyglet.clock.schedule_once(Text, 1.0 / 60)

        elif message[0] == 'Pri':
            message.pop(0)
            recver = message.pop(0)
            sender = message.pop(0)
            time = message.pop(0)
            msg = message.pop(0)
            if recver == truth_name:
                player.queue(prisound)
                player.play()
                NextText.append(('Pri', f'{time}    From {sender}>>> {msg}'))
                pyglet.clock.schedule_once(Text, 1.0 / 60)
            elif sender == truth_name:
                player.queue(prisound)
                player.play()
                NextText.append(('Pri', f'{time}    To {recver}>>> {msg}'))
                pyglet.clock.schedule_once(Text, 1.0 / 60)

Da = T(target=beforeText)
Da.start()

mainwin = pyglet.window.Window(height=900, width=1400, resizable=True, caption=f'{truth_name}\'sTradChat Chat Window')
mainwin.push_handlers(board)

cw = pyglet.window.Window(height=250, width=130, resizable=True, caption=f'{truth_name}\'s TradChat Control Panel')
cw.push_handlers(board)
cw.set_minimum_size(height=240, width=120)
heart = pyglet.image.load("graphics/Immaculate Heart.png")
cw.set_icon(heart)
mainwin.set_icon(heart)
mainTextSquare = pyglet.shapes.BorderedRectangle(-700, 0, 200000, 55, border=15, border_color=(0, 0, 0))

@mainwin.event
def on_draw():
    mainwin.clear()
    for text in list_of_text:
        text.draw()
    mainTextSquare.draw()
    MESSAGELabel.draw()

shiftPressed = False

@mainwin.event
def on_key_release(s, m):
    global shiftPressed
    if s == k.LSHIFT:
        shiftPressed = False
    if s == k.RSHIFT:
        shiftPressed = False

@mainwin.event
def on_key_press(s, m):
    global shiftPressed, MESSAGE, MESSAGELabel
    if s == k.LEFT:
        MESSAGELabel.x -= 40
    if s == k.RIGHT:
        MESSAGELabel.x += 40
    if s == k.RSHIFT:
        shiftPressed = True
    if s == k.LSHIFT:
        shiftPressed = True
    if s == k.Q and shiftPressed:
        MESSAGE += 'Q'
    if s == k.W and shiftPressed:
        MESSAGE += 'W'
    if s == k.E and shiftPressed:
        MESSAGE += 'E'
    if s == k.R and shiftPressed:
        MESSAGE += 'R'
    if s == k.T and shiftPressed:
        MESSAGE += 'T'
    if s == k.Y and shiftPressed:
        MESSAGE += 'Y'
    if s == k.U and shiftPressed:
        MESSAGE += 'U'
    if s == k.I and shiftPressed:
        MESSAGE += 'I'
    if s == k.O and shiftPressed:
        MESSAGE += 'O'
    if s == k.P and shiftPressed:
        MESSAGE += 'P'
    if s == k.A and shiftPressed:
        MESSAGE += 'A'
    if s == k.S and shiftPressed:
        MESSAGE += 'S'
    if s == k.D and shiftPressed:
        MESSAGE += 'D'
    if s == k.F and shiftPressed:
        MESSAGE += 'F'
    if s == k.G and shiftPressed:
        MESSAGE += 'G'
    if s == k.H and shiftPressed:
        MESSAGE += 'H'
    if s == k.J and shiftPressed:
        MESSAGE += 'J'
    if s == k.K and shiftPressed:
        MESSAGE += 'K'
    if s == k.L and shiftPressed:
        MESSAGE += 'L'
    if s == k.Z and shiftPressed:
        MESSAGE += 'Z'
    if s == k.X and shiftPressed:
        MESSAGE += 'X'
    if s == k.C and shiftPressed:
        MESSAGE += 'C'
    if s == k.V and shiftPressed:
        MESSAGE += 'V'
    if s == k.B and shiftPressed:
        MESSAGE += 'B'
    if s == k.N and shiftPressed:
        MESSAGE += 'N'
    if s == k.M and shiftPressed:
        MESSAGE += 'M'
    if s == k.Q and not shiftPressed:
        MESSAGE += 'q'
    if s == k.W and not shiftPressed:
        MESSAGE += 'w'
    if s == k.E and not shiftPressed:
        MESSAGE += 'e'
    if s == k.R and not shiftPressed:
        MESSAGE += 'r'
    if s == k.T and not shiftPressed:
        MESSAGE += 't'
    if s == k.Y and not shiftPressed:
        MESSAGE += 'y'
    if s == k.U and not shiftPressed:
        MESSAGE += 'u'
    if s == k.I and not shiftPressed:
        MESSAGE += 'i'
    if s == k.O and not shiftPressed:
        MESSAGE += 'o'
    if s == k.P and not shiftPressed:
        MESSAGE += 'p'
    if s == k.A and not shiftPressed:
        MESSAGE += 'a'
    if s == k.S and not shiftPressed:
        MESSAGE += 's'
    if s == k.D and not shiftPressed:
        MESSAGE += 'd'
    if s == k.F and not shiftPressed:
        MESSAGE += 'f'
    if s == k.G and not shiftPressed:
        MESSAGE += 'g'
    if s == k.H and not shiftPressed:
        MESSAGE += 'h'
    if s == k.J and not shiftPressed:
        MESSAGE += 'j'
    if s == k.K and not shiftPressed:
        MESSAGE += 'k'
    if s == k.L and not shiftPressed:
        MESSAGE += 'l'
    if s == k.Z and not shiftPressed:
        MESSAGE += 'z'
    if s == k.X and not shiftPressed:
        MESSAGE += 'x'
    if s == k.C and not shiftPressed:
        MESSAGE += 'c'
    if s == k.V and not shiftPressed:
        MESSAGE += 'v'
    if s == k.B and not shiftPressed:
        MESSAGE += 'b'
    if s == k.N and not shiftPressed:
        MESSAGE += 'n'
    if s == k.M and not shiftPressed:
        MESSAGE += 'm'
    if s == k.NUM_1:
        MESSAGE += '1'
    if s == k.NUM_2:
        MESSAGE += '2'
    if s == k.NUM_3:
        MESSAGE += '3'
    if s == k.NUM_4:
        MESSAGE += '4'
    if s == k.NUM_5:
        MESSAGE += '5'
    if s == k.NUM_6:
        MESSAGE += '6'
    if s == k.NUM_7:
        MESSAGE += '7'
    if s == k.NUM_8:
        MESSAGE += '8'
    if s == k.NUM_9:
        MESSAGE += '9'
    if s == k.NUM_0:
        MESSAGE += '0'
    if s == k._1 and not shiftPressed:
        MESSAGE += '1'
    if s == k._2 and not shiftPressed:
        MESSAGE += '2'
    if s == k._3 and not shiftPressed:
        MESSAGE += '3'
    if s == k._4 and not shiftPressed:
        MESSAGE += '4'
    if s == k._5 and not shiftPressed:
        MESSAGE += '5'
    if s == k._6 and not shiftPressed:
        MESSAGE += '6'
    if s == k._7 and not shiftPressed:
        MESSAGE += '7'
    if s == k._8 and not shiftPressed:
        MESSAGE += '8'
    if s == k._9 and not shiftPressed:
        MESSAGE += '9'
    if s == k._0 and not shiftPressed:
        MESSAGE += '0'
    if s == k.SEMICOLON and not shiftPressed:
        MESSAGE += ';'
    if s == k.SEMICOLON and shiftPressed:
        MESSAGE += ':'
    if s == k._1 and shiftPressed:
        MESSAGE += '!'
    if s == k._2 and shiftPressed:
        MESSAGE += '@'
    if s == k._3 and shiftPressed:
        MESSAGE += '#'
    if s == k._4 and shiftPressed:
        MESSAGE += '$'
    if s == k._5 and shiftPressed:
        MESSAGE += '%'
    if s == k._6 and shiftPressed:
        MESSAGE += '^'
    if s == k._7 and shiftPressed:
        MESSAGE += '&'
    if s == k._8 and shiftPressed:
        MESSAGE += '*'
    if s == k._9 and shiftPressed:
        MESSAGE += '('
    if s == k._0 and shiftPressed:
        MESSAGE += ')'
    if s == k.SPACE:
        MESSAGE += ' '
    if s == k.PERIOD and not shiftPressed:
        MESSAGE += '.'
    if s == k.PERIOD and shiftPressed:
        MESSAGE += '>'
    if s == k.COMMA and shiftPressed:
        MESSAGE += '<'
    if s == k.COMMA and not shiftPressed:
        MESSAGE += ','
    if s == k.SLASH and shiftPressed:
        MESSAGE += '?'
    if s == k.SLASH and not shiftPressed:
        MESSAGE += '/'
    if s == k.QUOTELEFT and shiftPressed:
        MESSAGE += '"'
    if s == k.QUOTELEFT and not shiftPressed:
        MESSAGE += "'"
    if s == k.NUM_ADD:
        MESSAGE += '+'
    if s == k.NUM_SUBTRACT:
        MESSAGE += '-'
    if s == k.NUM_MULTIPLY:
        MESSAGE += '*'
    if s == k.NUM_DIVIDE:
        MESSAGE += '/'
    if s == k.MINUS and shiftPressed:
        MESSAGE += '_'
    if s == k.MINUS and not shiftPressed:
        MESSAGE += '-'
    if s == k.EQUAL and shiftPressed:
        MESSAGE += '+'
    if s == k.EQUAL and not shiftPressed:
        MESSAGE += '='
    if s in [k.ENTER, k.RETURN]:
        MESSAGELabel.x = 15
        MESSAGELabel.y = 15
        if MESSAGE == '':
            return
        if MESSAGE.startswith('@'):
            MEssage = list(MESSAGE)
            MEssage.pop(0)
            MESsage = MEssage.copy()
            while True:
                try:
                    MESsage.pop()
                    MeSSAGE = ''.join(MESsage)
                    if MeSSAGE in userinfo:
                        sendprivate(MeSSAGE, ''.join(MEssage).removeprefix(MeSSAGE))
                        break
                except IndexError:
                    break
        else:
            sendpublic(MESSAGE)
        MESSAGE = ''
    if s == k.BACKSPACE:
        with contextlib.suppress(IndexError):
            MESage = list(MESSAGE)
            MESage.pop()
            MESSAGE = ''.join(MESage)

@cw.event
def on_mouse_leave(x, y):
    global ls
    ls = [1, 1, 1]

def refreash():
    with contextlib.suppress(Exception):
        import Updater

@mainwin.event
def on_mouse_motion(x, y, dx, dy):
    if x < 100:
        for i in list_of_text:
            i.x += speed
    if x > mainwin.width-100:
        for i in list_of_text:
            i.x -= speed
    if y > mainwin.height-100:
        for i in list_of_text:
            i.y -= speed
    if y < 100:
        for i in list_of_text:
            i.y += speed

@cw.event
def on_mouse_press(x, y, but, mod):
    global MESSAGE, MESSAGELabel
    if query := Scene.point_query_nearest((x, y), 0, filt):
        if query.shape.id == 'public':
            MESSAGELabel.x = 15
            MESSAGELabel.y = 15
            if MESSAGE == '':
                return
            if MESSAGE.startswith('@'):
                MEssage = list(MESSAGE)
                MEssage.pop(0)
                MESsage = MEssage.copy()
                while True:
                    try:
                        MESsage.pop()
                        MeSSAGE = ''.join(MESsage)
                        if MeSSAGE in userinfo:
                            sendprivate(MeSSAGE, ''.join(MEssage).removeprefix(MeSSAGE))
                            break
                    except IndexError:
                        break
            else:
                sendpublic(MESSAGE)
            MESSAGE = ''
        if query.shape.id == 'update':
            UpThread = T(target=refreash)
            UpThread.start()

def Update(dt):
    global MESSAGELabel
    if MESSAGE.startswith('@'):
        MEsage = list(MESSAGE)
        MEsage.pop(0)
        MeSSAGE = ''.join(MEsage)
        if MeSSAGE in userinfo:
            MESSAGELabel.color = (255, 0, 0, 255)
        else:
            MESSAGELabel.color = (0, 0, 0, 255)
    MESSAGELabel = pyglet.text.Label(MESSAGE, color=MESSAGELabel.color, font_name='arial', font_size=MESSAGELabel.font_size, x=MESSAGELabel.x, y=MESSAGELabel.y)

@mainwin.event
def on_mouse_press(x, y, but, mod):
    global size
    if but == 1:
        if size > 10:
            size -= 1
        for text in list_of_text:
            text.font_size = size
    elif but == 4:
        if size < 28:
            size += 1
        for text in list_of_text:
            text.font_size = size

@cw.event
def on_mouse_motion(x, y, dx, dy):
    global ls
    if query := Scene.point_query_nearest((x, y), 0, filt):
        if query.shape.id == 'private':
            ls = [1, 1, 2]
        if query.shape.id == 'public':
            ls = [1, 2, 1]
        if query.shape.id == 'update':
            ls = [2, 1, 1]
    else:
        ls = [1, 1, 1]

@cw.event
def on_draw():
    cw.clear()
    if ls[1] == 1:
        pub2.draw()
    elif ls[1] == 2:
        pub1.draw()
    if ls[0] == 1:
        up2.draw()
    elif ls[0] == 2:
        up1.draw()

pyglet.clock.schedule_interval(Update, 1.0/60)
pyglet.app.run()
