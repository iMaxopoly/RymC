import io
import validators
import xlsxwriter


def prepare_1_hop_report(savepath, site_save_name, time_stamp):
    workbook = xlsxwriter.Workbook(savepath + "/" + site_save_name + "_" + time_stamp + ".xlsx")
    worksheet = workbook.add_worksheet("report_removeyourmedia")

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
    worksheet.write_string(row, col + 3, "3rd_party_link", title_format)
    worksheet.write_string(row, col + 4, "Cyberlocker_link", title_format)
    row += 1

    with io.open('./debug/' + site_save_name + "/" + time_stamp + "/links.txt", "r", encoding="utf-8") as f:
        for line in f:
            obj = line.split("<<@>>")
            if len(obj) != 5:
                continue
            licensor = obj[0]
            page_title = obj[1]
            site_link = obj[2]
            third_party_link = obj[3]
            cyberlocker_link = obj[4]
            if not validators.url(site_link, public=True) or not validators.url(cyberlocker_link, public=True):
                continue
            worksheet.write_string(row, col, licensor, data_format)
            worksheet.write_string(row, col + 1, page_title, data_format)
            worksheet.write_string(row, col + 2, site_link, data_format)
            worksheet.write_string(row, col + 3, third_party_link, data_format)
            worksheet.write_string(row, col + 4, cyberlocker_link, cyberlocker_format)
            row += 1

    workbook.close()
