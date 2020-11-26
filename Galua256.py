

def _byte(intValue):
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
    
def _byte_limit(num):
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
		_b = _byte(a^b);
		return _byte_limit(_b)

	def multiply(self,a, b):
		p = 0
		for i in range(8):
			if((b&1) != 0):
				p ^= a
				p = _byte_limit(p)
			carry = _byte(a & 0x80)
			a<<=1
			a = _byte_limit(a)

			if(carry != 0):
				a ^= self.mask
				
			b >>= 1
			if(b > 127):
				b = (-1)*(255 + 1 - b)
			

		return p
