import pandas as pd
import calendar
from datetime import datetime
import holidays
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    SimpleDocTemplate,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors

# Configurare orar
START_TIME = "10:00"
END_TIME = "19:00"
HOURS_WORKED = 8

# Observație generală pentru fiecare zi de muncă
DAILY_OBSERVATION = (
    "Activitate de dezvoltare software conform contractului "
    "individual de muncă."
)

# Zilele săptămânii în română
ZILE_ROMANA = [
    "Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"
]


def generate_pontaj_dataframe(month: int, year: int):
    num_days = calendar.monthrange(year, month)[1]
    dates = [datetime(year, month, day) for day in range(1, num_days + 1)]

    ro_holidays = holidays.RO(years=year, language="ro")

    rows = []
    total_hours = 0
    crt = 1
    zile_lucratoare = 0  # numără doar zilele efectiv lucrate

    for current_date in dates:
        weekday = current_date.weekday()
        day_name = ZILE_ROMANA[weekday]
        date_str = current_date.strftime("%d.%m.%Y")

        if weekday >= 5:
            continue  # Sâmbătă, Duminică

        if current_date in ro_holidays:
            rows.append([
                crt, date_str, day_name, "", "", "", 0,
                f"Zi liberă legală – {ro_holidays.get(current_date)}"
            ])
            crt += 1
            continue

        rows.append([
            crt, date_str, day_name, START_TIME, "1h", END_TIME,
            HOURS_WORKED, DAILY_OBSERVATION
        ])
        total_hours += HOURS_WORKED
        crt += 1
        zile_lucratoare += 1  # doar zilele efectiv lucrate

    # Adaugă total
    rows.append([
        "", "TOTAL", "", "", "", "", total_hours,
        f"{zile_lucratoare} zile lucrătoare."
    ])

    df = pd.DataFrame(rows, columns=[
        "Nr. Crt", "Data", "Zi", "Start", "Pauză", "Sfârșit",
        "Ore lucrate", "Observații"
    ])
    return df


def export_to_csv(df, month, year):
    file_name = f"pontaj_{year}_{month:02d}.csv"
    df.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f"[✔] Fișier CSV salvat: {file_name}")
    return file_name


def csv_to_excel(csv_file, month, year):
    file_name = f"pontaj_{year}_{month:02d}.xlsx"
    df = pd.read_csv(csv_file, encoding='utf-8-sig')
    df.to_excel(file_name, index=False)
    print(f"[✔] Fișier Excel salvat: {file_name}")
    return file_name


def excel_to_pdf(excel_file, month, year):

    # Înregistrează fontul DejaVuSans
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'fonts/dejavu-sans/DejaVuSans.ttf'))

    df = pd.read_excel(excel_file)
    file_name = f"pontaj_{year}_{month:02d}.pdf"

    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.alignment = TA_LEFT
    styleN.fontName = "DejaVuSans"  # Folosește fontul cu suport diacritice

    data = [[Paragraph(str(cell) if pd.notnull(cell) else "", styleN) for cell in row] for row in [list(df.columns)] + df.values.tolist()]

    col_widths = [18*mm, 22*mm, 22*mm, 15*mm, 15*mm, 17*mm, 18*mm, 80*mm]

    pdf = SimpleDocTemplate(file_name, pagesize=A4)
    table = Table(data, repeatRows=1, colWidths=col_widths)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-2, -1), 'CENTER'),
        ('ALIGN', (-1, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
            [colors.whitesmoke, colors.lightyellow]),
    ])
    table.setStyle(style)

    title = Paragraph(
        f"<b>PONTAJ – {calendar.month_name[month].upper()} {year}</b>",
        styles['Title']
    )
    elems = [title, Spacer(1, 12), table]
    pdf.build(elems)
    print(f"[✔] Fișier PDF salvat: {file_name}")
    return file_name


def main(month, year):
    df = generate_pontaj_dataframe(month, year)
    csv_file = export_to_csv(df, month, year)
    excel_file = csv_to_excel(csv_file, month, year)
    pdf_file = excel_to_pdf(excel_file, month, year)


# Exemplu de utilizare: Aprilie 2025
if __name__ == "__main__":
    main(4, 2025)
