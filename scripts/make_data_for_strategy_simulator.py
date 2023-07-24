import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "modules"))

from gp_info import SeasonInfo


def main():
    si = SeasonInfo(2023)
    df = si.get_data_for_strategy_simulator()
    df.to_csv(os.path.join(current_dir, "data/data_for_strategy_maker.csv"), index=False)


if __name__ == "__main__":
    main()