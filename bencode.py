#!/usr/bin/python3

__data = bytes();
__s = 0;
__l = 0;
__enc = False;
def encode(x):
    if type(x) == int:
        return 'i'.encode() + str(x).encode() + 'e'.encode();
    elif type(x) == str:
        x = x.encode('utf-8');
        return (str(len(x)) + ':').encode('ascii') + x;
    elif type(x) == dict:
        keys = list(x.keys());
        keys.sort();
        end = 'd'.encode();
        for i in keys:
            if type(i) == str:
                end += encode(i);
            else:
                raise TypeError("the kay must be str for dict.");
            end += encode(x[i]);
        end += 'e'.encode();
        return end;
    elif type(x) == list:
        end = 'l'.encode();
        for i in x:
            end += encode(i);
        end += 'e'.encode();
        return end;
    else:
        try:
            return (str(len(x)) + ':').encode('ascii') + x;
        except:
            raise TypeError('the arg data type is not support for bencode.');

def decode(x = None, enc=False):
    global __data, __s, __l, __enc;
    if enc != False:
        __enc = enc;
    if type(x) != bytes and x != None:
        raise TypeError("To decode the data type must be bytes.")
    elif x != None:
        __s = 0;
        __l = 0;
        __data = x;
        __l = len(__data);
    #dict
    if __data[__s] == 100:
        __s += 1;
        d = {};
        while __s < __l-1:
            if __data[__s] not in range(48, 58):
                break;
                #raise RuntimeError("the dict key must be str.");
            key = decode();
            value = decode();
            d.update({key:value});
        __s += 1;
        return d;
    #int
    elif __data[__s] == 105:
        temp = __s + 1;
        key = '';
        while __data[temp] in range(48, 58):
            key += str(__data[temp]-48);
            temp += 1;
        __s += len(key) + 2;
        return int(key);
    #string
    elif __data[__s] in range(48, 58):
        temp = __s;
        key  = '';
        while __data[temp] in range(48, 58):
            key += str(__data[temp]-48);
            temp += 1;
        temp += 1;
        key = __data[temp:temp+int(key)];
        __s = len(key)+temp;
        if type(__enc) == list:
            for ii in __enc:
                try:
                    return key.decode(ii);
                except:
                    continue;
        else:
            try:
                return key.decode('utf-8');
            except:
                try:
                    return key.decode(__enc);
                except:
                    return key;
    #list
    elif __data[__s] == 108:
        li = [];
        __s += 1;
        while __s < __l:
            if __data[__s] == 101:
                __s += 1;
                break;
            li.append(decode());
        return li;
