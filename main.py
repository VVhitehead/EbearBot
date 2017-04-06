#!/usr/bin/env python
# -*- coding: utf-8 -*-

import websocket
import time
import _thread
import json
import unicodedata
import subprocess
import google
import ED
import WA
import ssl
import readline
from OpenSSL import SSL

# v(all the global vars)v
comm = {'|source': '''The bot: https://github.com/WhiteheadV/EbearBot
The bear: https://github.com/WhiteheadV/ExistentialistBear\nThe art: jgs''',
'|help': '''Usage: \"|eb\" [args] (\"-s\" 4 source of last text or -say [string]),
\"|afk [reason](optional)\", \"|lmsg [recipient] [your message]\", \"|source\",
\"|g [query]\" (Search google), \"|ed [query]\" (Search Encyclopedia Dramatica),
\"|wa [query]\" (Compute answers with Wolphram Alpha)''',
'owname': 'botName#Pass'}

exceptions = [comm['owname'].split('#')[0]] # (other bot nicks go in this list)

chrlst = '1234567890:().·•º…«¯´×†‡?!\";|\/`\',<>*@#$%^&-+=[]{}~'

usrstat = {}

usrmsg = {}

usrlmsg = {}

flag = False

flags = [False, False, False, False, False, False, False, False, False]

def pnctMrk(strng):
    L = [':p', ':v', ':d', ':t', ':c', ':x', ':o', ':q', ':w', ':k', ':vv',
        ':f', '\'c']
    if (strng[-1] not in chrlst and
       any(strng.lower().endswith(sm) for sm in L) == False):
        strng += '.'
    return strng

def prsDrtn(seconds):
    dys = hrs = mins = 0
    scns = int(seconds)
    if seconds - scns > 0.5: scns += 1  # (((rounding)))
    if (scns / 86400) >= 1:
        dys = int(scns / 86400)
        scns %= 86400
    if (scns / 3600) >= 1:
        hrs = int(scns / 3600)
        scns %= 3600
    if (scns / 60) >= 1:
        mins = int(scns / 60)
        scns %= 60
    if dys == 1:
        return ('{0} day, {1:02d}:{2:02d}:{3:02d}'.format(dys, hrs, mins, scns))
    elif dys > 1:
        return ('{0} days, {1:02d}:{2:02d}:{3:02d}'.format(dys, hrs, mins, scns))
    return ('{0:01d}:{1:02d}:{2:02d}'.format(hrs, mins, scns))

def runBear(sors):
    if sors == 0:
        p = subprocess.Popen('./Ebear',
        cwd='/home/theone/Documents/Atom(SSD)/ExistentialistBear/',
        stdout=subprocess.PIPE, shell=False)
        (output, err) = p.communicate()
        ws.send(json.dumps({'cmd': 'chat', 'text': output.decode('utf-8')}))
    elif sors == 1:
        p = subprocess.Popen(['./Ebear', '-s'],
        cwd='/home/theone/Documents/Atom(SSD)/ExistentialistBear/',
        stdout=subprocess.PIPE, shell=False)
        (output, err) = p.communicate()
        ws.send(json.dumps({'cmd': 'chat', 'text': output.decode('utf-8')}))
    elif sors[0] == 2:
        p = subprocess.Popen(['./Ebear', '-say', sors[1]],
        cwd='/home/theone/Documents/Atom(SSD)/ExistentialistBear/',
        stdout=subprocess.PIPE, shell=False)
        (output, err) = p.communicate()
        ws.send(json.dumps({'cmd': 'chat', 'text': output.decode('utf-8')}))

def cmndBlk(msg):
    if msg['cmd'] == 'chat':
        if msg['text'].lower().strip() == '|eb':
            _thread.start_new_thread(runBear, (0,))
        elif msg['text'].lower().strip() == '|eb -s':
            _thread.start_new_thread(runBear, (1,))
        elif msg['text'].lower()[:9] == '|eb -say ' and len(msg['text']) > 9:
            _thread.start_new_thread(runBear, ((2, msg['text'][9:]),))
        elif msg['text'].lower().strip() == '|source':
            ws.send(json.dumps({'cmd': 'chat', 'text': ('%s') % comm['|source']}))
        elif (msg['text'].lower().strip() == '|help'
                or msg['text'].lower().strip() == '|h'):
            ws.send(json.dumps({'cmd': 'chat', 'text': ('%s') % comm['|help']}))
        elif msg['text'].lower()[:3] == '|g ':
            if len(msg['text'].strip()) > 3:
                ws.send(json.dumps({'cmd': 'chat', 'text': google.search(msg['text'][3:])}))
            else:
                ws.send(json.dumps({'cmd': 'chat', 'text': 'Usage is |g \"string\"'}))
        elif msg['text'].lower()[:4] == '|ed ':
            if len(msg['text']) > 4:
                ws.send(json.dumps({'cmd': 'chat', 'text': ED.search(msg['text'][4:])}))
            else:
                ws.send(json.dumps({'cmd': 'chat', 'text': 'Usage is |ed \"string\"'}))
        elif msg['text'].lower() == '|ed':
            ws.send(json.dumps({'cmd': 'chat', 'text': 'Usage is |ed \"string\"'}))
        elif msg['text'].lower()[:4] == '|wa ':
            if len(msg['text']) > 4:
                ws.send(json.dumps({'cmd': 'chat', 'text': WA.search(msg['text'][4:])}))
            else:
                ws.send(json.dumps({'cmd': 'chat', 'text': 'Usage is |wa \"string\"'}))
        elif msg['text'].lower() == '|wa':
            ws.send(json.dumps({'cmd': 'chat', 'text': 'Usage is |wa \"string\"'}))
        afk(msg)
        responses(msg)

def startup_hook():
    readline.insert_text('» ')
    readline.redisplay()

def out():
    try:
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode vi')
        readline.parse_and_bind('C-x: "\x16\n"')
        readline.set_pre_input_hook(startup_hook)
    except Exception as e:
        print (e)
        return
    while True:
        try:
            line = input()
            line = line.strip('» ')
            ws.send(json.dumps({'cmd': 'chat', 'text': line}))
        except EOFError:
            print ('EOF signaled, exiting...')
            break

def responses(msg):
    global flag
    m = msg['text'].lower()
    if m.startswith('what is love') and len(m) < 14 and not flag:
        ws.send(json.dumps({'cmd': 'chat', 'text': 'baby don\'t hurt me..'}))
        flag = True
    elif flag == True and (m == 'don\'t hurt me' or m == 'dont hurt me'):
        ws.send(json.dumps({'cmd': 'chat', 'text': 'no more...'}))
        flag = False
    if m.startswith('this is my rifle') and len(m) < 19 and not (any(flags)):
        ws.send(json.dumps({'cmd': 'chat', 'text': 'There are many like it..'}))
        flags[0] = True
    elif m.startswith('but this one is mine') and len(m) < 23 and flags[0]:
        ws.send(json.dumps({'cmd': 'chat',
            'text': 'My rifle is my best friend..'}))
        flags[0], flags[1] = False, True
    elif (m.startswith('it is my life') and len(m) < 16 and not flags[0]
            and flags[1]):
        ws.send(json.dumps({'cmd': 'chat',
            'text':'I must master it as I must master my life..'}))
        flags[:2], flags[2] = [False for f in flags[:2]], True
    elif (m.startswith('without me') and len(m) < 13 and not (any(flags[:2]))
            and flags[2]):
        ws.send(json.dumps({'cmd': 'chat', 'text': 'my rifle is useless..'}))
        flags[:3], flags[3] = [False for f in flags[:3]], True
    elif (m.startswith('without my rifle') and len(m) < 19 and
            not (any(flags[:3])) and flags[3]):
        ws.send(json.dumps({'cmd': 'chat', 'text': 'I am useless..'}))
        flags[:4], flags[4] = [False for f in flags[:4]], True
    elif (m.startswith('i must fire my rifle true') and len(m) < 29 and
            not (any(flags[:4])) and flags[4]):
        ws.send(json.dumps({'cmd': 'chat', 'text':
        'I must shoot straighter than my enemy who is trying to kill me...'}))
        flags[:] = [False for f in flags[:]]

def afk(msg):
    if msg['text'].lower()[:4] == '|afk' and msg['nick'] not in usrstat:
        if len(msg['text'].strip()) > 4:
            usrstat[msg['nick']] = msg['text'][4:].strip()
            ws.send(json.dumps({'cmd': 'chat', 'text': 'User @%s is now AFK: %s'
            % (msg['nick'], usrstat[msg['nick']])}))
        else:
            usrstat[msg['nick']] = ''
            ws.send(json.dumps({'cmd': 'chat', 'text': 'User @%s is now AFK'
            % (msg['nick'])}))
    elif msg['nick'] not in exceptions and not msg['text'].lower().startswith('|lmsg'):
        for key, val in usrstat.items():
            if '@%s' % (key) in msg['text'] and key != msg['nick']:
                if key != msg['text'].strip() and msg['text'].strip() != '@' + key:
                    usrmsg.setdefault(key,
                    {})[msg['nick']] = msg['text'].replace('@' + key, '', 1)
                if val != '':
                    ws.send(json.dumps({'cmd': 'chat', 'text': '@%s user @%s is AFK: %s'
                        % (msg['nick'], key, val)}))
                else:
                    ws.send(json.dumps({'cmd': 'chat', 'text': '@%s user @%s is AFK'
                        % (msg['nick'], key)}))
            if msg['nick'] == key:
                if msg['text'][0] == '|':
                    break
                ws.send(json.dumps({'cmd': 'chat', 'text': 'User @%s is now back.' % (key)}))
                del usrstat[key]
                for k, v in usrmsg.items():
                    if k == msg['nick']:
                        for key, val in v.items():
                            ws.send(json.dumps({'cmd': 'chat', 'text': '@%s user @%s left:%s'
                                % (k, key, val)}))
                            time.sleep(0.5)
                        del usrmsg[k]
                        break
                break

def leaveMsg(msg):
    if msg['cmd'] == 'chat':
        if msg['text'].lower()[:5] == '|lmsg' and len(msg['text']) > 7:
            try:
                n = msg['text'][5:].strip().split(None, 1)[0].replace('@', '', 1)
                m = msg['text'][5:].strip().split(None, 1)[1]
                t = time.time()
            except IndexError:
                ws.send(json.dumps({'cmd': 'chat', 'text':
                    'Usage is |lmsg [recipient] [your message]'}))
                return
            if len(n) > 0 and len(m) > 0 and n != comm['owname'].split('#')[0]:
                usrlmsg.setdefault(n, {})[msg['nick']] = m, t
                ws.send(json.dumps({'cmd': 'chat', 'text': ('@%s user @%s will get '
                'your message the first time he writes something or joins this room.')
                    % (msg['nick'], n)}))
            else:
                ws.send(json.dumps({'cmd': 'chat', 'text':
                    'Usage is |lmsg [recipient] [your message]'}))
        for key, val in usrlmsg.items():
            if key.lower() == msg['nick'].lower():
                for k, v in val.items():
                    ws.send(json.dumps({'cmd': 'chat', 'text': '@%s user @%s '
                    'left you(%s ago): %s'
                        % (key, k, prsDrtn(time.time() - v[1]), v[0])}))
                    time.sleep(0.5)
                del usrlmsg[key]
                break
    elif msg['cmd'] == 'onlineAdd':
        for key, val in usrlmsg.items():
            if key.lower() == msg['nick'].lower():
                for k, v in val.items():
                    ws.send(json.dumps({'cmd': 'chat', 'text': '@%s user @%s '
                    'left you(%s ago): %s'
                        % (key, k, prsDrtn(time.time() - v[1]), v[0])}))
                    time.sleep(0.5)
                del usrlmsg[key]
                break

def heartBeat():
    while(True):
        time.sleep(40)
        ws.send(json.dumps({'cmd': 'ping'}))

def on_message(ws, message):
    message = json.loads(message)
    for i in message:
        unicodedata.normalize('NFKD', i).encode('ascii', 'ignore')
        #print (i, message[i])
    cmndBlk(message)
    leaveMsg(message)

def on_error(ws, error):
    print (error)

def on_close(ws):
    print ('### closed ###')

def on_open(ws):
    ws.send(json.dumps({'cmd': 'join', 'channel': 'programming', 'nick': comm['owname']}))
    _thread.start_new_thread(heartBeat, ())
    _thread.start_new_thread(out, ())


if __name__ == '__main__':
    ws = websocket.WebSocketApp('wss://hack.chat/chat-ws',
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,
                              )
    ws.on_open = on_open
    ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})
