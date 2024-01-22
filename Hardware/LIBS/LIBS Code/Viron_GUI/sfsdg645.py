import instruments as ik
class DG645:
    def __init__(self, comstring):
        try:
            self.unit = ik.srs.SRSDG645.open_from_uri(comstring)
        except:
            self.unit = None
            # raise IOError('Unable to connect to DG645 - Check your com port and ensure it was closed properly before'
            #               ' connecting again')
        else:
            print('Connection was successful.')
            print(self.unit.query('*IDN?'))

        self.optlist = ['0', 't0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.unitdict = {
            's'     :   'e0',
            'ms'    :   'e-3',
            'us'    :   'e-6',
            'ns'    :   'e-9',
            'ps'    :   'e-12'
        }
    def sendcmd(self, command):
        self.unit.sendcmd(command)

    def query(self, command):
        return self.unit.query(command)

    def get_all_delays(self):
        for i in range(10):
            rtn = self.query('DLAY?' + str(i))
            rtn = rtn.split(',')
            print(self.optlist[i] + ' = ' + self.optlist[int(rtn[0])] + str(rtn[1]))
            
    def get_delay(self, target):
        rtn = self.query('DLAY?' + str(target))
        rtn = rtn.split(',')
        return rtn
              
    def display_delay(self, target, link, unit, delay):
        # fix these targets 
        string = 'DLAY '
        string += str(self.optlist.index(target.lower())) + ','
        string += str(self.optlist.index(link.lower())) + ','
        string += str(delay) + str(self.unitdict[unit])
        print(string)
        self.sendCommand(string)

    def close(self):
        self.unit.sendcmd('IFRS 0')
        print('Connection closed successfully')
        
        
    def setDelay(self, target, link, delay, unit):
        # target = self.chosenDelayTarget.get()
        # link = self.chosenDelayTargetLink.get()
        # unit = self.chosenDelayUnit.get()
        # delay = self.delayEntry.get()
        try:
            float(delay)
        except:
            print('Invalid input, ya doofus')
            return
        print(target, link, unit, delay)
        string = 'DLAY '
        string += str(self.optlist.index(target.lower())) + ','
        string += str(self.optlist.index(link.lower())) + ','
        string += str(delay) + str(self.unitdict[unit])
        self.sendCommand(string)
        