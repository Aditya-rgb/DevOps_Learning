#Importing psutil module for monitoring the CPU
import psutil  
#Defining a Class CPUMonitor to handle the monitoring of the CPU
class CPUMonitor:

    #Passing two arguments to the init function "alert1" and "alert2" as emergency thresholds:)
    def __init__(self, alert1, alert2):
        self.alert1 = alert1  
        self.alert2 = alert2  
        
    #creating function called "healthify" to handle CPU monitoring.
    def healthify(self):
        print("Monitoring CPU usage... Press Ctrl+C to terminate.")  
        try:
            while True:
                #Using psutil module to get current CPU usage % keeping the interval 1.5 seconds 
                current_cpu_usage = psutil.cpu_percent(1.5)  
                #Warning - 2, if the CPU threshold crosses 90%
                if (current_cpu_usage > self.alert2):
                    print("Alert! CPU usage exceeds threshold: 90%")  
                #Warning - 1, if the CPU threshold crosses 85%
                elif (current_cpu_usage > self.alert1):
                    print("Alert! CPU usage exceeds threshold: 85%")  
                else:
                    #printing a catchy and funky phrase for the user:)
                    print(f"Relax, Your CPU is cruising at {current_cpu_usage}%", end='\r') 
        #Handelling the exception for keyboard interuption
        except KeyboardInterrupt:
            print("\nYou have stopped the monitoring...") 
        #Handelling other exceptiosns if any
        except Exception as e:
            print(f"\nEncountered error {e}")  

if __name__ == "__main__":

    warning_one = 85  #first warning threshold set to 85
    warning_two = 90  #second warning threshold set to 90
    start = CPUMonitor(warning_one, warning_two) #Creating the object for our class "CPUMonitor"
    #Starting the monitoring process:)
    start.healthify()  
