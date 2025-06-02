import argparse
import random

"""
FOR QUICK TESTING : python3 data_maker.py -s 1000 -c 4 -lb 0 -ub 10 -t 0 -sr 100 fakeData.csv
    The numbers represent the following:
        sample size // number of channels // lower bound value // upper bound value // starting time // sample rate // file
    JUST COPY+PASTE AND CHANGE THE VALUES AS NECESSARY

F.Y.I it will generate a point at time X per channel i.e. four points at time 0 if the # of channels is 4
    so if the sample_size is 1000 and the channels is 4, it will generate 4000
"""


def makeData(
    fp,
    num_of_pts: int,
    num_of_channels: int,
    range_low: int,
    range_high: int,
    start_time: float,
    time_step: float,
):
    fp.write("Time,Voltage,Channel\n")

    time = start_time

    for i in range(num_of_pts):
        pt_time = str(time)
        for j in range(num_of_channels):
            pt_val = str(random.randint(range_low, range_high) + random.random())
            pt_channel = str(j + 1)
            pt = pt_time + "," + pt_val + "," + pt_channel + "\n"
            fp.write(pt)
        time += time_step

    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "csvFILE", help="a csv file to write the data to", default="fakeData.csv"
    )
    parser.add_argument(
        "-s",
        "--sample_size",
        type=int,
        help="the number of points to be generated",
        default=1000,
    )
    parser.add_argument(
        "-c", "--channels", type=int, help="the number of channels", default=1
    )
    parser.add_argument(
        "-lb",
        "--lower_bound",
        type=int,
        help="the lower bound of values to select from",
        default=-5,
    )
    parser.add_argument(
        "-ub",
        "--upper_bound",
        type=int,
        help="the upper bound of values to select from",
        default=5,
    )
    parser.add_argument(
        "-t",
        "--time_start",
        type=float,
        help="the starting time of the data",
        default=0,
    )
    parser.add_argument(
        "-sr",
        "--sample_rate",
        type=int,
        help="the rate at which data is sampled per second",
        default=100,
    )

    args = parser.parse_args()

    fp = open(args.csvFILE, "w")

    step = 1 / args.sample_rate

    print("Generating data...")
    makeData(
        fp,
        args.sample_size,
        args.channels,
        args.lower_bound,
        args.upper_bound,
        args.time_start,
        step,
    )
    fp.close()
    print("Saving data...")
    print("----Data Stats----")
    print(
        f"Total Data : {args.sample_size * args.channels} points ({args.channels}x{args.sample_size})"
    )
    print(f"Sample Rate : {args.sample_rate}")
    print(
        f"Starting time : {args.time_start}\tEnding time : {args.time_start + (step*args.sample_size)}"
    )
    print(f"Value Range : {args.lower_bound} to {args.upper_bound}")
