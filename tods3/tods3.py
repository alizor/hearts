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

def dump_tods3(name, header_size, mi, ma):

    try:
        os.mkdir('TODS3_txt')
    except:
        pass
    
    f = open(name, 'rb')
    o = open('TODS3_txt/' + name + '.txt', 'wb')
    pointers = []
    table = guess_pointers(name, header_size, mi, ma)

    for p in table:
        f.seek(p, 0)
        pointers.append(struct.unpack('<L', f.read(4))[0])

    pointers.append(os.path.getsize(name))
    
    for i in range(len(pointers)-1):
        f.seek(pointers[i], 0)
        o.write(b'[%04X]\n' % table[i])
        r = f.read(pointers[i+1]-pointers[i]-1).replace(b'\x00', b'\x0A')
        o.write(r)
        o.write(b'\n---------------------\n')

    o.close()
    f.close()

    print ("Extracting %s" % name)

def dump_titledata():
    name = 'TODS3_TitleData.dat'
    f = open(name, 'rb')
    o = open('TODS3_txt/' + 'TODS3_TitleData.dat.txt', 'wb')
    
    pointers = []
    table = []
    offsets = []
    f.seek(0x14, 0)
    text_offset = struct.unpack('<L', f.read(4))[0]
    f.read(4)
    r = 0x1C
    
    while r < text_offset:
        pointers.append(struct.unpack('<L', f.read(4))[0])
        table.append(f.tell())
        pointers.append(struct.unpack('<L', f.read(4))[0])
        table.append(f.tell())
        f.read(12)
        r += 20
        
    pointers.append(os.path.getsize(name))

    for i in range(len(pointers)-1):
        f.seek(text_offset + pointers[i], 0)
        n = pointers[i+1]-pointers[i]-1
        o.write(b'[%04X]\n' % table[i])
        o.write(f.read(n))
        o.write(b'\n---------------------\n')
        
    f.close()
    o.close()

    print ("Extracting %s" % name)

def dump_curestone():
    name = 'TODS3_CureStoneData.dat'
    f = open(name, 'rb')
    o = open('TODS3_txt/' + name + '.txt', 'wb')

    f.seek(8,0)
    sections = int((struct.unpack('<L', f.read(4))[0]/16)) - 1
    f.read(4)

    count = {}
    pointers = []
    current = 0

    for i in range(sections):
        p = struct.unpack('<L', f.read(4))[0]
        if p == current:
            count[p] += 1
        else:
            pointers.append(p)
            current = p
            count[p] = 1
        f.read(12)

    pointers.append(os.path.getsize(name))

    for i in range(len(pointers)-1):
        f.seek(pointers[i], 0)
        o.write(b'[%04d]\n' % count[pointers[i]])
        o.write(f.read(pointers[i+1]-pointers[i]-1))
        o.write(b'\n---------------------\n')

    f.close()
    o.close()

    print ("Extracting %s" % name)
    

def insert_text(name, header_size):

    try:
        os.mkdir('TODS3_new')
    except:
        pass
    
    f = open('TODS3_txt/' + name + '.txt', 'rb')
    o = open('TODS3_new/' + name, 'wb')
    dat = open(name, 'rb')
    
    special = ['TODS3_BtlMemoData.dat', 'TODS3_OutLineData.dat']
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
            if name in special:
                line = line.replace(b'\x0A', b'\x00')
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
        dump_tods3('TODS3_BtlMemoData.dat', 8, 4, 300)
        dump_tods3('TODS3_OutLineData.dat', 8, 1, 400)
        dump_tods3('TODS3_SormaSkillData.dat', 0x14, 4, 400)
        dump_tods3('TODS3_SpirLinkData.dat', 8, 1, 400)
        dump_tods3('TODS3_StrategyData.dat', 8, 4, 300)
        dump_titledata()
        dump_curestone()
    elif sys.argv[1] == '-i':
        insert_text('TODS3_BtlMemoData.dat', 8)
        insert_text('TODS3_OutLineData.dat', 8)
        insert_text('TODS3_SormaSkillData.dat', 0x14)
        insert_text('TODS3_SpirLinkData.dat', 8)
        insert_text('TODS3_StrategyData.dat', 8)

        
    sys.exit(1)
