from datetime import datetime

class Stats:

    def __init__(self, command, id):
        self.command = command
        self.response = None
        self.id = id

        self.start_time = datetime.now()
        self.end_time = None
        self.duration = None


    def add_response(self, response):
        self.response = response
        self.end_time = datetime.now()
        self.duration = self.get_duration()


    def get_duration(self):
        diff = self.end_time - self.start_time
        return diff.total_seconds()


    def print_stats(self):
        print ('\nid: {0}'.format(self.id))
        print ('command: {0}'.format(self.command))
        print ('response: {0}'.format(self.response))
        print ('start time: {0}'.format(self.start_time))
        print ('end_time: {0}'.format(self.end_time))
        print ('duration: {0}\n'.format(self.duration))


    def got_response(self):
        if self.response is None:
            return False
        else:
            return True


    def return_stats(self):
        str = ''
        str +=  '\nid: {0}'.format(self.id)
        str += 'command: {0}'.format(self.command)
        str += 'response: {0}'.format(self.response)
        str += 'start time: {0}'.format(self.start_time)
        str += 'end_time: {0}'.format(self.end_time)
        str += 'duration: {0}\n'.format(self.duration)
        return str