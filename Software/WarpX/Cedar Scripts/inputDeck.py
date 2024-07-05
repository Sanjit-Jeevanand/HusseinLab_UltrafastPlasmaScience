class constants():
    '''
    Class to contain user defined constants used elsewhere in the simultion block
    '''

    def __init__(self,ne,lambda_laser):
        '''
        Electron density in units of cm^-3
        Laser wavelength in units of um
        '''
        self.ne = ne
        self.lambda_laser = lambda_laser

        self.ne = self.ne*1e6
        self.nc = 1.12e27/self.lambda_laser**2

    def generateConstantsString(self):
        header = f'{"#"*35}\n{"#"*12} CONSTANTS {"#"*12}\n{"#"*35}'
        body = f'my_constants.nc = {self.nc}\nmy_constants.ne = {self.ne}'
        return f'{header}\n{body}'
    
class numerics():
    def __init__(self,solver,movingWindow,loadBalancing,boost):
        '''
        Solver for the electromagnetic field
        movingWindow is the velocity of the moving window
        load balancing is the load balancing interval
        boost is the gamma boost factor
        '''
        self.solver = solver
        self.movingWindow = movingWindow
        self.loadBalancing = loadBalancing
        self.boost = boost

    def generateNumericsString(self):
        header = f'{"#"*35}\n{"#"*12} NUMERICS {"#"*12}\n{"#"*35}'
        warpXBody = f'warpx.verbose = 1\nwarpx.do_dive_cleaning = 0\nwarpx.use_filter = 1\nwarpx.cfl = 1. # if 1., the time step is set to its CFL limit'
        algoBody = f'algo.maxwell_solver = {self.solver}\nalgo.load_balance_intervals = {self.loadBalancing}\nalgo.particle_shape = 3'
        if self.movingWindow:
            movingBody = f'warpx.do_moving_window = 1\nwarpx.moving_window_dir = z\nwarpx.moving_window_v = {self.movingWindow} # units of speed of light'
        else:
            movingBody = f'warpx.do_moving_window = 0\n'

        if self.boost:
            boostHeader = f'{"#"*35}\n{"#"*10} BOOSTED FRAME {"#"*10}\n{"#"*35}'
            boostBody = f'warpx.boost_direction = z\nwarpx.gamma_boost = {self.boost}'
            boostStr = f'{boostHeader}\n{boostBody}'
        else:
            boostStr = ''

        return f'{header}\n\n{warpXBody}\n{algoBody}\n\n{movingBody}\n\n{boostStr}'


if __name__ == "__main__":
    c = constants(2e18,0.8)
    n = numerics('ckc',1,100,10)
    #print(c.generateConstantsString())
    print(n.generateNumericsString())