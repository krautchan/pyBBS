'''
Created on Jul 17, 2012

@author: teddydestodes
'''
import os, re
from struct import unpack

class TermInfo(object):
    
    numre = re.compile('^%(?P<mod>(:-)|[+#])?(?P<len>[0-9]*?(.[0-9]))?(?P<type>[doxXs])')
    pushre = re.compile('^%p(?P<pn>[1-9])')
    ire = re.compile('^%\{(?P<val>[0-9]{1,2})\}')
    cre = re.compile('^%\'(?P<val>{.+?\})\'')
    boolcaps = ('bw',
                'am',
                'xsb',
                'xhp',
                'xenl',
                'eo',
                'gn',
                'hc',
                'km',
                'hs',
                'in',
                'da',
                'db',
                'mir',
                'msgr',
                'os',
                'eslok',
                'xt',
                'hz',
                'ul',
                'xon',
                'nxon',
                'mc5i',
                'chts',
                'nrrmc',
                'npc',
                'ndscr',
                'ccc',
                'bce',
                'hls',
                'xhpa',
                'crxm',
                'daisy',
                'xvpa',
                'sam',
                'cpix',
                'lpix',
                'OTbs',
                'OTns',
                'OTnc',
                'OTMT',
                'OTNL',
                'OTpt',
                'OTxr')
    numcaps  = ('cols',
                'it',
                'lines',
                'lm',
                'xmc',
                'pb',
                'vt',
                'wsl',
                'nlab',
                'lh',
                'lw',
                'ma',
                'wnum',
                'colors',
                'pairs',
                'ncv',
                'bufsz',
                'spinv',
                'spinh',
                'maddr',
                'mjump',
                'mcs',
                'mls',
                'npins',
                'orc',
                'orl',
                'orhi',
                'orvi',
                'cps',
                'widcs',
                'btns',
                'bitwin',
                'bitype',
                'OTug',
                'OTdC',
                'OTdN',
                'OTdB',
                'OTdT',
                'OTkn',)
    
    strcaps  = ('cbt',
                'bel',
                'cr',
                'csr',
                'tbc',
                'clear',
                'el',
                'ed',
                'hpa',
                'cmdch',
                'cup',
                'cud1',
                'home',
                'civis',
                'cub1',
                'mrcup',
                'cnorm',
                'cuf1',
                'll',
                'cuu1',
                'cvvis',
                'dch1',
                'dl1',
                'dsl',
                'hd',
                'smacs',
                'blink',
                'bold',
                'smcup',
                'smdc',
                'dim',
                'smir',
                'invis',
                'prot',
                'rev',
                'smso',
                'smul',
                'ech',
                'rmacs',
                'sgr0',
                'rmcup',
                'rmdc',
                'rmir',
                'rmso',
                'rmul',
                'flash',
                'ff',
                'fsl',
                'is1',
                'is2',
                'is3',
                'if',
                'ich1',
                'il1',
                'ip',
                'kbs',
                'ktbc',
                'kclr',
                'kctab',
                'kdch1',
                'kdl1',
                'kcud1',
                'krmir',
                'kel',
                'ked',
                'kf0',
                'kf1',
                'kf10',
                'kf2',
                'kf3',
                'kf4',
                'kf5',
                'kf6',
                'kf7',
                'kf8',
                'kf9',
                'khome',
                'kich1',
                'kil1',
                'kcub1',
                'kll',
                'knp',
                'kpp',
                'kcuf1',
                'kind',
                'kri',
                'khts',
                'kcuu1',
                'rmkx',
                'smkx',
                'lf0',
                'lf1',
                'lf10',
                'lf2',
                'lf3',
                'lf4',
                'lf5',
                'lf6',
                'lf7',
                'lf8',
                'lf9',
                'rmm',
                'smm',
                'nel',
                'pad',
                'dch',
                'dl',
                'cud',
                'ich',
                'indn',
                'il',
                'cub',
                'cuf',
                'rin',
                'cuu',
                'pfkey',
                'pfloc',
                'pfx',
                'mc0',
                'mc4',
                'mc5',
                'rep',
                'rs1',
                'rs2',
                'rs3',
                'rf',
                'rc',
                'vpa',
                'sc',
                'ind',
                'ri',
                'sgr',
                'hts',
                'wind',
                'ht',
                'tsl',
                'uc',
                'hu',
                'iprog',
                'ka1',
                'ka3',
                'kb2',
                'kc1',
                'kc3',
                'mc5p',
                'rmp',
                'acsc',
                'pln',
                'kcbt',
                'smxon',
                'rmxon',
                'smam',
                'rmam',
                'xonc',
                'xoffc',
                'enacs',
                'smln',
                'rmln',
                'kbeg',
                'kcan',
                'kclo',
                'kcmd',
                'kcpy',
                'kcrt',
                'kend',
                'kent',
                'kext',
                'kfnd',
                'khlp',
                'kmrk',
                'kmsg',
                'kmov',
                'knxt',
                'kopn',
                'kopt',
                'kprv',
                'kprt',
                'krdo',
                'kref',
                'krfr',
                'krpl',
                'krst',
                'kres',
                'ksav',
                'kspd',
                'kund',
                'kBEG',
                'kCAN',
                'kCMD',
                'kCPY',
                'kCRT',
                'kDC',
                'kDL',
                'kslt',
                'kEND',
                'kEOL',
                'kEXT',
                'kFND',
                'kHLP',
                'kHOM',
                'kIC',
                'kLFT',
                'kMSG',
                'kMOV',
                'kNXT',
                'kOPT',
                'kPRV',
                'kPRT',
                'kRDO',
                'kRPL',
                'kRIT',
                'kRES',
                'kSAV',
                'kSPD',
                'kUND',
                'rfi',
                'kf11',
                'kf12',
                'kf13',
                'kf14',
                'kf15',
                'kf16',
                'kf17',
                'kf18',
                'kf19',
                'kf20',
                'kf21',
                'kf22',
                'kf23',
                'kf24',
                'kf25',
                'kf26',
                'kf27',
                'kf28',
                'kf29',
                'kf30',
                'kf31',
                'kf32',
                'kf33',
                'kf34',
                'kf35',
                'kf36',
                'kf37',
                'kf38',
                'kf39',
                'kf40',
                'kf41',
                'kf42',
                'kf43',
                'kf44',
                'kf45',
                'kf46',
                'kf47',
                'kf48',
                'kf49',
                'kf50',
                'kf51',
                'kf52',
                'kf53',
                'kf54',
                'kf55',
                'kf56',
                'kf57',
                'kf58',
                'kf59',
                'kf60',
                'kf61',
                'kf62',
                'kf63',
                'el1',
                'mgc',
                'smgl',
                'smgr',
                'fln',
                'sclk',
                'dclk',
                'rmclk',
                'cwin',
                'wingo',
                'hup',
                'dial',
                'qdial',
                'tone',
                'pulse',
                'hook',
                'pause',
                'wait',
                'u0',
                'u1',
                'u2',
                'u3',
                'u4',
                'u5',
                'u6',
                'u7',
                'u8',
                'u9',
                'op',
                'oc',
                'initc',
                'initp',
                'scp',
                'setf',
                'setb',
                'cpi',
                'lpi',
                'chr',
                'cvr',
                'defc',
                'swidm',
                'sdrfq',
                'sitm',
                'slm',
                'smicm',
                'snlq',
                'snrmq',
                'sshm',
                'ssubm',
                'ssupm',
                'sum',
                'rwidm',
                'ritm',
                'rlm',
                'rmicm',
                'rshm',
                'rsubm',
                'rsupm',
                'rum',
                'mhpa',
                'mcud1',
                'mcub1',
                'mcuf1',
                'mvpa',
                'mcuu1',
                'porder',
                'mcud',
                'mcub',
                'mcuf',
                'mcuu',
                'scs',
                'smgb',
                'smgbp',
                'smglp',
                'smgrp',
                'smgt',
                'smgtp',
                'sbim',
                'scsd',
                'rbim',
                'rcsd',
                'subcs',
                'supcs',
                'docr',
                'zerom',
                'csnm',
                'kmous',
                'minfo',
                'reqmp',
                'getm',
                'setaf',
                'setab',
                'pfxl',
                'devt',
                'csin',
                's0ds',
                's1ds',
                's2ds',
                's3ds',
                'smglr',
                'smgtb',
                'birep',
                'binel',
                'bicr',
                'colornm',
                'defbi',
                'endbi',
                'setcolor',
                'slines',
                'dispc',
                'smpch',
                'rmpch',
                'smsc',
                'rmsc',
                'pctrm',
                'scesc',
                'scesa',
                'ehhlm',
                'elhlm',
                'elohlm',
                'erhlm',
                'ethlm',
                'evhlm',
                'sgr1',
                'slength',
                'OTi2',
                'OTrs',
                'OTnl',
                'OTbc',
                'OTko',
                'OTma',
                'OTG2',
                'OTG3',
                'OTG1',
                'OTG4',
                'OTGR',
                'OTGL',
                'OTGU',
                'OTGD',
                'OTGH',
                'OTGV',
                'OTGC',
                'meml',
                'memu',
                'box1')

    def __init__(self, term):
        term = term.lower()
        self.term = term
        self.boolvals = []
        self.numvals = []
        self.strvals = []
        if os.path.exists(os.path.join('/','lib','terminfo',term[0],term)):
            self.loadTermInfo()
        else:
            print '@todo'
            
    
    def tigets(self,cap,*args):
        str = self._getStrCap(cap);
        if str == None:
            return ''
        buf = ''
        arglst = []
        stack = []
        sp = 0
        level = 0
        clevel = 0
        skip = False
        while sp < len(str) and str[sp]:
            # print str[sp:]
            # print level, clevel, skip, buf
            if skip != False :
                if str[sp:sp+2] == '%?':
                    clevel += 1
                    sp += 2
                elif str[sp:sp+2] == '%;':
                    if clevel == level and skip == ';':
                        skip = False
                    else:
                        clevel -= 1
                    sp += 2
                elif str[sp:sp+2] == '%e':
                    if clevel == level and skip == 'e':
                        
                        skip = False
                    sp += 2
                else:
                    sp += 1
                continue

            if str[sp] != '%':
                buf += str[sp]
                sp +=1
            else:
                if str[sp+1] == '%':
                    buf += '%'
                    sp += 2
                if str[sp+1] == '?':
                    if skip == False:
                        level += 1
                    sp += 2
                if str[sp+1] == ';':
                    level -= 1
                    sp += 2
                    continue
                if str[sp+1] == 't':
                    v = stack.pop()
                    if v:
                        sp += 2
                    else:
                        skip = 'e' #skip to else
                        clevel = level
                        sp += 2
                        continue
                if str[sp+1] == 'e':
                    skip = ';' #skip to end of if
                    clevel = level
                    sp += 2
                    continue
                if str[sp+1] == 'c':
                    buf.append(str[sp:sp+2])
                    arglst.append(stack.pop())
                    sp += 2
                if str[sp+1] == 's':
                    buf.append(str[sp:sp+2])
                    arglst.append(stack.pop())
                    sp += 2
                if str[sp+1] in ('+','-','*','/','m'):
                    stack.append(self._arithmeticOp(str[sp+1], stack.pop(), stack.pop()))
                    sp += 2
                if str[sp+1] in ('&','|','^'):
                    stack.append(self._bitOp(str[sp+1], stack.pop(), stack.pop()))
                    sp += 2
                if str[sp+1] in ('=','<','>'):
                    stack.append(self._logicalOp(str[sp+1], stack.pop(), stack.pop()))
                    sp += 2
                if str[sp+1] == 'i':
                    args[0] += 1
                    args[1] += 1
                    sp += 2
                m = re.match(self.numre,str[sp:])
                if m:
                    if m.group('len') == None:
                        buf += '{%d:%s}' % (len(arglst),m.group('type'))
                    else:
                        buf += '{%d:%s%s}' % (len(arglst),m.group('len'),m.group('type'))
                    arglst.append(stack.pop())
                    sp += len(m.group())
                m = re.match(self.pushre,str[sp:])
                if m:
                    stack.append(args[int(m.group('pn'))-1])
                    sp += len(m.group())
                m = re.match(self.ire,str[sp:])
                if m:
                    stack.append(int(m.group('val')))
                    sp += len(m.group())
                m = re.match(self.cre,str[sp:])
                if m:
                    stack.append(m.group('val'))
                    sp += len(m.group())
        return buf.format(*arglst)
    
    def _logicalOp(self, op, parm2, parm1):
        if op == '=':
            return parm1 == parm2
        if op == '>':
            return parm1 > parm2
        if op == '<':
            return parm1 < parm2
    
    def _bitOp(self, op, parm2, parm1):
        if op == '&':
            return parm1 & parm2
        if op == '|':
            return parm1 | parm2
        if op == '^':
            return parm1 ^ parm2
    
    def _arithmeticOp(self, op, parm2, parm1):
        if op == '+':
            return parm1 + parm2
        if op == '-':
            return parm1 - parm2
        if op == '*':
            return parm1 * parm2
        if op == '/':
            return parm1 / parm2
        if op == 'm':
            return parm1 % parm2
    
    def tigeti(self,capname):
        return int(self._getNumCap(capname));
    
    def dump(self):
        for cap in self.boolcaps:
            if self.boolcaps.index(cap) < len(self.boolvals):
                print cap, self.boolvals[self.boolcaps.index(cap)]
            else:
                break
        for cap in self.numcaps:
            if self.numcaps.index(cap) < len(self.numvals):
                print cap, self.numvals[self.numcaps.index(cap)]
            else:
                break
        for cap in self.strcaps:
            if self.strcaps.index(cap) < len(self.strvals):
                print cap, self.strvals[self.strcaps.index(cap)]
            else:
                break
    
    def initTerm(self):
        return self.tigets('is1')+self.tigets('is2')
    
    def _getStrCap(self, cap):
        if self.strcaps.index(cap) < len(self.strvals):
            return self.strvals[self.strcaps.index(cap)]
        else:
            return None
    
    def _getNumCap(self, cap):
        try:
            if self.numcaps.index(cap) < len(self.numvals):
                return self.numvals[self.numcaps.index(cap)]
            else:
                return None
        except ValueError:
            return None
    
    def _getCap(self, cap):
        try:
            if self.caps.index(cap):
                return self.capvals[self.caps.index(cap)]
        except ValueError:
            return False
    
    def loadTermInfo(self):
        ti = open(os.path.join('/','lib','terminfo',self.term[0],self.term))
        (mn, snam, sboo, snum, soff, sstab) = unpack('HHHHHH',ti.read(12))
        if mn != 282:
            ti.close()
            return False
        self.name = ti.read(snam-1)
        ti.read(1) #we dont need that NULL
        for c in ti.read(sboo):
            if ord(c) == 0:
                self.boolvals.append(False)
            if ord(c) == 1:
                self.boolvals.append(True)
        
        if (mn+snam+sboo) % 2 == 1:
            ti.read(1)
        for i in range(0,snum):
            val = unpack('H',ti.read(2))[0]
            if val == 65535:
                self.numvals.append(None)
            else:
                self.numvals.append(val)
        off = []
        for i in range(0,soff):
            val = unpack('H',ti.read(2))[0]
            if val == 65535:
                self.strvals.append(None)
            else:
                ind = len(self.strvals)
                off.append((val,ind))
                self.strvals.append('')
        for offset, capindex in off:
            c = ' '
            while ord(c) != 0:
                c = ti.read(1)
                if ord(c) == 0:
                    break
                self.strvals[capindex] += c
        ti.close()
        
#ti = TermInfo('xterm')

#ti.dump()