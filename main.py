import ctypes

t00 = [ 0x8, 0x1, 0x7, 0xD, 0x6, 0xF, 0x3, 0x2, 0x0, 0xB, 0x5, 0x9, 0xE, 0xC, 0xA, 0x4];
t01 = [ 0xE, 0xC, 0xB, 0x8, 0x1, 0x2, 0x3, 0x5, 0xF, 0x4, 0xA, 0x6, 0x7, 0x0, 0x9, 0xD];
t02 = [ 0xB, 0xA, 0x5, 0xE, 0x6, 0xD, 0x9, 0x0, 0xC, 0x8, 0xF, 0x3, 0x2, 0x4, 0x7, 0x1];
t03 = [ 0xD, 0x7, 0xF, 0x4, 0x1, 0x2, 0x6, 0xE, 0x9, 0xB, 0x3, 0x0, 0x8, 0x5, 0xC, 0xA];
t10 = [ 0x2, 0x8, 0xB, 0xD, 0xF, 0x7, 0x6, 0xE, 0x3, 0x1, 0x9, 0x4, 0x0, 0xA, 0xC, 0x5];
t11 = [ 0x1, 0xE, 0x2, 0xB, 0x4, 0xC, 0x3, 0x7, 0x6, 0xD, 0xA, 0x5, 0xF, 0x9, 0x0, 0x8];
t12 = [ 0x4, 0xC, 0x7, 0x5, 0x1, 0x6, 0x9, 0xA, 0x0, 0xE, 0xD, 0x8, 0x2, 0xB, 0x3, 0xF];
t13 = [ 0xB, 0x9, 0x5, 0x1, 0xC, 0x3, 0xD, 0xE, 0x6, 0x4, 0x7, 0xF, 0x2, 0x0, 0x8, 0xA];

MDS = [
        [0x01, 0xEF, 0x5B, 0x5B],
        [0x5B, 0xEF, 0xEF, 0x01],
        [0xEF, 0x5B, 0x01, 0xEF],
        [0xEF, 0x01, 0xEF, 0x5B],
      ]

WRITE = 0;
FILE = 1;


def _byte_256(intValue):
    _b = bin(intValue)[-8:];
    if _b[0] == 'b':
        _b = bin(intValue)[-10:];
        if  _b[0] == '-':
            return(_byte_limit(int(bin(intValue)[-10:], 2)))
        else: 
            return(_byte_limit(int(bin(intValue)[-9:],2)))
    _b = bin(intValue)[-9:];
    if _b[0] == '-':
        return(_byte_limit(int(bin(intValue)[-9:], 2)))
    return(_byte_limit(int(bin(intValue)[-8:], 2)))
    
def _byte_limit_256(num):
    mask = (1 << 8) - 1
    little = num & mask
    if(little > 127):
        return (-1)*(255 + 1 - little)
    if little < -127:
        return (255 + 1 + little)
    return little

class Galua:
    def __init__(self,mask):
        self.mask = mask


    
    def add(self,a, b):
        _b = _byte_256(a^b);
        return _byte_limit_256(_b)

    def multiply(self,a, b):
        p = 0
        for i in range(8):
            if((b&1) != 0):
                p ^= a
                p = _byte_limit_256(p)
            carry = _byte_256(a & 0x80)
            a<<=1
            a = _byte_limit_256(a)

            if(carry != 0):
                a ^= self.mask
                
            b >>= 1
            if(b > 127):
                b = (-1)*(255 + 1 - b)
            

        return p


def _byte_limit(_b):
    _bin = bin(_b);
    _bin_size = len(_bin) -2 
    _n = _bin
    _n = _n.replace('0','1');
    _n = _n.replace('1b','0b'); 
    _n = int(_n, 2);
    if (_bin_size % 8) == 0 and _bin[2] == '1':
        if _b > 0:
            return((-1)*(_n + 1 - _b))
        else:
            return((_n + 1 + _b))
    return _b
    mask = (1 << 8) - 1
    little = num & mask
    if(little > 127):
        return (-1)*(255 + 1 - little)
    if little < -127:
        return (255 + 1 + little)
    return little

def _getByte(num):
    mask = (1 << 8) - 1
    little = num & mask
    if(little > 127):
        return (-1)*(255 + 1 - little)
    if little < -127:
        return (255 + 1 + little)
    return little

_RS = [
        [_getByte(0x01), _getByte(0xA4), _getByte(0x55), _getByte(0x87), _getByte(0x5A), _getByte(0x58), _getByte(0xDB), _getByte(0x9E)],
        [_getByte(0xA4), _getByte(0x56), _getByte(0x82), _getByte(0xF3), _getByte(0x1E), _getByte(0xC6), _getByte(0x68), _getByte(0xE5)],
        [_getByte(0x02), _getByte(0xA1), _getByte(0xFC), _getByte(0xC1), _getByte(0x47), _getByte(0xAE), _getByte(0x3D), _getByte(0x19)],
        [_getByte(0xA4), _getByte(0x55), _getByte(0x87), _getByte(0x5A), _getByte(0x58), _getByte(0xDB), _getByte(0x9E), _getByte(0x03)],
     ]



def encrypt(plainText, key, debug):
    roundKey01 = roundKeys(key,0);
    roundKey23 = roundKeys(key,1);
    roundKey45 = roundKeys(key,2);
    roundKey67 = roundKeys(key,3);
    whitened = whitening(plainText, roundKey01[0], roundKey01[1], roundKey23[0], roundKey23[1]);
    for i in range(16):
        #print("whitened : [",i,']',whitened)
        whitened = encryptionRound(whitened, key, i)
        whitened = [whitened[2], whitened[3], whitened[0], whitened[1]]

    whitened = [whitened[2], whitened[3], whitened[0], whitened[1]];
    whitened = whitening(whitened, roundKey45[0], roundKey45[1], roundKey67[0], roundKey67[1])
    return whitened;

def decrypt(cypheredText, key, debug):
    roundKey01 = roundKeys(key,0);
    roundKey23 = roundKeys(key,1);
    roundKey45 = roundKeys(key,2);
    roundKey67 = roundKeys(key,3);

    whitened = whitening(cypheredText, roundKey45[0], roundKey45[1], roundKey67[0], roundKey67[1])

    whitened = [whitened[2], whitened[3], whitened[0], whitened[1]]

    for i in range(15, -1, -1):
        #print('Whitened [',i,'] : ',whitened);
        whitened = deryptionRound(whitened, key, i)
        whitened = [whitened[2], whitened[3], whitened[0], whitened[1]]

    whitened = whitening(whitened, roundKey01[0], roundKey01[1], roundKey23[0], roundKey23[1])
    return whitened;

def deryptionRound(input, key, round):
    s = getS(key)
    t0 = h(input[2],s[1], s[0])
    t1 = h(shiftLeft_32(input[3], 8),s[1],s[0])
    pPht = pht(t0,t1)
    _roundKeys = roundKeys(key, round + 4);
    f0 = _32bit_ops(pPht[0] + _roundKeys[0]);
    f1 = _32bit_ops(pPht[1] + _roundKeys[1]);

    p2 = shiftLeft_32(input[0], 1) ^ f0;# ito yung mali
    p3 = shiftRight_32((input[1] ^ f1), 1)
    '''
    print(" Round: ", round);
    print("s: ",  s)
    print("t0: ",  t0 , " PARAMS: ",input[2],s[1], s[0])
    print("t1: ",  t1)
    print("pPht: ",  pPht)
    print("_roundKeys: ",  _roundKeys)
    print("f0: ",  f0)
    print("f1: ",  f1)
    print("p2: ",  p2, " PARAMS: ",input[0])
    print("p3: ",  p3)
    print("=============================")
    '''

    return [p2, p3, input[2], input[3]]

def encryptionRound(input, key, round):
    #print("key: ", key)
    s = getS(key)
    t0 = h(input[0], s[1], s[0])
    t1 = h(shiftLeft_32(input[1],8),s[1],s[0])
    pPht = pht(t0,t1)
    roundKeys2r_8_2r_9 = roundKeys(key,round+4)
    f0 = _32bit_ops(pPht[0] + roundKeys2r_8_2r_9[0]);
    f1 = _32bit_ops(pPht[1] + roundKeys2r_8_2r_9[1]);
    c2 = shiftRight_32((f0 ^ input[2]), 1); # ito yung mali
    c3 = _32bit_ops((f1 ^ shiftLeft_32(input[3], 1)));
    '''
    print(" Round: ", round);
    print("s: ",  s)
    print("t0: ",  t0)
    print("t0: ",  t0 , " PARAMS: ",input[0], s[1], s[0])
    print("pPht: ",  pPht)
    print("roundKeys2r_8_2r_9: ",  roundKeys2r_8_2r_9)
    print("f0: ",  f0)
    print("f1: ",  f1)
    print("c2: ",  c2, " PARAMS: ",(f0 ^ input[2]) ," [ ", f0 ," ," , input[2])
    print("c3: ",  c3)
    print("=============================")
    '''

    return [input[0], input[1], c2, c3 ]

def getS(key):
    m0 = key[0]
    m1 = key[1]
    m2 = key[2]
    m3 = key[3]
    S0 = RS(m0,m1)
    S1 = RS(m2,m3)
    #print("S0: ", S0)
    #print("S1: ", S1)
    return([S0,S1])

def RS(X,Y):
    x = _asBytes(X)
    y = _asBytes(Y)
    XY = x + y
    matrix = _RS;
    galua = Galua(0b01001101);
    S = multiply(galua, matrix , XY)
    return fromBytes(S)

def whitening(plainText, k0, k1, k2, k3):
    #print(plainText[2] ^ k2," sasakyan");
    return([
            _32bit_ops(plainText[0] ^ k0),
            _32bit_ops(plainText[1] ^ k1),
            _32bit_ops(plainText[2] ^ k2),
            _32bit_ops(plainText[3] ^ k3),
        ])


def _32bit_ops(ops):
    a=ctypes.c_int32(ops)
    return a.value

def multiply(galua,matrix, vector):
    S = [0]*len(vector)
    for i in range(len(matrix)):
        RSrow = matrix[i]
        S[i] = galua.multiply(RSrow[0],vector[0])
        #print(S[i] , " RSrow[0]: ",RSrow[0], " vector[0]:", vector[0] , "  KABOG [i] : " , i );
        for j in range(1, len(RSrow)):
            S[i] = galua.add(S[i], galua.multiply(RSrow[j], vector[j]))

    return S

def fromBytes(intVal):
    S0 = 0;
    for i in range(4):
        S0 |= ((0xFF & intVal[i]) << (i * 8))
    return _byte_limit(S0);

def q0(intValue):
    a0 = _getByte((intValue >> 4) & 0xF)
    b0 = _getByte(intValue & 0xF)
    a1 = _getByte(a0 ^ b0)
    b1 = _getByte(a0 ^ ((b0 & 1) << 3 | b0 >> 1) ^ ((8*a0) & 0xF))
    a2 = t00[a1];
    b2 = t01[b1];
    a3 = _getByte(a2 ^ b2)
    b3 = _getByte(a2 ^ ((b2 & 1) << 3 | b2 >> 1) ^ ((8*a2) & 0xF))
    a4 = t02[a3]
    b4 = t03[b3]
    result = _getByte( (b4<<4) | a4 );
    return result;

def q1(intValue):
    a0 = _getByte((intValue >> 4) & 0xF)
    b0 = _getByte(intValue & 0xF)
    a1 = _getByte(a0 ^ b0)
    b1 = _getByte(a0 ^ ((b0 & 1) << 3 | b0 >> 1) ^ ((8*a0) & 0xF))
    a2 = t10[a1];
    b2 = t11[b1];
    a3 = _getByte(a2 ^ b2)
    b3 = _getByte(a2 ^ ((b2 & 1) << 3 | b2 >> 1) ^ ((8*a2) & 0xF))
    a4 = t12[a3]
    b4 = t13[b3]
    result = _getByte( (b4<<4) | a4 ) ;
    return result;

def _asBytes(intValue):
    return([_getByte(intValue),
            _getByte(intValue >> 8),
            _getByte(intValue >> 16),
            _getByte(intValue >> 24),
            ])

def h(input, l1, l2):
    galua = Galua(0b01101001);
    x = _asBytes(input)
    y = _asBytes(l2)
    z = _asBytes(l1)
   # print(_byte( q0(x[0]) ^ y[0]) , ' Input : ' , input, ' q1( _byte( q0(x[2]) ^ y[2]) ) ^ z[2] :',q1( _byte( q0(x[2]) ^ y[2]) ) ^z[2], " x[2]: ", x[2])
    result = [
        q1(_getByte(q0( _getByte( q0(x[0]) ^ y[0]) ) ^z[0])),
        q0(_getByte(q0( _getByte( q1(x[1]) ^ y[1]) ) ^z[1])),
        q1(_getByte(q1( _getByte( q0(x[2]) ^ y[2]) ) ^z[2])),
        q0(_getByte(q1( _getByte( q1(x[3]) ^ y[3]) ) ^z[3])),
    ]
    #print(" Resulttt : ", fromBytes(multiply(galua, MDS, result)))
    #print(" Resulttt : ",multiply(galua, MDS, result))
    return fromBytes(multiply(galua, MDS, result))



def _limiter(num,distance):
    _b = "{0:b}".format(num)
    _b = _negative_twos_complement(num)
    _b_length = len(_b);
    if(_b_length < 25+(8-distance)): # 25 -8 = 1
        return 0;
    _to_get = _b_length - 24 - (8-distance);

    _b = _b[0:_to_get];
    return int(_b,2)

def shiftLeft_32(val, distance):
    return (_32bit_ops(val << distance) | _limiter(val, distance) )

def _latest_1s(_b):
    for i in range(len(_b)):
        if _b[-i] == '1':
            if -i == 0 : 
                return -1
            else :
                return -i
    return -1;

def _negative_twos_complement(num):
    _b = "{0:b}".format(num)
    if(num < 0):
        _b = _b[1:]
        x = len(_b);
        y = 16

        if y < x :
            temp = x/y
            if temp != 0.0:
                temp = int(temp) + 1
            temp = int(temp);
            y *= temp

        _add = (y-x);
        _b = ('0'*_add+"{0:b}".format(num*-1))

        _l = _latest_1s(_b)
        _b = _b[0:_l].replace('0','3').replace('1','0').replace('3','1')

        _b = _b +'1'+ '0'*(-_l-1)
    return _b


def shiftRight_32(num, distance):
    _r = -2147483648;
    if (num % 2 == 0):
        _r = 0;
    if(num < 0):
        return (int(int(_negative_twos_complement(num),2)/2) | _r)
    return (_32bit_ops(num >> distance) | _r)

def pht(a, b):
    a1 = _32bit_ops(a+b)
    b1 = _32bit_ops(a+2*b)
    return [ a1, b1]

def roundKeys(key,round):
    m0 = key[0];
    m1 = key[1];
    m2 = key[2];
    m3 = key[3];

    Me = [m0, m2]
    Mo = [m1, m3]
    rho = (1 << 24) | (1 << 16) | (1 << 8) | 1;
    Ai = h(2 * round * rho, Me[0], Me[1]);
    Bi = shiftLeft_32(h((2 * round + 1) * rho, Mo[0], Mo[1]), 8)
    pPht = pht(Ai, Bi)
    K2i = pPht[0]
    K2i_1 = shiftLeft_32(pPht[1], 9)
    return([K2i, K2i_1])


def convertInput(input, offset):
    result = [0]*4
    for i in range(4):
        temp = 0
        for j in range(4):
            index = 4 * i + j + offset
            if(index >= len(input)):
                temp |= 0   
            else:
                temp |= ((0xFF & input[index]) << (8 * j))
        result[i] = temp 
    return result

def _get_string_bytes(plainText):
    arr = bytes(plainText, 'ascii')
    result = []
    for byte in arr:
        result.append(byte)
    return result

#main()

def _int_to_char(int):
    stop = 0
    result = ''
    for i in range(4):
        _b = _asBytes(int[i])
        for x in range(len(_b)):
            _h = (hex((_getByte(_b[x])) & 0xff)[2:]);
            if _h == '0':
                stop+=1
            if stop == 2 : return result
            if len(_h) == 1 : _h = '0'+_h
            #print(_h)
            result += _h
    return result

def Chevy(plainText, key):
    plainText = _get_string_bytes(plainText);
    p = [0]*4
    p = convertInput(plainText,0)
    #print(_int_to_char(encrypt(p,key,False)))
    #print(encrypt(p,key,False), " Toyo")
    #print(encrypt(p,key,False),  " Wazap")
    return _int_to_char(encrypt(p,key,False));

def _message_to_int(message):
    result = [0]*4
    try :
        for i in range(4):
            temp = [0]*4
            end = 8 * (i+1) - 1;
            _b = ''
            for j in range(4):
                first = end - (j*2)
                _b += message[first-1] + message[first]
                #print("message : ", message, " first : ", first)
            result[i] = _32bit_ops(int(_b,16));
    except:
        print("Not decryptable!")
    return result

def Chevy_Decrypt(encrypted_text, key):
    p = _message_to_int(encrypted_text)
    return _int_to_char(decrypt(p,key,False));

def Camry(plainText):
    result = []
    _l = len(plainText)/16
    if (_l % 1) != 0.0: _l= _l+1
    _l = int(_l)
    temp = 0
    for i in range(_l):
        end = temp + 16
        if end > _l:
            end = temp + ( _l - temp)

        end = temp + 16 
        result.append(plainText[temp: end])
        temp += 16
    return result

def Camry_32(plainText):
    result = []
    _l = len(plainText)/32
    if (_l % 1) != 0.0: _l= _l+1
    _l = int(_l)
    temp = 0
    for i in range(_l):
        end = temp + 32
        if end > _l:
            end = temp + ( _l - temp)

        end = temp + 32
        result.append(plainText[temp: end])
        temp += 32
    return result

def _TwoFish_Encrypt(plainText, key, stat, dir):
    
    key = _get_string_bytes(key);
    k = [0]*4
    k = convertInput(key,0)
    plainText = Camry(plainText)
    #print(plainText)
    
    #print("plainText : ", plainText)
    encrypted_text = []
    for i in range(len(plainText)):
        encrypted_text.append(Chevy(plainText[i],k))

    _enc_result = ''.join(encrypted_text);
    print()
    print("Encrypted Text : ",_enc_result)
    print()
    if stat == FILE:
        print(" I will now encrypt the file : ", dir)
        f = open(dir,'w')
        f.write(_enc_result)
        print("Successfull! check the file now")


def _TwoFish_Decrypt(encryptedText, key, stat, dir):
    key = _get_string_bytes(key);
    k = [0]*4
    k = convertInput(key,0)
    _array_encryptedText = Camry_32(encryptedText)
    decrypted_text = []
    for i in range(len(_array_encryptedText)):
        decrypted_text.append(Chevy_Decrypt(_array_encryptedText[i],k))

    decrypted_text_join = ''.join(decrypted_text)
    decrypted_text_join = decrypted_text_join.replace("00",'');
    #decrypted_text = bytes.fromhex(''.join(decrypted_text)).decode('utf-8')
    print()
    try:
        print("Decrypted Text: ",bytes.fromhex(decrypted_text_join).decode('utf-8'))
    except:
        print("Decrypted Text: ",decrypted_text_join)
    print()
    if stat == FILE:
        print(" I will create a file now at the directory : ", dir)
        f = open(dir,'w')
        f.write(bytes.fromhex(decrypted_text_join).decode('utf-8'))
        print("Successfull Decrypted! check the file now")
    
def _Write():
    print("[E]ncrypt or [D]ecrypt? : ", end='')
    _c = input()
    print("Text : ", end='')
    plainText = input()
    _k_bol = True
    while (_k_bol):
        print("Please input the key that is maximum of 16 letters =>  ", end='')
        key = input()
        if len(key) <= 16 : 
            _k_bol = False
        else:
            print(" 16 letters or less only!")
    
    if _c.upper() == 'E':
        _TwoFish_Encrypt(plainText, key, WRITE, False)
    elif _c.upper() == 'D':
        _TwoFish_Decrypt(plainText, key, WRITE, False)

def _File():
    print("Kindly type the directory of the text file which includes the name of it for example C:/Desktop/Eco.txt => ", end='')
    _dir = input()
    _dir = '/'.join(_dir.split('\\'));
    _read = open(_dir)
    plainText =_read.read();
    print("The text : => ", plainText)

    print("[E]ncrypt or [D]ecrypt? : ", end='')
    _c = input()
    print("Please input the key that is maximum of 16 letters => ",end='')
    _k_bol = True
    while (_k_bol):
        key = input()
        if len(key) <= 16 : 
            _k_bol = False
        else:
            print(" 16 letters or less only!")
    if _c == 'E':
        _TwoFish_Encrypt(plainText, key, FILE, _dir)
    elif _c == 'D':
        _TwoFish_Decrypt(plainText, key, FILE, _dir)


def main():
    _c = ''
    while(_c != 'Y'):
        print()
        print("What type : [W]rite or a [F]ile? : ", end='')
        _c = input()
        if _c.upper() == 'W':
            _Write()
        elif _c.upper() == 'F':
            _File()
        else:
            print("Want to exit ? [Y]es or [N]o : ", end='')
            _c = input()
            _c = _c.upper()
   

#f = open("C:/Users/pc/Desktop/Github/test.txt","r")
#print(f.read())



main()


