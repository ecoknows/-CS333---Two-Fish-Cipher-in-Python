#print(1073741824>>8 )
#890AED7052FFE4577C4D4D63F9349660
# -13477738
# 9FB63337151BE9C71306D159EA7AFAA4
# 9FB63337151BE9C7136D159EA7AFAA4
import ctypes

def _32bit_ops(ops):
    a=ctypes.c_int32(ops)
    return a.value

print(len("82168b77b7ef6e133d248cdca179754"))
def _limiter(num,distance):
    _b = "{0:b}".format(num)
    if(num < 0):
        _b = _b[1:]
        x = len(_b);
        y = 16

        if y < x :
            y *= round(x/y)

        _add = (y-x);
        _b = ('0'*_add+"{0:b}".format(num*-1))
        _b = _b.replace('0','3').replace('1','0').replace('3','1')

    _b_length = len(_b);
    if(_b_length < 25+(8-distance)): # 25 -8 = 1
        return 0;
    _to_get = _b_length - 24 - (8-distance);

    _b = _b[0:_to_get];
    return int(_b,2)



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

#10010110
#print( _32bit_ops(1256843351 >> 1) | 0);

#_len = '001100001000000100111100010';
#print(len(_len), " len ")

#for i in range(15, -1, -1):
#    print(i)
    #383501559
    #3911465737

#print(_32bit_ops(-993410215))
#print(_32bit_ops(1740595672)," CcCfsadsad")
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
        #print(_b, ' 1')
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


def _getByte(num):
    mask = (1 << 8) - 1
    little = num & mask
    if(little > 127):
        return (-1)*(255 + 1 - little)
    if little < -127:
        return (255 + 1 + little)
    return little

Hex_ = 0x294C5E41
_FULL = "415E4C29 DB12A70F 8AEE9F3D B2C872D3"


def _dec_message(message):
    result = [0]*4
    for i in range(4):
        temp = [0]*4
        end = 8 * (i+1) - 1;
        _b = ''
        for j in range(4):
            first = end - (j*2)
            _b += message[first-1] + message[first]
        result[i] = _32bit_ops(int(_b,16));
    print(result)

#print((-3968645>>1) | (-2147483648) ," He" )
#print(shiftRight_32(-3968645, 1), " Answer")
'''
te_ = '00110000100000010011110001010000'
latest_1s = _latest_1s(te_);
print(latest_1s)
print(te_[0:-4])
'''

#print(185207048 ^ -390470641 , 'cc')

#print(_limiter(-184821906,9))
'''
test = ('0'*4+"{0:b}".format(184821906));

test = test.replace('0','3').replace('1','0').replace('3','1')
print(_limiter(int(test,2), 9))
'''



#print((28 % 8) << (184821906))
# 184821906 - > 9