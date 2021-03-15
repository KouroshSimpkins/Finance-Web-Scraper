""" My Reading/Writing Code. Data_Read_Write.Reader takes a csv file, the list to write to and the column to write, to make it easier to work with data in a CSV. Writer takes the data from a list and writes it to a txt file for later usage with other modules."""

def Reader(Input_File, Output_List, Column_Name):
    import csv

    with open(Input_File, "r") as Input_File:
        reader = csv.DictReader(Input_File, delimiter = ',')
        for row in reader:
            Next_Item = row[Column_Name]
            Next_Item = Next_Item.strip()
            Output_List.append(Next_Item)

def Writer(Output_File, Input_List):
    with open(Output_File, "a") as output_file:
    for Item in Input_List:
        output_file.write(Item)
        output_file.write('\n')
