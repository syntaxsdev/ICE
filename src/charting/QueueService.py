from twelvedata import TDClient
from twelvedata.time_series import TimeSeries
from datetime import datetime as dt
import time

class QueueService():

    creditsPM : int = None
    remaining = 0
    minuteStarted : int = 0
    _queue : dict = {}
    busy = False

    def __init__(self, credits):
        self.creditsPM = credits
        self.remaining = credits


    def queue(self, timeseries : TimeSeries, format : str):
        while (self.busy == True):
            time.sleep(1)
            if (self.busy == False):
                break
        #Make the queue busy
        self.busy = True
        #Refresh the queue to clear any space
        self.QueueRefresh()
        
        credits = len(timeseries.as_url()) if type(timeseries.as_url()) is list else 1

        print("Queuing {0} credits".format(credits))
        if (self.remaining - credits) >= 0:
            #Do the queueing
            currTime = self._unixunique()
            self._queue[currTime] = credits
            self.remaining -= credits
            #End of queueing
        else:
            print("The queue is full. Retrying...")
            while (self.remaining - credits) < 0:
                self.QueueRefresh()
                time.sleep(2)
                #if the queue opens up
                if (self.remaining - credits) >= 0:
                    print("The queue is open.")
                    #Do the queueing
                    currTime = self._unixunique()
                    self._queue[currTime] = credits
                    self.remaining -= credits
                    #End of queueing
                    break
        #Do the timeseries
        retval = None
        if format == "pandas":
            retval = timeseries.as_pandas()
        elif format == "json":
            retval = timeseries.as_json()
        #End of timeseries
        self.busy = False
        return retval
                

    def _credit_check(self):
        self.remaining = self.remaining if self.remaining < self.creditsPM else self.creditsPM
          

    def QueueRefresh(self):
        queue = self._queue.copy()

        for q in queue:
            currTime = self._unixunique()

            #If the queue has been there for 60 seconds remove it
            if (currTime - q) >= 60:
                credits = self._queue.pop(q)
                self.remaining += credits

        return self.remaining


    def _unixunique(self):
        return time.time()

    def _unix(self):
        ms = dt.now()
        return int(time.mktime(ms.timetuple()))