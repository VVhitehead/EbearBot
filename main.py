#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import websocket
import time
import _thread
import json
import unicodedata
import subprocess
import Google
import ED
import WA
import ssl
import readline
import re
import urllib.request

# v(all the global vars)v
com = {'owname': 'botName#Pass', 'owntrip': 'tripcode'}

comm = {'|source': '''The bot: https://github.com/WhiteheadV/EbearBot
The bear: https://github.com/WhiteheadV/ExistentialistBear\nThe art: jgs''',
'|help': '''Usage / List of **commands**: 
\"**|eb** [args]\" (**-s** 4 getting source of the last said text or **-say** [_custom_ string](Any _arbitrary_ string))
\"**|afk** [reason]\"(_Optional_ argument)
\"**|lmsg** [recipient nick] [your message]\" (Leave a message via nickname - **Works _with_** `/whisper` @{} **lmsg** [recipient nick] [your message])
\"**|tmsg** [recipient trip] [your message]\" (Leave a message via tripcode - **Works _with_** `/whisper` @{} **tmsg** [recipient trip] [your message])
\"**|source**\" (About the bot) 
\"**|g** [query]\" (Search google) 
\"**|ed** [query]\" (Search Encyclopedia Dramatica) - $\\large{{\\color{{red}}\\mathbf{{Deprecated}}}}$
\"**|wa** [query]\" [//TeXForm](_Optional_(returns output in LaTeX form)) (Compute answers with Wolphram Alpha)'''.format(com['owname'].split('#')[0],
                                                                                                                          com['owname'].split('#')[0])}

exceptions = [com['owname'].split('#')[0]] # (nicks of other bots go in this list)

usrstat = {}
usrmsg = {}
usrlmsg = {}
usrtripmsg = {}
usrwsptmsg = {}
usrwmsg = {}

flag = False
flags = [False, False, False, False, False, False, False, False, False]

joined = 0
eeCounter = 0
wspCnt = 0


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
    prefix = '```text \n'
    #sufix = '```' # redundant as in the prefix formats strings that follow and 
    if sors == 0:
        p = subprocess.Popen('./Ebear',
        cwd='~/.../ExistentialistBear/', # YOUR path to ExistentialistBear folder containing the executable
        stdout=subprocess.PIPE, shell=False)
        (output, err) = p.communicate()
        ws.send(json.dumps({'cmd': 'chat', 'text': prefix + output.decode('utf-8')}))
    elif sors == 1:
        p = subprocess.Popen(['./Ebear', '-s'],
        cwd='~/.../ExistentialistBear/', # YOUR path to ExistentialistBear folder containing the executable
        stdout=subprocess.PIPE, shell=False)
        (output, err) = p.communicate()
        ws.send(json.dumps({'cmd': 'chat', 'text': prefix + output.decode('utf-8')}))
    elif sors[0] == 2:
        p = subprocess.Popen(['./Ebear', '-say', sors[1]],
        cwd='~/.../ExistentialistBear/', # YOUR path to ExistentialistBear folder containing the executable
        stdout=subprocess.PIPE, shell=False)
        (output, err) = p.communicate()
        ws.send(json.dumps({'cmd': 'chat', 'text': prefix + output.decode('utf-8')}))


def runDYM(word, n=5):
    if int(n) > 10:
        return runDYM(word, n=10) # Sanitize output by allowing maximum of 10 results!
    p = subprocess.Popen(['dym', '-c', '-n', '{}'.format(n), '{}'.format(word)],
        cwd = '/usr/bin',
        stdout = subprocess.PIPE, shell = False)
    (output, err) = p.communicate()
    frmtd_output = '==Did you mean?==\n'
    url = 'https://www.thefreedictionary.com/'
    for i, chunk in enumerate(output.decode('utf-8').split('\n')[:-1]):
        frmtd_output += '[{}]({})\n'.format(str(i + 1) + '. ' + chunk, url + chunk)
    ws.send(json.dumps({'cmd': 'chat', 'text': frmtd_output})) # Modify output b4 sending

def cmndBlk(msg):
    if msg['cmd'] == 'chat':
        if msg['text'].lower().strip() == '|eb':
            _thread.start_new_thread(runBear, (0,))
        elif msg['text'].lower().strip() == '|eb -s':
            _thread.start_new_thread(runBear, (1,))
        elif msg['text'].lower()[:9] == '|eb -say ' and len(msg['text']) > 9:
            _thread.start_new_thread(runBear, ((2, msg['text'][9:]),))
        elif msg['text'].lower()[:8] == '|dym -n ':
            _thread.start_new_thread(runDYM, ((2, '{}'.format(msg['text'][9:])), msg['text'][8:10]))
        elif msg['text'].lower()[:5] == '|dym ' and len(msg['text']) > 7:
            _thread.start_new_thread(runDYM, ((2, '{}'.format(msg['text'][5:])),))
        elif msg['text'].lower().strip() == '|source':
            ws.send(json.dumps({'cmd': 'chat', 'text': ('%s') % comm['|source']}))
        elif (msg['text'].lower().strip() == '|help'
                or msg['text'].lower().strip() == '|h'):
            ws.send(json.dumps({'cmd': 'chat', 'text': ('%s') % comm['|help']}))
        elif msg['text'].lower()[:3] == '|g ':
            if len(msg['text'].strip()) > 3:
                ws.send(json.dumps({'cmd': 'chat', 'text': Google.search(msg['text'][3:])}))
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
        elif msg['text'].lower() == '|uptime':
            ws.send(json.dumps({'cmd': 'chat', 'text': '%s' % prsDrtn(time.time() - joined)}))
        afk(msg)
        responses(msg)


def startup_hook():
    readline.insert_text('❯ ')
    readline.redisplay()


def out():
    try:
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode vi')
        readline.parse_and_bind('C-x: "\x16\n"')
        readline.set_pre_input_hook(startup_hook)
    except Exception as e:
        print(e)
        return
    while True:
        try:
            line = input()
            line = line.strip('❯ ')
            ws.send(json.dumps({'cmd': 'chat', 'text': line}))
        except EOFError:
            print('EOF signaled, exiting...')
            break


def responses(msg):
    global flag
    m = msg['text'].lower()
    if m.startswith('what is love') and len(m) < 14 and not flag:
        ws.send(json.dumps({'cmd': 'chat', 'text': 'baby don\'t hurt me..'}))
        flag = True
    elif flag is True and (m == 'don\'t hurt me' or m == 'dont hurt me'):
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
    if ('can' in msg and ('help' in msg or 'ask' in msg)):
        if ('can help' not in msg and 'can\'t help' not in msg and
            'cant help' not in msg and 'won\'t help' not in msg):
            ws.send(json.dumps({'cmd': 'chat',
            'text': 'Don\'t ask to ask, ask your question.'}))

def afk(msg):
    if msg['text'].lower()[:4] == '|afk' and msg['nick'] not in usrstat:
        if len(msg['text'].strip()) > 4:
            usrstat[msg['nick']] = msg['text'][4:].strip()
            ws.send(json.dumps({'cmd': 'chat', 'text': 'User @%s is now **AFK**: %s'
            % (msg['nick'], usrstat[msg['nick']])}))
        else:
            usrstat[msg['nick']] = ''
            ws.send(json.dumps({'cmd': 'chat', 'text': 'User @%s is now **AFK**'
            % (msg['nick'])}))
    elif msg['nick'] not in exceptions and not msg['text'].lower().startswith('|lmsg') and not msg['text'].lower().startswith('|tmsg'):
        for key, val in usrstat.items():
            if '@%s' % (key) in msg['text'] and key != msg['nick']:
                if key != msg['text'].strip() and msg['text'].strip() != '@' + key:
                    usrmsg.setdefault(key,
                    {})[msg['nick']] = msg['text'].replace('@' + key, '', 1)
                if val != '':
                    ws.send(json.dumps({'cmd': 'chat', 'text': '@%s user @%s is **AFK**: %s'
                        % (msg['nick'], key, val)}))
                else:
                    ws.send(json.dumps({'cmd': 'chat', 'text': '@%s user @%s is **AFK**'
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
            if len(n) > 0 and len(m) > 0 and msg['trip'] != com['owntrip']:
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

def leaveTripmsg(msg):
    if msg['cmd'] == 'chat':
        if msg['text'].lower()[:5] == '|tmsg':
            try:
                receiverTrip = msg['text'][5:].strip().split(None, 1)[0]
                senderTrip = msg['trip']
                m = msg['text'][5:].strip().split(None, 1)[1]
                t = time.time()
            except IndexError:
                ws.send(json.dumps({'cmd': 'chat', 'text':
                    'Usage is |tmsg [recipient] [your message]'}))
                return
            if len(receiverTrip) > 0 and len(m) > 0 and receiverTrip != senderTrip and receiverTrip != com['owntrip']:
                    usrtripmsg.setdefault(receiverTrip, {})[senderTrip] = m, t
                    ws.send(json.dumps({'cmd': 'chat', 'text': ('@%s user with the trip *__%s__* will get '
                    'your message the first time he writes something or joins this room.')
                        % (msg['nick'], receiverTrip)}))
            else:
                ws.send(json.dumps({'cmd': 'chat', 'text':
                    'Usage is |tmsg [recipient] [your message]'}))
        for key, val in usrtripmsg.items():
            if key == msg['trip']:
                for k, v in val.items():
                    ws.send(json.dumps({'cmd': 'chat', 'text': '@%s user with the trip *__%s__* '
                    'left you(%s ago): %s'
                        % (msg['nick'], k, prsDrtn(time.time() - v[1]), v[0])}))
                    time.sleep(0.5)
                del usrtripmsg[key]
                break
    elif msg['cmd'] == 'onlineAdd':
        for key, val in usrtripmsg.items():
            if key == msg['trip']:
                for k, v in val.items():
                    ws.send(json.dumps({'cmd': 'chat', 'text': '@%s user with the trip *__%s__* '
                    'left you(%s ago): %s'
                        % (msg['nick'], k, prsDrtn(time.time() - v[1]), v[0])}))
                    time.sleep(0.5)
                del usrtripmsg[key]
                break

def whisplveMsg(msg):
    if (msg['cmd'] == 'info' and msg['type'] == 'whisper'
        and msg['from'] != com['owname'].split('#')[0]
        and msg['trip'] != com['owname'].split('#')[1]):
            if msg['text'].lower().strip().split()[2] == '|lmsg' or msg['text'].lower().strip().split()[2] == 'lmsg':
                try:
                    n = msg['text'].strip().split()[3].replace('@', '', 1)
                    wspPreserv = re.compile('[\S\s]*')
                    ml = wspPreserv.findall(msg['text'])
                    m = ''.join(ml)
                    m = m.split('whispered: ', 1)[1]
                    m = m.strip().split(n, 1)[1]
                    t = time.time()
                except IndexError:
                    ws.send(json.dumps({'cmd': 'chat', 'text':
                        '/r Usage is /whisper @%s |lmsg [recipient] [your message]' % (com['owname'].split('#')[0])}))
                    return
                if len(n) > 0 and len(m) > 0 and msg['trip'] != com['owntrip']:
                    usrwmsg.setdefault(n, {})[msg['from']] = m, t
                    ws.send(json.dumps({'cmd': 'chat', 'text': '/r @%s user @%s will get '
                    'your message whispered the first time he writes something or joins this room.'
                        % (msg['from'], n)}))
                    global wspCnt
                    wspCnt += 1
                    print('Stored private message count: {}'.format(wspCnt))
                else:
                    ws.send(json.dumps({'cmd': 'chat', 'text':
                        '/r Usage is /whisper @%s |lmsg [recipient] [your message]' % (com['owname'].split('#')[0])}))
                    return
            for key, val in usrwmsg.items():
                if key.lower() == msg['from'].lower():
                    for k, v in val.items():
                        ws.send(json.dumps({'cmd': 'chat', 'text': '/whisper @%s user @%s '
                        'left you(%s ago): %s'
                            % (key, k, prsDrtn(time.time() - v[1]), v[0])}))
                        time.sleep(0.5)
                    del usrwmsg[key]
                    wspCnt -= 1
                    print('Stored private message count: {}'.format(wspCnt))
                    break
    elif msg['cmd'] == 'onlineAdd' or msg['cmd'] == 'chat':
        for key, val in usrwmsg.items():
            if key.lower() == msg['nick'].lower():
                for k, v in val.items():
                    ws.send(json.dumps({'cmd': 'chat', 'text': '/whisper @%s user @%s '
                    'left you(%s ago): %s'
                        % (key, k, prsDrtn(time.time() - v[1]), v[0])}))
                    time.sleep(0.5)
                del usrwmsg[key]
                wspCnt -= 1
                print('Stored private message count: {}'.format(wspCnt))
                break

def whspTripMsg(msg):
    if (msg['cmd'] == 'info' and msg['type'] == 'whisper'
        and msg['from'] != com['owname'].split('#')[0]
        and msg['trip'] != com['owntrip']):
            if msg['text'].lower().strip().split()[2] == '|tmsg' or msg['text'].lower().strip().split()[2] == 'tmsg':
                try:
                    receiverTrip = msg['text'].strip().split()[3]
                    senderTrip = msg['trip']
                    wspPreserv = re.compile('[\S\s]*')
                    ml = wspPreserv.findall(msg['text'])
                    m = ''.join(ml)
                    m = m.split('whispered: ', 1)[1]
                    m = m.strip().split(receiverTrip, 1)[1]
                    t = time.time()
                except IndexError:
                    ws.send(json.dumps({'cmd': 'chat', 'text':
                        '/r Usage is /whisper @%s |tmsg [recipient trip] [your message]' % (com['owname'].split('#')[0])}))
                    return
                if len(receiverTrip) == 6 and len(m) > 0 and receiverTrip != senderTrip and receiverTrip != com['owntrip']:
                    usrwsptmsg.setdefault(receiverTrip, {})[senderTrip] = m, t
                    ws.send(json.dumps({'cmd': 'chat', 'text': '/r user with the trip *__%s__* will get '
                    'your message whispered the first time he writes something or joins this room.'
                        % (receiverTrip)}))
                    global wspCnt
                    wspCnt += 1
                    print('Stored private message count: {}'.format(wspCnt))
                else:
                    ws.send(json.dumps({'cmd': 'chat', 'text':
                        '/r Usage is /w @%s |tmsg [recipient trip] [your message]' % (com['owname'].split('#')[0])}))
                if msg['trip'] in usrwsptmsg.keys():
                    for key, val in usrwsptmsg.items():
                        if key == msg['trip']:
                            for k, v in val.items():
                                ws.send(json.dumps({'cmd': 'chat', 'text': '/r @%s user with the trip *__%s__* '
                                'left you(%s ago): %s'
                                    % (msg['from'], k, prsDrtn(time.time() - v[1]), v[0])}))
                                time.sleep(0.5)
                            del usrwsptmsg[key]
                            wspCnt -= 1
                            print('Stored private message count: {}'.format(wspCnt))
                            break
            elif msg['trip'] in usrwsptmsg.keys():
                    for key, val in usrwsptmsg.items():
                        if key == msg['trip']:
                            for k, v in val.items():
                                ws.send(json.dumps({'cmd': 'chat', 'text': '/r @%s user with the trip *__%s__* '
                                'left you(%s ago): %s'
                                    % (msg['from'], k, prsDrtn(time.time() - v[1]), v[0])}))
                                time.sleep(0.5)
                            del usrwsptmsg[key]
                            wspCnt -= 1
                            print('Stored private message count: {}'.format(wspCnt))
                            break

    elif msg['cmd'] == 'onlineAdd' or msg['cmd'] == 'chat':
        for key, val in usrwsptmsg.items():
            if key == msg['trip']:
                for k, v in val.items():
                    ws.send(json.dumps({'cmd': 'chat', 'text': '/whisper @%s user with the trip *__%s__* '
                    'left you(%s ago): %s'
                        % (msg['nick'], k, prsDrtn(time.time() - v[1]), v[0])}))
                    time.sleep(0.5)
                del usrwsptmsg[key]
                wspCnt -= 1
                print('Stored private message count: {}'.format(wspCnt))
                break


def renderImgur(msg):
    if msg['cmd'] == 'chat':
        content_regx = re.compile(r'<meta name=\"twitter:image\".+?content=\"(.*?)\">') # Extract imgur source link
        imageBody = []
        valid_urls = ["https://imgur.io/", "https://imgur.com/"]
        for word in msg['text'].split():
            if [url for url in valid_urls if word.startswith(url)]:
                purl = urllib.request.urlopen(word.split(' ')[0])
                urlbytes = purl.read()
                urlstr = urlbytes.decode('utf8')
                purl.close()
                imageBody.append(urlstr)
        for ib in imageBody:
            imageUrl = str(content_regx.findall(ib)[0])
            ws.send(json.dumps({'cmd': 'chat', 'text': '![]({})'.format(imageUrl)})) # Use markdown image syntax implemented in the client to render the image inside text
            time.sleep(0.2)


def on_message(ws, message):
    message = json.loads(message)
    for i in message:
        unicodedata.normalize('NFKD', i).encode('ascii', 'ignore').decode('utf8')
        #print (i, message[i])
    cmndBlk(message)
    leaveMsg(message)
    whisplveMsg(message)
    leaveTripmsg(message)
    whspTripMsg(message)
    renderImgur(message)
 
def on_error(ws, error):
    if f'{error}' == "'type'": # otherwise prints 'type' on join
        pass
    elif f'{error}' == "'trip'": # stop multiple 'trip' prints on |tmsg
        pass
    else:
        print(error)

def on_close(ws):
    print('Private message count: {}'.format(wspCnt))
    print('### closed ###')

def on_open(ws):
    ws.send(json.dumps({'cmd': 'join', 'channel': 'programming', 'nick': com['owname']}))
    ws.send(json.dumps({'cmd': 'chat', 'text':'/color #007fff'}))
    global joined
    joined = time.time()
    _thread.start_new_thread(out, ())


if __name__ == '__main__':
    ws = websocket.WebSocketApp('wss://hack.chat/chat-ws',
                                 on_open = on_open,
                                 on_message = on_message,
                                 on_error = on_error,
                                 on_close = on_close,
                               )
    ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})

