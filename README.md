# pyCASW (A Python-based framework for Coupled Analysis of Input Intensity and Output Intensity of Arable Land Based on Sliding Windows)
pyCASW is a GUI (graphical user interface) made in tkinter for coupled analysis of input intensity and output intensity of arable land based on sliding windows. It integrates correlation and partial correlation analysis. By calculating the correlation coefficient between input intensity and output intensity in different value ranges, the influence process of input intensity on output intensity can be explained.<br><br>
Usage:<br>
1.Input:<br>
      •	Click “Select File” to select a csv file (Each sample of the csv file needs to be organized by line, and columns represent indicators.).<br>
2.Parameter setting:<br>
      •	Select the correlation analysis mode and the mode of sliding on demand.<br>
      •	Select the independent variable and dependent variable participating in the analysis in the combo box.<br>
      •	Select control variables of partial correlation analysis in list box.<br>
      •	Click “Scatter Chart” can visualize independent and dependent variables through scatter plot.<br>
      •	The size and step width of the sliding window can be set in the text box (The default value of the size is the total number of samples or the value range of independent variables decided by the sliding mode that the user chooses, and the default value of the step is 1.).<br>
3.Output:<br>
      •	Click “Calculate” can draw scatter plot of mean value of each value range and correlation coefficient. <br>
      • Click “save” can output the result of correlation and partial correlation analysis as a csv file.<br>

<br>
Note: Test data is provided. The researchers in many fields may benefit from pyCASW by obtaining a fast way to analysis the coupling relationship between multiple variables in complex systems.<br>
Thank you for using pyCASW!
