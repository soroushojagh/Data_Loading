from ast import ExceptHandler
import os, subprocess, re, time, shutil, csv
import codecs

# unzip all the files
# remove all zip files
# move empty files to "broken" directory
# find and move old data
# find broken data in new data's and move them to "broken" directory
# add new-correct files to new file list
# show the report(all/old/new/ new-broken/new-correct)


main_dir = '/home/psycho/Documents/Code/python/test_load_data/'
new_dir = 'ppm2/'
old_data_dir = main_dir + 'old/'
broken_data_dir = main_dir  + 'broken/'
correct_data_dir = main_dir + 'correct/'
count_all_files = 0
count_old_files = 0
count_new_files = 0
count_correct_files = 0
count_broken_files = 0
count_new_correct_files = 0
count_80_files = 0
count_81_files = 0
count_82_files = 0
count_87_files = 0
old_list_file = main_dir + 'old.txt'
new_list_file = main_dir + 'new.txt'
old_list = []
new_list = []
dir_87 = main_dir + '87'
dir_82 = main_dir + '82'
dir_81 = main_dir + '81'
dir_80 = main_dir + '80'
PATTERN = "^[+-]?((180\.?0*$)|(((1[0-7][0-9])|([0-9]{0,2}))\.?[0-9]*$))"
# initialing directory structure
if os.path.exists(old_data_dir) is False:
    os.mkdir(old_data_dir)
if os.path.exists(broken_data_dir) is False:
    os.mkdir(broken_data_dir)
if os.path.exists(correct_data_dir) is False:
    os.mkdir(correct_data_dir)
if os.path.exists(dir_87) is False:
    os.mkdir(dir_87)
if os.path.exists(dir_82) is False:
    os.mkdir(dir_82)
if os.path.exists(dir_81) is False:
    os.mkdir(dir_81)
if os.path.exists(dir_80) is False:
    os.mkdir(dir_80)

# unzipping
zip_count = len(os.listdir(main_dir + new_dir))
csv_count = 0
for ff in range(zip_count):
    if ff%10==0:
        time.sleep(1)
    csv_count+=1
    if ff==1:
        os.system(f"cd {main_dir + new_dir } && unzip '*.zip'")
 
    if csv_count == zip_count:
        os.system(f"cd {main_dir + new_dir } && rm -rf *.zip")
        break


# old data  and empty files
if os.path.exists(old_list_file):
    with open(old_list_file) as ol:
        old_list = ol.readlines()
count_all_files = len(os.listdir(main_dir + new_dir))
for fs in os.listdir(main_dir + new_dir):
    if os.path.getsize(main_dir + new_dir + fs) < 1 * 1024:
        count_broken_files +=1
        
        os.system(f"mv {main_dir}{new_dir}{fs}  {broken_data_dir}")
    
    for od in old_list:
        if fs == od:
            count_old_files +=1
            os.system(f"mv {main_dir}{new_dir}{fs} {old_data_dir}")


for f in os.listdir(main_dir + new_dir):
    if os.path.getsize(main_dir + new_dir + f) < 1 * 1024:
            count_broken_files +=1
            # print(f"valid lat/lang for 99999")
            os.system(f"mv {main_dir}{new_dir}{f}  {broken_data_dir}")
    if len(os.listdir(main_dir + new_dir))<1:
        break
    counts2 = 0
    cols=[]
    broken_flag1 = 0
    broken_flag2 = 0
    broken_flag3 = 0
    broken_flag4 = 0
    broken_flag5 = 0
    rows=[]
    try:
     with codecs.open(main_dir+ new_dir+f, 'r') as csv_file:
        try:
            if csv_file :
                csv_data = csv.DictReader((l.replace('\0', '') for l in csv_file))
                rows = csv_data 
                find=0
                print('find',f,find)   

                for c in rows:
                    broken_file = ''
                    i=c
                    # print(i)
                    sample_counter = 0
                    if rows and c is None:
                        print("shettttt")
                    else:
                        for i in rows:
                            if sample_counter >20 : 
                                continue
                            if i is None:
                                print('salam')
                            else:
                                latitude = i['latitude']
                                longitude = i['longitude']
                                
                                match1 = re.match(PATTERN,latitude)
                                match2 = re.match(PATTERN,longitude)
                                # i is not lat                
                                if len(latitude)>5 and match1 is not None and match2 is not None:
                                    print(f"valid lat/lang for ")
                                    if os.path.exists(f"{main_dir}{new_dir}{f}"):
                                        shutil.move(f"{main_dir}{new_dir}{f}",f"{correct_data_dir}{f}")
                                    count_correct_files+=1
                                    find+=1
                                else:
                                    broken_flag5 = 1
                                    # os.system(f"mv {main_dir}{new_dir}{f} {broken_data_dir}{f}")
                                    print(f"valid lat/lang for 111111111111111111111 ")
                                    if os.path.exists(f"{main_dir}{new_dir}{f}"):
                                        shutil.move(f"{main_dir}{new_dir}{f}",f"{broken_data_dir}{f}")
                                        broken_file = f
                                        continue
                                sample_counter+=1
                                find+=1
                    

                    
                
                if len(cols) == 80:
                    count_80_files+=1
                    os.system(f"mv {main_dir}{new_dir}{f} {dir_80}")
                elif len(cols) == 81:
                    count_81_files+=1
                    os.system(f"mv {main_dir}{new_dir}{f} {dir_81}")
                elif len(cols) == 82:
                    count_82_files+=1
                    os.system(f"mv {main_dir}{new_dir}{f} {dir_82}")
                elif len(cols) == 87:
                    count_87_files+=1
                    os.system(f"mv {main_dir}{new_dir}{f} {dir_87}")

                # counts2+=len(rows[1:])
                if broken_flag1+broken_flag2+broken_flag3+broken_flag4+broken_flag5>1:
                    count_broken_files+=1
            else:
                print('salam')
        except:
            print("bugggggg")
    except Exception :
        print('bug',Exception,f)
        if os.path.exists(f"{main_dir}{new_dir}{f}"):
            shutil.move(f"{main_dir}{new_dir}{f}",f"{broken_data_dir}{f}")
            broken_file = f
        continue
    
    

print(f" All Files : {count_all_files}")
print(f" Broken Files : {count_broken_files}")
print(f" OLD Files : {count_old_files}")
print(f" Correct Files : {count_correct_files}")
print(f" 87 => : {count_87_files}")
print(f" 82 => : {count_82_files}")
print(f" 80 => : {count_80_files}")
print(f" 81 => : {count_81_files}")

# https://drive.google.com/uc?id=1kvKIYiOGDhclLgfv6_6E8wqNBGUzxqfH&export=download
# https://drive.google.com/file/d/1kvKIYiOGDhclLgfv6_6E8wqNBGUzxqfH/view?usp=sharing
# https://googledrive.com/host/1kvKIYiOGDhclLgfv6_6E8wqNBGUzxqfH