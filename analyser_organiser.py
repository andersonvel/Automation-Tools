
import argparse
import os
import shutil
import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd 

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--organiser', action='store_true')
group.add_argument('--analyser', action='store_true')
parser.add_argument('path',type= str )
args = parser.parse_args()


if  os.path.exists(args.path) :
    pass
else :
    print("Given path is not exists Please check the input path ")
    exit()


if args.organiser:

    #step 1 :  Get the all available file names in the given directory 

    current_path = args.path

    all_files = []

    def get_files(path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                yield file

    for file in get_files(current_path):
        all_files.append(file)



    #step 2 : based on extention name create a folder if not already there 

    folders = []

    all = os.listdir(current_path)

    required = []

    for _ in all_files:
        try :
            r = _.rindex(".")
            r2 = _[r+1:]
            if r2 not in required :
                required.append(r2)
        except Exception as e:
            print("error at indexing",e)
            

    for i in required :
        if os.path.isdir(i):
            pass 
        else :
            os.mkdir(i)


    #step 3 : Loop through all the files then move each file to respective folders 

    for _ in all_files:

        r3 = _.rindex(".")
        folder_name =  _[r3+1:]

        try :
            if _ == "final.py" :
                continue
            shutil.move(f"{current_path}/{_}",f"{current_path}/{folder_name}/{_}")
           
        except Exception as e :
            print("Got error at moving",e)
            print(f"paaths : {current_path}/{_}",f"{current_path}/{folder_name}/{_}")


    print("Organiser completed successfully....!")

     

elif args.analyser:

    #1.reads all files 
   
    path = args.path
    x = []
    y = []
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            x.append(os.path.join(root, name))
        
        for name in directories:
            y.append(os.path.join(root, name))


    #2.get each file sizes :

    main = list()
    all_ext = []
    for _ in x :
        p = _
        file_stats = os.stat(_)
        kb = file_stats.st_size
    
        name = 0
        r3 = _.rindex(".")
        ext =  _[r3+1:]


        temp = {"ext":ext,"kb":kb,"name":p}
        main.append(temp)
        if ext not in all_ext:
            all_ext.append(ext)

    all_ext_dict = dict.fromkeys(all_ext,0)

    for i in main :
        ce = i["ext"] 
        all_ext_dict[ce] = all_ext_dict[ce] + i["kb"]
        

    counts = []
    for i in all_ext :
        count = 0 

        for j in main :
            if j["ext"] == i :
                count = count + 1
            
        counts.append(count)

    chart_data = list(all_ext_dict.values())

    chart_data_mb = [k*0.000001 for k in chart_data ]

    chart_label = list(all_ext_dict.keys())

    GBsize = [float(i*0.000000001) for i in chart_data]

    dict = {'Extention': chart_label, 'Size(MB)': chart_data_mb ,
           "Size(GB)":GBsize,"counts":counts } 
        
    extention_data = pd.DataFrame(dict)


    plt.figure(figsize=(20, 20))

    plots = sns.barplot(x="Extention", y="Size(MB)", data=extention_data)

    for bar in plots.patches:

        plots.annotate(format(bar.get_height(), '.2f'),
                    (bar.get_x() + bar.get_width() / 2,
                        bar.get_height()), ha='center', va='center',
                    size=15, xytext=(0, 8),
                    textcoords='offset points')

    plt.xlabel("Extentions", size=14)

    plt.ylabel("Size(MB)", size=14)

    plt.title("Directory Size Analysis")

    plt.show()

    extention_data.to_csv("size_table.csv")




    print('Analyser completed successfully....!')
    
    print("\n")

    print("For more information please check size_table.csv")


























































