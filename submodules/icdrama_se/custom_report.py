import os

import io
import validators
import xlsxwriter


def prepare_report(savepath, time_stamp):
    cyberlocker_link_files = []
    for (dirpath, dirnames, filenames) in os.walk("./debug/" + time_stamp):
        cyberlocker_link_files.extend(filenames)
        break

    workbook = xlsxwriter.Workbook(savepath + "/" + time_stamp + ".xlsx")
    worksheet = workbook.add_worksheet("icdrama_se_removeyourmedia")

    row = 0
    col = 0

    title_format = workbook.add_format()
    title_format.set_bold()
    title_format.set_bottom()
    title_format.set_align("center")
    title_format.set_font_name('Times New Roman')
    title_format.set_font_size(12)

    data_format = workbook.add_format()
    data_format.set_font_name('Verdana')
    data_format.set_font_size(9)
    data_format.set_text_v_align(3)

    cyberlocker_format = workbook.add_format()
    cyberlocker_format.set_font_name('Verdana')
    cyberlocker_format.set_font_size(9)
    cyberlocker_format.set_font_color('blue')

    worksheet.set_column(0, 0, 30)
    worksheet.set_column(1, 1, 50)
    worksheet.set_column(2, 2, 70)
    worksheet.set_column(3, 3, 70)
    worksheet.set_column(4, 4, 70)

    worksheet.write_string(row, col, "Licensor", title_format)
    worksheet.write_string(row, col + 1, "Site_Pagetitle", title_format)
    worksheet.write_string(row, col + 2, "Site_link", title_format)
    worksheet.write_string(row, col + 3, "Videobug_link", title_format)
    worksheet.write_string(row, col + 4, "Cyberlocker_link", title_format)
    row += 1

    with io.open('./debug/icdrama.se/' + time_stamp + "/cyberlocker-links.txt", "r", encoding="utf-8") as f:
        for line in f:
            obj = line.split("<<@>>")
            if line == "" \
                    or len(obj) != 5 \
                    or not validators.url(obj[1], public=True) \
                    or not validators.url(obj[3], public=True) \
                    or not validators.url(obj[4], public=True):
                continue

            worksheet.write_string(row, col, obj[0], data_format)
            worksheet.write_string(row, col + 1, obj[2], data_format)
            worksheet.write_string(row, col + 2, obj[3], data_format)
            worksheet.write_string(row, col + 3, obj[1], data_format)
            worksheet.write_string(row, col + 4, obj[4], cyberlocker_format)
            row += 1

    workbook.close()
