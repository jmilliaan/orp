import pandas as pd
from datetime import datetime

class LogData:
    def __init__(self):
        self.logtime = []
        self.oxygen_list = []
        self.pressure_list = []
        self.phase_list = []
  
    def add_oxygen(self, o2):
        now = datetime.now()
        self.logtime.append(now.strftime("%H:%M:%S"))
        self.oxygen_list.append(o2)
            
    def add_pressure(self, pressure, phase):
        self.pressure_list.append(pressure)
        self.phase_list.append(phase)
        
    def create_dataframe(self):
        list_of_size = [len(self.logtime),
                        len(self.oxygen_list),
                        len(self.pressure_list),
                        len(self.phase_list)]
        min_size = min(list_of_size)
        dataset = {"time":self.logtime[:min_size], 
                    "o2":self.oxygen_list[:min_size], 
                    "pressure":self.pressure_list[:min_size], 
                    "phase":self.phase_list}

        df = pd.DataFrame(dataset)
        
        return df

    def to_excel(self):
        df = self.create_dataframe()
        filename = f"orp_{datetime.now().strftime('%d/%m/%Y')}_log.xlsx"
        df.to_excel(filename)

    def to_csv(self):
        df = self.create_dataframe()
        filename = f"orp_{datetime.now().strftime('%d/%m/%Y')}_log.csv"
        df.to_csv(filename)