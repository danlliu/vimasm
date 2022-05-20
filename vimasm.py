
import sys
import re

# python3 vimasm.py (lc2k file) (outfile)

def command(cmd, end=False, goto=None): 
    if end:
        return b':' + cmd.encode() + b'\x0dq!\n'
    if goto is not None:
        return b':' + cmd.encode() + b'\x0d' + f'{goto}gg'.encode() + b'"ayy@a\n'
    return b':' + cmd.encode() + b'\x0dj"ayy@a\n'

defvar = lambda varname: command(f'let {varname} = 0')
showreg = lambda: command('let r0 r1 r2 r3 r4 r5 r6 r7', True)

# instructions

# add  rdest ra rb
add = lambda rd, ra, rb: command(f'let r{rd} = r{ra} + r{rb}')
# sub  rdest ra rb
sub = lambda rd, ra, rb: command(f'let r{rd} = r{ra} - r{rb}')
# nor  rdest ra rb
nor = lambda rd, ra, rb: command(f'let r{rd} = invert(or(r{ra}, r{rb}))')
# nand rdest ra rb
nand = lambda rd, ra, rb: command(f'let r{rd} = invert(and(r{ra}, r{rb}))')
# xor  rdest ra rb
xor = lambda rd, ra, rb: command(f'let r{rd} = xor(r{ra}, r{rb})')

# set  rdest #imm
set_ = lambda rd, imm: command(f'let r{rd} = {imm}')
# zero rdest
zero = lambda rd: command(f'let r{rd} = 0')
# inc  rdest
inc = lambda rd: command(f'let r{rd} += 1')
# dec  rdest
dec = lambda rd: command(f'let r{rd} -= 1')

# For conditional jumps: `dest` is a zero-indexed line in the original assembly file.
# beq  ra rb dest
beq = lambda ra, rb, dest: b':' + f'if r{ra} == r{rb} | {dest} | else | + | endif'.encode() + b'\x0d' + b'"ayy@a\n'
# bne  ra rb dest
bne = lambda ra, rb, dest: b':' + f'if r{ra} != r{rb} | {dest} | else | + | endif'.encode() + b'\x0d' + b'"ayy@a\n'
# blt  ra rb dest
blt = lambda ra, rb, dest: b':' + f'if r{ra} < r{rb} | {dest} | else | + | endif'.encode() + b'\x0d' + b'"ayy@a\n'
# bgt  ra rb dest
bgt = lambda ra, rb, dest: b':' + f'if r{ra} > r{rb} | {dest} | else | + | endif'.encode() + b'\x0d' + b'"ayy@a\n'
# ble  ra rb dest
ble = lambda ra, rb, dest: b':' + f'if r{ra} <= r{rb} | {dest} | else | + | endif'.encode() + b'\x0d' + b'"ayy@a\n'
# bge  ra rb dest
bge = lambda ra, rb, dest: b':' + f'if r{ra} >= r{rb} | {dest} | else | + | endif'.encode() + b'\x0d' + b'"ayy@a\n'

# nop
nop = lambda: b'j"ayy@a\n'
# hlt
hlt = lambda: b'G$V\n'

def parse_line(line):
    sp = line.split()
    if sp[0] == 'set':
        sp[0] = 'set_'
    if sp[0][0] == 'b':
        sp[3] = str(int(sp[3]) + 9)

    return eval(f'{sp[0]}({",".join(sp[1:])})')

if __name__ == '__main__':
    with open(sys.argv[2], 'wb') as f:
        f.write(defvar('r0'))                       # 1
        f.write(defvar('r1'))                       # 2
        f.write(defvar('r2'))                       # 3
        f.write(defvar('r3'))                       # 4
        f.write(defvar('r4'))                       # 5
        f.write(defvar('r5'))                       # 6
        f.write(defvar('r6'))                       # 7
        f.write(defvar('r7'))                       # 8
        # program starts on 9

        with open(sys.argv[1], 'r') as ifile:
            for line in ifile:
                f.write(parse_line(line))

        f.write(b'Halted! Hit ESC then run :let r0 r1 r2 r3 r4 r5 r6 r7 to see register contents.')

