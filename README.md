# Tales of Hearts DS translation project

# Tools

Python:

https://www.python.org/downloads/

CrystaTile2: For extracting files and decompressing them

https://www.romhacking.net/utilities/818/

DSLazy: For extracting and creating the entire ROM

https://www.romhacking.net/utilities/793/

BatchLZ77: For LZ11 compression

https://gbatemp.net/download/batchlz77.11736/


# General info

TODS3 files are in the root folder, not all of them have text.

CTODS3 and TODS9 files are in the 'item' folder.

Scripts are in the 'm' folder, when extracted, you need to decompress the SCP files (LZ11).

Skits are in the 'fc' folder, 'fcscr.b' and 'fcscr.dat', you need to decompress them (LZ11).

# Instructions

### Extracting/Inserting files

You can use CT2 and DSLazy to extract/insert files.

If you just want to test small files like arm9, tods3, ctods3 and tods9, I recommend manually importing them on CT2 instead of building a new ROM.

If you want to replace the fps4 files like m.b and m.dat, I recommend using DSLazy to create a new ROM.

### arm9

1 - Open the ROM on CT2 and press CTRL+N to view the files

2 - Right click on arm9.bin and select "Extract (U)"

3 - Put arm9.bin on the same folder of the script and run "extract_arm9.bat"

4 - Edit the text file and rename it to "text.txt"

5 - Run "insert_arm9.bat" and open CT2

6 - Right click on arm9.bin, select Compression and choose the arm9_trans.bin

### fps4

1 - To extract the script, put m.b and m.dat on the fps4 folder.

2 - Run "extract_m.bat", then "extract_m_files.bat".

3 - To insert the folders back to m.b and m.dat, create a new folder "pack" and put the new "m" folder and its files.

4 - Run "pack_m" and "pack_files".

### tods3, tods9 and ctods3

1 - Extract the respective files and put them on their respective folders.

2 - Run "extract_filetype.bat" to extract the text files.

3 - Translate the text files and run "insert_filetype.bat" to create a new folder with the translated files.

# Help needed

Extracting and inserting the script/skits: TSS files.

Extracting and inserting overlay files.
