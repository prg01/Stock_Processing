# importing csv module 
import csv 
import time
import datetime
  
# csv file name 
#filename = "snp.csv"
filename_in   = "all_stocks_5yr.csv"
filename_out  = "all_stocks_5yr_updated.csv"
  
# initializing the titles and rows list 
fields = [] 
rows = [] 
# The counter to measure the total number of different stock symbols.
N = 1
cnt_20 = 0
cnt_50 = 0

close_20 = 0
close_50 = 0

ratio_20 = 0
ratio_50 = 0

# The array to store closing values for 20 and 50 mean value
arr_close_20 = []
arr_close_20.append(float(0))
arr_close_50 = []
arr_close_50.append(float(0))

# The counter to measure the total data points of each stock symbols.
data_cnt = 0

# The max value for each day.
max_value = 0
current_year = 0
prev_year = 0

# Array to store the number of data points of each stock synbol. This will be N deep array.
stock_data_pnt = []

# internal counter i
i = 0
j = 0

# to measure elasped time
start_time = time.time()

# Array to store the time plots
elapsed_time = []
 
# reading csv file 
with open(filename_in, 'r') as in_csvfile, open(filename_out, 'w') as out_csvfile: 
    # creating a csv reader object 
    csvreader = csv.reader(in_csvfile) 
    csvwriter = csv.writer(out_csvfile) 
      
    # extracting field names through first row 
    fields = csvreader.next() 
    fields_new = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_20', 'Ratio_20', 'Close_50', 'Ratio_50', 'Name']
    print(fields)
    print(fields_new)
    # Writing field names through first row 
    csvwriter.writerow(fields_new) 
  
    # extracting each data row one by one 
    for row in csvreader: 
        rows.append(row) 

        prev_year = current_year
        date = datetime.datetime.strptime(rows[i][0], "%Y-%m-%d")
        current_year = date.year
        close_curr = float(rows[i][4])
        if ((i > 0) and (rows[i][6] != rows[i-1][6])):
          # Logic for moving average
          cnt_20 = 0
          cnt_50 = 0
          close_20 = (sum(arr_close_20) + close_curr)/20
          close_50 = (sum(arr_close_50) + close_curr)/20
          ratio_20 = close_curr/close_20
          ratio_50 = close_curr/close_50

          stock_data_pnt.append(i)
          stock_data_pnt[N-1] = data_cnt
          if (max_value < rows[i-1][2]):
            max_value = rows[i-1][2]
          print("The max value of stock %s: for the year %s: is %s:"%(rows[i-1][6],prev_year,max_value))
          max_value = rows[i][2]
          #print(current_year)
          N += 1
          data_cnt = 1
          if (N == 2 or N == 11 or N == 101 or N == 201 or N == 301 or N == 401 or N == 501):
            elapsed_time.append(j)
            elapsed_time[j] = time.time() - start_time
            print(elapsed_time[j])
            j += 1
        #elif (i > 0):
        else:
          # Running Average logic
          #print("NEW DATA")
          #print(cnt_50)
          #print(close_curr)
          #print(sum(arr_close_50))
          #print((sum(arr_close_50)) + close_curr)
          #print(cnt_50 + 1)
          if (cnt_50 >= 1):
            if (cnt_50 <= 48):
              arr_close_50.append(float(cnt_50))
              close_50 = float((float(sum(arr_close_50)) + close_curr)/float((cnt_50 + 1)))
            else:
              close_50 = float((float(sum(arr_close_50)) + close_curr)/float(50))
          else:
            close_50 = close_curr

          ratio_50 = close_curr/close_50

          #print(close_50)
          #print(ratio_50)
          
          if (cnt_20 >= 1):
            if (cnt_20 <= 18):
              arr_close_20.append(float(cnt_20))
              close_20 = float((float(sum(arr_close_20)) + close_curr)/float((cnt_20 + 1)))
            else:
              close_20 = float((float(sum(arr_close_20)) + close_curr)/float(20))
          else:
            close_20 = close_curr

          ratio_20 = close_curr/close_20
          row_new = rows[i][:6] + [close_20, ratio_20, close_50, ratio_20, rows[i][6]]
          csvwriter.writerow(row_new) 

          arr_close_50[cnt_50 % 49] = close_curr
          arr_close_20[cnt_20 % 19] = close_curr

          cnt_20 += 1
          cnt_50 += 1
          # END Running Average logic

          if (i == 0):
            max_value = rows[0][2]
          if ((max_value < rows[i][2]) and (prev_year == current_year)):
            max_value = rows[i][2]
          if ((i >0) and (current_year != prev_year)):
            print("The max value of stock %s: for the year %s: is %s:"%(rows[i-1][6],prev_year,max_value))
            max_value = rows[i][2]
          data_cnt += 1
        i += 1
 
    # get total number of rows 
    print("The max value of stock %s: for the year %s: is %s:"%(rows[i-1][6],current_year,max_value))

print("LOOP unrolling starts!!!")

# new start time
start_time_1 = time.time()

# Array to store the time plots
elapsed_time_1 = []

# Since we are unrolling by 5. Each row will have a year value. so we need 5 year value variable to store this information.
# We need one more year variable to store the data from last row of previous set. Since the comparison is a continous one.
# prev years
prev_year_5 = 0 # This represents the year for the last row from the previous set of 5.
prev_year_4 = 0 # Eq to k = 0 
prev_year_3 = 0 # Eq to k = 1 
prev_year_2 = 0 # Eq to k = 2 
prev_year_1 = 0 # Eq to k = 3 
current_year_1 = 0 # Eq to k = 4 

N = 1

#
symbl_0 = "TEMP"

# large value for each day
large = []

# New range for unrolling
range_int = i/5             # We are unrolling by 5
                                # Range int gives us the quotient of divisiblity by 5
range_loop = (range_int*5) -1   # Max range of main loop. We reach to this value by following logic
                                # Suppose i is 24, range_int will be 4 i
                                # So max range of for loop will be 0 to 19.
                                # Because if we take it to 20 another for loop will trigger, taking the count to 25.
overflow = i%5
data_cnt_1 = 0

# counters
k = 0
l = 0


for k in range(0,range_loop,5):
   prev_year_5 = current_year_1
   date = datetime.datetime.strptime(rows[k][0], "%Y-%m-%d")
   prev_year_4 = date.year
   date = datetime.datetime.strptime(rows[k+1][0], "%Y-%m-%d")
   prev_year_3 = date.year
   date = datetime.datetime.strptime(rows[k+2][0], "%Y-%m-%d")
   prev_year_2 = date.year
   date = datetime.datetime.strptime(rows[k+3][0], "%Y-%m-%d")
   prev_year_1 = date.year
   date = datetime.datetime.strptime(rows[k+4][0], "%Y-%m-%d")
   current_year_1 = date.year
   large = [rows[k][2],rows[k+1][2],rows[k+2][2],rows[k+3][2],rows[k+4][2]]
   # current 5 symbols to be processed plus the last symbol for previous group for continous comparison
   symbl_5 = symbl_0
   symbl_4 = rows[k][6]
   symbl_3 = rows[k+1][6]
   symbl_2 = rows[k+2][6]
   symbl_1 = rows[k+3][6]
   symbl_0 = rows[k+4][6]
   # This if else section checks if the symbol has changed
   # If the symbol changes from old_symbol to new_symbol than we print the max_value for the old_symbol for the latest year.
   # We also maintain the counter to check the elapsed time since that depends on how many symbols have been processed.
   if ((symbl_5 != symbl_4) and (k > 0)):
     stock_data_pnt.append(k)
     stock_data_pnt[N-1] = data_cnt_1
     print("The max value of stock %s: for the year %s: is %s:"%(symbl_5,prev_year_5,max_value_1))
     # Since the symbol changed happened for the first data of new set itself
     # we update the max_value to the first days' largest value of the new symbol
     max_value_1 = large[0]
     # Line intentionally left vacant
     N += 1
     data_cnt_1 = 1
     if (N == 2 or N == 11 or N == 101 or N == 201 or N == 301 or N == 401 or N == 501):
       elapsed_time_1.append(l)
       elapsed_time_1[l] = time.time() - start_time_1
       print(elapsed_time_1[l])
       l += 1
   elif (symbl_4 != symbl_3):
     stock_data_pnt.append(k)
     stock_data_pnt[N-1] = data_cnt_1
     # Since the symbol changed happened after the first data of new set
     # we need to compare and update max_value with all the data from old_symbol in the current unrolled group
     # Here only 1 comparison needed
     if (max_value_1 < large[0]):
       max_value_1 = large[0]
     print("The max value of stock %s: for the year %s: is %s:"%(symbl_4,prev_year_4,max_value_1))
     # Since the symbol changed happened
     # we update the max_value to the first days' largest value of the new symbol
     max_value_1 = large[1]
     # Line intentionally left vacant
     N += 1
     data_cnt_1 = 1
     if (N == 2 or N == 11 or N == 101 or N == 201 or N == 301 or N == 401 or N == 501):
       elapsed_time_1.append(l)
       elapsed_time_1[l] = time.time() - start_time_1
       print(elapsed_time_1[l])
       l += 1
   elif (symbl_3 != symbl_2):
     stock_data_pnt.append(k)
     stock_data_pnt[N-1] = data_cnt_1
     # Since the symbol changed happned after the first data of new set
     # we need to compare and update max_value with all the data from old_symbol in the current unrolled group
     # Here 2 comparison needed
     if (max_value_1 < large[0]):
       max_value_1 = large[0]
     if (max_value_1 < large[1]):
       max_value_1 = large[1]
     # Line intentionally left vacant
     print("The max value of stock %s: for the year %s: is %s:"%(symbl_3,prev_year_3,max_value_1))
     # Since the symbol changed happened
     # we update the max_value to the first days' largest value of the new symbol
     max_value_1 = large[2]
     N += 1
     data_cnt_1 = 1
     if (N == 2 or N == 11 or N == 101 or N == 201 or N == 301 or N == 401 or N == 501):
       elapsed_time_1.append(l)
       elapsed_time_1[l] = time.time() - start_time_1
       print(elapsed_time_1[l])
       l += 1
   elif (symbl_2 != symbl_1):
     stock_data_pnt.append(k)
     stock_data_pnt[N-1] = data_cnt_1
     # Since the symbol changed happened after the first data of new set
     # we need to compare and update max_value with all the data from old_symbol in the current unrolled group
     # Here 3 comparison needed
     if (max_value_1 < large[0]):
       max_value_1 = large[0]
     if (max_value_1 < large[1]):
       max_value_1 = large[1]
     if (max_value_1 < large[2]):
       max_value_1 = large[2]
     # Line intentionally left vacant
     print("The max value of stock %s: for the year %s: is %s:"%(symbl_2,prev_year_2,max_value_1))
     # Since the symbol changed happened
     # we update the max_value to the first days' largest value of the new symbol
     max_value_1 = large[3]
     N += 1
     data_cnt_1 = 1
     if (N == 2 or N == 11 or N == 101 or N == 201 or N == 301 or N == 401 or N == 501):
       elapsed_time_1.append(l)
       elapsed_time_1[l] = time.time() - start_time_1
       print(elapsed_time_1[l])
       l += 1
   elif (symbl_1 != symbl_0):
     stock_data_pnt.append(k)
     stock_data_pnt[N-1] = data_cnt_1
     # Since the symbol changed happened after the first data of new set
     # we need to compare and update max_value with all the data from old_symbol in the current unrolled group
     # Here 4 comparison needed
     if (max_value_1 < large[0]):
       max_value_1 = large[0]
     if (max_value_1 < large[1]):
       max_value_1 = large[1]
     if (max_value_1 < large[2]):
       max_value_1 = large[2]
     if (max_value_1 < large[3]):
       max_value_1 = large[3]
     print("The max value of stock %s: for the year %s: is %s:"%(symbl_1,prev_year_1,max_value_1))
     # Since the symbol changed happened
     # we update the max_value to the first days' largest value of the new symbol
     max_value_1 = large[4]
     # Line intentionally left vacant
     N += 1
     data_cnt_1 = 1
     if (N == 2 or N == 11 or N == 101 or N == 201 or N == 301 or N == 401 or N == 501):
       elapsed_time_1.append(l)
       elapsed_time_1[l] = time.time() - start_time_1
       print(elapsed_time_1[l])
       l += 1
   else:
     data_cnt_1 += 1
     if (k == 0):
       max_value_1 = rows[k][2]
     else:
       # Since the year changed happened for the first data of new set
       # we need to update max_value with all the first data from new_year in the current unrolled group
       if (prev_year_5 != prev_year_4):
         print("The max value of stock %s: for the year %s: is %s:"%(symbl_5,prev_year_5,max_value_1))
         max_value_1 = large[0]
       # Since the year changed happened after the first data of new set
       # we need to compare and update max_value with all the data from old_year in the current unrolled group
       # Here only 1 comparison needed
       elif (prev_year_4 != prev_year_3):
         if (max_value_1 < large[0]):
           max_value_1 = large[0]
         print("The max value of stock %s: for the year %s: is %s:"%(symbl_4,prev_year_4,max_value_1))
         max_value_1 = large[1]
       # Since the year changed happened after the first data of new set
       # we need to compare and update max_value with all the data from old_year in the current unrolled group
       # Here 2 comparisons needed
       elif (prev_year_3 != prev_year_2):
         if (max_value_1 < large[0]):
           max_value_1 = large[0]
         if (max_value_1 < large[1]):
           max_value_1 = large[1]
         print("The max value of stock %s: for the year %s: is %s:"%(symbl_3,prev_year_3,max_value_1))
         max_value_1 = large[2]
       # Since the year changed happened after the first data of new set
       # we need to compare and update max_value with all the data from old_year in the current unrolled group
       # Here 3 comparisons needed
       elif (prev_year_2 != prev_year_1):
         if (max_value_1 < large[0]):
           max_value_1 = large[0]
         if (max_value_1 < large[1]):
           max_value_1 = large[1]
         if (max_value_1 < large[2]):
           max_value_1 = large[2]
         print("The max value of stock %s: for the year %s: is %s:"%(symbl_2,prev_year_2,max_value_1))
         max_value_1 = large[3]
       # Since the year changed happened after the first data of new set
       # we need to compare and update max_value with all the data from old_year in the current unrolled group
       # Here 4 comparisons needed
       elif (prev_year_1 != current_year_1):
         if (max_value_1 < large[0]):
           max_value_1 = large[0]
         if (max_value_1 < large[1]):
           max_value_1 = large[1]
         if (max_value_1 < large[2]):
           max_value_1 = large[2]
         if (max_value_1 < large[3]):
           max_value_1 = large[3]
         print("The max value of stock %s: for the year %s: is %s:"%(symbl_1,prev_year_1,max_value_1))
         max_value_1 = large[4]
       # No year change
       # we need to compare and update max_value with all the data in the current unrolled group
       # Here 5 comparisons needed
       else:
         if (max_value_1 < large[0]):
           max_value_1 = large[0]
         if (max_value_1 < large[1]):
           max_value_1 = large[1]
         if (max_value_1 < large[2]):
           max_value_1 = large[2]
         if (max_value_1 < large[3]):
           max_value_1 = large[3]
         if (max_value_1 < large[4]):
           max_value_1 = large[4]


if (overflow != 0):
  for k in range (range_loop,range_loop+overflow-1):
  # We do K plus 2 because as per pervious example of 24 value. Range_loop = 19.
  # We have already processed upto 20 now we need to process from 21 so 
  # So K + 2 is range_loop + 2. 19 + 2 = 21 
     if (max_value < row[k+2][2]):
       max_value = row[k+2][2]

print("The max value of stock %s: for the year %s: is %s:"%(rows[k-1][6],current_year_1,max_value_1))


print("Total no. of rows: %d"%(csvreader.line_num)) 
  
# printing the field names 
print('Field names are:' + ', '.join(field for field in fields)) 
# print total number of symbols
print ("Total no. of symbols: %d"%(N)) 

# importing the required module 
import matplotlib.pyplot as plt 
  
# x axis values 
x = [1,10,100,200,300,400,500] 
# corresponding y axis is elapsed_time[] 
  
# plotting the points  
#plt.plot(x, elapsed_time) 

# plotting points as a scatter plot for regular loop 
plt.scatter(x, elapsed_time, color= "blue",  
            marker= ".", s=30, label = "Regular Loop") 

# plotting points as a scatter plot for unrolled loop 
#plt.scatter(x, elapsed_time_1, color= "red",  
#            marker= ".", s=30, label = "Unrolled Loop") 
  
# naming the x axis 
plt.xlabel('Number of Symbols (Companies) Processed') 
# naming the y axis 
plt.ylabel('System time elapsed(Seconds).') 
# plotting legend
plt.legend(loc = 'best')
  
# giving a title to my graph 
plt.title('Benchmark: Processing csv data') 
  
# function to show the plot 
plt.show()



#  printing first 5 rows 
#print('\nFirst 5 rows are:\n') 
#for row in rows[:5]: 
    # parsing each column of a row 
#    for col in row: 
#        print("%10s"%col), 
#    print('\n') 
