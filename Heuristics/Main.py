"""
AMMM Lab Heuristics - Priority Assignment Version
Main function for crypto-mining cooperative
"""

from argparse import ArgumentParser
from pathlib import Path
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Heuristics.datParser import DATParser
from AMMMGlobals import AMMMException
from Heuristics.ValidateConfig import ValidateConfig
from Heuristics.validateInputData import ValidateInputData
from Heuristics.solvers.solver_Greedy import Solver_Greedy
from Heuristics.solvers.solver_GRASP import Solver_GRASP
from problem.instance import Instance


class Main:
    def __init__(self, config):
        self.config = config

    def run(self, data):
        try:
            if self.config.verbose:
                print('Creating Problem Instance...')
            instance = Instance(self.config, data)

            if not instance.checkInstance():
                print('Instance is infeasible.')
                solution = instance.createSolution()
                solution.makeInfeasible()
                solution.saveToFile(self.config.solutionFile)
                return 1

            if self.config.verbose:
                print('Solving the Problem...')

            if self.config.solver == 'Greedy':
                solver = Solver_Greedy(self.config, instance)
            elif self.config.solver == 'GRASP':
                solver = Solver_GRASP(self.config, instance)
            else:
                raise AMMMException('Solver %s not supported.' % str(self.config.solver))

            solution = solver.solve()
            print('Total Objective (collected bid): %.6f' % solution.getFitness())
            solution.saveToFile(self.config.solutionFile)
            return 0

        except AMMMException as e:
            print('Exception:', e)
            return 1


if __name__ == '__main__':
    parser = ArgumentParser(description='AMMM Lab Heuristics - Crypto-Mining Priority')
    parser.add_argument('-c', '--configFile', nargs='?', type=Path,
                        default=Path(__file__).parent / 'config/config.dat', help='specifies the config file')
    args = parser.parse_args()

    config = DATParser.parse(args.configFile)
    ValidateConfig.validate(config)
    inputData = DATParser.parse(config.inputDataFile)
    ValidateInputData.validate(inputData)

    if config.verbose:
        print('AMMM Lab Heuristics - Priority Assignment')
        print('------------------------------------------')
        print('Config file: %s' % args.configFile)
        print('Input Data file: %s' % config.inputDataFile)

    main = Main(config)
    sys.exit(main.run(inputData))
