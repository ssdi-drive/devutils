'''
Created on 04-Nov-2016

@author: dgraja
'''

import csv
import json
from datetime import datetime


def data_to_text(data):
    '''
        Conver the unicode data to writeable text
    '''
    result = ''
    try:
        text = data
        if not isinstance(data, unicode) and not isinstance(data, str):
            text = unicode(data)
        if isinstance(text, unicode):
            text = unicode.encode(text, 'utf-8', 'ignore')
        result = text
    except Exception as ex:
        print "conversion to text failed %r" % data
        print ex
    return result


def linearize_dict(dt, prefix="", result={}):
    """
        Make a nested dictionary flat (without nesting)
    """
    for key, val in dt.iteritems():
        if isinstance(val, dict):
            linearize_dict(val, prefix + key + "_", result)
        else:
            result[prefix + key] = data_to_text(val)
    return result


def get_fieldnames(dict_array):
    """
        Get the master list of all keys in the array of dictionaries
    """
    all_keys = []
    for entry in dict_array:
        if isinstance(entry, dict):
            new_keys = [k for k in entry.keys() if k not in all_keys]
            all_keys = all_keys + new_keys
    return all_keys



def write_json_as_csv(data, outfile):
    """
        Write an array of complex json structure as tocsv file after flattening the json
    """
    
    converted = [linearize_dict(item, result={}) for item in data]
    with open(outfile, 'wb+') as fp:
        writer = csv.DictWriter(fp, fieldnames=get_fieldnames(converted), lineterminator='\n')
        writer.writeheader()
        for row in converted:
#             print row
            try:
                writer.writerow(row)
            except Exception as e:
                print e
                print row
    return


def update_date_values(dict_array):
    """
        Update the long Date (unix file time style) to readable strings 
        in the given array of dictionaries 
    """
    if not isinstance(dict_array, (list, tuple)):
        raise Exception("invalid type for dict_array")
    
    for entry in dict_array:
        for k,v in entry.iteritems():
            if "Date" in k:
                converted = datetime.utcfromtimestamp(float(v)/1000)
                entry[k] = str(converted)
    return dict_array


def write_json_as_csv_with_date_conversion(data, outfile):
    """
        Write an array of complex json structure as tocsv file after flattening the json
    """
    
    converted = [linearize_dict(item, result={}) for item in data]
    converted = update_date_values(converted)
    with open(outfile, 'wb+') as fp:
        writer = csv.DictWriter(fp, fieldnames=get_fieldnames(converted), lineterminator='\n')
        writer.writeheader()
        for row in converted:
#             print row
            try:
                writer.writerow(row)
            except Exception as e:
                print e
                print row
    return


def main():
    source_file = r"E:\Temporary Files\2016\Nov\Nov-04-2016\get-change-summary.json"
    out_file = r"E:\Temporary Files\2016\Nov\Nov-04-2016\get-change-summary.csv"
    data = dict()
    with open(source_file, "r") as fp:
        data = json.load(fp)
        
#     converted = [linearize_dict(item, result={}) for item in data['fileSystemChanges']]
# #     converted = [item for item in converted if "fileSystemItem_creationDate" in item]
#     converted = update_date_values(converted)
    write_json_as_csv_with_date_conversion(data=data['fileSystemChanges'], outfile=out_file)
    print "output file: %s created !!\n\n" % out_file


if __name__ == '__main__':
    main()
    pass
