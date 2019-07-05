import datetime


class Date(object):
    def __init__(self):
        self.human_readable = None
        self.cp_readable = None

    def cp_to_human(self):
        pass

    '''
    21/9/2019 ---------> 2019-9-21
    June 21, 2019 --------->2019-6-21 
    '''
    def human_to_cp(self, date):
        try:
            self.cp_readable = datetime.datetime.strptime(date, "%d/%m/%Y").date()
        except ValueError:
            self.cp_readable = datetime.datetime.strptime(date,"%B %d, %Y").date()
        return self.cp_readable
