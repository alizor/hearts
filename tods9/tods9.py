import os, struct, sys

def guess_pointers(name, header_size, mi, ma):
    f = open(name, 'rb')
    f.seek(header_size, 0)
    block_size = struct.unpack('<L', f.read(4))[0] - header_size
    pointer = block_size
    mi = int(mi)
    ma = int(ma)
    read = 0
    f.seek(header_size, 0)
    table = []

    while read < block_size:
        nx = struct.unpack('<L', f.read(4))[0]
        if (nx-pointer >= mi) and (nx-pointer <= ma):
            pointer = nx
            table.append(f.tell()-4)
        read += 4

    f.close()

    return table


def dump_TODS9(name, header_size, mi, ma):

    try:
        os.mkdir('TODS9_txt')
    except:
        pass
    
    f = open(name, 'rb')
    o = open('TODS9_txt/' + name + '.txt', 'wb')

    pointer_table = guess_pointers(name, header_size, mi, ma)

    for i in range(len(pointer_table)):
        f.seek(pointer_table[i], 0)
        p = struct.unpack('<L', f.read(4))[0]
        f.seek(p, 0)
        o.write(b'[%04X]\n' % pointer_table[i])
        b = f.read(1)
        while b != b'\x00':
            o.write(b)
            b = f.read(1)
        o.write(b'\n-------------------\n')

    o.close()
    f.close()

    print ("Extracting %s" % name)

def insert_text(name, header_size):

    try:
        os.mkdir('TODS9_new')
    except:
        pass
    
    f = open('TODS9_txt/' + name + '.txt', 'rb')
    o = open('TODS9_new/' + name, 'wb')
    dat = open(name, 'rb')

    lines = []
    indexes = []
    pointers = []
    count = 0
    line_buffer = bytes()

    dat.seek(header_size, 0)
    header_block = struct.unpack('<L', dat.read(4))[0]
    dat.seek(0, 0)
    header = dat.read(header_block)
    buffer = header_block
    dat.close()

    o.write(header)
    
    for line in f:
        if b'------' in line:
            lines.append(line_buffer[:-1])
            pointers.append(buffer)
            buffer += len(line_buffer)
            line_buffer = bytes()
        elif b'[' and b']' in line and len(line) == 7:
            n = int(line.decode()[1:-2], 16)
            indexes.append(n)
        else:
            line_buffer += line

    f.close()

    for l in lines:
        o.write(l)
        o.write(b'\x00')
        
    for i in range(len(pointers)):
        o.seek(indexes[i], 0)
        o.write(struct.pack('<L', pointers[i]))

    o.close()

    print ("Inserting %s" % name)

if __name__ == '__main__':
    if sys.argv[1] == '-e':
        dump_TODS9('TODS9_AccessoryData.dat', 0x10, 2, 400)
        dump_TODS9('TODS9_GradeShopData.dat', 0x10, 2, 400)
        dump_TODS9('TODS9_ItemData.dat', 0x10, 2, 132)
        dump_TODS9('TODS9_MaterialData.dat', 0x10, 2, 400)
        dump_TODS9('TODS9_SormaData.dat', 0x10, 2, 400)
        dump_TODS9('TODS9_ValueData.dat', 0x10, 2, 400)
    elif sys.argv[1] == '-i':
        insert_text('TODS9_AccessoryData.dat', 0x10)
        insert_text('TODS9_GradeShopData.dat', 0x10)
        insert_text('TODS9_ItemData.dat', 0x10)
        insert_text('TODS9_MaterialData.dat', 0x10)
        insert_text('TODS9_SormaData.dat', 0x10)
        insert_text('TODS9_ValueData.dat', 0x10)
    sys.exit()
