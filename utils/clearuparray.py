def cleanup(list):
    res = []
    for element in list:
        if element != []:
         res.append(element)
    return res

def arraytostring(array):
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in array:
        str1 += ele
 
    # return string
    return str1

def splitteams(str):
   str.split('vs')
   return str
      
