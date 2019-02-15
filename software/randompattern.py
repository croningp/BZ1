'''daughter class to perfrom random experiment '''

#import parent class
import experiment_parent

class random_experiment(experiment_parent.AutomatedPlatform):
    def __init__(self):
        super().__init__()

        def perform_experiment(self):
            #call fill, then do experiment, call clean
            super().fill_experiment()
            # activate random pattern for 1 minute 30 times
            # need variable titles
            exp_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            self.rv.record_threaded( exp_time )
            for i in range(30):
                self.b.activate_rand(exp_time)
                time.sleep(60*1)
                self.b.disable_all()
            
            super().clean_experiment()

if __name__ == "__main__":

    rexp = random_experiment()

    for i in range(1): # number of experiments
        rexp.perform_experiment()
