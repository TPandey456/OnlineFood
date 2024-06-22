import datetime

def generate_order_number(pk):
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  
#(202406051306Second --> YYYY MM DD hour minute second )datetime+pk   this is the method to create the oreder number

    order_no= current_datetime+str(pk) 
    return order_no