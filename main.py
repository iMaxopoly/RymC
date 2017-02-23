import os

import sys
import time
import datetime

import io
from gooey import Gooey
from gooey import GooeyParser
from multiprocessing import freeze_support

from routine import routine


@Gooey(monospace_display=True, program_name="RymC 1.0 - All websites bundle")
def parser_args():
    p = GooeyParser(description="RymC is a complete scraper bundle for removeyourmedia.com")
    subparsers = p.add_subparsers(help='options', dest='subparser_name')

    icdrama_se_fields = subparsers.add_parser('icdrama.se')
    icdrama_se_fields.add_argument(
        'savepath', metavar='Reports save location',
        default="./Reports",
        help='Click the browse button to locate the directory where reports will be saved.',
        widget="DirChooser")
    icdrama_se_fields.add_argument(
        'clientspath', metavar='Clients folder location',
        default="./Clients",
        help='Click the browse button to locate the Clients folder which contains text files containing brand names.',
        widget="DirChooser")
    icdrama_se_fields.add_argument('workers', default=30, type=int, help='Number of threads.')
    icdrama_se_fields.add_argument('chromeWorkers', default=10, type=int, help='Maximum number of chrome instances.')

    novelascoreanas_es_fields = subparsers.add_parser('novelascoreanas.es')
    novelascoreanas_es_fields.add_argument(
        'savepath', metavar='Reports save location',
        default="./Reports",
        help='Click the browse button to locate the directory where reports will be saved.',
        widget="DirChooser")
    novelascoreanas_es_fields.add_argument(
        'clientspath', metavar='Clients folder location',
        default="./Clients",
        help='Click the browse button to locate the Clients folder which contains text files containing brand names.',
        widget="DirChooser")
    novelascoreanas_es_fields.add_argument('workers', default=30, type=int, help='Number of threads.')

    estrenosdoramas_net_fields = subparsers.add_parser('estrenosdoramas.net')
    estrenosdoramas_net_fields.add_argument(
        'savepath', metavar='Reports save location',
        default="./Reports",
        help='Click the browse button to locate the directory where reports will be saved.',
        widget="DirChooser")
    estrenosdoramas_net_fields.add_argument(
        'clientspath', metavar='Clients folder location',
        default="./Clients",
        help='Click the browse button to locate the Clients folder which contains text files containing brand names.',
        widget="DirChooser")
    estrenosdoramas_net_fields.add_argument('workers', default=30, type=int, help='Number of threads.')

    dopeka_com_fields = subparsers.add_parser('dopeka.com')
    dopeka_com_fields.add_argument(
        'savepath', metavar='Reports save location',
        default="./Reports",
        help='Click the browse button to locate the directory where reports will be saved.',
        widget="DirChooser")
    dopeka_com_fields.add_argument(
        'clientspath', metavar='Clients folder location',
        default="./Clients",
        help='Click the browse button to locate the Clients folder which contains text files containing brand names.',
        widget="DirChooser")
    dopeka_com_fields.add_argument('workers', default=30, type=int, help='Number of threads.')

    myasiantv_se_fields = subparsers.add_parser('myasiantv.se')
    myasiantv_se_fields.add_argument(
        'savepath', metavar='Reports save location',
        default="./Reports",
        help='Click the browse button to locate the directory where reports will be saved.',
        widget="DirChooser")
    myasiantv_se_fields.add_argument(
        'clientspath', metavar='Clients folder location',
        default="./Clients",
        help='Click the browse button to locate the Clients folder which contains text files containing brand names.',
        widget="DirChooser")
    myasiantv_se_fields.add_argument('workers', default=30, type=int, help='Number of threads.')

    doramasjc_com_fields = subparsers.add_parser('doramasjc.com')
    doramasjc_com_fields.add_argument(
        'savepath', metavar='Reports save location',
        default="./Reports",
        help='Click the browse button to locate the directory where reports will be saved.',
        widget="DirChooser")
    doramasjc_com_fields.add_argument(
        'clientspath', metavar='Clients folder location',
        default="./Clients",
        help='Click the browse button to locate the Clients folder which contains text files containing brand names.',
        widget="DirChooser")
    doramasjc_com_fields.add_argument('workers', default=30, type=int, help='Number of threads.')

    boxasian_com_fields = subparsers.add_parser('boxasian.com')
    boxasian_com_fields.add_argument(
        'savepath', metavar='Reports save location',
        default="./Reports",
        help='Click the browse button to locate the directory where reports will be saved.',
        widget="DirChooser")
    boxasian_com_fields.add_argument(
        'clientspath', metavar='Clients folder location',
        default="./Clients",
        help='Click the browse button to locate the Clients folder which contains text files containing brand names.',
        widget="DirChooser")
    boxasian_com_fields.add_argument('workers', default=30, type=int, help='Number of threads.')

    kissasian_com_fields = subparsers.add_parser('kissasian.com')
    kissasian_com_fields.add_argument(
        'savepath', metavar='Reports save location',
        default="./Reports",
        help='Click the browse button to locate the directory where reports will be saved.',
        widget="DirChooser")
    kissasian_com_fields.add_argument(
        'clientspath', metavar='Clients folder location',
        default="./Clients",
        help='Click the browse button to locate the Clients folder which contains text files containing brand names.',
        widget="DirChooser")
    kissasian_com_fields.add_argument('workers', default=30, type=int, help='Number of threads.')

    gooddrama_to_fields = subparsers.add_parser('gooddrama.to')
    gooddrama_to_fields.add_argument(
        'savepath', metavar='Reports save location',
        default="./Reports",
        help='Click the browse button to locate the directory where reports will be saved.',
        widget="DirChooser")
    gooddrama_to_fields.add_argument(
        'clientspath', metavar='Clients folder location',
        default="./Clients",
        help='Click the browse button to locate the Clients folder which contains text files containing brand names.',
        widget="DirChooser")
    gooddrama_to_fields.add_argument('workers', default=30, type=int, help='Number of threads.')

    dramago_com_fields = subparsers.add_parser('dramago.com')
    dramago_com_fields.add_argument(
        'savepath', metavar='Reports save location',
        default="./Reports",
        help='Click the browse button to locate the directory where reports will be saved.',
        widget="DirChooser")
    dramago_com_fields.add_argument(
        'clientspath', metavar='Clients folder location',
        default="./Clients",
        help='Click the browse button to locate the Clients folder which contains text files containing brand names.',
        widget="DirChooser")
    dramago_com_fields.add_argument('workers', default=30, type=int, help='Number of threads.')

    dramalove_tv_fields = subparsers.add_parser('dramalove.tv')
    dramalove_tv_fields.add_argument(
        'savepath', metavar='Reports save location',
        default="./Reports",
        help='Click the browse button to locate the directory where reports will be saved.',
        widget="DirChooser")
    dramalove_tv_fields.add_argument(
        'clientspath', metavar='Clients folder location',
        default="./Clients",
        help='Click the browse button to locate the Clients folder which contains text files containing brand names.',
        widget="DirChooser")
    dramalove_tv_fields.add_argument('workers', default=30, type=int, help='Number of threads.')

    doramastv_com_fields = subparsers.add_parser('doramastv.com')
    doramastv_com_fields.add_argument(
        'savepath', metavar='Reports save location',
        default="./Reports",
        help='Click the browse button to locate the directory where reports will be saved.',
        widget="DirChooser")
    doramastv_com_fields.add_argument(
        'clientspath', metavar='Clients folder location',
        default="./Clients",
        help='Click the browse button to locate the Clients folder which contains text files containing brand names.',
        widget="DirChooser")
    doramastv_com_fields.add_argument('workers', default=30, type=int, help='Number of threads.')

    dramanice_to_fields = subparsers.add_parser('dramanice.to')
    dramanice_to_fields.add_argument(
        'savepath', metavar='Reports save location',
        default="./Reports",
        help='Click the browse button to locate the directory where reports will be saved.',
        widget="DirChooser")
    dramanice_to_fields.add_argument(
        'clientspath', metavar='Clients folder location',
        default="./Clients",
        help='Click the browse button to locate the Clients folder which contains text files containing brand names.',
        widget="DirChooser")
    dramanice_to_fields.add_argument('workers', default=30, type=int, help='Number of threads.')

    nineanime_to_fields = subparsers.add_parser('9anime.to')
    nineanime_to_fields.add_argument(
        'savepath', metavar='Reports save location',
        default="./Reports",
        help='Click the browse button to locate the directory where reports will be saved.',
        widget="DirChooser")
    nineanime_to_fields.add_argument(
        'clientspath', metavar='Clients folder location',
        default="./Clients",
        help='Click the browse button to locate the Clients folder which contains text files containing brand names.',
        widget="DirChooser")
    nineanime_to_fields.add_argument('workers', default=30, type=int, help='Number of threads.')

    args = p.parse_args()
    return args


def main():
    args = parser_args()

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')

    files = []
    for (dirpath, dirnames, filenames) in os.walk(args.clientspath):
        files.extend(filenames)
        break

    client_dict = {}
    for m_file in files:
        licensor = m_file[0:-4]
        with io.open(args.clientspath + "/" + m_file, "r", encoding="utf-8") as fo:
            for line in fo:
                string_list = []
                if line != "" and line not in string_list:
                    brand = line.strip("\t\r\n '\"")
                    client_dict[brand] = licensor

    routine(timestamp, args, client_dict)


if __name__ == '__main__':
    freeze_support()

    nonbuffered_stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stdout = nonbuffered_stdout

    main()
