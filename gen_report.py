import sys

from report_0_hop import prepare_0_hop_report
from report_1_hop import prepare_1_hop_report


def main():
    if len(sys.argv) is not 3:
        print "Example usage is:"
        print "\tgen_report.* {site-name} {time-stamp} {hops}"
        print "Where:"
        print "\tFirst parameter is name of site, eg. icdrama.se"
        print "\tSecond parameter is the time stamp"
        print "\tThird parameter is a number of how many hops the report has, usually 1 or 0"
        exit()

    site_name = sys.argv[1]
    time_stamp = sys.argv[2]
    report_hops = None
    try:
        report_hops = int(sys.argv[3])
    except ValueError:
        print "Hops value was incorrect, should be a number. Try either 0 or 1."
        exit()

    if report_hops == 0:
        prepare_0_hop_report("./Reports" + "/" + site_name + "_" + time_stamp + ".xlsx", site_name, time_stamp)
    elif report_hops == 1:
        prepare_1_hop_report("./Reports" + "/" + site_name + "_" + time_stamp + ".xlsx", site_name, time_stamp)


if __name__ == '__main__':
    main()
