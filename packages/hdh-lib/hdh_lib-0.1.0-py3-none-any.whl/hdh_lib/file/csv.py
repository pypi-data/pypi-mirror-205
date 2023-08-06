# csv.py
import os
import logging
import csv        # csv files. e.g. csv.DictWriter

# ================================================================
# Csv Export
# ================================================================
# Writes the given list as a csv format file.
# Inputs: DictArr - Dict array.
# https://docs.python.org/3/library/csv.html 
# TBD Use - with open("myfile.txt", "w") as file1:
#    file1.write("Hello \n")
#    Takes care of closing the file   
def write(DictArr, DstFile, FileAppend) :
  # Prepare the output file
  FileHdrList= []
  for Col in DictArr[0] :
    FileHdrList.append(Col)
  if FileAppend == True :
    file_writer= open(DstFile, 'a')
    csv_writer= csv.DictWriter(file_writer, fieldnames=FileHdrList)
  else :
    file_writer= open(DstFile, 'w')
    # Write the header
    csv_writer= csv.DictWriter(file_writer, fieldnames=FileHdrList)
    csv_writer.writeheader()

  # Prepare the dict used to write each row
  #RowDict= {}
  #for Col in FileHdrList :
  #  RowDict[Col]= ''

  # Write the rows
  for row in DictArr :
    csv_writer.writerow(row)

  # Write complete, close file
  file_writer.close()
  Message= "WriteToCsv(): completed export to " + DstFile
  #LogWrite(Message)

  # write

# ================================================================
# Csv Import
# ================================================================
# Reads the given csv file into a Dict array
# Input:  source file name
# Outputs: DictArr - Dict array.
# https://docs.python.org/3/library/csv.html 
def read(SrcFileName) :
  FunctionName= "ReadCsv()"
  DictArr= []
  #LogWrite(FunctionName + ": Reading " + SrcFileName)
  with open(SrcFileName, 'r') as csv_file:            # Takes care of closing the file
    csv_reader= csv.DictReader(csv_file)              # Create the reader. Reads each row as dict.
    ColHeaderList= csv_reader.fieldnames              # list of column names

    nCols= len(ColHeaderList)
    #print (FunctionName, ": #Cols: ", nCols, " Hdr: ", ColHeaderList)
    # Read each row
    for row in csv_reader :                           # Each row is a dict
      CsvRowDict= dict()                              # alt: = {}
      ColIndex= 0
      for Col in ColHeaderList :
        Key= Col
        Value= row[Key]
        CsvRowDict[Key]= Value
        ColIndex += 1
      
      #print(CsvRowDict)
      DictArr.append(CsvRowDict)


  #print(DictArr)
  return DictArr

  # end read

# ================================================================
# Read the csv file, extract the specified field from each row, and return as a List.
# Intended to be a generic csv file reader, e.g. for original, distilled, etc. files.
# This ignores all the other columns that may be in the file.
# Returns: list (1D array) containing just the specified field. e.g. the form ['cmfn1', 'cmfn2', .....]
def read_field(SrcFileName, FieldName) :
  FunctionName= "ReadCsvFileField()"
  ItemCount= 0
  Result_List= []                                     # e.g. ["acme", "big tech", ...]
  DictArr= ReadCsv(SrcFileName)                       # Returns array of dict items [{CMFN:abc, MfrId:123}, ...]

  RowCount= 0
  for row in DictArr :                                # Process the rows
    OutputDict= dict()
    FieldValue= row[FieldName]  

    # Append this CMFN to the list.
    Result_List.append(FieldValue)

    ItemCount += 1
    if (ItemCount >= 9999999) :                       # Testing - Limit processing
      break

  # Completed file  
  #LogWrite(FunctionName + ": read " + SrcFileName + ", " + str(ItemCount) + " items.")

  return Result_List

  # end read_field







