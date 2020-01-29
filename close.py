import win32com.client
Excel = win32com.client.Dispatch('Excel.Application')
wb = Excel.Workbooks.Open(r'E:\test1\Result.xlsx')
wb.Save()
wb.Close()
Excel.Quit()