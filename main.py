#!/usr/bin/env python

import websocket
import _thread
import time
import json
import unicodedata
import subprocess
import google
import ED
import ssl
import readline
from OpenSSL import SSL


comm = {'|source': '''The bot: https://github.com/WhiteheadV/Ebear-Bot
The bear: https://github.com/WhiteheadV/ExistentialistBear\nThe art: jgs''',
'|help': '''Usage: \"|eb\" [args] (\"-s\" 4 source of last text or -say [string]),
\"|afk [reason](optional)\", \"|lmsg [recipient] [your message]\", \"|source\",
\"|g [query]\" (Search google), \"|ed [query]\" (Search Encyclopedia Dramatica)''',
'owname': 'botName#Pass'}

exceptions = [comm['owname'].split('#')[0]] # (((other bot nicks go here)))

chrlst = '1234567890:().·•º…«¯´×†‡?!\";|\/`\',<>*@#$%^&-+=[]{}~'

usrstat = {}

usrmsg = {}

usrlmsg = {}

flag = False

def pnctMrk(strng):
    L = [':p', ':v', ':d', ':t', ':c', ':x', ':o', ':q', ':w', ':k', ':vv', ':f', '\'c']
    if (strng[-1] not in chrlst and
       any(strng.lower().endswith(sm) for sm in L) == False):
        strng += '.'
    return strng

def prsDrtn(seconds):
    dys = hrs = mins = 0
    # (((rounding)))
    scns = int(seconds)
    if seconds - scns > 0.5: scns += 1
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

def run(*args):
    ws.send(json.dumps({'cmd': 'chat', 'text': runBear(args)}))

def runBear(sors):
    if not sors:
        p = subprocess.Popen('./Ebear',
        cwd='path to ExistentialistBear/',
        stdout=subprocess.PIPE, shell=False)
        (output, err) = p.communicate()
        return output.decode('utf-8')
    elif sors[0] == 1:
        p = subprocess.Popen(['./Ebear', '-s'],
        cwd='path to ExistentialistBear/',
        stdout=subprocess.PIPE, shell=False)
        (output, err) = p.communicate()
        return output.decode('utf-8')
    elif sors[0] == 2:
        p = subprocess.Popen(['./Ebear', '-say', sors[1]],
        cwd='path to ExistentialistBear/',
        stdout=subprocess.PIPE, shell=False, universal_newlines=True)
        (output, err) = p.communicate()
        return output

def cmndBlk(msg):
    if msg['cmd'] == 'chat':
        if msg['text'].lower().strip() == '|eb':
            _thread.start_new_thread(run, ())
        elif msg['text'].lower().strip() == '|eb -s':
            _thread.start_new_thread(run, ((1,)))
        elif msg['text'].lower()[:13] == '|eb -say ' and len(msg['text']) > 13:
            _thread.start_new_thread(run, ((2, msg['text'][13:])))
        elif msg['text'].lower()[:9] == '|eb -say ' and len(msg['text']) > 9:
            _thread.start_new_thread(run, ((2, msg['text'][9:])))
        elif msg['text'].lower().strip() == '|source':
            ws.send(json.dumps({'cmd': 'chat', 'text': ('%s') % comm['|source']}))
        elif (msg['text'].lower().strip() == '|help'
                or msg['text'].lower().strip()) == '|h':
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
        afk(msg)
        responses(msg)

def out():
    readline.parse_and_bind('C-k: ";\n"')
    text = []
    line = ';'
    while True:
        line = input('$> ')
        if line.endswith(';'):
            text.append(line[:-1])
        elif line:
            text.append(line)
            ws.send(json.dumps({'cmd': 'chat', 'text': '\n'.join(text)}))
            text = []

def responses(msg):
    global flag
    mssg = msg['text'].lower()
    if mssg[:12]  == 'what is love' or mssg[:13] == 'what is love?':
        ws.send(json.dumps({'cmd': 'chat', 'text': 'baby don\'t hurt me'}))
        flag = True
    elif flag == True and (mssg == 'don\'t hurt me' or mssg == 'dont hurt me'):
        ws.send(json.dumps({'cmd': 'chat', 'text': 'no more'}))
        flag = False

def afk(msg):
    if msg['text'].lower()[:4] == '|afk' and msg['nick'] not in usrstat:
        if len(msg['text'].strip()) > 4:
            usrstat[msg['nick']] = msg['text'][4:].strip()
            ws.send(json.dumps({'cmd': 'chat', 'text': 'User @%s is now afk: %s'
            % (msg['nick'], usrstat[msg['nick']])}))
        else:
            usrstat[msg['nick']] = ''
            ws.send(json.dumps({'cmd': 'chat', 'text': 'User @%s is now afk.'
            % (msg['nick'])}))
    elif msg['nick'] not in exceptions and '|lmsg' not in msg['text'].lower():
        for key, val in usrstat.items():
            if '@%s' % (key) in msg['text'] and key != msg['nick']:
                if val != '':
                    ws.send(json.dumps({'cmd': 'chat', 'text': '@%s user @%s is afk: %s'
                        % (msg['nick'], key, val)}))
                    if key != msg['text'].strip():
                        usrmsg.setdefault(key,
                        {})[msg['nick']] = msg['text'].replace('@' + key, '', 1)
                else:
                    ws.send(json.dumps({'cmd': 'chat', 'text': '@%s user @%s is afk.'
                        % (msg['nick'], key)}))
                    if key != msg['text'].strip():
                        usrmsg.setdefault(key,
                        {})[msg['nick']] = msg['text'].replace('@' + key, '', 1)
            if msg['nick'] == key:
                if msg['text'][0] == '|' and len(msg['text']) > 1:
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
            #Fix this mess l8er
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
        time.sleep(50)
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
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://hack.chat/chat-ws',
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,
                              )
    ws.on_open = on_open
    ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})
