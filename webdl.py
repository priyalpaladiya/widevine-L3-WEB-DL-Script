import os
from typing import DefaultDict

print("\nWEBDL Script by parnex")
print("Required files : yt-dlp.exe, mkvmerge.exe, mp4decrypt.exe, aria2c.exe\n")

filename = input("Enter the output file name (no spaces) : ")
mpdurl = input("Enter MPD URL : ")

os.system(f'yt-dlp --external-downloader aria2c --allow-unplayable-formats --no-check-certificate -F "{mpdurl}"')

vid_id = input("\nEnter Video ID : ")
audio_id = input("Enter Audio ID : ")
os.system(f'yt-dlp --external-downloader aria2c --allow-unplayable-formats --no-check-certificate -f {vid_id}+{audio_id} "{mpdurl}"')

os.system("ren *.mp4 encrypted.mp4")
os.system("ren *.m4a encrypted.m4a")
os.system('ren *.log key.txt')

with open("key.txt", 'r') as f:
    file = f.readlines()

length = len(file)

dict_key = {}
dict_kid = {}

for i in range(0, length):
    key = file[i][60 : 92]
    kid = file[i][98 : 130]

    dict_key['key' + str(i)] = key
    dict_kid['kid' + str(i)] = kid

print("\nDecrypting .....")
os.system(f'mp4decrypt.exe --key {dict_kid["kid0"]}:{dict_key["key0"]} encrypted.m4a decrypted.m4a')
os.system(f'mp4decrypt.exe --key {dict_kid["kid0"]}:{dict_key["key0"]} encrypted.mp4 decrypted.mp4')

print("Merging .....")
os.system(f'mkvmerge.exe -o {filename}.mkv decrypted.mp4 decrypted.m4a')
print("\nAll Done .....")

print("\nDo you want to delete the Encrypted Files : Press 1 for yes , 2 for no")
delete_choice = int(input("Enter Response : "))

if delete_choice == 1:
    os.remove("encrypted.m4a")
    os.remove("encrypted.mp4")
    os.remove("decrypted.m4a")
    os.remove("decrypted.mp4")
else:
    quit()