import os, struct, sys

def dump_CTODS3(name, block_size):

    try:
        os.mkdir('CTODS3_txt')
    except:
        pass
    
    f = open(name, 'rb')
    o = open('CTODS3_txt/' + name + '.txt', 'wb')

    pointers = []
    offsets = []
    pointer = struct.unpack('<L', f.read(4))[0]
    files = int(pointer / block_size)
    f.seek(0, 0)
    
    for i in range(files):
        offsets.append(f.tell())
        pointers.append(struct.unpack('<L', f.read(4))[0])
        f.read(block_size - 4)

    for i in range(files):
        f.seek(pointers[i], 0)
        o.write(b'[%04X]\n' % offsets[i])
        b = f.read(1)
        while b != b'\x00':
            o.write(b)
            b = f.read(1)
        o.write(b'\n-------------------\n')

    o.close()
    f.close()

    print ("Extracting %s" % name) 

def insert_text(name):

    try:
        os.mkdir('CTODS3_new')
    except:
        pass
    
    f = open('CTODS3_txt/' + name + '.txt', 'rb')
    o = open('CTODS3_new/' + name, 'wb')
    dat = open(name, 'rb')

    lines = []
    indexes = []
    pointers = []
    line_buffer = bytes()

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
        dump_CTODS3('CTODS3_AccessoryShopData.bin', 0x60)
        dump_CTODS3('CTODS3_CurestoneShopData.bin', 0x4C)
        dump_CTODS3('CTODS3_MaterialShopData.bin', 0x44)
        dump_CTODS3('CTODS3_ToolShopdata.bin', 0x38)
    elif sys.argv[1] == '-i':
        insert_text('CTODS3_AccessoryShopData.bin')
        insert_text('CTODS3_CurestoneShopData.bin')
        insert_text('CTODS3_MaterialShopData.bin')
        insert_text('CTODS3_ToolShopData.bin')
    sys.exit(1)
