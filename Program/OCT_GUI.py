from tkinter.filedialog import *
from tkinter.simpledialog import *
import cv2
import numpy as np
from matplotlib import path
import openpyxl




########################################  함수 #############################################
def draw_circle(event, x, y, flags, param):
    global img2
    global OpenCV_Check
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img2, (x, y), 2, (255, 255, 255), -1)
        list_x.append(x)
        list_y.append(y)
        if len(list_x) >= 2 and  len(list_y) >= 2:
            for i in range(len(list_x)-1):
                cv2.line(img2, (list_x[i], list_y[i]), (list_x[i+1], list_y[i+1]), (0, 255, 0), 2 )

    if event == cv2.EVENT_RBUTTONDOWN:
        OpenCV_Check = True
        list_x.clear()
        list_y.clear()
        Load_image()

def onChange(emp):
    pass

def Load_image():
    OpenCV_Check = False

    if len(list_x) >= 0 and len(list_y) >= 0 :
        list_x.clear()
        list_y.clear()
    global img2
    global image
    global mask
    global FolderName

    while True:
        file = askopenfilename()
        # file = "test1.bmp"
        st = file.split("/")
        FileName = st[-1]
        FolderName = st[-2]

        if len(FolderName) < 9:
            FolderName = st[-3]

        try:
        #이미지 불러오기
            Img = cv2.imread(file , cv2.IMREAD_COLOR)
            height , width = Img.shape[:2]
            break
        except:
            if file == "":
                break
            messagebox.showerror("이미지 에러" , "이미지 파일을 불러오는중 오류가 발생하였습니다.")
            continue


    edges = cv2.Canny(Img, Canny_X, Canny_X * 3, apertureSize=3)
    gray = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    minLineLength = 400
    maxLineGap = 100
    lines = cv2.HoughLinesP(edges, 1, np.pi / 360, 100, minLineLength, maxLineGap)


    for i in range(len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            cv2.line(Img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.line(Img, (y1, x1), (y2, x2), (0, 0, 255), 3)
            if x2 - x1 == 0:
                length = y2 - y1
            else:
                length = x2 - x1
    img2 = Img[0:length+10 , length+20:width]
    height, width = img2.shape[:2]
    img2 = cv2.pyrUp(img2, dstsize=(width * 2, height * 2), borderType=cv2.BORDER_DEFAULT)

    image = img2.copy()
    copy_img = img2.copy()
    while True:
        cv2.imshow('image', img2)
        cv2.setMouseCallback("image", draw_circle)
        if cv2.waitKey(1) & 0xFF == (ord("c")):
            cv2.destroyAllWindows()
            break
        if OpenCV_Check == True:
            cv2.destroyAllWindows()
            break

    if len(list_x) > 0 or len(list_y) > 0 :
        point1 = np.array([list_x, list_y], np.int32)
        point1 = point1.T
        green = (255, 255, 255)
        cv2.fillPoly(copy_img, [point1], green)

    # 영역 자르기
        mask = cv2.bitwise_xor(img2, copy_img)

        cv2.imshow("mask" , mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        OpenCV_Check = False
    else:
        mask = img2

def Draw_Micro():
    #미세혈관 영역 생성 => 기본 이미지 image
    #point1 -> 사용자의 폴리곤
    #point2 -> 아랫변 생성
    global point2
    tmp_x.clear()
    tmp_y.clear()

    point1 = np.array([list_x, list_y], np.int32)
    point1 = point1.T

    p1 = path.Path(point1)
    draw_img = image.copy()
    if len(user_list) > 0:
        user_list.clear()
        ############################ core code ###############################
    if list_x[0] <= list_x[-1]:
        list_x[-1] = list_x[0] - 1

    if list_y[0] <= list_y[-1]:
        list_y[-1] = list_y[0] - 1

        ############################ core code ###############################

    cv2.polylines(draw_img , [point1] ,True , (0,0,255) , 2)
    x = list_x
    y = list_y
    emp_y = []
    for i in y:
        user_list.append(i + user_input)
        # emp_y.append(i - 2)

    if (x.index(max(x)) > x.index(min(x))):
        x.reverse()
        y.reverse()
        for i in range(x.index(min(x)), x.index(max(x)) + 1):
            tmp_x.append(x[i])
            tmp_y.append(y[i])

        # 새 리스트에 아랫변 삽입
        for i in range(x.index(max(x)), x.index(min(x)) - 1, -1):
            tmp_x.append(x[i])
            tmp_y.append(user_list[i])

    else:
        for i in range(x.index(max(x)), x.index(min(x)) + 1):
            tmp_x.append(x[i])
            tmp_y.append(y[i])

        # 새 리스트에 아랫변 삽입
        for i in range(x.index(min(x)), x.index(max(x)) - 1, -1):
            tmp_x.append(x[i])
            tmp_y.append(user_list[i])

    point2 = np.array([tmp_x, tmp_y], np.int32)
    point2 = point2.T
    p2 = path.Path(point2)

    cv2.polylines(draw_img, [point2], True, (255, 0, 0), 2)

    cv2.imshow("Draw_micro" , draw_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def Basic_Threshold():
    # 기본 이진화
    global basic_Threshold
    global Check_basic
    global thresh , maxval
    img = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow("Basic_Threshold", cv2.WINDOW_AUTOSIZE)
    ret, basic_Threshold = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    cv2.createTrackbar('thresh', 'Basic_Threshold', 0, 255, onChange)
    cv2.createTrackbar('maxval', 'Basic_Threshold', 0, 255, onChange)
    switch = "0: OFF\n1: ON"
    cv2.createTrackbar(switch, 'Basic_Threshold', 0, 1, onChange)

    while True:
        cv2.imshow('Basic_Threshold', basic_Threshold)

        if cv2.waitKey(1) & 0xFF == (ord("c")):
            cv2.destroyAllWindows()
            break

        thresh = cv2.getTrackbarPos('thresh', 'Basic_Threshold')
        maxval = cv2.getTrackbarPos('maxval', 'Basic_Threshold')
        s = cv2.getTrackbarPos(switch, 'Basic_Threshold')
        if s == 0:
            basic_Threshold[:] = 0
        else:
            ret, basic_Threshold = cv2.threshold(img, thresh, maxval, cv2.THRESH_BINARY)
    cv2.destroyAllWindows()
    Check_basic = True

def Adptive_Threshold():
    # 적응 이진화
    global dst
    global Check_dst
    global blockSize , del_num
    img = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow("Adptive_Threshold", cv2.WINDOW_AUTOSIZE)
    dst = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 0)

    cv2.createTrackbar('blockSize', 'Adptive_Threshold', 13, 255, onChange)
    cv2.createTrackbar('del_num', 'Adptive_Threshold', 0, 10, onChange)
    switch = "0: OFF\n1: ON"
    cv2.createTrackbar(switch, 'Adptive_Threshold', 0, 1, onChange)

    while True:
        cv2.imshow('Adptive_Threshold', dst)

        if cv2.waitKey(1) & 0xFF == (ord("c")):
            cv2.destroyAllWindows()
            break

        blockSize = cv2.getTrackbarPos('blockSize', 'Adptive_Threshold')
        del_num = cv2.getTrackbarPos('del_num', 'Adptive_Threshold')
        s = cv2.getTrackbarPos(switch, 'Adptive_Threshold')
        if s == 0:
            dst[:] = 0
        else:
            if blockSize % 2 == 0:
                blockSize = blockSize + 1
            if blockSize < 3:
                blockSize = 3
            dst = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, del_num)
    cv2.destroyAllWindows()
    Check_dst = True


def Basic_Threshold_Check():
    # 기본 이진화 변수
    # thresh =0 ; maxval = 0
    if thresh == 0 and maxval == 0:
        Real_Cheaker("Basic" , 0 , 0)
    else:
        Real_Cheaker("Basic" , thresh , maxval)

def Adptive_Threshold_Cheak():
    # 적응 이진화 변수
    # blockSize = 0; del_num = 0
    if blockSize == 0 and del_num == 0:
        Real_Cheaker("Adp" , 0 , 0)
    else:
        Real_Cheaker("Adp" , blockSize, del_num)


def Real_Cheaker(*para):
    global all_pixels
    global vessel_pixels
    global Micro_vessel_pixels
    global Micro_all_vessel_pixels
    if len(tmp_x) <= 0 and len(tmp_y) <= 0:
        Draw_Micro()
    image = img2.copy()
    copy_img = img2.copy()
    p2 = path.Path(point2)

    x = list_x
    y = list_y

    point1 = np.array([list_x, list_y], np.int32)
    point1 = point1.T
    p1 = path.Path(point1)

    all_pixels = 0  # 전체 픽셀
    vessel_pixels = 0  # 전체 혈관 픽셀
    Micro_all_vessel_pixels = 0  # 미세혈관 전체 픽셀
    Micro_vessel_pixels = 0  # 미세혈관 픽셀

    if len(list_x) > 0 or len(list_y) > 0:
        point1 = np.array([list_x, list_y], np.int32)
        point1 = point1.T
        green = (255, 255, 255)
        cv2.fillPoly(copy_img, [point1], green)

        # 영역 자르기
        mask = cv2.bitwise_xor(img2, copy_img)
    if len(tmp_x) <= 0 or len(tmp_y) <= 0:
        Draw_Micro()

    if para[0] == "Basic":
        if para[1] == 0 and para[2] == 0:
        # 이진화 시키기
            img = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            ret, basic_Threshold = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        else:
            img = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            ret, basic_Threshold = cv2.threshold(img, para[1], para[2], cv2.THRESH_BINARY)

        for i in range(min(x), max(x) - 1):  # x
            for j in range(min(y), max(y) - 1):  # y
                if p2.contains_points([(i, j)]):
                    all_pixels += 1
                    if basic_Threshold[j, i] == 0:
                        vessel_pixels += 1

        CVI = (vessel_pixels / all_pixels) * 100

        messagebox.showinfo("info","  혈관 넓이 : {0} \n  혈관 값  : {1}\n  CVI 값 \t   :{2:0.2f}%".format(all_pixels, vessel_pixels, CVI))
        label1.configure(text="\t혈관 넓이 : {0}".format(all_pixels) ,fg = "white" ,bg = "black")
        label2.configure(text="\t혈관 값 :   {0}".format(vessel_pixels), fg="white", bg="black")
        label3.configure(text="\tCVI  값 :   {0:0.2f}%".format(CVI), fg="white", bg="black")
        FolderName_list.append(FolderName)
        all_pixels_list.append(all_pixels)
        vessel_pixels_list.append(vessel_pixels)
        cvi1_list.append(CVI)
        Micro_all_vessel_pixel_list.append("")
        Micro_vessel_pixel_list.append("")
        cvi2_list.append("")

    else:
        if para[1] == 0 and para[2] == 0:
        # 이진화 시키기
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            dst = cv2.adaptiveThreshold(mask, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 33, 0)
        else:
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            dst = cv2.adaptiveThreshold(mask, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, para[1], para[2])
        for i in range(min(x), max(x) - 1):  # x
            for j in range(min(y), max(y) - 1):  # y
                if p2.contains_points([(i, j)]):
                    Micro_all_vessel_pixels += 1
                    if dst[j, i] == 0:
                        Micro_vessel_pixels += 1

        CVI = (Micro_vessel_pixels / Micro_all_vessel_pixels) * 100
        messagebox.showinfo("info","  미세혈관 넓이 : {0} \n  미세혈관 값 : {1}\n CVI 값 \t   :{2:0.2f}%".format(Micro_all_vessel_pixels,Micro_vessel_pixels, CVI))
        label1.configure(text="\t미세혈관 넓이 : {0}".format(Micro_all_vessel_pixels), fg="white", bg="black")
        label2.configure(text="\t미세혈관 값 :   {0}".format(Micro_vessel_pixels), fg="white", bg="black")
        label3.configure(text="\tCVI  값 :       {0:0.2f}%".format(CVI), fg="white", bg="black")
        FolderName_list.append(FolderName)
        all_pixels_list.append("")
        vessel_pixels_list.append("")
        cvi1_list.append("")
        Micro_all_vessel_pixel_list.append(Micro_all_vessel_pixels)
        Micro_vessel_pixel_list.append(Micro_vessel_pixels)
        cvi2_list.append(CVI)

    tmp_x.clear()
    tmp_y.clear()

    # 아래 변수들 전역변수로 저장하기 변수 명도 변경하기
    #


def Save_Excel():
    ftypes = [('엑셀 파일', '.xlsx'), ('All files', '*')]
    title = '파일명 입력'
    ExcelFile = asksaveasfilename(filetypes = ftypes , title = title , initialfile='OCT.xlsx' )
    write_wb = openpyxl.Workbook()
    write_ws = write_wb['Sheet']
    # 이름이 있는 시트를 생성
    # write_ws = write_wb.create_sheet('Sheet1')
    ######
    # Sheet1에다 입력
    # write_ws = write_wb.active
    write_ws['A1'] = '환자 번호'  ## FolderName
    write_ws['B1'] = '혈관 넓이'
    write_ws['C1'] = '혈관   값'
    write_ws['D1'] = '맥락막 CVI'
    write_ws['E1'] = '미세혈관 넓이'
    write_ws['F1'] = '미세혈관   값'
    write_ws['G1'] = '미세혈관  CVI'
    try:
        # 리스트로 저장해서 값 추가
        for i in range(len(FolderName_list)):
            write_ws.append([FolderName_list[i],all_pixels_list[i], vessel_pixels_list[i], cvi1_list[i],
                             Micro_all_vessel_pixel_list[i], Micro_vessel_pixel_list[i], cvi2_list[i]])
        if ExcelFile.find("xlsx") == -1:
            write_wb.save(ExcelFile + ".xlsx")
        else:
            write_wb.save(ExcelFile)
            messagebox.showinfo("info", "저장 완료!")

    except:
        messagebox.showerror("Error" , "엑셀로 저장에 실패하였습니다.")
def Save_txt():
    # TxtFile = askopenfilename
    # if exist TxtFile
    # 내용 추가하기
    # else
    # 새로 메모장 작성하기
    pass


def Change_Canny():
    global Canny_X
    X = askinteger(title = "Canny 변수 입력" , prompt="Canny 변수 값을 설정하세요 : ")
    Canny_X = X

def Change_UserInput():
    global user_input
    X = askinteger(title = "아랫변수 입력" , prompt="미세혈관의 영역크기를 설정하세요 : ")
    print(X)
    user_input = X // (200 // 50)
def esc():
    window.quit()
    window.destroy()


########################## 변수 선언 ##################################

# file  파일 정보를 담을 변수
# Img  이미지 변수
# x , y 좌표 정보를 담을 리스트
# height , width 이미지 파일의 크기를 담을 변수 -> 확대시 사용
# OpenCV_Cheak openCV가 실행중인지 체크할 bool 값
# Canny_X => OCT 이미지 녹색 선을 체크하기 위한 값 , 옵션으로 변경할 수 있다. 값이 낮을 수록 많은 선이 체크됨

file = "test1.bmp"
list_x = []
list_y = []
height = 0
width = 0
OpenCV_Check = False
Img = ""
Canny_X = 270

#기본 이진화 변수
thresh =0 ; maxval = 0
#적응 이진화 변수
blockSize = 0 ;  del_num = 0

user_list = []
user_input = 120 // (200 // 50)
tmp_x = []
tmp_y = []

FolderName_list = []

all_pixels_list = []
vessel_pixels_list = []
cvi1_list = []

Micro_all_vessel_pixel_list= []
Micro_vessel_pixel_list =[]
cvi2_list = []

###################################### GUI ##############################
window=tkinter.Tk()

window.title("Program_Ieye" )

window.geometry("400x125")
window.resizable(False, False)
window.iconbitmap("II.ico" )
window.configure(background='black')
label1=tkinter.Label(window, text="\t혈관 넓이 : " , fg = "white" , background = "black")
label2=tkinter.Label(window, text="\t혈관 값 : " , fg = "white" , background = "black")
label3=tkinter.Label(window, text="\tCVI  값 : " , fg = "white" , background = "black")
label4=tkinter.Label(window, text="\t정상인의 평균 미세혈관 CVI : 40%~70%" , fg = "white" , background = "black")
label1.place(x = "0" , y = "0")
label2.place(x = "0" , y = "25")
label3.place(x = "0" , y = "50")
label4.place(x = "30" , y = "75")


menubar=tkinter.Menu(window)

menu_1=tkinter.Menu(menubar, tearoff = 0  ,bg="black" , fg = "white" )
menu_1.add_command(label="이미지 불러오기", command=Load_image)
menu_1.add_command(label="미세혈관 영역 생성", command=Draw_Micro)
menu_1.add_command(label="기본 이진화" , command = Basic_Threshold)
menu_1.add_command(label="적응 이진화" , command = Adptive_Threshold)

menubar.add_cascade(label="이미지 관련 메뉴", menu=menu_1)

menu_2=tkinter.Menu(menubar, tearoff=0 , bg="black" , fg = "white" )
menu_2.add_command(label="기본 이진화로 측정" , command = Basic_Threshold_Check)
menu_2.add_command(label="적응 이진화로 측정" , command = Adptive_Threshold_Cheak)
menu_2.add_command(label="엑셀 으로 저장하기" , command = Save_Excel)

menubar.add_cascade(label="측정 관련 메뉴", menu=menu_2)

menu_3=tkinter.Menu(menubar, tearoff=0 , bg="black" , fg = "white" )
menu_3.add_command(label="Canny 값 변경" , command = Change_Canny)
menu_3.add_command(label="아랫변 변경" , command = Change_UserInput )
menu_3.add_command(label="프로그램 종료" , command = esc)

menubar.add_cascade(label="프로그램 관련 메뉴", menu=menu_3)

window.config(menu=menubar)
window.mainloop()
