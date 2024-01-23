import instruments as ik
class DG645:
    def __init__(self, comstring):
        try:
            self.unit = ik.srs.SRSDG645.open_serial(comstring, 9600)
        except:
            self.unit = None
            # raise IOError('Unable to connect to DG645 - Check your com port and ensure it was closed properly before'
            #               ' connecting again')
        else:
            print('Connection was successful.')
            print(self.unit.query('*IDN?'))

        self.optlist = ['t0', 't1', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        
        self.unitdict = {
            's'     :   'e0',
            'ms'    :   'e-3',
            'us'    :   'e-6',
            'ns'    :   'e-9',
            'ps'    :   'e-12'
        }
        
        self.triggersourcedict = {
            'internal'  :   '0',
            'external rising edge'  :   '1',
            'external falling edge' :   '2',
            'single shot external rising edge' :   '3',
            'single shot external falling edge' :   '4',
            'single shot'   :   '5',
            'line'  :  '6',
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
        value = float(rtn[1])
        
       # Define the modified unit dictionary
        mod_unit_dict = {
            's': 10**0,
            'ms': 10**-3,
            'us': 10**-6,
            'ns': 10**-9,
            'ps': 10**-12
        }

        # Determine the appropriate unit based on the magnitude of the value
        magnitude = 1
        for unit, exponent in mod_unit_dict.items():
            if float(exponent) <= abs(value) < 1000:
                magnitude = exponent
                break

        # Convert the value to the appropriate unit
        scaled_value = value / magnitude
        
        return [self.optlist[int(rtn[0])], str(scaled_value), str(unit)]
              
    def display_delay(self, target):
        # fix these targets 
        string = 'DISP '
        string += "11,"+str(self.optlist.index(target.lower()))
        print(string)
        self.sendcmd(string)

    def close(self):
        self.unit.sendcmd('IFRS 0')
        print('Connection closed successfully')
        
        
    def setDelay(self, target, link, delay, unit):
        try:
            float(delay)
        except:
            print('Invalid input, ya doofus')
            return
        print(target, link, unit, delay)
        string = 'DLAY '
        # string += str(self.optlist.index(target.lower())) + ','
        string += str(target) + ","
        string += str(self.optlist.index(link.lower())) + ','
        string += str(delay) + str(self.unitdict[unit])
        self.sendcmd(string)

        
    def get_amplitude(self, target):
        rtn = self.query("LAMP?"+str(target))
        return rtn
    
    def set_amplitude(self, target, amplitude):
        self.sendcmd("LAMP "+str(target)+","+str(amplitude))
        
    def get_offset(self, target):
        rtn = self.query("LOFF?"+str(target))
        return rtn
    
    def set_offset(self, target, offset):
        self.sendcmd("LOFF "+str(target)+","+str(offset))
        
    def get_trigger_source(self):
        rtn = self.query("TSRC?")
        return rtn
        
    def set_trigger_source(self, source):
        self.sendcmd("TSRC "+str(self.triggersourcedict[source.lower()]))
        