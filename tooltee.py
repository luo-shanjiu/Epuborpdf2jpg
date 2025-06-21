from pdf2image import convert_from_path
from PIL import Image
import zipfile
import shutil
import re
import os


'''






'''
Image.MAX_IMAGE_PIXELS = None



def pdf_to_jpg(pdf_path, output_folder, basename,dpix):
    try:
        images= convert_from_path(
        pdf_path=pdf_path, 
        dpi=dpix, 
        fmt="jpeg",
        output_folder=output_folder,
        )
        pages=len(images)
        os.chdir(output_folder)
        listout=os.listdir()
        listpack=[]
        listf=[]
        for tte in listout:
            underscore_index = tte.rfind("-")
            dot_index = tte.rfind(".")
            number_str = tte[underscore_index + 1:dot_index]
            number = int(number_str)
            listpack.append([tte,number])
    
        for i in range(pages):
            for j in listpack:
                if j[1]==i+1:
                    listf.append(j[0])
    
        print(os.getcwd())

        del images

        for i in range(pages):
            os.rename(listf[i], f"{basename}_{i + 1}.jpg")

        os.chdir(f"{output_folder}/..")

        print(f"{basename}completed")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise RuntimeError(f"Failed to convert PDF to JPG: {e}")     
    



        



def extract_jpg_from_epub(epub_path, output_folder,basename):
    try:
        create_new_folder("reload_folder")
        htmlchick=[]
        jpgchick=[]
    #1.创建reload_folder,初始化htmlchick

        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            zip_ref.extractall("reload_folder")
    #2.解压epub文件至reload_folder

        listncx=os.listdir(os.path.join(os.getcwd(),"reload_folder","xml"))
        os.chdir(os.path.join(os.getcwd(),"reload_folder","xml"))  
    #3.下沉至<xml>
        
        with open(listncx[0], "r", encoding="utf-8") as file:
            for line in file:
  
                pattern = r'<content src="([^"]+)"/>'
                match = re.search(pattern, line)
                if match:
            # 提取URL并添加到htmlchick列表中
                    htmlchick.append(os.path.basename(match.group(1)))        
    #4.读取.ncx文件
    #5.读取.ncx文件中的<content>标签
    #6.htmlchick.append["page-241495.html"]

        os.chdir(os.path.join(os.getcwd(),".."))
        os.chdir(os.path.join(os.getcwd(),"html"))
    #7.上浮至<reload>
    #8.下沉至<html>
        
        for i in htmlchick:
            with open(i, "r", encoding="utf-8") as file:
                for line in file:
                    pattern = r'<img[^>]*src="[^"]*/([^"]+)"'
                    match = re.search(pattern, line)
                    if match:
                        path=os.path.basename(match.group(1))
                        jpgchick.append(path)

        os.chdir(os.path.join(os.getcwd(),".."))
        output_folder = os.path.join(os.getcwd(), "..", output_folder)

        for i in os.listdir(os.path.join(os.getcwd(), "image")):
            #print(i)
            if i =="cover.jpg":
                shutil.copy(os.path.join("image", i), os.path.join(output_folder, f"{basename}_cover.jpg"))
                print(f"{basename}_cover.jpg completed")
                break

        for i in  range(len(jpgchick)):
            shutil.copy(os.path.join("image", jpgchick[i]), os.path.join(output_folder, f"{basename}_{i + 1}.jpg")) 
            print(f"{basename}_{i + 1}.jpg completed")                                 
    #9.由htmlchick读取html文件
         #10.读取html文件中的<img>标签
         #11.读取<img>标签中的src属性保存为path
         #12.save jpg as basename+n

        os.chdir(os.path.join(os.getcwd(),".."))
        shutil.rmtree("reload_folder")

        print(f"{basename}completed")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise RuntimeError(f"Failed to extract JPG from EPUB: {e}")


    #13.del reload     








def create_new_folder(folder_name):
    new_folder_path = os.path.join(os.getcwd(), folder_name)
    os.makedirs(new_folder_path)
    return new_folder_path






firstpath=os.getcwd()
#当前文件夹路径

folderkik=[]
#存放文件夹名称

pdfturn=[]
#存放pdf文件路径与名字    ["/1/XXXXX.pdf","XXXXXX.pdf"]
epubturn=[]
#存放epub文件路径与名字    ["/1/XXXXX.epub","XXXXXX.epub"]


file_list = os.listdir(firstpath)

# 获取当前文件夹中的所有文件名


for file in file_list:
    if os.path.isdir(file):
        folderkik.append(file)
    elif file.endswith('.pdf'):
        pdfturn.append([file,file.replace(".pdf","")])
    elif file.endswith('.epub'):
        epubturn.append([file,file.replace(".epub","")])


if len(folderkik)!=0:
    for i in folderkik:
        if len(os.listdir(i)) != 0:
            file_list_i = os.listdir(i)
            for file in file_list_i:
                if file.endswith('.pdf'):
                    pdfturn.append([i+"/"+file,file.replace(".pdf","")])
                elif file.endswith('.epub'):
                    epubturn.append([i+"/"+file,file.replace(".epub","")])

print(pdfturn)
print(epubturn)
print(folderkik)



if len(pdfturn) != 0:
    for file in pdfturn:
        print(f"Processing {file[0]}")
        new_folder_path = create_new_folder(file[1])
        pdf_to_jpg(file[0], new_folder_path, file[1],200)


if len(epubturn) != 0:
    for file in epubturn:
        print(f"Processing {file[0]}")
        new_folder_path = create_new_folder(file[1])
        extract_jpg_from_epub(file[0], new_folder_path, file[1])




#pdf_to_jpg('第0话 妹妹与敞不开的房间①.pdf',"test","test")