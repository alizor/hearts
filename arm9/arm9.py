import os, struct, sys

# free space
# 0x000A7DDC
# 0x000AB060 (0x75C)

status_pointer = 0xB0060 # 33
status_sector = 0xAFF44

parameters_sections = 32
parameters_pointer = 0x88DF8
parameters_sector = 0xB0160

menu_sections = 609
menu_pointer = 0xB25A4
menu_sector = 0xB035C
_A0250B02 = [0x6B40C, 0x6B574, 0x6B5BC, 0x6B650, 0x6B67C, 0x6B6E0, 0x6B70C,
             0x6B724, 0x6B73C, 0x6B754, 0x6B774, 0x6B78C, 0x6B7A8, 0x6B7C8]

def extract_menu():
    
    f = open('arm9.bin', 'rb')
    o = open('menu_j.txt', 'wb')

    f.seek(menu_pointer, 0)
    text_pointers = []
    pointers_orders = {}

    for i in range(menu_sections):
        text_pointers.append(struct.unpack('<L', f.read(4))[0] - 0x2000000)
        pointers_orders[text_pointers[i]] = i
        f.read(12)

    f.seek(min(text_pointers), 0)
    text_pointers.append(menu_pointer)
    sorted_list = sorted(text_pointers)

    for i in range(menu_sections):
        f.seek(sorted_list[i], 0)
        o.write(b'[%04d]\n' % text_pointers.index(sorted_list[i]))
        b = f.read(1)
        while b != b'\x00':
            o.write(b)
            b = f.read(1)
        o.write(b'\n---------------------\n')

    f.close()
    o.close()

def insert_menu():
    
    f = open('text.txt', 'rb')
    arm9 = open('arm9_trans.bin', 'r+b')

    lines = []
    indexes = []
    count = 0
    buffer = menu_sector + 0x02000000
    size_limit = menu_pointer - menu_sector
    line_buffer = bytes()
    byte_buffer = bytes()
    new_pointer = 0
    di = {}
    
    for line in f:
        if b'------' in line:
            lines.append(line_buffer[:-1])
            line_buffer = bytes()
        elif b'[' and b']' in line:
            n = int(line.decode()[1:-2])
            indexes.append(n)
        else:
            line_buffer += line

    for l in lines:
        rest = (4 - len(l) % 4)
        byte_buffer += l + (b'\x00' * rest)
        di[indexes[count]] = buffer
        buffer += len(l) + rest
        count += 1
        if count == 62:
            new_pointer = menu_sector + len(byte_buffer) + 0x02000000
            byte_buffer += struct.pack('<L', menu_pointer - 4 + 0x02000000)
            buffer += 4

    if len(byte_buffer) > size_limit:
        print ('Error! File is larger than the limit, dif = %d' % (len(byte_buffer) - size_limit))
        sys.exit(1)
    else:
        byte_buffer += b'\x00' * (size_limit - len(byte_buffer))

    arm9.seek(menu_sector, 0)
    arm9.write(byte_buffer)
    arm9.seek(menu_pointer, 0)

    for i in range(count):
        arm9.write(struct.pack('<L', di[i]))
        arm9.read(12)

    for i in _A0250B02:
        arm9.seek(i, 0)
        arm9.write(struct.pack('<L', new_pointer))

    f.close()
    arm9.close()


if __name__ == '__main__':
    if sys.argv[1] == '-e':
        extract_menu()
    elif sys.argv[1] == '-i':
        insert_menu()
    sys.exit(1)
