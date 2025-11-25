import sys
import argparse

from core.simulation import Simulation


class HelpOnErrorParser(argparse.ArgumentParser):
    def error(self, _):
        self.print_help()
        sys.exit(2)


def parse_args():    
    parser = HelpOnErrorParser(description="Spatial Hash Grid Demo Parameters")

    parser.add_argument("-n", type=int, required=False, help="Number of particles (min: 10, max: 500)")
    parser.add_argument("-r", type=int, required=False, help="The particles' radius (min: 5, max: 20)")
    parser.add_argument("-v", type=int, required=False, help="The particles' velocity (min: 50, max: 300)")
    parser.add_argument("-s", choices=["naive", "shg"], required=False, help="Collision strategy: naive or using spatial hash grid")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    simulation = Simulation(args.n, args.r, args.v, args.s)