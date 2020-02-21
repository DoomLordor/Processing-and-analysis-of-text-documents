import win32com.client
import os
name = input("Имя файла: ")
Excel = win32com.client.Dispatch('Excel.Application')
wb = Excel.Workbooks.Open(os.getcwd() + '\\Results\\{}.xlsx'.format(name))
wb.Save()
wb.Close()
Excel.Quit()