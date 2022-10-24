import math
# the pounce language runtime

def deepcopy(l):
    newlist = []
    for e in l:
        if isArray(e):
            newlist.append(deepcopy(e))
        else:
            newlist.append(e)
    return newlist

# def deepcopy_aux(l):
#     foreach e in l:
#         if type(e) == 'list'
#             return  

def pounceReplace(id, val):
    def r (ele):
        if ele == id:
            return val
        return ele
    return r

def _compose(s, pl):
    global words
    # usage: [phrase] [new-word-name] compose
    new_word = s.pop()
    new_definition = s.pop()
    words[new_word[0]] = new_definition
    return [s, pl]
def _pounce(s, pl):
    # [param1 param2] [phrase]
    phrase = deepcopy(s.pop())
    params = s.pop().copy()
    while len(params) > 0 :
        id = params.pop()
        val = s.pop()
        rep = pounceReplace(id, val)
        phrase = list(map(rep, phrase))
    pl = phrase+pl
    return [s, pl]
def _crouch(s, pl):
    # [param1 param2] [phrase]
    phrase = deepcopy(s.pop())
    params = s.pop().copy()
    while len(params) > 0 :
        id = params.pop()
        val = s.pop()
        rep = pounceReplace(id, val)
        phrase = list(map(rep, phrase))
    s.append(phrase)
    return [s, pl]
def _dup(s, pl):
    a = s[-1]
    if isArray(a):
        s.append(deepcopy(a))
    else:
        s.append(a)
    return [s, pl]
def _add(s, pl):
    a = s.pop()
    b = s.pop()
    s.append(a + b)
    return [s, pl]
def _sub(s, pl):
    a = s.pop()
    b = s.pop()
    s.append(b - a)
    return [s, pl]
def _mult(s, pl):
    a = s.pop()
    b = s.pop()
    s.append(a * b)
    return [s, pl]
def _divide(s, pl):
    a = s.pop()
    b = s.pop()
    s.append(b / a)
    return [s, pl]
def _modulo(s, pl):
    a = s.pop()
    b = s.pop()
    s.append(b % a)
    return [s, pl]
def _abs(s, pl):
    a = s.pop()
    s.append(abs(a))
    return [s, pl]
def _sin(s, pl):
    a = s.pop()
    s.append(math.sin(a))
    return [s, pl]
def _cos(s, pl):
    a = s.pop()
    s.append(math.cos(a))
    return [s, pl]
def _floor(s, pl):
    a = s.pop()
    s.append(math.floor(a))
    return [s, pl]
def _eq(s, pl):
    a = s.pop()
    b = s.pop()
    s.append(a == b)
    return [s, pl]
def _gt(s, pl):
    a = s.pop()
    b = s.pop()
    s.append(b > a)
    return [s, pl]
def _lt(s, pl):
    a = s.pop()
    b = s.pop()
    s.append(b < a)
    return [s, pl]
def _ift(s, pl):
    then_block = s.pop()
    expression = s.pop()
    if expression:
        if isArray(then_block):
            pl = then_block+pl
        else:
            pl.insert(0, then_block)
    return [s, pl]
def _ifte (s, pl):
    else_block = s.pop()
    then_block = s.pop()
    expression = s.pop()
    if expression:
        if isArray(then_block):
            #print(then_block)
            pl = then_block+pl
        else:
            pl.insert(0, then_block)
    else:
        if isArray(else_block):
            pl = else_block+pl
        else:
            pl.insert(0, else_block)
    return [s, pl]
def _get(s, l): # (dict key -- dict value)
    key = s.pop()
    dictionary = s[-1]
    s.append(dictionary[key])
    return [s, l]
def _set(s, l): # (dict value key -- dict)
    key = s.pop()
    value = s.pop()
    dictionary = s[-1]
    dictionary[key] = value
    return [s, l]
def _apply(s, l): # (dict key fun -- dict)
    fun = s.pop()
    key = s[-1]
    #l.insert(0, ['get', fun, key, 'set'])
    l.insert(0, 'set')
    l.insert(0, key)
    l = fun+l                                     # concat arrays so that the program list (l) has words on it, not a list
    l.insert(0, 'get')
    return [s, l]
def _swap(s, l):
    a = s.pop()
    b = s.pop()
    s.append(a)
    s.append(b)
    return [s, l]
def _drop(s, l):
    a = s.pop()
    return [s, l]
def _dip(s, l):
    f = s.pop()
    a = s.pop()
    l.insert(0, a)
    l = f+l
    return [s, l]

words = {
  'compose': _compose,
  'pounce': _pounce,
  'crouch': _crouch,
  'dup': _dup,
  '+': _add,
  '-': _sub,
  '*': _mult,
  '/': _divide,
  '%': _modulo,
  'abs': _abs,
  'floor': _floor,
  '==': _eq,
  '<': _lt,
  '>': _gt,
  'if': _ift,
  'if-else': _ifte,
  'get': _get,
  'set': _set,
  'app': _apply,
  'swap': _swap,
  'drop': _drop,
  'dip': _dip,
  'sin': _sin,
  'cos': _cos
}

def isValue(e, fun):
    return (isinstance(e, int)
            or isinstance(e, float)
            or isinstance(e, bool)
            or (isinstance(e, str) and not e in fun.keys()))

def isNumber(e):
    return isinstance(e, int) or isinstance(e, float)

def isArray(a):
    return isinstance(a, (list,))

def isRecord(a):
    return isinstance(a, (dict,))

#from inspect import isfunction
def isfunction(candidate):
    return not (isinstance(candidate, str) or isinstance(candidate, (list,)))


#def runScript(program_script, vs):
#    pl = jp.parse(program_script)
#    return purr(pl, words)

def purr(pl, words=words, debug = False, stack = []):
    vs = []
    while pl != None and len(pl) > 0:
        next = pl[0]
        pl = pl[1:]
        # if debug:
        #     print('about to', vs, next)
        #     time.sleep(0.3)
        
        if isValue(next, words) or isArray(next) or isRecord(next):
            if next == 'true':
                vs.append(True)
            elif next == 'false':
                vs.append(False)
            else:
                vs.append(next)
        elif next in words.keys():
            # if debug:
            #     print('applying', vs, next, pl)
            #     time.sleep(0.3)
            
            if isfunction(words[next]):
                (vs, pl) = words[next](vs, pl)
            elif isinstance(words[next], str):
                pl = jp.parse(words[next]) + pl
            elif isRecord(words[next]):
                if 'args' in words[next].keys():
                    arg_rec = {}
                    while len(words[next].args) > 0:
                        arg_rec[words[next].args.pop()] = s.pop()
                    (vs, pl) =  words[next].func(vs, pl, arg_rec)
            else:
                pl = words[next] + pl
        else:
            print('unknown term or word:', next)
    return vs

