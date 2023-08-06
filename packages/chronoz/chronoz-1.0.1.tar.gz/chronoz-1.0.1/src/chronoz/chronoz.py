import time

###### Licence and money  ########
#This work is under CC0 licence. This is mostly equivalent to public domain.
#The spirit is that you do whatever you want and I deny any responsibility if it somehow backfire.
#That said, I would appreciate if you would keep the result as open source.
#And I would even more appreciate if you could donate me a little something
#Tipee : https://www.tipeee.com/holy-python
#paypal : https://www.paypal.com/us/cgi-bin/webscr?cmd=_send-money&nav=1&email=simon.zozol@gmail.com


# The important part is decorator "def chronometer(chrono_name):"
# This is not thread safe



#Usage:
#  @chronometer("chrono1")
#  def myFunction(lapse, position, speed):
#    suite
# This will start (create if needed) the chonometer "chrono1" then stop as the function stops
def chronometer(chrono_name):
    def real_decorator(function):
        #  @wraps(function)   #for introspection
        def __wraper(*args, **kwargs):
            _default_set.start(chrono_name)
            result = function(*args, **kwargs)
            _default_set.stop(chrono_name)
            return result
        return __wraper
    return real_decorator

def getChrono(chrono):
    return _default_set.get(chrono)

def display_chrono(chrono): # chrono can be an object "Compound_Chrono" or a string (or any hashable, if need be)
    print(_default_set[chrono])

def display_all():
    _default_set.display_all()





#TODO: Real_time_chrono and CPU chrono should both inherit the same virtual class
class Real_time_chrono:
    def __init__(self, start_now = False):
        self.name = "elapsed time"
        self.total_recorded = 0.0 # elased time in seconds
        if start_now :
            #Selon le type de chrono, get current time donne l'orloge system, le temp CPU ou tot autre
            self.start_time = self.getCurrentTime() 
        else:
            self.start_time = None

    def getCurrentTime(self):
        # For this implementation, getCurrentTime give the real elapsed time 

#        return time.perf_counter()
# Code below is cleanner but has to be optimised
       try:
           return time.perf_counter() # python >= 3.3
       except AttributeError:
           return time.time() # this timer is not monotonic!    

    def total(self):
        try:
            return self.total_recorded +  self.getCurrentTime() - self.start_time
        except TypeError: #if self.starttime == None
            return self.total_recorded

    def start(self):
        self.start_time = self.getCurrentTime()

    def stop(self):
        self.total_recorded += self.getCurrentTime() - self.start_time          
        self.start_time = None
            
    def __enter__(self):
        self.start()
    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def reset(self):
        self.total_recorded = 0.0 
        self.start_time = None


    def __str__(self):
        return self.name+' total:'+str(self.total())+'s'
       

#This give the CPU execution time for a given bit of code
#Result may be plain wrong in a multithread scenario
class CPU_Chrono(Real_time_chrono):
    def __init__(self, start_now = False):
        super().__init__(start_now)
        self.name = "CPU time"

    def getCurrentTime(self):
        #It gives the CPU time of the process
        return time.process_time()
    
class Compound_Chrono():  
    def __init__(self, name, start_now = False):
        self.name = name
        self.chrono_list =[]
        self.chrono_list.append(Real_time_chrono(start_now))
        self.chrono_list.append(CPU_Chrono(start_now))

    def start(self):
        list_time_stamp = []
        for chrono in self.chrono_list:
            chrono.start()

                    
    def stop(self):        
        for chrono in self.chrono_list:
            chrono.stop()
            
    def __enter__(self):
        self.start()
    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()        
            
    def reset(self):
        for chrono in self.chrono_list:
            chrono.reset()

    def __str__(self):
        result = ''
        for chrono in self.chrono_list:
            result += '<Chrono "' + self.name + '".'+str(chrono)+' >\n'  

        return result
                   
    def __hash__(self):
        '''return the hash of self.name
           The goal is that you can search in a dictionary using
           either dict[object] or dict[name]'''
        return hash(self.name)

    
#TODO Should not inherit dictonary. Some function of Dict should not be available
class Chrono_set(dict):
    def add(self, chrono):
        if isinstance(chrono, Compound_Chrono):
            self[chrono] = chrono
        else:
            self[chrono] = Compound_Chrono(chrono)  

    def get(self, chrono):
        try:
            return self[chrono]
        except KeyError :
            self.add(chrono)  
            return self[chrono]
        
    def start(self, chrono):
        ''' a priori chrono is a string, a number or a "Chrono" object. '''
        self.get(chrono).start()
       
    def stop(self, chrono):
        self[chrono].stop()

    def display(self, chrono):
        print(self[chrono])

    def display_all(self):
        for chrono in self.values():
            print (chrono)


#This is the set used by the funcion display_chrono and display_all
_default_set = Chrono_set()



