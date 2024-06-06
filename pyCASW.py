# -*- coding: utf-8 -*- 
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from scipy import stats
import pingouin as pg
import chardet
from matplotlib import rcParams

# Create main window
root = tk.Tk()
root.title('pyCASW')
root.geometry('540x380+500+200')
root.resizable(0,0)

config = {
    "font.family":'Arial',
    "axes.unicode_minus": False
}
rcParams.update(config)
plt.rcParams['text.color'] = 'black'

# Filter out columns with numerical types
def screen(df):
    a=df.dtypes
    dfindex=[]
    for i in range(len(a)):
        if(a[i]=="float64" or a[i]=="int64" ):
            dfindex.append(i)
    df1=df.iloc[:,dfindex]
    return df1

# Read CSV files for various data types
def readdf(csv_file_path):
    f=open(csv_file_path, 'rb')
    d = chardet.detect(f.read())['encoding']
    f.close()
    encodings = ['gbk','utf-8','utf-8-sig','GB2312','gb18030']
    if d==encodings[0] :
        df = pd.read_csv(csv_file_path,encoding=encodings[0])
    elif d==encodings[1] :
        df = pd.read_csv(csv_file_path,encoding=encodings[1])
    elif d==encodings[2] :
        df = pd.read_csv(csv_file_path,encoding=encodings[2])
    elif d==encodings[3] :
        df = pd.read_csv(csv_file_path,encoding=encodings[3])
    elif d==encodings[4] :
        df = pd.read_csv(csv_file_path,encoding=encodings[4])
    else:
        df = pd.read_csv(csv_file_path,encoding=d)	
    return df

# Input CSV file
def import_csv_data():
    global v
    global df
    global nrow
    csv_file_path = askopenfilename()
    if csv_file_path.split('.')[-1]=="csv":
        v.set(csv_file_path)
        try:
            df=readdf(csv_file_path)
        except:
            v.set('')
            tk.messagebox.showerror(title='Error', message='The file failed to open!\nPlease check the file path!') 
        else:
            nrow=df.shape[0]        
            numdf=screen(df)        
            cbox1['value']= list(numdf)
            cbox2['value']= list(numdf)
            cbox1.current(0)
            cbox2.current(1)
            #Insert elements to listbox
            listbox1.delete(0, "end")
            for item in list(numdf):
                listbox1.insert("end",item)
    elif csv_file_path=='':
        return
    else:
        tk.messagebox.showerror(title='Error', message='Please select a csv file!') 
      
# Select CSV file
tk.Label(root, text='Input csv file:').grid(row=0, column=0)
v = tk.StringVar()
entry = tk.Entry(root, width=20,textvariable=v).grid(row=0, column=1)
button0=tk.Button(root, text='Select File',command=import_csv_data)
button0.grid(row=0, column=2)

# Set correlation mode
tk.Label(root, text='Mode selection:').grid(row=1, column=0)
site1 = [('Correlation analysis',1),
        ('Partial correlation analysis',2)]
m1 = tk.IntVar()
m1.set(1)
for name, num in site1:
    radio_button1 = tk.Radiobutton(root,text = name, variable = m1,value =num)
    radio_button1.grid(row=1, column=num)

# Set sliding mode
tk.Label(root, text='Set sliding mode:').grid(row=2, column=0)
site2 = [('By the quantity of samples',1),
        ('By the value range\nof independent variable',2)]
m2 = tk.IntVar() 
m2.set(1)
for name, num in site2:
    radio_button2 = tk.Radiobutton(root,text = name, variable = m2,value =num)
    radio_button2.grid(row=2, column=num)

# Select independent and dependent variable
tk.Label(root, text='Select independent\nand dependent variable:').grid(row=3, column=0)
cbox1 = ttk.Combobox(root, state='readonly', width=15)
cbox1.grid(row=3, column=1)
cbox2= ttk.Combobox(root, state='readonly', width=15)
cbox2.grid(row=3, column=2)

# Create sub windows to draw scatter plot
def show1():
    top1=tk.Toplevel()
    top1.resizable(0,0)
    figure = Figure(figsize=(7,5),dpi=100)
    ax = figure.add_subplot(111)
    x = df[cbox1.get()]
    y = df[cbox2.get()]
    ax.scatter(x,y,s=4)
    ax.set_xlabel(str(cbox1.get()),fontproperties = 'Arial',size =12)
    ax.set_ylabel(str(cbox2.get()),fontproperties = 'Arial',size =12)
    canvas = FigureCanvasTkAgg(figure,top1)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)
    canvas.get_tk_widget().pack()   
    top1.mainloop()

# Draw a scatter plot
button1=tk.Button(root, text='Scatter plot',state='disabled', command=show1)
button1.grid(row=4, column=2)

# Display range of independent variables
tk.Label(root, text='Value range of\nindependent variable:').grid(row=4, column=0)
t1 = tkinter.Text(root,width=20, height=1)
t1.grid(row=4, column=1)
t1['state'] = 'disabled'

# Display sample quantity
tk.Label(root, text='Sample quantity:').grid(row=5, column=0)
t2 = tkinter.Text(root,width=20, height=1)
t2.grid(row=5, column=1)
t2['state'] = 'disabled'

#Select control variables of partial correlation analysis
tk.Label(root, text='Select control variables\nof partial correlation analysis:').grid(row=6, column=0)
listbox1 =tk.Listbox(root,selectmode="multiple",exportselection=0,height=5)
listbox1.grid(row=6, column=1)

# Bind dropdown menu event
def func1(event):
    global rmin
    global rmax
    rmin=df[cbox1.get()].min()
    rmax=df[cbox1.get()].max()
    cbox2['value']= list(df)
    e1['state'] = 'normal'
    e2['state'] = 'normal'
    t1['state'] = 'normal'
    t1.delete(0.0, tk.END)
    t1.insert('insert',str(rmin)+"~"+str(rmax))
    t1['state'] = 'disabled'
    t2['state'] = 'normal'
    t2.delete(0.0, tk.END)
    t2.insert('insert',str(nrow))
    t2['state'] = 'disabled'
cbox1.bind("<<ComboboxSelected>>",func1)

def func2(event):
    button1['state'] = 'normal'
    button2['state'] = 'normal'
cbox2.bind("<<ComboboxSelected>>",func2)    

def func3(event):
    button3['state'] = 'normal'

def check1(input):
    try:
        float(input) 
        return True
    except:
        e1.delete(0,tk.END)
        e1.after_idle(lambda: e1.configure(validate="focusout"))
        return False           
CheckValid1=root.register(check1)

def check2(input):
    try:
        float(input) 
        return True
    except:
        e2.delete(0,tk.END)
        e2.after_idle(lambda: e2.configure(validate="focusout"))
        return False   
CheckValid2=root.register(check2)

# Set the size and step width of the sliding window
tk.Label(root, text='Set the size and step width\nof the sliding window:').grid(row=7, column=0)
rstring1 = tk.StringVar()
rstring2 = tk.StringVar()
e1 = tkinter.Entry(root, width=18,state='disabled',textvariable =rstring1,validate ="focusout",validatecommand=(CheckValid1,'%P'))
e1.grid(row=7, column=1)
e2 = tkinter.Entry(root, width=18,state='disabled',textvariable =rstring2,validate ="focusout",validatecommand=(CheckValid2,'%P'))
e2.grid(row=7, column=2)

# save result file
def save():   
    Files = [ ('CSV File', '*.csv')]
    file = asksaveasfile(filetypes=Files, defaultextension=Files)
    resultdf.to_csv(file,line_terminator="\n", encoding="utf_8_sig",index=False) 

# Create sub windows to draw scatter plot of mean value of each range and correlation coefficient
def show2():
    top2=tk.Toplevel()
    top2.title('Scatter plot of mean value of each range and correlation coefficient')
    top2.resizable(0,0)
    tk.Label(top2, text='black: p>=0.05; blue: p<0.05*; green: p<0.01**; red: p<0.001***').pack()
    figure = Figure(figsize=(7,5),dpi=100)
    ax = figure.add_subplot(111)
    resultdf1=resultdf[resultdf['p value']>=0.05]
    resultdf2=resultdf[(resultdf['p value']<0.05)&(resultdf['p value']>=0.01)]
    resultdf3=resultdf[(resultdf['p value']<0.01)&(resultdf['p value']>=0.001)]
    resultdf4=resultdf[resultdf['p value']<0.001]
    x1 = resultdf1["mean value"]
    y1 = resultdf1["correlation coefficient"]
    x2 = resultdf2["mean value"]
    y2 = resultdf2["correlation coefficient"]
    x3 = resultdf3["mean value"]
    y3 = resultdf3["correlation coefficient"]
    x4 = resultdf4["mean value"]
    y4 = resultdf4["correlation coefficient"]
    ax.scatter(x1,y1,s=8,c='k')
    ax.scatter(x2,y2,s=8,c='b')
    ax.scatter(x3,y3,s=8,c='g')
    ax.scatter(x4,y4,s=8,c='r')
    ax.set_xlabel(str(cbox1.get()),fontproperties = 'Arial',size =12)
    ax.set_ylabel(str(cbox2.get()),fontproperties = 'Arial',size =12)
    canvas = FigureCanvasTkAgg(figure,top2)
    canvas.draw()
    canvas.get_tk_widget().pack()
    button3=tk.Button(top2, text='save', command=save).pack()
    top2.mainloop()

def checke1(input):
    if input != "" :   
        try:
            float(input)
            if float(input) <=0 :
                tk.messagebox.showerror(title='Error', message='invalid input!') 
                e1.delete(0,tk.END)
                e1.after_idle(lambda: e1.configure(validate="focusout"))
                return False
            if m2.get()==1:
                try:
                    int(input)
                    if int(input) > nrow :
                        tk.messagebox.showerror(title='Error', message='invalid input!') 
                        e1.delete(0,tk.END)
                        e1.after_idle(lambda: e1.configure(validate="focusout"))
                        return False
                    else:
                        return True
                except:
                    tk.messagebox.showerror(title='Error', message='invalid input!') 
                    return False 
            elif m2.get()==2:          
                if float(input) > rmax-rmin :
                    tk.messagebox.showerror(title='Error', message='invalid input!') 
                    e1.delete(0,tk.END)
                    e1.after_idle(lambda: e1.configure(validate="focusout"))
                    return False
                else:
                    return True
        except:
            tk.messagebox.showerror(title='Error', message='invalid input!') 
            return False    
    else:
        return True

def checke2(input):
    if input != "" :  
        try:
            float(input) 
            if m2.get()==1:
                try:
                    int(input)
                except:
                    tk.messagebox.showerror(title='Error', message='invalid input!') 
                    e2.delete(0,tk.END)
                    e2.after_idle(lambda: e2.configure(validate="focusout"))
                    return False 
            if float(input) <=0 :
                tk.messagebox.showerror(title='Error', message='invalid input!') 
                e2.delete(0,tk.END)
                e2.after_idle(lambda: e2.configure(validate="focusout"))
                return False 
            else:
                return True
        except:
            tk.messagebox.showerror(title='Error', message='invalid input!') 
            e2.delete(0,tk.END)
            e2.after_idle(lambda: e2.configure(validate="focusout"))
            return False
    else:
        return True

def cal():
    global resultdf
    resultdf= pd.DataFrame(columns = ['Interval ID','x','y','control variable','minimum value','maximum value',
                                      'mean value','sample number','correlation coefficient','p value']) 
    try:
        if e1.get()!="":
            float(e1.get())
        if e2.get()!="":
            float(e2.get())
        if checke1(e1.get()) & checke2(e2.get()):
            if m1.get()==1:
                if m2.get()==1: 
                    if e1.get() == "" :
                        qujian = nrow
                        s_pearson = stats.pearsonr(df[cbox1.get()], df[cbox2.get()])
                        resultdf.loc[0]=[1,cbox1.get(),cbox2.get(),"null",rmin,rmax,df[cbox1.get()].mean(),nrow,s_pearson[0],s_pearson[1]]
                        show2()
                    elif e2.get() == "" :
                        qujian = int(e1.get())
                        sortdf=df.sort_values(by=[cbox1.get()])
                        qujiannum=nrow-qujian+1
                        for i in range(qujiannum):
                            cal_df=sortdf[i:i+qujian]
                            s_pearson = stats.pearsonr(cal_df[cbox1.get()], cal_df[cbox2.get()])
                            resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),"null",cal_df[cbox1.get()].min(),cal_df[cbox1.get()].max(),cal_df[cbox1.get()].mean(),qujian,s_pearson[0],s_pearson[1]]
                        show2()
                    elif e2.get() != "":
                        qujian = int(e1.get())
                        buchang=int(e2.get())
                        qujiannum=int((nrow-qujian)/buchang)+1
                        sortdf=df.sort_values(by=[cbox1.get()])
                        for i in range(qujiannum):
                            cal_df=sortdf[i*buchang:i*buchang+qujian]
                            s_pearson = stats.pearsonr(cal_df[cbox1.get()], cal_df[cbox2.get()])
                            resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),"null",cal_df[cbox1.get()].min(),cal_df[cbox1.get()].max(),cal_df[cbox1.get()].mean(),qujian,s_pearson[0],s_pearson[1]]
                        show2()
                if m2.get()==2:
                    if e1.get() == "" :
                        qujian = nrow
                        s_pearson = stats.pearsonr(df[cbox1.get()], df[cbox2.get()])
                        resultdf.loc[0]=[1,cbox1.get(),cbox2.get(),"null",rmin,rmax,df[cbox1.get()].mean(),nrow,s_pearson[0],s_pearson[1]]
                        show2()
                    elif e2.get() == "" :
                        qujian = float(e1.get())
                        qujiannum=int(rmax-rmin-qujian)+1
                        for i in range(qujiannum):
                            cal_df=df[(df[cbox1.get()]>=rmin+i) & (df[cbox1.get()]<=rmin+i+qujian)]
                            if cal_df.shape[0]<2:
                                resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),"null",cal_df[cbox1.get()].min(),cal_df[cbox1.get()].max(),cal_df[cbox1.get()].mean(),cal_df.shape[0],np.nan,np.nan]
                            else:
                                s_pearson = stats.pearsonr(cal_df[cbox1.get()], cal_df[cbox2.get()])
                                resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),"null",cal_df[cbox1.get()].min(),cal_df[cbox1.get()].max(),cal_df[cbox1.get()].mean(),cal_df.shape[0],s_pearson[0],s_pearson[1]]
                        show2()
                    elif e2.get() != "":
                        qujian = float(e1.get())
                        buchang=float(e2.get())
                        qujiannum=int((rmax-rmin-qujian)/buchang)+1
                        for i in range(qujiannum):
                            cal_df=df[(df[cbox1.get()]>=rmin+i*buchang) & (df[cbox1.get()]<=rmin+i*buchang+qujian)]
                            if cal_df.shape[0]<2:
                                resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),"null",cal_df[cbox1.get()].min(),cal_df[cbox1.get()].max(),cal_df[cbox1.get()].mean(),cal_df.shape[0],np.nan,np.nan]
                            else:
                                s_pearson = stats.pearsonr(cal_df[cbox1.get()], cal_df[cbox2.get()])
                                resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),"null",cal_df[cbox1.get()].min(),cal_df[cbox1.get()].max(),cal_df[cbox1.get()].mean(),cal_df.shape[0],s_pearson[0],s_pearson[1]]
                        show2()

            if m1.get()==2:   
                items =[]
                items = listbox1.curselection()
                if len(items)==0:
                    tk.messagebox.showerror(title='Error', message='No control variable selected!') 
                else:
                    ichose = [] 
                    for i in range(len(items)):
                        ichose.append(listbox1.get(items[i]))
                    if cbox1.get() in ichose:
                        tk.messagebox.showerror(title='Error', message='Control variables include the independent variable!')
                    elif cbox2.get() in ichose:
                        tk.messagebox.showerror(title='Error', message='Control variables include the dependent variables!') 
                    else:
                        if m2.get()==1: 
                            if e1.get() == "" :
                                qujian = nrow
                                Pairwise_table=pg.partial_corr(data=df, x=cbox1.get(), y=cbox2.get(), covar=ichose)
                                resultdf.loc[0]=[1,cbox1.get(),cbox2.get(),ichose,rmin,rmax,df[cbox1.get()].mean(),nrow,Pairwise_table['r'][0],Pairwise_table['p-val'][0]]
                                show2()
                            elif e2.get() == "" :
                                qujian = int(e1.get())
                                sortdf=df.sort_values(by=[cbox1.get()])
                                qujiannum=nrow-qujian+1
                                for i in range(qujiannum):
                                    cal_df=sortdf[i:i+qujian]
                                    Pairwise_table=pg.partial_corr(data=cal_df, x=cbox1.get(), y=cbox2.get(), covar=ichose)
                                    resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),ichose,cal_df[cbox1.get()].min(),cal_df[cbox1.get()].max(),cal_df[cbox1.get()].mean(),qujian,Pairwise_table['r'][0],Pairwise_table['p-val'][0]]
                                show2()
                            elif e2.get() != "":
                                qujian = int(e1.get())
                                buchang=int(e2.get())
                                qujiannum=int((nrow-qujian)/buchang)+1
                                sortdf=df.sort_values(by=[cbox1.get()])
                                for i in range(qujiannum):
                                    cal_df=sortdf[i*buchang:i*buchang+qujian]
                                    Pairwise_table=pg.partial_corr(data=cal_df, x=cbox1.get(), y=cbox2.get(), covar=ichose)
                                    resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),ichose,cal_df[cbox1.get()].min(),cal_df[cbox1.get()].max(),cal_df[cbox1.get()].mean(),qujian,Pairwise_table['r'][0],Pairwise_table['p-val'][0]]
                                show2()
                        if m2.get()==2:
                            if e1.get() == "" :
                                qujian = nrow
                                Pairwise_table=pg.partial_corr(data=df, x=cbox1.get(), y=cbox2.get(), covar=ichose)
                                resultdf.loc[0]=[1,cbox1.get(),cbox2.get(),ichose,rmin,rmax,df[cbox1.get()].mean(),nrow,Pairwise_table['r'][0],Pairwise_table['p-val'][0]]
                                show2()
                            elif e2.get() == "" :
                                qujian = float(e1.get())
                                qujiannum=int(rmax-rmin-qujian)+1
                                for i in range(qujiannum):
                                    cal_df=df[(df[cbox1.get()]>=rmin+i) & (df[cbox1.get()]<=rmin+i+qujian)]
                                    if cal_df.shape[0]==0:
                                        resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),ichose,np.nan,np.nan,np.nan,0,np.nan,np.nan]
                                    elif cal_df.shape[0]<3:
                                        resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),ichose,cal_df[cbox1.get()].min(),cal_df[cbox1.get()].max(),cal_df[cbox1.get()].mean(),cal_df.shape[0],np.nan,np.nan]
                                    else:
                                        try:
                                            Pairwise_table=np.nan
                                            Pairwise_table=pg.partial_corr(data=cal_df, x=cbox1.get(), y=cbox2.get(), covar=ichose)
                                        except:
                                            pass
                                        finally:
                                            if type(Pairwise_table) == pd.core.frame.DataFrame:
                                                resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),ichose,cal_df[cbox1.get()].min(),cal_df[cbox1.get()].max(),cal_df[cbox1.get()].mean(),cal_df.shape[0],Pairwise_table['r'][0],Pairwise_table['p-val'][0]]
                                            else:
                                                resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),ichose,cal_df[cbox1.get()].min(),cal_df[cbox1.get()].max(),cal_df[cbox1.get()].mean(),cal_df.shape[0],np.nan,np.nan]
                                show2()
                            elif e2.get() != "":
                                qujian = float(e1.get())
                                buchang=float(e2.get())
                                qujiannum=int((rmax-rmin-qujian)/buchang)+1
                                for i in range(qujiannum):
                                    cal_df=df[(df[cbox1.get()]>=rmin+i*buchang) & (df[cbox1.get()]<=rmin+i*buchang+qujian)]
                                    if cal_df.shape[0]==0:
                                        resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),ichose,np.nan,np.nan,np.nan,0,np.nan,np.nan]
                                    elif cal_df.shape[0]<3:
                                        resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),ichose,cal_df[cbox1.get()].min(),cal_df[cbox1.get()].max(),cal_df[cbox1.get()].mean(),cal_df.shape[0],np.nan,np.nan]
                                    else:
                                        try:
                                            Pairwise_table=np.nan
                                            Pairwise_table=pg.partial_corr(data=cal_df, x=cbox1.get(), y=cbox2.get(), covar=ichose)
                                        except:
                                            pass
                                        finally:
                                            if type(Pairwise_table) == pd.core.frame.DataFrame:
                                                resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),ichose,cal_df[cbox1.get()].min(),cal_df[cbox1.get()].max(),cal_df[cbox1.get()].mean(),cal_df.shape[0],Pairwise_table['r'][0],Pairwise_table['p-val'][0]]
                                            else:
                                                resultdf.loc[i]=[i+1,cbox1.get(),cbox2.get(),ichose,cal_df[cbox1.get()].min(),cal_df[cbox1.get()].max(),cal_df[cbox1.get()].mean(),cal_df.shape[0],np.nan,np.nan]
                                show2()
        else:
            return
    except:
        tk.messagebox.showerror(title='Error', message='Please check the input!') 
        e1.delete(0,tk.END)
        e1.after_idle(lambda: e1.configure(validate="focusout"))
        e2.delete(0,tk.END)
        e2.after_idle(lambda: e2.configure(validate="focusout"))
        top2.destory()
        return


# Calculating button
button2=tk.Button(root, text='Calculate',state='disabled', command=cal)
button2.grid(row=8, column=1)

# Run
root.mainloop()
