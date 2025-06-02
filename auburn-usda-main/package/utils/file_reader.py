import csv

from package.utils.data_classes import DataPoint


def csvRead(filepath: str, channels: int = 1) -> list[DataPoint]:
    """Reads a csv file and returns data as a list of DataPoints
    :param filepath: the file path to read the csv from
    :param channels: number of channels
    :returns: list of DataPoints
    """
    data = []
    with open(filepath, newline="") as csvfile:
        reader = csv.reader(csvfile)

        # If there is a header, skip
        csvTestBytes = csvfile.read(1024)
        csvfile.seek(0)
        if csv.Sniffer().has_header(csvTestBytes):
            next(reader)

        for row in reader:
            if len(row) < 3:
                continue
            data.append(DataPoint(row[0], row[1], row[2]))
    return data

    # if not csvFormatCheck(df.iloc[0], channels):
    #    print("Error") TODO: reimplement csvFormatCheck


def anaDecode(filepath: str) -> list[str]:
    """Reads .ana files in binary format and parses them to be readable
    :param filepath: filepath of .ana file to read from
    """

    lines = []
    with open(filepath, "rb") as f:
        f.read(1)  # Skip the first character
        f.read(1)  # Skip the second character
        line = ""
        while True:
            c = f.read(1)
            if not c:
                break  # End of file
            if c == b"\n":
                f.read(1)  # Skip the character after newline
                lines.append(line)
                line = ""
            if c != b"\x00":
                line += c.decode("utf-8", errors="ignore")
    return lines


def anaRead(filepath: str) -> list[DataPoint]:
    """Reads an .ana file and returns data as a list of DataPoint
    :param: filepath to read .ana file from
    :returns: list of DataPoints
    """
    lines = anaDecode(filepath)
    data = []
    for elem in lines:
        if not elem:
            continue
        channel, time, voltage = elem.split()
        data.append(DataPoint(time, voltage, channel))
    return data
