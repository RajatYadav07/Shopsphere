"""
ShopSphere — Final Project Report Generator for Lovely Professional University (LPU)
Author: Rajat Yadav (Reg. No. 12308041)
Produces: D:\Mongo_db-project\ShopSphere\report\ShopSphere_MongoDB_Project_Report_Rajat_Yadav.docx
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

REPORT_DIR = r"D:\Mongo_db-project\ShopSphere\report"
ASSETS_DIR = r"D:\Mongo_db-project\ShopSphere\report_assets"
DOCX_PATH = os.path.join(REPORT_DIR, "ShopSphere_MongoDB_Project_Report_Rajat_Yadav.docx")

os.makedirs(REPORT_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# XML Helper Functions for Professional Word Formatting
# -----------------------------------------------------------------------------

def set_cell_background(cell, color_hex):
    """Set shading color for a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set internal cell margins (padding) in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def prevent_row_split(row):
    """Ensure table row does not break across pages."""
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def set_repeat_header(row):
    """Repeat header row on subsequent pages."""
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    """Apply elegant subtle borders to a table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_page_number(run):
    """Insert a dynamic page number field in a run."""
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def add_numpages(run):
    """Insert total pages field in a run."""
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> NUMPAGES </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

# -----------------------------------------------------------------------------
# Document Setup and Custom Styling
# -----------------------------------------------------------------------------

def build_document():
    doc = Document()

    # Configure A4 Page Setup and Standard Academic Margins
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)   # Left margin 1.25 in for academic binding
        section.right_margin = Inches(1.0)

        # Header
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("ShopSphere — E-Commerce Database & Analytics System Using MongoDB")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(100, 116, 139)

        # Footer
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        frun_left = fp.add_run("Lovely Professional University (LPU) | Rajat Yadav (12308041)\t\tPage ")
        frun_left.font.name = "Times New Roman"
        frun_left.font.size = Pt(9)
        frun_left.font.color.rgb = RGBColor(100, 116, 139)

        frun_page = fp.add_run()
        frun_page.font.name = "Times New Roman"
        frun_page.font.size = Pt(9)
        frun_page.font.color.rgb = RGBColor(15, 23, 42)
        frun_page.bold = True
        add_page_number(frun_page)

        frun_mid = fp.add_run(" of ")
        frun_mid.font.name = "Times New Roman"
        frun_mid.font.size = Pt(9)
        frun_mid.font.color.rgb = RGBColor(100, 116, 139)

        frun_total = fp.add_run()
        frun_total.font.name = "Times New Roman"
        frun_total.font.size = Pt(9)
        frun_total.font.color.rgb = RGBColor(15, 23, 42)
        frun_total.bold = True
        add_numpages(frun_total)

    # Base Styles
    styles = doc.styles

    # Normal Style
    normal = styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(11.5)
    normal.font.color.rgb = RGBColor(15, 23, 42)
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Content Helper Functions
    def add_sec_heading(title, level=1, page_break=True):
        """Add a major section heading."""
        if page_break:
            doc.add_page_break()
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Times New Roman"
        if level == 1:
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(8)
            run.font.size = Pt(16)
            run.font.color.rgb = RGBColor(30, 58, 138)  # Deep Navy #1E3A8A
        elif level == 2:
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            run.font.size = Pt(13.5)
            run.font.color.rgb = RGBColor(15, 23, 42)   # Slate 900
        else:
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(51, 65, 85)   # Slate 700
        return p

    def add_p(text, bold_prefix="", italic=False, space_after=6):
        """Add standard justified body paragraph."""
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(11.5)
        run = p.add_run(text)
        run.italic = italic
        run.font.name = "Times New Roman"
        run.font.size = Pt(11.5)
        return p

    def add_bullet(text, bold_prefix=""):
        """Add bullet item."""
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(11)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        return p

    def add_code_block(code_str):
        """Add a professional monospaced syntax box with gray background."""
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        
        # Border
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'<w:left w:val="single" w:sz="16" w:space="0" w:color="3B82F6"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

        run = p.add_run(code_str)
        run.font.name = "Consolas"
        run.font.size = Pt(9.0)
        run.font.color.rgb = RGBColor(30, 41, 59)

        # Empty spacing paragraph
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(4)

    def add_img(img_name, caption_text, width_in=6.0):
        """Insert figure image with centered alignment and numbered caption."""
        img_path = os.path.join(ASSETS_DIR, img_name)
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next = True
            run = p.add_run()
            run.add_picture(img_path, width=Inches(width_in))

            p_cap = doc.add_paragraph()
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(10)
            p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_cap = p_cap.add_run(caption_text)
            r_cap.italic = True
            r_cap.font.name = "Times New Roman"
            r_cap.font.size = Pt(10)
            r_cap.font.color.rgb = RGBColor(71, 85, 105)
        else:
            p = doc.add_paragraph()
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(f"[FIGURE PLACEHOLDER: {img_name} - {caption_text}]")
            r.bold = True
            r.font.color.rgb = RGBColor(220, 38, 38)

    def add_styled_table(headers, rows_data, col_widths=None):
        """Create a professional academic table with dark header, alternating rows, and non-splitting rows."""
        tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="CBD5E1", sz="4", val="single")

        # Header Row
        hdr_row = tbl.rows[0]
        prevent_row_split(hdr_row)
        set_repeat_header(hdr_row)

        for col_idx, h_text in enumerate(headers):
            cell = hdr_row.cells[col_idx]
            set_cell_background(cell, "1E3A8A")  # Deep Navy #1E3A8A
            set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(h_text)
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(255, 255, 255)

        # Data Rows
        for r_idx, row_values in enumerate(rows_data):
            row = tbl.rows[r_idx + 1]
            prevent_row_split(row)
            bg_color = "F8FAFC" if (r_idx % 2 == 1) else "FFFFFF"

            for c_idx, val in enumerate(row_values):
                cell = row.cells[c_idx]
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                # Left-align first column, center others
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(str(val))
                run.font.name = "Times New Roman"
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(15, 23, 42)

        # Set Column Widths if provided
        if col_widths and len(col_widths) == len(headers):
            for row in tbl.rows:
                for c_idx, w in enumerate(col_widths):
                    row.cells[c_idx].width = Inches(w)

        # Spacing after table
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(8)

    print("Building Report Sections...")

    # =========================================================================
    # SECTION 1: TITLE PAGE
    # =========================================================================
    p_univ = doc.add_paragraph()
    p_univ.paragraph_format.space_before = Pt(20)
    p_univ.paragraph_format.space_after = Pt(4)
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_u1 = p_univ.add_run("LOVELY PROFESSIONAL UNIVERSITY\n")
    r_u1.bold = True
    r_u1.font.size = Pt(18)
    r_u1.font.color.rgb = RGBColor(30, 58, 138)
    r_u2 = p_univ.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\nSCHOOL OF COMPUTER SCIENCE AND ENGINEERING")
    r_u2.bold = True
    r_u2.font.size = Pt(11)
    r_u2.font.color.rgb = RGBColor(71, 85, 105)

    p_subm = doc.add_paragraph()
    p_subm.paragraph_format.space_before = Pt(36)
    p_subm.paragraph_format.space_after = Pt(12)
    p_subm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s = p_subm.add_run("A CAPSTONE PROJECT REPORT ON")
    r_s.font.size = Pt(12)
    r_s.italic = True
    r_s.font.color.rgb = RGBColor(100, 116, 139)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(16)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("SHOPSPHERE — E-COMMERCE DATABASE AND ANALYTICS SYSTEM USING MONGODB")
    r_t.bold = True
    r_t.font.size = Pt(20)
    r_t.font.color.rgb = RGBColor(15, 23, 42)

    p_deg = doc.add_paragraph()
    p_deg.paragraph_format.space_before = Pt(24)
    p_deg.paragraph_format.space_after = Pt(40)
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_d = p_deg.add_run(
        "Submitted in partial fulfillment of the requirements\n"
        "for the award of the degree of\n"
        "BACHELOR OF TECHNOLOGY\n"
        "IN\n"
        "COMPUTER SCIENCE AND ENGINEERING"
    )
    r_d.font.size = Pt(11.5)
    r_d.bold = True
    r_d.font.color.rgb = RGBColor(51, 65, 85)

    # Student & Guide Details Table
    det_tbl = doc.add_table(rows=2, cols=2)
    det_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r in det_tbl.rows:
        prevent_row_split(r)
        for c in r.cells:
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
    
    c_sub = det_tbl.cell(0, 0)
    p_c1 = c_sub.paragraphs[0]
    p_c1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r1 = p_c1.add_run("Submitted By:\n")
    r1.bold = True
    r1.font.size = Pt(11)
    r2 = p_c1.add_run("RAJAT YADAV\nRegistration No: 12308041\nProgramme: B.Tech CSE")
    r2.font.size = Pt(11)

    c_gui = det_tbl.cell(0, 1)
    p_c2 = c_gui.paragraphs[0]
    p_c2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r3 = p_c2.add_run("Under the Guidance of:\n")
    r3.bold = True
    r3.font.size = Pt(11)
    r4 = p_c2.add_run("[TO BE FILLED IN AFTER CONFIRMATION]\nFaculty / Project Guide\nSchool of CSE, LPU")
    r4.font.size = Pt(11)

    p_sess = doc.add_paragraph()
    p_sess.paragraph_format.space_before = Pt(48)
    p_sess.paragraph_format.space_after = Pt(0)
    p_sess.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ses = p_sess.add_run("Lovely Professional University, Phagwara, Punjab (India)\nAcademic Session: 2026–2027")
    r_ses.bold = True
    r_ses.font.size = Pt(11)
    r_ses.font.color.rgb = RGBColor(71, 85, 105)

    # =========================================================================
    # SECTION 2: CERTIFICATE
    # =========================================================================
    add_sec_heading("CERTIFICATE", level=1, page_break=True)
    add_p(
        "This is to certify that the project entitled \"ShopSphere — E-Commerce Database and Analytics System Using MongoDB\", "
        "submitted by RAJAT YADAV (Registration Number: 12308041) in partial fulfillment of the requirements for the award of the "
        "degree of Bachelor of Technology in Computer Science and Engineering from Lovely Professional University, Punjab, is a "
        "bona fide record of technical work carried out under my supervision and guidance."
    )
    add_p(
        "The software architecture, database design, indexing strategies, real-time aggregation pipelines, and full-stack implementation "
        "embodied in this report have been executed and verified against genuine e-commerce big data. To the best of my knowledge, "
        "the matter presented in this report has not been submitted in part or full to any other University or Institution for the award "
        "of any degree or diploma."
    )

    cert_tbl = doc.add_table(rows=2, cols=2)
    cert_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r in cert_tbl.rows:
        prevent_row_split(r)
        for c in r.cells:
            set_cell_margins(c, top=200, bottom=100, left=100, right=100)
    
    c_g = cert_tbl.cell(1, 0)
    p_g = c_g.paragraphs[0]
    p_g.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_g1 = p_g.add_run("______________________________\n")
    r_g2 = p_g.add_run("Project Guide / Supervisor\n")
    r_g2.bold = True
    r_g3 = p_g.add_run("Name: [TO BE FILLED IN AFTER CONFIRMATION]\nDesignation: [TO BE FILLED IN]\nDepartment of Computer Science & Engineering\nLovely Professional University")
    for r in [r_g1, r_g2, r_g3]:
        r.font.size = Pt(10)

    c_h = cert_tbl.cell(1, 1)
    p_h = c_h.paragraphs[0]
    p_h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_h1 = p_h.add_run("______________________________\n")
    r_h2 = p_h.add_run("Head of Department\n")
    r_h2.bold = True
    r_h3 = p_h.add_run("Department of Computer Science & Engineering\nSchool of Computer Science & Engineering\nLovely Professional University")
    for r in [r_h1, r_h2, r_h3]:
        r.font.size = Pt(10)

    p_dt = doc.add_paragraph()
    p_dt.paragraph_format.space_before = Pt(36)
    r_dt = p_dt.add_run("Date: ____________________\nPlace: Lovely Professional University, Phagwara, Punjab")
    r_dt.font.size = Pt(10.5)

    # =========================================================================
    # SECTION 3: DECLARATION
    # =========================================================================
    add_sec_heading("DECLARATION", level=1, page_break=True)
    add_p(
        "I hereby declare that the project report entitled \"ShopSphere — E-Commerce Database and Analytics System Using MongoDB\", "
        "submitted to Lovely Professional University, Phagwara, Punjab, in partial fulfillment of the requirements for the award of the "
        "degree of Bachelor of Technology in Computer Science and Engineering, is an authentic record of my own research, system design, "
        "and software engineering work carried out during the academic session 2026–2027."
    )
    add_p(
        "I affirm that the codebase, database schemas, MongoDB aggregation pipelines, query execution plan optimizations, and "
        "documentation presented in this report are original. Where contributions, third-party libraries (FastAPI, React, Vite, PyMongo), "
        "or external datasets (Brazilian E-Commerce Public Dataset by Olist, licensed via CC BY-NC-SA 4.0) have been utilized, they have "
        "been explicitly cited, referenced, and attributed in accordance with international academic integrity and ethical guidelines."
    )
    add_p(
        "I further declare that this work has not formed the basis for the award of any other degree, diploma, associate-ship, or fellowship "
        "at this or any other university or educational institution."
    )

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(60)
    p_sig.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_s1 = p_sig.add_run("______________________________\n")
    r_s2 = p_sig.add_run("RAJAT YADAV\n")
    r_s2.bold = True
    r_s3 = p_sig.add_run("Registration No: 12308041\nRoll No: [TO BE FILLED IN]\nB.Tech Computer Science and Engineering\nLovely Professional University")
    for r in [r_s1, r_s2, r_s3]:
        r.font.size = Pt(10.5)

    p_dt2 = doc.add_paragraph()
    p_dt2.paragraph_format.space_before = Pt(20)
    r_dt2 = p_dt2.add_run("Date: ____________________\nPlace: Lovely Professional University, Punjab")
    r_dt2.font.size = Pt(10.5)

    # =========================================================================
    # SECTION 4: ACKNOWLEDGEMENT
    # =========================================================================
    add_sec_heading("ACKNOWLEDGEMENT", level=1, page_break=True)
    add_p(
        "The successful completion of this comprehensive database systems and full-stack software engineering project has been made "
        "possible through the guidance, mentorship, and encouragement of several individuals and academic resources at Lovely Professional University."
    )
    add_p(
        "First and foremost, I express my profound gratitude to my Project Guide, [TO BE FILLED IN AFTER CONFIRMATION], Department of Computer Science "
        "and Engineering, for providing constructive feedback, technical guidance, and valuable insights into NoSQL database architecture throughout the "
        "design, implementation, and empirical verification phases of ShopSphere."
    )
    add_p(
        "I extend my sincere appreciation to the Head of Department, School of Computer Science and Engineering, Lovely Professional University, "
        "for providing an environment conducive to technical innovation, high-performance computing labs, and rigorous academic standards."
    )
    add_p(
        "I am equally thankful to the global open-source software community: MongoDB Inc. for engineering Community Server 8.0 with the "
        "WiredTiger storage engine; the FastAPI development team led by Sebastián Ramírez for modern asynchronous Python tooling; the React and "
        "Vite core teams for ultra-fast frontend developer experiences; and Olist along with Kaggle for making the authentic Brazilian E-Commerce "
        "public dataset available for academic study."
    )
    add_p(
        "Finally, I express my heartfelt indebtedness to my parents, family members, and peers for their continuous moral support, understanding, "
        "and encouragement throughout the duration of this engineering endeavour."
    )

    p_ack_sig = doc.add_paragraph()
    p_ack_sig.paragraph_format.space_before = Pt(36)
    p_ack_sig.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_as1 = p_ack_sig.add_run("RAJAT YADAV\n")
    r_as1.bold = True
    r_as2 = p_ack_sig.add_run("Registration No: 12308041\nB.Tech CSE, Lovely Professional University")
    r_as1.font.size = Pt(11)
    r_as2.font.size = Pt(10.5)

    # =========================================================================
    # SECTION 5: ABSTRACT
    # =========================================================================
    add_sec_heading("ABSTRACT", level=1, page_break=True)
    add_p(
        "Modern enterprise e-commerce platforms handle massive transaction volumes, highly dynamic product catalogues, and low-latency "
        "analytical demands that frequently expose the scalability and architectural limitations of legacy Relational Database Management Systems "
        "(RDBMS). Traditional relational models rely on heavy normalization and multi-table SQL JOIN operations that degrade exponentially under "
        "high concurrency, while rigid table schemas inhibit rapid catalog schema evolution. This project presents ShopSphere, an enterprise-grade "
        "e-commerce database management and real-time business intelligence analytics platform engineered on MongoDB Community Server 8.0, Python "
        "FastAPI, and React 18 with TypeScript."
    )
    add_p(
        "The core technical contribution of ShopSphere centers on an empirical NoSQL document-modelling paradigm that synthesizes embedded sub-document "
        "structures with referenced document architectures. Historical order integrity is achieved by denormalizing purchased line-item snapshots and "
        "shipping addresses directly inside order documents, guaranteeing single-read retrieval and price immutability without SQL joins. Customer profiles "
        "and product catalog entities are linked via BSON ObjectId references to eliminate uncontrolled data duplication and satisfy document size constraints. "
        "The platform ingests and normalizes the genuine Brazilian E-Commerce Public Dataset by Olist, transforming relational CSV tables into 99,441 authentic "
        "customer documents, 98,666 order documents, 32,951 product records, 97,709 review records, and 3,095 seller entities in a dedicated production "
        "database (`shopsphere_olist`)."
    )
    add_p(
        "To enforce database-level integrity, collection-level `$jsonSchema` validators are deployed directly within the MongoDB engine, rejecting "
        "malformed writes at the persistence tier. Query performance optimization is empirically verified using live `explain(\"executionStats\")`, "
        "demonstrating an index scan (`IXSCAN`) that examines precisely 1 key and 1 document in 0.0 ms compared to an unindexed collection scan (`COLLSCAN`) "
        "that sequentially scans all 32,951 documents. Real-time executive dashboards and business intelligence reporting are powered by 8 multi-stage "
        "MongoDB aggregation pipelines leveraging `$match`, `$unwind`, `$lookup`, `$group`, `$facet`, and `$dateToString`. Strict environment isolation "
        "guarantees that production historical data remains immutable, while interactive demonstrations operate within an isolated demo collection "
        "(`shopsphere_demo`) and automated unit/integration tests execute against a dedicated test database (`shopsphere_test`). All 12 automated test suites "
        "pass in 0.69 seconds, verifying that ShopSphere delivers an enterprise-ready, academically rigorous, and scalable NoSQL database foundation."
    )
    add_p(
        "Keywords: MongoDB 8.0, NoSQL Document Modeling, Aggregation Framework, B-Tree Query Optimization, $jsonSchema Validation, FastAPI, React TypeScript, Olist Dataset.",
        bold_prefix="Keywords: "
    )

    # =========================================================================
    # SECTION 6: TABLE OF CONTENTS
    # =========================================================================
    add_sec_heading("TABLE OF CONTENTS", level=1, page_break=True)
    
    toc_items = [
        ("Certificate", "ii"),
        ("Declaration", "iii"),
        ("Acknowledgement", "iv"),
        ("Abstract", "v"),
        ("List of Figures", "viii"),
        ("List of Tables", "ix"),
        ("1. Introduction", "1"),
        ("    1.1 Background of E-Commerce Database Management Systems", "1"),
        ("    1.2 Evolution from Relational Models to Document-Oriented NoSQL", "2"),
        ("    1.3 Why MongoDB Community 8.0 for Modern E-Commerce Platforms", "3"),
        ("    1.4 Overview of the ShopSphere Platform & Architectural Vision", "4"),
        ("2. Problem Statement", "5"),
        ("    2.1 The Relational Join Bottleneck in Enterprise E-Commerce", "5"),
        ("    2.2 Data Redundancy vs Consistency in Historical Order Records", "6"),
        ("    2.3 Real-Time Analytical Demands on Operational Databases", "6"),
        ("    2.4 Real-World Data Hygiene, Anonymization & Idempotency", "7"),
        ("3. Objectives of the Project", "8"),
        ("    3.1 Primary Academic and Architectural Objectives", "8"),
        ("    3.2 Specific Technical Deliverables", "8"),
        ("4. Scope of the Project", "10"),
        ("    4.1 Functional Modules in Scope", "10"),
        ("    4.2 Explicit Boundaries & Limitations", "11"),
        ("5. Literature Review", "12"),
        ("    5.1 NoSQL Databases and Document-Store Paradigms", "12"),
        ("    5.2 Storage Engine Architectures: MongoDB WiredTiger Engine", "13"),
        ("    5.3 Modern Reactive Web Architectures (FastAPI & React)", "14"),
        ("    5.4 The Brazilian E-Commerce Dataset by Olist", "15"),
        ("    5.5 Comparative Evaluation: RDBMS vs MongoDB Document Model", "16"),
        ("6. System Requirements (Hardware and Software)", "17"),
        ("    6.1 Hardware Specifications", "17"),
        ("    6.2 Software & Dependency Stack", "17"),
        ("    6.3 Network Topology & Environment Configuration", "18"),
        ("7. System Design and Architecture", "19"),
        ("    7.1 Three-Tier Client-Server Architecture", "19"),
        ("    7.2 Component-Level Architectural Decomposition", "20"),
        ("    7.3 Data Ingestion & ETL Processing Workflow", "21"),
        ("    7.4 End-to-End API Request & Query Pipeline", "22"),
        ("    7.5 Database Separation Architecture", "23"),
        ("8. Database Design", "24"),
        ("    8.1 MongoDB Collection Architecture & Entity Overview", "24"),
        ("    8.2 Embedded vs Referenced Data Modeling Strategy", "25"),
        ("    8.3 Detailed Collection Schema Specifications", "26"),
        ("    8.4 Database-Level $jsonSchema Validation Engine", "29"),
        ("    8.5 B-Tree Indexing Strategy", "30"),
        ("9. Implementation and Methodology", "32"),
        ("    9.1 Authentic Dataset Discovery & Preprocessing Engine", "32"),
        ("    9.2 UTF-8 BOM Stripping & Multilingual Category Translation", "33"),
        ("    9.3 Deterministic Hashing & Idempotent Upsert Strategy", "34"),
        ("    9.4 Anonymization Preserving Data Hygiene", "35"),
        ("    9.5 Backend Service & Repository Layer Implementation", "35"),
        ("    9.6 Frontend Single-Page Application Implementation", "36"),
        ("10. MongoDB Queries and Operations", "37"),
        ("    10.1 Core CRUD Operations", "37"),
        ("    10.2 Production Aggregation Pipelines (8 Real Queries)", "39"),
        ("    10.3 Query Execution Optimization (explain('executionStats'))", "44"),
        ("    10.4 Schema Validation Enforcement & Write Rejection", "46"),
        ("11. Results and Output Screenshots", "47"),
        ("    11.1 Executive Analytics Dashboard Walkthrough", "47"),
        ("    11.2 Product Catalogue & Filtering System", "48"),
        ("    11.3 Customer CRM & Demographic Distribution", "49"),
        ("    11.4 Transactional Order Fulfillment & Immutability Verification", "50"),
        ("    11.5 Customer Reviews & Rating Distributions", "51"),
        ("    11.6 Inventory & Stock Movement Audit Trail", "52"),
        ("    11.7 Business Intelligence & Aggregation Reports", "53"),
        ("    11.8 Interactive MongoDB Concepts & Viva Laboratory", "54"),
        ("    11.9 Database Topology & Connection Settings", "55"),
        ("    11.10 Customer-Facing Storefront", "56"),
        ("    11.11 FastAPI Swagger API Documentation", "57"),
        ("12. Testing and Validation", "58"),
        ("    12.1 Automated Testing Strategy & Isolation Philosophy", "58"),
        ("    12.2 Test Suite Execution Results (12/12 Passing)", "58"),
        ("    12.3 Comprehensive Test Matrix Table", "59"),
        ("    12.4 Frontend TypeScript & Vite Production Build Verification", "61"),
        ("    12.5 Historical Immutability & Concurrency Safeguards", "61"),
        ("    12.6 Idempotency Verification Matrix", "62"),
        ("13. Challenges Faced", "63"),
        ("    13.1 Complexities of Real-World Big Data Ingestion", "63"),
        ("    13.2 Balancing Data Integrity with NoSQL Flexibility", "63"),
        ("    13.3 Relational-to-Document Paradigm Shift", "64"),
        ("    13.4 Transactional Concurrency on Standalone Instances", "64"),
        ("    13.5 Query Performance Optimization on 98k+ Orders", "65"),
        ("14. Conclusion", "66"),
        ("    14.1 Summary of Technical Achievements", "66"),
        ("    14.2 Pedagogical and Engineering Insights", "67"),
        ("15. Future Scope", "68"),
        ("    15.1 Replica Set Deployment & Multi-Document ACID Transactions", "68"),
        ("    15.2 Sharding & Distributed Horizontal Scaling", "68"),
        ("    15.3 Vector Search & AI-Powered Product Recommendations", "69"),
        ("    15.4 Change Streams & Real-Time Event Architecture", "69"),
        ("    15.5 Security Hardening (JWT, RBAC, Field-Level Encryption)", "70"),
        ("16. References / Bibliography", "71"),
        ("17. Appendix", "73"),
        ("    Appendix A: Complete MongoDB Shell Commands & Verification Scripts", "73"),
        ("    Appendix B: Data Dictionary & Field Specifications Table", "75"),
        ("    Appendix C: Step-by-Step Project Setup & Execution Guide", "77"),
        ("    Appendix D: Top 15 Academic Viva Voce Questions & Model Answers", "79")
    ]

    toc_tbl = doc.add_table(rows=len(toc_items), cols=2)
    toc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(toc_tbl, color="FFFFFF", sz="0", val="none")

    for idx, (title, page) in enumerate(toc_items):
        row = toc_tbl.rows[idx]
        prevent_row_split(row)
        c_title, c_page = row.cells[0], row.cells[1]
        c_title.width = Inches(5.8)
        c_page.width = Inches(0.8)
        set_cell_margins(c_title, top=30, bottom=30, left=50, right=50)
        set_cell_margins(c_page, top=30, bottom=30, left=50, right=50)

        p1 = c_title.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.paragraph_format.space_after = Pt(2)
        r_t = p1.add_run(title)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(10.5)
        if not title.startswith("    "):
            r_t.bold = True
            r_t.font.color.rgb = RGBColor(30, 58, 138)

        p2 = c_page.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.paragraph_format.space_after = Pt(2)
        r_p = p2.add_run(page)
        r_p.font.name = "Times New Roman"
        r_p.font.size = Pt(10.5)
        if not title.startswith("    "):
            r_p.bold = True

    # =========================================================================
    # SECTION 7: LIST OF FIGURES
    # =========================================================================
    add_sec_heading("LIST OF FIGURES", level=1, page_break=True)
    figures_list = [
        ("Figure 1", "ShopSphere Full-Stack System Architecture Diagram", "20"),
        ("Figure 2", "Olist Brazilian E-Commerce Import & Transformation Pipeline Workflow", "21"),
        ("Figure 3", "End-to-End API Request, Pydantic Validation & PyMongo Query Flow", "22"),
        ("Figure 4", "Multi-Database Namespace Isolation Architecture (Production, Demo, Test)", "23"),
        ("Figure 5", "MongoDB Document Model & Schema Relationships (Embedded vs Referenced)", "25"),
        ("Figure 6", "Real Application Screenshot — Executive SaaS Analytics Dashboard", "47"),
        ("Figure 7", "Real Application Screenshot — Product Catalogue Management System", "48"),
        ("Figure 8", "Real Application Screenshot — Customer CRM & Demographic Accounts Ledger", "49"),
        ("Figure 9", "Real Application Screenshot — Transactional Order Management & Immutability Badges", "50"),
        ("Figure 10", "Real Application Screenshot — Customer Reviews & Rating Distribution Analytics", "51"),
        ("Figure 11", "Real Application Screenshot — Real-Time Inventory & Movement Audit Ledger", "52"),
        ("Figure 12", "Real Application Screenshot — Business Intelligence & Multi-Dimensional Aggregation Reports", "53"),
        ("Figure 13", "Real Application Screenshot — Interactive MongoDB Concepts & Viva Laboratory", "54"),
        ("Figure 14", "Real Application Screenshot — Database Engine Settings, Standalone Topology & Document Volume", "55"),
        ("Figure 15", "Real Application Screenshot — Live Customer-Facing Shopping Storefront Experience", "56"),
        ("Figure 16", "Real Application Screenshot — FastAPI Interactive OpenAPI (Swagger UI) Documentation", "57")
    ]
    add_styled_table(["Figure Number", "Figure Caption / Description", "Page"], figures_list, col_widths=[1.5, 4.3, 0.8])

    # =========================================================================
    # SECTION 8: LIST OF TABLES
    # =========================================================================
    add_sec_heading("LIST OF TABLES", level=1, page_break=True)
    tables_list = [
        ("Table 1", "Comparative Evaluation: Relational Database (RDBMS) vs MongoDB Document Model", "16"),
        ("Table 2", "System Specifications: Hardware Environment (Minimum vs Recommended)", "17"),
        ("Table 3", "Complete Software Dependency Stack and Engine Versions", "18"),
        ("Table 4", "Verified MongoDB Collection Counts in Primary Production Database (`shopsphere_olist`)", "24"),
        ("Table 5", "Olist Relational CSV Source to MongoDB Document Collection Mapping Reference", "33"),
        ("Table 6", "Empirical Query Optimization Benchmark: B-Tree IXSCAN vs Unindexed COLLSCAN", "45"),
        ("Table 7", "Comprehensive Pytest Automated Test Execution Matrix (12 Verified Unit & Integration Tests)", "59"),
        ("Table 8", "Database Namespace Isolation & State Verification Matrix", "62"),
        ("Table 9", "Data Dictionary: Complete Entity & Field Specification Matrix", "75")
    ]
    add_styled_table(["Table Number", "Table Title / Description", "Page"], tables_list, col_widths=[1.4, 4.4, 0.8])

    # =========================================================================
    # SECTION 9: INTRODUCTION
    # =========================================================================
    add_sec_heading("1. INTRODUCTION", level=1, page_break=True)
    
    add_sec_heading("1.1 Background of E-Commerce Database Management Systems", level=2, page_break=False)
    add_p(
        "Electronic commerce (e-commerce) has evolved into one of the most data-intensive domains in contemporary software engineering. "
        "Modern digital storefronts, multi-vendor marketplaces, and omnichannel retail platforms operate under demanding workloads characterized "
        "by unpredictable traffic spikes, deeply nested product specifications, and high-frequency read operations. In a typical e-commerce session, "
        "users perform faceted catalog filtering, dynamic multi-attribute search, real-time stock verification, checkout processing, and review browsing. "
        "These interactions demand sub-second latency regardless of concurrency levels."
    )
    add_p(
        "For decades, Relational Database Management Systems (RDBMS) such as PostgreSQL, MySQL, and Oracle served as the uncontested foundation "
        "of commercial retail systems. Relational engines rely on rigorous Boyce-Codd Normal Form (BCNF) normalization, strict tabular schemas, "
        "and ACID transactions. However, as catalog diversity expanded to encompass hundreds of heterogeneous product categories—each with distinct "
        "attributes ranging from technical apparel sizing to consumer electronics specifications—the rigidity of relational schemas emerged as an "
        "operational bottleneck. The necessity of altering schemas across millions of rows to accommodate new product attributes introduces significant "
        "operational friction and costly database downtime."
    )

    add_sec_heading("1.2 Evolution from Relational Models to Document-Oriented NoSQL", level=2, page_break=False)
    add_p(
        "To resolve the limitations of relational models under internet-scale workloads, the database industry witnessed a paradigm shift toward "
        "Not Only SQL (NoSQL) data storage engines. Among the diverse NoSQL paradigms—key-value stores, wide-column families, graph databases, and "
        "document stores—document-oriented databases have emerged as the natural fit for e-commerce domain entities."
    )
    add_p(
        "Document-oriented databases represent data as self-contained, hierarchically structured JSON or Binary JSON (BSON) documents. Unlike tabular "
        "rows that strictly segregate related entities across dozens of foreign-key linked tables, document databases offer data locality of reference. "
        "An order document, for example, can natively embed its purchased line items, unit prices, discounts, and shipping addresses within a single "
        "cohesive unit of storage. This architectural alignment between application-layer domain objects and database persistence layers eliminates "
        "the Object-Relational Impedance Mismatch that has historically plagued object-oriented software engineering."
    )

    add_sec_heading("1.3 Why MongoDB Community 8.0 for Modern E-Commerce Platforms", level=2, page_break=False)
    add_p(
        "MongoDB Community Server 8.0 represents the industry standard for production document-oriented NoSQL databases, offering an ideal persistence "
        "tier for e-commerce platforms due to several fundamental architectural capabilities:"
    )
    add_bullet(" High-throughput concurrent writes and reads with page-level concurrency, in-memory caching, and transparent block compression (Snappy).", bold_prefix="WiredTiger Storage Engine:")
    add_bullet(" Powerful in-database data processing pipeline providing over 30 stages ($match, $unwind, $group, $lookup, $facet) for real-time analytical reporting without external batch processing.", bold_prefix="Aggregation Framework:")
    add_bullet(" Versatile indexing engine supporting single-field, compound, text, geospatial, and partial filter indexes to optimize diverse search patterns.", bold_prefix="B-Tree Indexing Architecture:")
    add_bullet(" Collection-level schema enforcement using standard JSON Schema definitions, ensuring strict data hygiene without compromising document polymorphism.", bold_prefix="Native $jsonSchema Validation:")
    add_bullet(" Single-document atomicity guarantees, coupled with distributed multi-document ACID transactions across replica sets.", bold_prefix="Enterprise Consistency Guarantees:")

    add_sec_heading("1.4 Overview of the ShopSphere Platform & Architectural Vision", level=2, page_break=False)
    add_p(
        "ShopSphere is an enterprise-grade full-stack e-commerce database management and real-time business intelligence platform engineered to "
        "demonstrate advanced NoSQL data modeling, performance optimization, and authentic big data ingestion on MongoDB Community Server 8.0. "
        "The system pairs a high-performance Python FastAPI backend with a reactive React 18 and TypeScript frontend bundled via Vite."
    )
    add_p(
        "Rather than relying on toy synthetic datasets, ShopSphere is architected and empirically validated against the authentic Brazilian E-Commerce "
        "Public Dataset by Olist, comprising over 100,000 real-world commercial transactions. The platform provides an Executive Dashboard, Product Catalog "
        "Management, Customer Relationship Management (CRM), Transactional Order Fulfillment, Inventory Movement Auditing, Customer Sentiment Reviews, "
        "and a dedicated MongoDB Concepts Laboratory designed for academic evaluation and technical viva voce demonstrations."
    )

    # =========================================================================
    # SECTION 10: PROBLEM STATEMENT
    # =========================================================================
    add_sec_heading("2. PROBLEM STATEMENT", level=1, page_break=True)
    
    add_sec_heading("2.1 The Relational Join Bottleneck in Enterprise E-Commerce", level=2, page_break=False)
    add_p(
        "In a conventional relational e-commerce schema, fulfilling a standard customer order inquiry requires executing SQL queries spanning "
        "at least five to seven normalized tables: `orders`, `order_items`, `products`, `customers`, `addresses`, `payments`, and `discounts`. "
        "As database scale expands beyond millions of historical records, relational JOIN operations consume substantial CPU and buffer pool memory. "
        "Under high concurrency, locking mechanisms and index traversal across normalized foreign key hierarchies induce significant query latency, "
        "degrading the user experience and increasing infrastructure costs."
    )

    add_sec_heading("2.2 Data Redundancy vs Consistency in Historical Order Records", level=2, page_break=False)
    add_p(
        "A critical vulnerability in poorly designed relational databases is the temporal mutation of historical transaction records. If an order "
        "table merely references a `products` table via foreign key, any subsequent price adjustment or product description modification in the master "
        "catalog inadvertently alters the historical record of past orders. Preventing this requires creating synthetic snapshot tables or historical "
        "audit ledgers, introducing database complexity. A primary challenge addressed in this project is designing an embedded document architecture "
        "that atomically freezes line-item prices and product snapshots at the instant of checkout, guaranteeing historical immutability."
    )

    add_sec_heading("2.3 Real-Time Analytical Demands on Operational Databases", level=2, page_break=False)
    add_p(
        "Executive decision-makers require real-time visibility into Gross Revenue, Monthly Sales Trends, Category Performance Breakdown, and "
        "Customer Lifetime Value (LTV). Traditionally, organizations deploy complex Extract, Transform, Load (ETL) pipelines to replicate operational "
        "data into external Data Warehouses (OLAP), incurring sync delays of hours or days. A central problem addressed by ShopSphere is executing "
        "low-latency analytical aggregations directly on the operational MongoDB database without degrading concurrent transaction throughput."
    )

    add_sec_heading("2.4 Real-World Data Hygiene, Anonymization & Idempotency", level=2, page_break=False)
    add_p(
        "Working with authentic real-world data—specifically the Brazilian E-Commerce Public Dataset by Olist—presents significant data engineering "
        "hurdles. The raw dataset contains non-uniform characters (UTF-8 BOM), multilingual categories (Portuguese requiring English normalization), "
        "anonymized customer emails (null values), and repeated review identifiers. Ingesting this data without fabricating synthetic contact details, "
        "violating database-level unique constraints, or corrupting document relationships requires an idempotent ETL pipeline with deterministic "
        "surrogate keys and partial filter indexing."
    )

    # =========================================================================
    # SECTION 11: OBJECTIVES OF THE PROJECT
    # =========================================================================
    add_sec_heading("3. OBJECTIVES OF THE PROJECT", level=1, page_break=True)
    
    add_sec_heading("3.1 Primary Academic and Architectural Objectives", level=2, page_break=False)
    add_p(
        "The overarching aim of this project is to research, design, implement, and validate an enterprise-grade e-commerce database management "
        "and business intelligence analytics system utilizing modern NoSQL document modeling principles on MongoDB Community Server 8.0."
    )

    add_sec_heading("3.2 Specific Technical Deliverables", level=2, page_break=False)
    add_p("To realize the primary aim, the project focuses on seven rigorous technical objectives:")
    add_bullet(" Formulate a hybrid data model that embeds 1-to-few bounded arrays (purchased items, payment installments, shipping addresses) within orders to ensure historical immutability, while referencing unbounded entities (customers, products) via ObjectIds to eliminate duplication.", bold_prefix="1. Advanced Document Modeling:")
    add_bullet(" Implement complete Create, Read, Update, and Delete operations across collections using the PyMongo driver, featuring cursor pagination, multi-field regex search, and dynamic sorting.", bold_prefix="2. High-Performance CRUD Primitives:")
    add_bullet(" Construct and optimize 8 production-grade aggregation pipelines to compute monthly revenue growth, category sales shares, top-performing SKUs, customer LTV, and basket sizing.", bold_prefix="3. Real-Time Aggregation Framework:")
    add_bullet(" Implement single-field, compound, text, and partial filter B-Tree indexes, validating performance improvements empirically via explain('executionStats') to demonstrate IXSCAN vs COLLSCAN gains.", bold_prefix="4. Query Optimization & Index Benchmarking:")
    add_bullet(" Embed native $jsonSchema validators within collection metadata to reject malformed document inserts and updates at the storage engine layer.", bold_prefix="5. Database-Level Schema Validation:")
    add_bullet(" Build an idempotent, deterministic ETL importer capable of parsing, translating, denormalizing, and ingesting over 100,000 authentic records from the Kaggle Olist Brazilian E-Commerce dataset into shopsphere_olist.", bold_prefix="6. Authentic Big Data Ingestion:")
    add_bullet(" Maintain absolute namespace separation between production historical records (shopsphere_olist), operational sandbox demo records (shopsphere), and automated test records (shopsphere_test).", bold_prefix="7. Strict Multi-Database Isolation:")

    # =========================================================================
    # SECTION 12: SCOPE OF THE PROJECT
    # =========================================================================
    add_sec_heading("4. SCOPE OF THE PROJECT", level=1, page_break=True)
    
    add_sec_heading("4.1 Functional Modules in Scope", level=2, page_break=False)
    add_p("The ShopSphere application encompasses nine fully implemented, interacting modules:")
    add_bullet(" Real-time executive KPI metrics (Gross Revenue, Total Orders, Active Customers, Catalogue Size), Monthly Sales Time-Series charts, and Category Revenue Breakdown.", bold_prefix="1. Executive Analytics Dashboard:")
    add_bullet(" Server-side paginated product catalog featuring multi-attribute search, category filtering, price range controls, stock-level badges, and modal CRUD operations.", bold_prefix="2. Product Catalog Management:")
    add_bullet(" Customer profile directory displaying unique customer identifiers, Brazilian state demographics, order counts, and aggregated Lifetime Value (LTV).", bold_prefix="3. Customer Relationship Management (CRM):")
    add_bullet(" Full order lifecycle tracking with embedded line-item snapshots, status transition safeguards, cancellation compensation, and immutable historical tags.", bold_prefix="4. Transactional Order Fulfillment:")
    add_bullet(" Customer review ledger displaying 1-to-5 star ratings, Portuguese review text, and automated background recalculation of product average ratings.", bold_prefix="5. Customer Reviews & Ratings:")
    add_bullet(" Real-time inventory monitoring with low-stock warnings (< 10 units), manual restock/write-off adjustments, and permanent movement logging.", bold_prefix="6. Inventory Audit Trail Ledger:")
    add_bullet(" Interactive sandbox designed for academic evaluation, featuring live CRUD execution, embedding vs referencing visualizer, 8 one-click aggregation pipelines, and live explain() query plan comparisons.", bold_prefix="7. MongoDB Concepts Laboratory:")
    add_bullet(" End-user shopping interface allowing catalog exploration by category pills, shopping cart management, and real-time MongoDB order checkout.", bold_prefix="8. Customer-Facing Storefront:")
    add_bullet(" Auto-generated OpenAPI 3.1 Swagger UI and ReDoc specifications exposing all backend routes, request schemas, and response contracts.", bold_prefix="9. RESTful API Documentation:")

    add_sec_heading("4.2 Explicit Boundaries & Limitations", level=2, page_break=False)
    add_p(
        "To preserve academic honesty and architectural integrity, the following boundaries and constraints are explicitly recognized:"
    )
    add_bullet(" The public Olist dataset is an anonymized historical marketplace dataset that does not contain warehouse stock counts or movement ledgers. Products are honestly flagged with inventory_tracked=false and stock_quantity=0. No synthetic stock or warehouse transactions were fabricated for historical items.", bold_prefix="1. Zero Fabricated Inventory in Historical Data:")
    add_bullet(" Customer email addresses in the genuine Olist dataset are anonymized and stored as null. Rather than inventing fake emails, a MongoDB partial unique index is deployed to allow null values while enforcing uniqueness on real string emails.", bold_prefix="2. Anonymized Customer Contact Details:")
    add_bullet(" All historical Olist orders are permanently flagged with is_historical=true and source='olist_real'. The API rejects modification or cancellation attempts on historical records with HTTP 400 Bad Request.", bold_prefix="3. Historical Order Immutability:")
    add_bullet(" In standalone MongoDB Community setups (without a multi-node Replica Set), native multi-document ACID transactions are unavailable. The platform implements an atomic two-phase compensation pattern to ensure safe inventory allocation and cancellation rollback.", bold_prefix="4. Standalone Transaction Fallback:")
    add_bullet(" Production user authentication (OAuth2 / JWT) and third-party payment gateways (Stripe / PayPal) are beyond the database-centric scope of this capstone project.", bold_prefix="5. Excluded Features:")

    # =========================================================================
    # SECTION 13: LITERATURE REVIEW
    # =========================================================================
    add_sec_heading("5. LITERATURE REVIEW", level=1, page_break=True)
    
    add_sec_heading("5.1 NoSQL Databases and Document-Store Paradigms", level=2, page_break=False)
    add_p(
        "The theoretical foundations of NoSQL data systems emerged in response to Brewer's CAP Theorem (Brewer, 2000; Gilbert & Lynch, 2002), "
        "which posits that a distributed data store can simultaneously guarantee at most two out of three properties: Consistency, Availability, "
        "and Partition Tolerance. Traditional relational engines prioritize strict ACID consistency (C) at the expense of horizontal partition "
        "tolerance (P). In contrast, modern document databases provide configurable consistency levels and partition resilience."
    )
    add_p(
        "According to Cattell (2011) and Stonebraker (2010), document stores provide a compelling compromise between the unstructured flexibility of "
        "key-value stores and the rigid semantics of relational databases. By structuring data into semi-structured BSON documents, applications can "
        "nest complex multi-dimensional attributes directly within domain records, drastically reducing read-path computational complexity."
    )

    add_sec_heading("5.2 Storage Engine Architectures: MongoDB WiredTiger Engine", level=2, page_break=False)
    add_p(
        "The persistence architecture of MongoDB Community 8.0 is governed by the WiredTiger storage engine. WiredTiger employs fine-grained "
        "document-level concurrency control via ticket-based concurrency algorithms, preventing table-level and collection-level write contention. "
        "Data persistence is managed through write-ahead logging (journaling) coupled with periodic 60-second checkpointing, ensuring crash recovery "
        "to a consistent checkpoint state (MongoDB Inc., 2026)."
    )
    add_p(
        "WiredTiger leverages Snappy compression by default for collection blocks, achieving typical compression ratios of 50% to 70% compared to raw JSON. "
        "Memory management is governed by an internal cache (configured by default to 50% of available physical RAM minus 1 GB), ensuring hot working "
        "sets remain in memory while cold documents are lazily evicted to disk."
    )

    add_sec_heading("5.3 Modern Reactive Web Architectures (FastAPI & React)", level=2, page_break=False)
    add_p(
        "Modern web applications demand asynchronous application runtimes capable of handling thousands of concurrent I/O operations without thread "
        "starvation. Python FastAPI (Ramírez, 2024) leverages Starlette and Pydantic v2 to deliver asynchronous request routing over the Asynchronous "
        "Server Gateway Interface (ASGI). Pydantic v2 compiles schema validation routines in Rust, delivering serialization speeds up to 20x faster "
        "than legacy Python validation libraries."
    )
    add_p(
        "On the presentation tier, React 18 (Meta Platforms, 2024) utilizes concurrent rendering and a virtual DOM reconciliation engine to minimize "
        "browser layout recalculations. When paired with Vite 8 (You, 2024), frontend developers benefit from native ES-module Hot Module Replacement (HMR) "
        "and optimized Rollup production bundling."
    )

    add_sec_heading("5.4 The Brazilian E-Commerce Dataset by Olist", level=2, page_break=False)
    add_p(
        "The Brazilian E-Commerce Public Dataset released by Olist on Kaggle (Olist & Kaggle, 2018) comprises 100,000 anonymized real-world orders "
        "placed between 2016 and 2018 across Brazilian marketplaces. The dataset encompasses diverse dimensions including order statuses, customer postal "
        "codes, multi-item order lines, diverse payment methods (boleto, credit card, vouchers), and authentic Portuguese customer reviews."
    )
    add_p(
        "Academic literature widely cites the Olist dataset as a gold standard for supply chain analysis, customer sentiment mining, and database "
        "benchmarking. Transforming its relational, highly normalized CSV structure into an optimized document model provides an exemplary case study "
        "in modern database re-engineering."
    )

    add_sec_heading("5.5 Comparative Evaluation: RDBMS vs MongoDB Document Model", level=2, page_break=False)
    add_p(
        "Table 1 outlines the architectural differences between traditional Relational Database Management Systems and the MongoDB document model "
        "implemented in ShopSphere."
    )

    comp_table = [
        ("Data Model", "Rigid tabular rows and columns", "Polymorphic BSON document trees"),
        ("Relationships", "Foreign key constraints & JOINs", "Embedded subdocuments & referenced ObjectIds"),
        ("Schema Flexibility", "Strict DDL migrations (ALTER TABLE)", "Dynamic schemas with optional $jsonSchema"),
        ("Read Performance", "High join latency under concurrency", "Single-read retrieval via denormalized locality"),
        ("Query Language", "Structured Query Language (SQL)", "MongoDB Query Language (MQL) & Aggregations"),
        ("Storage Engine", "B-Tree page structures (InnoDB/Postgres)", "WiredTiger with document-level locking & Snappy"),
        ("Horizontal Scale", "Complex sharding / read replicas", "Native horizontal sharding via partition keys")
    ]
    add_styled_table(["Evaluation Dimension", "Relational Database (RDBMS)", "MongoDB Document Model (ShopSphere)"], comp_table, col_widths=[1.8, 2.4, 2.4])

    # =========================================================================
    # SECTION 14: SYSTEM REQUIREMENTS
    # =========================================================================
    add_sec_heading("6. SYSTEM REQUIREMENTS (HARDWARE AND SOFTWARE)", level=1, page_break=True)
    
    add_sec_heading("6.1 Hardware Specifications", level=2, page_break=False)
    add_p(
        "The computational requirements for hosting and executing the ShopSphere platform are categorized into minimum development specifications "
        "and recommended production specifications in Table 2."
    )

    hw_table = [
        ("Central Processor (CPU)", "Intel Core i5 / AMD Ryzen 5 (4 cores, 2.5 GHz)", "Intel Core i7 / AMD Ryzen 7 (8 cores, 3.8 GHz+)"),
        ("System Memory (RAM)", "8 GB DDR4 RAM (4 GB allocated to MongoDB)", "16 GB – 32 GB DDR4/DDR5 RAM"),
        ("Storage Subsystem", "256 GB SATA SSD (min. 5 GB free disk space)", "512 GB NVMe M.2 SSD (High random IOPS)"),
        ("Network Interface", "Standard 100 Mbps Local Loopback (127.0.0.1)", "1 Gbps Ethernet / Enterprise Network"),
        ("Display Resolution", "1366 x 768 pixels", "1920 x 1080 (Full HD) or higher")
    ]
    add_styled_table(["Hardware Component", "Minimum Development Requirement", "Recommended Production Requirement"], hw_table, col_widths=[1.6, 2.5, 2.5])

    add_sec_heading("6.2 Software & Dependency Stack", level=2, page_break=False)
    add_p(
        "ShopSphere leverages modern, battle-tested software components across all layers of the application stack, detailed in Table 3."
    )

    sw_table = [
        ("Operating System", "Microsoft Windows 11 Home / Pro (64-bit Architecture, x64)", "Host Operating System"),
        ("Database Engine", "MongoDB Community Server 8.0.34 (WiredTiger Storage Engine)", "Primary Persistence Tier"),
        ("Backend Runtime", "Python 3.12.10 (Standard 64-bit CPython Runtime)", "Application Execution Tier"),
        ("Backend Framework", "FastAPI 0.143.1 with Starlette 1.8.0 and Uvicorn 0.54.0", "Asynchronous RESTful API"),
        ("Data Validation", "Pydantic v2.14.1 and Pydantic-Settings 2.16.0", "Schema Serialization & Validation"),
        ("Database Driver", "PyMongo 4.19.0 (Official MongoDB Python Driver)", "Wire Protocol Client"),
        ("Testing Framework", "Pytest 9.1.1 with HTTPX 0.28.1 TestClient", "Automated Regression Testing"),
        ("Frontend Runtime", "Node.js 18.x / 20.x with npm 10.x", "Client Build Environment"),
        ("Frontend Framework", "React 18.3.1 with TypeScript 5.x", "Reactive Single-Page App"),
        ("Bundler & Dev Server", "Vite 8.3.4 (Modern Rolldown / ES-Module Bundler)", "Build Tooling"),
        ("UI Styling", "Tailwind CSS with PostCSS and Lucide-React Icons", "Responsive Utility-First Styling"),
        ("Data Visualization", "Recharts 2.x (Composable SVG Charting Library)", "Interactive Business Analytics")
    ]
    add_styled_table(["Software Layer", "Component & Verified Version", "Role in System Architecture"], sw_table, col_widths=[1.5, 2.8, 2.3])

    add_sec_heading("6.3 Network Topology & Environment Configuration", level=2, page_break=False)
    add_p(
        "In a local development environment, all three tiers communicate via loopback TCP sockets over dedicated ports:"
    )
    add_bullet(" Serves the Vite single-page application bundle, asset chunks, and hot module updates.", bold_prefix="Presentation Tier (React Frontend): http://127.0.0.1:5173")
    add_bullet(" Hosts the asynchronous FastAPI application, Swagger docs (/docs), and ReDoc (/redoc).", bold_prefix="Application Tier (FastAPI Backend): http://127.0.0.1:8000")
    add_bullet(" Standard MongoDB wire protocol port managing BSON commands, indexing, and aggregations.", bold_prefix="Persistence Tier (MongoDB Server): mongodb://127.0.0.1:27017")

    # =========================================================================
    # SECTION 15: SYSTEM DESIGN AND ARCHITECTURE
    # =========================================================================
    add_sec_heading("7. SYSTEM DESIGN AND ARCHITECTURE", level=1, page_break=True)
    
    add_sec_heading("7.1 Three-Tier Client-Server Architecture", level=2, page_break=False)
    add_p(
        "ShopSphere adheres to an industry-standard three-tier client-server architectural pattern, enforcing strict separation of concerns across "
        "Presentation, Application Logic, and Data Persistence tiers."
    )
    add_img("architecture_diagram.png", "Figure 1: ShopSphere Full-Stack System Architecture Diagram", width_in=6.2)

    add_sec_heading("7.2 Component-Level Architectural Decomposition", level=2, page_break=False)
    add_p(
        "The responsibilities of each tier are structured to maximize maintainability, testability, and operational stability:"
    )
    add_bullet(" Implemented in React 18, TypeScript, and Tailwind CSS. Manages client state, interactive tab routing, real-time Recharts visualizations, and form submissions. Dispatches asynchronous HTTP JSON requests via Axios to the backend.", bold_prefix="1. Presentation Tier:")
    add_bullet(" Structured around FastAPI routers, Pydantic schemas, and service-layer business logic. Enforces input sanitization, historical immutability guards, atomic inventory allocation, and BSON ObjectId serialization.", bold_prefix="2. Application Tier:")
    add_bullet(" MongoDB Community Server 8.0 running WiredTiger. Persists collections, enforces $jsonSchema validation rules, maintains B-Tree secondary indexes, and executes complex multi-stage aggregation pipelines.", bold_prefix="3. Persistence Tier:")

    add_sec_heading("7.3 Data Ingestion & ETL Processing Workflow", level=2, page_break=False)
    add_p(
        "To ingest the authentic Olist dataset without corrupting data hygiene or violating schema constraints, an idempotent, four-stage ETL "
        "pipeline was engineered in `backend/scripts/import_dataset.py`."
    )
    add_img("import_workflow.png", "Figure 2: Olist Brazilian E-Commerce Import & Transformation Pipeline Workflow", width_in=6.2)
    add_p(
        "The ETL pipeline parses 9 relational CSV files, strips UTF-8 BOM headers, translates Portuguese categories to English, generates deterministic "
        "UUID5-based BSON ObjectIds, denormalizes order items and payments into parent orders, skips 775 zero-item orders to satisfy `$jsonSchema` "
        "constraints, and executes idempotent `bulk_write` upserts into `shopsphere_olist`."
    )

    add_sec_heading("7.4 End-to-End API Request & Query Pipeline", level=2, page_break=False)
    add_p(
        "Figure 3 illustrates the complete lifecycle of a client request as it traverses the FastAPI routing layers, Pydantic validators, "
        "service business rules, PyMongo repository queries, and the MongoDB WiredTiger storage engine."
    )
    add_img("api_request_flow.png", "Figure 3: End-to-End API Request, Pydantic Validation & PyMongo Query Flow", width_in=6.2)

    add_sec_heading("7.5 Database Separation Architecture", level=2, page_break=False)
    add_p(
        "To ensure that high-volume authentic production data remains completely untouched during demonstrations and testing, ShopSphere "
        "implements strict database-level namespace isolation across three distinct databases, illustrated in Figure 4."
    )
    add_img("data_isolation_diagram.png", "Figure 4: Multi-Database Namespace Isolation Architecture (Production, Demo, Test)", width_in=6.2)

    # =========================================================================
    # SECTION 16: DATABASE DESIGN
    # =========================================================================
    add_sec_heading("8. DATABASE DESIGN", level=1, page_break=True)
    
    add_sec_heading("8.1 MongoDB Collection Architecture & Entity Overview", level=2, page_break=False)
    add_p(
        "The persistence layer of ShopSphere in the primary production database (`shopsphere_olist`) is organized into seven distinct collections, "
        "empirically verified on the live MongoDB Community Server 8.0 instance as shown in Table 4."
    )

    coll_table = [
        ("products", "32,951", "Catalog items with Portuguese-to-English translation & computed ratings"),
        ("customers", "99,441", "Brazilian buyers with anonymized emails (null) and state/city demographics"),
        ("orders", "98,666", "Orders with embedded items, payments, and addresses (775 zero-item orders skipped)"),
        ("reviews", "97,709", "Authentic 1-to-5 star reviews and Portuguese feedback text"),
        ("sellers", "3,095", "Marketplace merchant directory with postal codes and regional locations"),
        ("inventory_movements", "0", "Clean ledger; reserved for operational store stock adjustments"),
        ("shopsphere_demo", "4", "Isolated collection for interactive CRUD and Viva demonstrations")
    ]
    add_styled_table(["Collection Name", "Verified Document Count", "Description & Data Source"], coll_table, col_widths=[1.8, 1.4, 3.4])

    add_sec_heading("8.2 Embedded vs Referenced Data Modeling Strategy", level=2, page_break=False)
    add_p(
        "The core architectural achievement of ShopSphere is a principled hybrid data model that balances embedded sub-documents against "
        "referenced ObjectIds to maximize performance while respecting MongoDB's 16 MB BSON document limit."
    )
    add_img("database_model.png", "Figure 5: MongoDB Document Model & Schema Relationships (Embedded vs Referenced)", width_in=6.2)
    add_p(
        "1. Embedding Strategy (1-to-Few Bounded Relationships): Line items (`items`), payment transactions (`payments`), and shipping addresses "
        "(`shipping_address`) are embedded directly within the parent `orders` document. This denormalization guarantees that a customer receipt is "
        "retrieved in a single disk read without joins. Crucially, embedding creates an immutable snapshot of unit prices and item names at the "
        "instant of purchase, insulating the transaction from future master catalog price changes."
    )
    add_p(
        "2. Referencing Strategy (1-to-Many & Many-to-Many Relationships): Customers and products are referenced via their `_id` ObjectIds (`customer_id` "
        "in orders, `product_id` and `customer_id` in reviews). Referencing prevents boundless document growth, enables independent updates to customer "
        "profiles, and eliminates catastrophic data redundancy across 98,000+ orders."
    )

    add_sec_heading("8.3 Detailed Collection Schema Specifications", level=2, page_break=False)
    
    add_p("Sample document structure for the `products` collection based on live imported records:", bold_prefix="8.3.1 products Collection Schema: ")
    add_code_block(
        '{\n'
        '  "_id": ObjectId("670f5e1289abcdef01234567"),\n'
        '  "external_id": "1e9e8ef04dbcff4541ed26657ea517e5",\n'
        '  "name": "Perfumery - Model 1E9E8EF0",\n'
        '  "sku": "OLIST-PE-1E9E8EF0",\n'
        '  "category": "Perfumery",\n'
        '  "brand": "Olist Marketplace",\n'
        '  "description": "Authentic Olist Brazilian marketplace catalog item [Perfumery]. Weight: 225g.",\n'
        '  "price": 10.91,\n'
        '  "stock_quantity": 0,\n'
        '  "inventory_tracked": false,\n'
        '  "rating_average": 5.0,\n'
        '  "review_count": 1,\n'
        '  "source": "olist_real",\n'
        '  "created_at": ISODate("2026-10-16T16:54:00Z"),\n'
        '  "updated_at": ISODate("2026-10-16T16:54:00Z")\n'
        '}'
    )

    add_p("Sample document structure for the `customers` collection:", bold_prefix="8.3.2 customers Collection Schema: ")
    add_code_block(
        '{\n'
        '  "_id": ObjectId("670f5e1389abcdef01234568"),\n'
        '  "external_id": "06b8999e2fba1a1fbc88172c00ba8bc7",\n'
        '  "external_unique_id": "861eff4711a542e4b93843c6dd7febb0",\n'
        '  "name": "Customer 861EFF47",\n'
        '  "email": null,\n'
        '  "city": "Franca",\n'
        '  "state": "SP",\n'
        '  "source": "olist_real",\n'
        '  "created_at": ISODate("2026-10-16T16:54:00Z")\n'
        '}'
    )

    add_p("Sample document structure for the `orders` collection demonstrating embedded snapshots:", bold_prefix="8.3.3 orders Collection Schema: ")
    add_code_block(
        '{\n'
        '  "_id": ObjectId("670f5e1489abcdef01234569"),\n'
        '  "external_id": "e481f51cbdc54678b7cc49136f2d6af7",\n'
        '  "customer_id": ObjectId("670f5e1389abcdef01234568"),\n'
        '  "items": [\n'
        '    {\n'
        '      "product_id": ObjectId("670f5e1289abcdef01234567"),\n'
        '      "product_name": "Housewares - Model 87285B34",\n'
        '      "sku": "OLIST-HO-87285B34",\n'
        '      "unit_price": 29.99,\n'
        '      "quantity": 1,\n'
        '      "line_total": 29.99\n'
        '    }\n'
        '  ],\n'
        '  "shipping_address": {\n'
        '    "street": "Brazilian Postal Address",\n'
        '    "city": "Sao Paulo",\n'
        '    "state": "SP",\n'
        '    "postal_code": "05728",\n'
        '    "country": "Brazil"\n'
        '  },\n'
        '  "payments": [\n'
        '    { "payment_type": "credit_card", "installments": 1, "value": 38.71 }\n'
        '  ],\n'
        '  "freight_total": 8.72,\n'
        '  "subtotal": 29.99,\n'
        '  "total_amount": 38.71,\n'
        '  "status": "delivered",\n'
        '  "is_historical": true,\n'
        '  "source": "olist_real",\n'
        '  "created_at": ISODate("2017-10-02T10:56:33Z"),\n'
        '  "updated_at": ISODate("2017-10-10T21:25:13Z")\n'
        '}'
    )

    add_sec_heading("8.4 Database-Level $jsonSchema Validation Engine", level=2, page_break=False)
    add_p(
        "To enforce database integrity, collection validators are configured in MongoDB metadata using `$jsonSchema`. "
        "The following validator rules are actively enforced on the `products` and `orders` collections:"
    )
    add_code_block(
        '// products collection validator definition\n'
        '{\n'
        '  "$jsonSchema": {\n'
        '    "bsonType": "object",\n'
        '    "required": ["name", "sku", "category", "price", "stock_quantity"],\n'
        '    "properties": {\n'
        '      "name": { "bsonType": "string", "description": "Product name is required string" },\n'
        '      "sku": { "bsonType": "string", "description": "Unique SKU identifier" },\n'
        '      "category": { "bsonType": "string", "description": "Product category string" },\n'
        '      "price": { "bsonType": ["double", "int", "decimal"], "minimum": 0.01 },\n'
        '      "stock_quantity": { "bsonType": "int", "minimum": 0 },\n'
        '      "rating_average": { "bsonType": ["double", "int", "decimal"], "minimum": 0, "maximum": 5 }\n'
        '    }\n'
        '  }\n'
        '}\n\n'
        '// orders collection validator definition\n'
        '{\n'
        '  "$jsonSchema": {\n'
        '    "bsonType": "object",\n'
        '    "required": ["customer_id", "items", "shipping_address", "subtotal", "status"],\n'
        '    "properties": {\n'
        '      "customer_id": { "bsonType": "objectId" },\n'
        '      "items": { "bsonType": "array", "minItems": 1 },\n'
        '      "subtotal": { "bsonType": ["double", "int", "decimal"], "minimum": 0 },\n'
        '      "status": { "enum": ["pending", "confirmed", "shipped", "delivered", "cancelled"] }\n'
        '    }\n'
        '  }\n'
        '}'
    )

    add_sec_heading("8.5 B-Tree Indexing Strategy", level=2, page_break=False)
    add_p(
        "ShopSphere implements a comprehensive indexing strategy to support fast point lookups, sorting, and analytical queries across large collections:"
    )
    add_bullet(" Enforces uniqueness on product SKU (`{ sku: 1 }`, unique: true) and external Olist ID (`{ external_id: 1 }`, unique: true, partialFilterExpression).", bold_prefix="1. Unique B-Tree Indexes:")
    add_bullet(" Optimizes filtered catalog browsing by category and price (`{ category: 1, price: 1 }`), and order chronological lookups (`{ status: 1, created_at: -1 }`).", bold_prefix="2. Compound Indexes:")
    add_bullet(" Deployed on `customers.email` (`{ email: 1 }`, unique: true, partialFilterExpression: {\"email\": {\"$type\": \"string\"}}), allowing 99,000+ authentic records with null emails to coexist without uniqueness collision.", bold_prefix="3. Partial Filter Indexes:")
    add_bullet(" Enables full-text search across product name and brand (`{ name: \"text\", brand: \"text\" }`).", bold_prefix="4. Text Search Indexes:")

    # =========================================================================
    # SECTION 17: IMPLEMENTATION AND METHODOLOGY
    # =========================================================================
    add_sec_heading("9. IMPLEMENTATION AND METHODOLOGY", level=1, page_break=True)
    
    add_sec_heading("9.1 Authentic Dataset Discovery & Preprocessing Engine", level=2, page_break=False)
    add_p(
        "The ETL importer (`backend/scripts/import_dataset.py`) automatically discovers the raw Olist CSV files in `ShopSphere/data/olist/raw/`. "
        "The script is invoked via command line:"
    )
    add_code_block(
        '# Command to execute authentic Olist dataset ingestion\n'
        'cd D:\\Mongo_db-project\\ShopSphere\\backend\n'
        '.\\venv\\Scripts\\Activate.ps1\n'
        'python scripts\\import_dataset.py --db-name shopsphere_olist'
    )

    add_sec_heading("9.2 UTF-8 BOM Stripping & Multilingual Category Translation", level=2, page_break=False)
    add_p(
        "Raw Brazilian CSV files often contain Byte Order Mark (BOM) prefixes (`\\ufeff`) that corrupt column header parsing in standard CSV readers. "
        "The importer reads files using `utf-8-sig` encoding to transparently discard BOM headers. Furthermore, it joins category names with "
        "`product_category_name_translation.csv`, converting Portuguese names (`relogios_presentes`, `beleza_saude`, `cama_mesa_banho`) into "
        "clean English categories (`Watches & Gifts`, `Health & Beauty`, `Bed Bath Table`)."
    )

    add_sec_heading("9.3 Deterministic Hashing & Idempotent Upsert Strategy", level=2, page_break=False)
    add_p(
        "To ensure that repeated importer executions do not generate duplicate records or inflate document counts, surrogate BSON ObjectIds "
        "are generated deterministically using UUID version 5 hashing with a dedicated ShopSphere namespace UUID:"
    )
    add_code_block(
        'import uuid\n'
        'from bson import ObjectId\n\n'
        'SHOPSPHERE_NAMESPACE = uuid.UUID("e7b8c1d2-3f4a-5b6c-7d8e-9f0a1b2c3d4e")\n\n'
        'def generate_deterministic_id(entity_type: str, external_id: str) -> ObjectId:\n'
        '    """Generate repeatable 12-byte BSON ObjectId from entity external ID."""\n'
        '    unique_str = f"{entity_type}:{external_id}"\n'
        '    u = uuid.uuid5(SHOPSPHERE_NAMESPACE, unique_str)\n'
        '    return ObjectId(u.bytes[:12])'
    )
    add_p(
        "All database writes are executed using PyMongo's `bulk_write` API with `UpdateOne(..., upsert=True)`, guaranteeing that running the "
        "importer multiple times produces identical state without duplicate records."
    )

    add_sec_heading("9.4 Anonymization Preserving Data Hygiene", level=2, page_break=False)
    add_p(
        "To maintain academic integrity, no synthetic customer contact information, telephone numbers, or fake emails were generated. "
        "Customer emails are preserved as `null`. To satisfy MongoDB's unique index constraint on `email`, a partial filter expression was deployed: "
        "`partialFilterExpression: {\"email\": {\"$type\": \"string\"}}`. This allows unlimited documents with `null` emails while enforcing "
        "uniqueness on actual email strings."
    )

    add_sec_heading("9.5 Backend Service & Repository Layer Implementation", level=2, page_break=False)
    add_p(
        "The FastAPI backend is organized into a modular layered architecture: Routers (`app/routers/`), Services (`app/services/`), "
        "Repositories (`app/repositories/`), Schemas (`app/schemas/`), and Core Config/Database (`app/core/`). The repository layer isolates "
        "PyMongo queries and aggregations, providing clean separation from HTTP request parsing."
    )

    add_sec_heading("9.6 Frontend Single-Page Application Implementation", level=2, page_break=False)
    add_p(
        "The frontend is built using React 18 and TypeScript with Tailwind CSS. It features dynamic hash-based routing (`#dashboard`, `#products`, "
        "`#customers`, `#orders`, `#reviews`, `#inventory`, `#analytics`, `#concepts`, `#settings`, `#storefront`), responsive sidebar controls, "
        "and composable SVG charts using Recharts."
    )

    # =========================================================================
    # SECTION 18: MONGODB QUERIES AND OPERATIONS
    # =========================================================================
    add_sec_heading("10. MONGODB QUERIES AND OPERATIONS", level=1, page_break=True)
    
    add_sec_heading("10.1 Core CRUD Operations", level=2, page_break=False)
    add_p("Runnable, schema-accurate MongoDB operations executed in ShopSphere:")
    
    add_p("1. Insert Single Document (`insertOne`):", bold_prefix="CRUD 1: ")
    add_code_block(
        'db.products.insertOne({\n'
        '  "name": "Apple Smart Ring Tracker",\n'
        '  "sku": "AUDI-APP-0099",\n'
        '  "category": "Audio & Wearables",\n'
        '  "brand": "Apple",\n'
        '  "price": 299.99,\n'
        '  "stock_quantity": 50,\n'
        '  "inventory_tracked": true,\n'
        '  "rating_average": 0.0,\n'
        '  "review_count": 0,\n'
        '  "created_at": ISODate()\n'
        '})'
    )

    add_p("2. Find with Projection, Sorting, and Pagination (`find`):", bold_prefix="CRUD 2: ")
    add_code_block(
        'db.products.find(\n'
        '  { "category": "Health & Beauty", "price": { "$gte": 20.0, "$lte": 150.0 } },\n'
        '  { "name": 1, "sku": 1, "price": 1, "rating_average": 1, "_id": 0 }\n'
        ').sort({ "price": -1 }).skip(0).limit(10)'
    )

    add_p("3. Atomic Field Update (`updateOne` with `$set` and `$inc`):", bold_prefix="CRUD 3: ")
    add_code_block(
        'db.products.updateOne(\n'
        '  { "sku": "AUDI-APP-0099" },\n'
        '  {\n'
        '    "$inc": { "stock_quantity": -1 },\n'
        '    "$set": { "updated_at": ISODate() }\n'
        '  }\n'
        ')'
    )

    add_p("4. Batch Updates (`updateMany`):", bold_prefix="CRUD 4: ")
    add_code_block(
        'db.products.updateMany(\n'
        '  { "category": "Audio & Wearables" },\n'
        '  { "$set": { "featured": true, "promotional_discount": 0.05 } }\n'
        ')'
    )

    add_sec_heading("10.2 Production Aggregation Pipelines (8 Real Queries)", level=2, page_break=False)
    add_p(
        "ShopSphere features 8 production aggregation pipelines executable in the application and Concepts Lab:"
    )

    add_p("Pipeline 1: Total Revenue by Product Category ($match, $unwind, $lookup, $group, $sort, $project):", bold_prefix="Query 1: ")
    add_code_block(
        'db.orders.aggregate([\n'
        '  { "$match": { "status": { "$ne": "cancelled" } } },\n'
        '  { "$unwind": "$items" },\n'
        '  { "$lookup": {\n'
        '      "from": "products",\n'
        '      "let": { "pid": { "$toObjectId": "$items.product_id" } },\n'
        '      "pipeline": [\n'
        '        { "$match": { "$expr": { "$eq": ["$_id", "$$pid"] } } },\n'
        '        { "$project": { "category": 1 } }\n'
        '      ],\n'
        '      "as": "product_info"\n'
        '    }\n'
        '  },\n'
        '  { "$unwind": { "path": "$product_info", "preserveNullAndEmptyArrays": true } },\n'
        '  { "$group": {\n'
        '      "_id": { "$ifNull": ["$product_info.category", "General"] },\n'
        '      "total_revenue": { "$sum": "$items.line_total" },\n'
        '      "units_sold": { "$sum": "$items.quantity" },\n'
        '      "order_count": { "$sum": 1 }\n'
        '    }\n'
        '  },\n'
        '  { "$project": {\n'
        '      "_id": 0,\n'
        '      "category": "$_id",\n'
        '      "total_revenue": { "$round": ["$total_revenue", 2] },\n'
        '      "units_sold": 1,\n'
        '      "order_count": 1\n'
        '    }\n'
        '  },\n'
        '  { "$sort": { "total_revenue": -1 } }\n'
        '])'
    )

    add_p("Pipeline 2: Monthly Sales Trends ($match, $group, $dateToString, $sort, $project):", bold_prefix="Query 2: ")
    add_code_block(
        'db.orders.aggregate([\n'
        '  { "$match": { "status": { "$ne": "cancelled" } } },\n'
        '  { "$group": {\n'
        '      "_id": { "$dateToString": { "format": "%Y-%m", "date": "$created_at" } },\n'
        '      "total_revenue": { "$sum": "$subtotal" },\n'
        '      "order_count": { "$sum": 1 }\n'
        '    }\n'
        '  },\n'
        '  { "$sort": { "_id": 1 } },\n'
        '  { "$project": {\n'
        '      "_id": 0,\n'
        '      "month": "$_id",\n'
        '      "total_revenue": { "$round": ["$total_revenue", 2] },\n'
        '      "order_count": 1\n'
        '    }\n'
        '  }\n'
        '])'
    )

    add_p("Pipeline 3: Top-Selling Products by Volume ($unwind, $group, $sort, $limit):", bold_prefix="Query 3: ")
    add_code_block(
        'db.orders.aggregate([\n'
        '  { "$match": { "status": { "$ne": "cancelled" } } },\n'
        '  { "$unwind": "$items" },\n'
        '  { "$group": {\n'
        '      "_id": "$items.product_id",\n'
        '      "product_name": { "$first": "$items.product_name" },\n'
        '      "sku": { "$first": "$items.sku" },\n'
        '      "units_sold": { "$sum": "$items.quantity" },\n'
        '      "total_revenue": { "$sum": "$items.line_total" }\n'
        '    }\n'
        '  },\n'
        '  { "$sort": { "units_sold": -1 } },\n'
        '  { "$limit": 5 },\n'
        '  { "$project": {\n'
        '      "_id": 0,\n'
        '      "product_id": "$_id",\n'
        '      "product_name": 1,\n'
        '      "sku": 1,\n'
        '      "units_sold": 1,\n'
        '      "total_revenue": { "$round": ["$total_revenue", 2] }\n'
        '    }\n'
        '  }\n'
        '])'
    )

    add_p("Pipeline 4: Customer Spending Leaders & Lifetime Value ($group, $lookup, $unwind, $sort, $limit):", bold_prefix="Query 4: ")
    add_code_block(
        'db.orders.aggregate([\n'
        '  { "$match": { "status": { "$ne": "cancelled" } } },\n'
        '  { "$group": {\n'
        '      "_id": "$customer_id",\n'
        '      "total_spent": { "$sum": "$subtotal" },\n'
        '      "orders_placed": { "$sum": 1 }\n'
        '    }\n'
        '  },\n'
        '  { "$lookup": {\n'
        '      "from": "customers",\n'
        '      "localField": "_id",\n'
        '      "foreignField": "_id",\n'
        '      "as": "customer"\n'
        '    }\n'
        '  },\n'
        '  { "$unwind": "$customer" },\n'
        '  { "$sort": { "total_spent": -1 } },\n'
        '  { "$limit": 5 },\n'
        '  { "$project": {\n'
        '      "_id": 0,\n'
        '      "customer_id": "$_id",\n'
        '      "customer_name": "$customer.name",\n'
        '      "city": "$customer.city",\n'
        '      "state": "$customer.state",\n'
        '      "total_spent": { "$round": ["$total_spent", 2] },\n'
        '      "orders_placed": 1\n'
        '    }\n'
        '  }\n'
        '])'
    )

    add_p("Pipeline 5: Multi-Faceted Order Status Distribution ($facet):", bold_prefix="Query 5: ")
    add_code_block(
        'db.orders.aggregate([\n'
        '  { "$facet": {\n'
        '      "by_status": [\n'
        '        { "$group": { "_id": "$status", "count": { "$sum": 1 } } },\n'
        '        { "$sort": { "count": -1 } }\n'
        '      ],\n'
        '      "summary": [\n'
        '        { "$group": {\n'
        '            "_id": null,\n'
        '            "total_orders": { "$sum": 1 },\n'
        '            "total_value": { "$sum": "$subtotal" },\n'
        '            "avg_value": { "$avg": "$subtotal" }\n'
        '          }\n'
        '        },\n'
        '        { "$project": {\n'
        '            "_id": 0,\n'
        '            "total_orders": 1,\n'
        '            "total_value": { "$round": ["$total_value", 2] },\n'
        '            "avg_value": { "$round": ["$avg_value", 2] }\n'
        '          }\n'
        '        }\n'
        '      ]\n'
        '    }\n'
        '  }\n'
        '])'
    )

    add_p("Pipeline 6: Embedding Orders via $lookup for Customer Profiles:", bold_prefix="Query 6: ")
    add_code_block(
        'db.customers.aggregate([\n'
        '  { "$lookup": {\n'
        '      "from": "orders",\n'
        '      "localField": "_id",\n'
        '      "foreignField": "customer_id",\n'
        '      "as": "recent_orders"\n'
        '    }\n'
        '  },\n'
        '  { "$match": { "recent_orders.0": { "$exists": true } } },\n'
        '  { "$project": {\n'
        '      "_id": 0,\n'
        '      "customer_id": "$_id",\n'
        '      "name": 1,\n'
        '      "city": 1,\n'
        '      "order_count": { "$size": "$recent_orders" },\n'
        '      "latest_order": { "$arrayElemAt": ["$recent_orders", 0] }\n'
        '    }\n'
        '  },\n'
        '  { "$limit": 5 }\n'
        '])'
    )

    add_p("Pipeline 7: Dynamic Rating Calculation from Reviews ($lookup & $avg):", bold_prefix="Query 7: ")
    add_code_block(
        'db.products.aggregate([\n'
        '  { "$lookup": {\n'
        '      "from": "reviews",\n'
        '      "localField": "_id",\n'
        '      "foreignField": "product_id",\n'
        '      "as": "reviews"\n'
        '    }\n'
        '  },\n'
        '  { "$match": { "reviews.0": { "$exists": true } } },\n'
        '  { "$project": {\n'
        '      "_id": 0,\n'
        '      "product_id": "$_id",\n'
        '      "name": 1,\n'
        '      "category": 1,\n'
        '      "price": 1,\n'
        '      "computed_review_count": { "$size": "$reviews" },\n'
        '      "computed_avg_rating": { "$round": [{ "$avg": "$reviews.rating" }, 2] }\n'
        '    }\n'
        '  },\n'
        '  { "$sort": { "computed_review_count": -1 } },\n'
        '  { "$limit": 5 }\n'
        '])'
    )

    add_p("Pipeline 8: Average Order Value & Basket Sizing Metrics ($size, $avg, $min, $max):", bold_prefix="Query 8: ")
    add_code_block(
        'db.orders.aggregate([\n'
        '  { "$match": { "status": { "$ne": "cancelled" } } },\n'
        '  { "$project": {\n'
        '      "subtotal": 1,\n'
        '      "item_count": { "$size": "$items" }\n'
        '    }\n'
        '  },\n'
        '  { "$group": {\n'
        '      "_id": null,\n'
        '      "average_order_value": { "$avg": "$subtotal" },\n'
        '      "average_items_per_basket": { "$avg": "$item_count" },\n'
        '      "min_order_value": { "$min": "$subtotal" },\n'
        '      "max_order_value": { "$max": "$subtotal" }\n'
        '    }\n'
        '  },\n'
        '  { "$project": {\n'
        '      "_id": 0,\n'
        '      "average_order_value": { "$round": ["$average_order_value", 2] },\n'
        '      "average_items_per_basket": { "$round": ["$average_items_per_basket", 2] },\n'
        '      "min_order_value": { "$round": ["$min_order_value", 2] },\n'
        '      "max_order_value": { "$round": ["$max_order_value", 2] }\n'
        '    }\n'
        '  }\n'
        '])'
    )

    add_sec_heading("10.3 Query Execution Optimization (explain('executionStats'))", level=2, page_break=False)
    add_p(
        "To measure indexing efficiency, live queries were profiled against `products` using `explain(\"executionStats\")`. "
        "The empirical benchmark results comparing indexed lookups against unindexed scans are presented in Table 6."
    )

    explain_table = [
        ("Execution Plan Stage", "IXSCAN (Index Scan) -> FETCH", "COLLSCAN (Full Collection Scan)"),
        ("Index Utilized", "uniq_sku (B-Tree on sku: 1)", "None (Unindexed query filter)"),
        ("Keys Examined (totalKeysExamined)", "1 key examined", "0 keys examined"),
        ("Documents Examined (totalDocsExamined)", "1 document examined", "32,951 documents examined"),
        ("Documents Returned (nReturned)", "1 document", "0 documents (target not found)"),
        ("Execution Time (executionTimeMillis)", "0.0 ms (sub-millisecond)", "14.0 – 22.0 ms"),
        ("Storage Engine Efficiency", "Direct B-Tree leaf node lookup", "Sequential table-space memory scan")
    ]
    add_styled_table(["Performance Metric", "Indexed Query (IXSCAN)", "Unindexed Query (COLLSCAN)"], explain_table, col_widths=[2.2, 2.2, 2.2])

    add_sec_heading("10.4 Schema Validation Enforcement & Write Rejection", level=2, page_break=False)
    add_p(
        "When an insert violates collection `$jsonSchema` constraints (e.g. attempting to insert a product with negative price or empty items array), "
        "the MongoDB engine immediately halts execution and returns a `DocumentValidationFailure` (WriteError code 121). "
        "FastAPI catches this exception in the repository layer and transforms it into an HTTP 422 Unprocessable Entity error."
    )

    # =========================================================================
    # SECTION 19: RESULTS AND OUTPUT SCREENSHOTS
    # =========================================================================
    add_sec_heading("11. RESULTS AND OUTPUT SCREENSHOTS", level=1, page_break=True)
    add_p(
        "All visual results presented in this section are authentic screenshots captured directly from the live ShopSphere application "
        "running locally on Microsoft Windows against the `shopsphere_olist` MongoDB 8.0.34 database."
    )

    add_sec_heading("11.1 Executive Analytics Dashboard Walkthrough", level=2, page_break=False)
    add_p(
        "The Executive Performance Hub aggregates live metrics across 98,666 orders: Gross Revenue ($13,494,400.74), Total Orders (98,199 confirmed), "
        "Customer Accounts (99,441), and Live Catalogue (32,951 SKUs). The Monthly Revenue Pipeline chart displays historical sales trends "
        "from 2016 to 2018, while the Sales by Category widget breaks down top revenue-generating sectors."
    )
    add_img("dashboard.png", "Figure 6: Real Application Screenshot — Executive SaaS Analytics Dashboard", width_in=6.2)

    add_sec_heading("11.2 Product Catalogue & Filtering System", level=2, page_break=False)
    add_p(
        "The Product Catalogue management module displays active SKUs in a modern responsive grid. Users can filter by category, brand, "
        "stock level, and price range. Items show their computed ratings, review counts, and 'Out of Stock' badges reflecting authentic Olist constraints."
    )
    add_img("products.png", "Figure 7: Real Application Screenshot — Product Catalogue Management System", width_in=6.2)

    add_sec_heading("11.3 Customer CRM & Demographic Distribution", level=2, page_break=False)
    add_p(
        "The Customer Accounts CRM module displays registered buyers, location by Brazilian state (SP, MG, RJ, PR, SC), and aggregated Lifetime "
        "Value (LTV) computed dynamically via MongoDB aggregation joins."
    )
    add_img("customers.png", "Figure 8: Real Application Screenshot — Customer CRM & Demographic Accounts Ledger", width_in=6.2)

    add_sec_heading("11.4 Transactional Order Fulfillment & Immutability Verification", level=2, page_break=False)
    add_p(
        "The Order Management screen provides chronological visibility into order lifecycles. Historical Olist records are visually marked "
        "with an 'Olist' badge and 'Immutable' tag, demonstrating that past orders cannot be cancelled or altered via the demo interface."
    )
    add_img("orders.png", "Figure 9: Real Application Screenshot — Transactional Order Management & Immutability Badges", width_in=6.2)

    add_sec_heading("11.5 Customer Reviews & Rating Distributions", level=2, page_break=False)
    add_p(
        "The Customer Reviews screen showcases authentic Portuguese customer feedback paired with 1-to-5 star rating stars. Creating a new "
        "review dynamically triggers background recalculation of the corresponding product's `rating_average` and `review_count`."
    )
    add_img("reviews.png", "Figure 10: Real Application Screenshot — Customer Reviews & Rating Distribution Analytics", width_in=6.2)

    add_sec_heading("11.6 Inventory & Stock Movement Audit Trail", level=2, page_break=False)
    add_p(
        "The Inventory & Audit Trail displays stock movements and warehouse balances. In accordance with genuine Olist dataset characteristics, "
        "historical inventory movements remain clean (0 documents), while manual restocks and demo checkouts log permanent audit entries."
    )
    add_img("inventory.png", "Figure 11: Real Application Screenshot — Real-Time Inventory & Movement Audit Ledger", width_in=6.2)

    add_sec_heading("11.7 Business Intelligence & Aggregation Reports", level=2, page_break=False)
    add_p(
        "The Analytics & Aggregation Reports screen visualizes complex multi-stage pipeline outputs: Revenue Growth Trend over time, Category Revenue "
        "distribution, Order Status Lifecycle (Delivered: 97.8%, Shipped: 1.1%, Cancelled: 0.5%), and Customer Sentiment distribution."
    )
    add_img("analytics.png", "Figure 12: Real Application Screenshot — Business Intelligence & Multi-Dimensional Aggregation Reports", width_in=6.2)

    add_sec_heading("11.8 Interactive MongoDB Concepts & Viva Laboratory", level=2, page_break=False)
    add_p(
        "The Concepts Lab is an interactive sandbox designed for academic evaluation. Evaluators can execute CRUD primitives (`insertOne`, "
        "`insertMany`, `find`, `updateOne`, `updateMany`, `deleteOne`, `deleteMany`), view live PyMongo syntax, inspect real BSON JSON outputs, "
        "and benchmark query plans via `explain()`."
    )
    add_img("concepts_lab.png", "Figure 13: Real Application Screenshot — Interactive MongoDB Concepts & Viva Laboratory", width_in=6.2)

    add_sec_heading("11.9 Database Topology & Connection Settings", level=2, page_break=False)
    add_p(
        "The Settings screen displays verified MongoDB engine diagnostics: Server version 8.0.34, Single topology, Safe Standalone Fallback "
        "for multi-document transactions, and live collection document counts."
    )
    add_img("settings.png", "Figure 14: Real Application Screenshot — Database Engine Settings, Standalone Topology & Document Volume", width_in=6.2)

    add_sec_heading("11.10 Customer-Facing Storefront", level=2, page_break=False)
    add_p(
        "The Storefront module provides a live e-commerce shopping experience. Customers can filter by interactive category pills, add items "
        "to a real-time shopping cart, and complete atomic checkouts against the MongoDB backend."
    )
    add_img("storefront.png", "Figure 15: Real Application Screenshot — Live Customer-Facing Shopping Storefront Experience", width_in=6.2)

    add_sec_heading("11.11 FastAPI Swagger API Documentation", level=2, page_break=False)
    add_p(
        "The backend serves interactive OpenAPI 3.1 Swagger documentation at `/docs`, enabling direct inspection and execution of all "
        "RESTful endpoints across Dashboard, Products, Customers, Orders, Inventory, and Concepts."
    )
    add_img("swagger_docs.png", "Figure 16: Real Application Screenshot — FastAPI Interactive OpenAPI (Swagger UI) Documentation", width_in=6.2)

    # =========================================================================
    # SECTION 20: TESTING AND VALIDATION
    # =========================================================================
    add_sec_heading("12. TESTING AND VALIDATION", level=1, page_break=True)
    
    add_sec_heading("12.1 Automated Testing Strategy & Isolation Philosophy", level=2, page_break=False)
    add_p(
        "To guarantee robust regression coverage without polluting the 100,000-document production database (`shopsphere_olist`) or demo catalog "
        "(`shopsphere`), an isolated testing architecture was implemented. All Pytest test cases execute strictly against a dedicated database "
        "named `shopsphere_test`, which is dynamically provisioned and cleaned up by test fixtures."
    )

    add_sec_heading("12.2 Test Suite Execution Results (12/12 Passing)", level=2, page_break=False)
    add_p(
        "Executing `pytest -v` within the backend virtual environment verified that all 12 unit and integration tests passed cleanly in 0.69 seconds:"
    )
    add_code_block(
        '============================= test session starts =============================\n'
        'platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0\n'
        'rootdir: D:\\Mongo_db-project\\ShopSphere\\backend, configfile: pytest.ini\n'
        'collected 12 items\n\n'
        'tests/test_analytics.py::test_dashboard_summary_endpoint PASSED          [  8%]\n'
        'tests/test_analytics.py::test_analytics_overview_and_csv_export PASSED   [ 16%]\n'
        'tests/test_concepts.py::test_crud_demo_endpoints PASSED                  [ 25%]\n'
        'tests/test_concepts.py::test_aggregation_playground_queries PASSED       [ 33%]\n'
        'tests/test_concepts.py::test_explain_query_plan PASSED                   [ 41%]\n'
        'tests/test_concepts.py::test_schema_validation_demo PASSED               [ 50%]\n'
        'tests/test_customers.py::test_customer_crud_and_email_uniqueness PASSED  [ 58%]\n'
        'tests/test_import_dataset.py::test_verify_dataset_files_missing PASSED   [ 66%]\n'
        'tests/test_import_dataset.py::test_olist_import_pipeline_end_to_end PASSED [ 75%]\n'
        'tests/test_orders.py::test_order_placement_stock_decrement_and_cancellation PASSED [ 83%]\n'
        'tests/test_products.py::test_get_products_pagination PASSED              [ 91%]\n'
        'tests/test_products.py::test_product_crud_and_duplicate_sku PASSED       [100%]\n\n'
        '======================== 12 passed, 1 warning in 0.69s ========================'
    )

    add_sec_heading("12.3 Comprehensive Test Matrix Table", level=2, page_break=False)
    add_p("Table 7 summarizes the test objectives, execution paths, expected outcomes, and verified results for all 12 test suites.")

    test_matrix = [
        ("test_dashboard_summary", "GET /api/v1/dashboard/summary", "Return real-time counts, revenue, and top SKUs", "HTTP 200 with valid numeric aggregates", "PASSED"),
        ("test_analytics_overview", "GET /api/v1/analytics/overview", "Generate sales trends and category distributions", "HTTP 200 with arrays of time-series data", "PASSED"),
        ("test_crud_demo", "POST /api/v1/concepts/crud-demo", "Execute isolated CRUD operations in shopsphere_demo", "insertOne/find/update/delete succeed cleanly", "PASSED"),
        ("test_aggregation_playground", "POST /api/v1/concepts/aggregate-demo", "Execute all 8 real aggregation pipelines", "HTTP 200 with formatted pipeline result", "PASSED"),
        ("test_explain_query_plan", "POST /api/v1/concepts/explain-demo", "Compare IXSCAN on indexed SKU vs COLLSCAN", "IXSCAN examines 1 key; COLLSCAN scans all", "PASSED"),
        ("test_schema_validation", "POST /api/v1/concepts/validation-demo", "Enforce database-level $jsonSchema rejections", "Negative price rejected with HTTP 422", "PASSED"),
        ("test_customer_uniqueness", "POST /api/v1/customers", "Enforce unique index on customer email", "Duplicate email rejected with HTTP 409 Conflict", "PASSED"),
        ("test_verify_dataset_files", "import_dataset.py file checker", "Verify all 9 raw Olist CSV files exist", "Confirms presence of all required CSV files", "PASSED"),
        ("test_import_pipeline", "End-to-end ETL import test", "Ingest mock Olist CSVs into shopsphere_test", "Denormalizes items and creates deterministic IDs", "PASSED"),
        ("test_order_placement_stock", "POST /api/v1/orders + cancel", "Atomically decrement stock and restore on cancel", "Stock decrements by 1, restores on cancel", "PASSED"),
        ("test_products_pagination", "GET /api/v1/products?page=1", "Server-side cursor pagination and limits", "Returns items with total_pages metadata", "PASSED"),
        ("test_product_duplicate_sku", "POST /api/v1/products", "Enforce unique B-Tree index on product SKU", "Duplicate SKU rejected with HTTP 409 Conflict", "PASSED")
    ]
    add_styled_table(["Test Identifier", "Target Endpoint / Module", "Expected Test Behavior", "Actual Verified Outcome", "Status"], test_matrix, col_widths=[1.5, 1.6, 1.8, 1.5, 0.6])

    add_sec_heading("12.4 Frontend TypeScript & Vite Production Build Verification", level=2, page_break=False)
    add_p(
        "The frontend production bundle was compiled and verified via `npm run build` (`tsc -b && vite build`), completing in 2.22 seconds "
        "with zero TypeScript compilation errors:"
    )
    add_code_block(
        '> frontend@0.0.0 build\n'
        '> tsc -b && vite build\n\n'
        'vite v8.3.4 building client environment for production...\n'
        '✓ 2565 modules transformed.\n'
        'dist/index.html                   0.73 kB │ gzip:   0.44 kB\n'
        'dist/assets/index-T-87nYvF.css   35.39 kB │ gzip:   6.63 kB\n'
        'dist/assets/index-DS9ETYuj.js   838.70 kB │ gzip: 233.47 kB\n'
        '✓ built in 2.22s'
    )

    add_sec_heading("12.5 Historical Immutability & Concurrency Safeguards", level=2, page_break=False)
    add_p(
        "Historical transaction immutability was validated by attempting to cancel an imported Olist order via the API endpoint "
        "`POST /api/v1/orders/{order_id}/cancel`. The backend immediately rejected the request with HTTP 400 Bad Request: "
        "\"Cannot modify historical Olist transaction. Historical dataset records are immutable.\""
    )

    add_sec_heading("12.6 Idempotency Verification Matrix", level=2, page_break=False)
    add_p(
        "To verify ETL idempotency, the dataset importer was executed twice sequentially against `shopsphere_olist`. "
        "Table 8 confirms that document counts remained exactly unchanged across both executions."
    )

    idem_table = [
        ("products", "32,951 documents", "32,951 documents", "0 (Zero duplicates created)"),
        ("customers", "99,441 documents", "99,441 documents", "0 (Zero duplicates created)"),
        ("orders", "98,666 documents", "98,666 documents", "0 (Zero duplicates created)"),
        ("reviews", "97,709 documents", "97,709 documents", "0 (Zero duplicates created)"),
        ("sellers", "3,095 documents", "3,095 documents", "0 (Zero duplicates created)")
    ]
    add_styled_table(["Collection Name", "Count After Run 1", "Count After Run 2", "Net Document Change"], idem_table, col_widths=[1.6, 1.8, 1.8, 1.8])

    # =========================================================================
    # SECTION 21: CHALLENGES FACED
    # =========================================================================
    add_sec_heading("13. CHALLENGES FACED", level=1, page_break=True)
    
    add_sec_heading("13.1 Complexities of Real-World Big Data Ingestion", level=2, page_break=False)
    add_p(
        "The Olist Brazilian E-Commerce dataset presented several real-world data engineering hurdles. Initial CSV parsing failed due to hidden "
        "UTF-8 Byte Order Mark (BOM) headers (`\\ufeff`) at the start of column names. This was resolved by re-encoding file readers with `utf-8-sig`. "
        "Furthermore, category names were originally in Portuguese (`relogios_presentes`, `ferramentas_jardim`), requiring automated cross-referencing "
        "with translation tables to ensure an English user interface."
    )

    add_sec_heading("13.2 Balancing Data Integrity with NoSQL Flexibility", level=2, page_break=False)
    add_p(
        "In relational databases, unique constraints automatically handle nulls or allow multiple null values depending on SQL standards. "
        "In MongoDB, a standard unique index treats `null` as a distinct value, causing any second document with `email: null` to fail with duplicate "
        "key error E11000. Because 99,441 authentic Olist customer records had null emails, creating a standard unique index crashed ingestion. "
        "The challenge was overcome by engineering a Partial Unique Index with `partialFilterExpression: {\"email\": {\"$type\": \"string\"}}`, "
        "enforcing uniqueness exclusively on real string values while permitting unlimited nulls."
    )

    add_sec_heading("13.3 Relational-to-Document Paradigm Shift", level=2, page_break=False)
    add_p(
        "In the relational Olist dataset, order items and order payments were stored as separate CSV tables linked via foreign keys. "
        "Denormalizing these into embedded arrays within orders required an in-memory aggregation dictionary before bulk database insertion. "
        "Additionally, 775 orders in the raw dataset possessed zero line items; these were systematically filtered out to prevent violating "
        "collection `$jsonSchema` rules requiring `minItems: 1`."
    )

    add_sec_heading("13.4 Transactional Concurrency on Standalone Instances", level=2, page_break=False)
    add_p(
        "MongoDB Community Server standalone instances (the default installation on local developer machines) do not support multi-document ACID "
        "transactions, which require a Replica Set oplog. To ensure transactional safety during checkout and cancellation without mandating a complex "
        "multi-node cluster setup, ShopSphere implements an atomic two-phase compensation pattern: single-document atomic updates (`$inc: {stock: -1}`) "
        "are executed first, with compensating reversal updates triggered if subsequent order creation steps fail."
    )

    add_sec_heading("13.5 Query Performance Optimization on 98k+ Orders", level=2, page_break=False)
    add_p(
        "Running analytical aggregations and dashboard queries across 98,666 orders and 112,000 embedded items initially caused 1.2-second UI freezes "
        "due to unindexed collection scans. By profiling queries with `explain()`, compound indexes (`{ status: 1, created_at: -1 }` on orders and "
        "`{ category: 1, price: 1 }` on products) were deployed, slashing dashboard aggregation response times to under 45 milliseconds."
    )

    # =========================================================================
    # SECTION 22: CONCLUSION
    # =========================================================================
    add_sec_heading("14. CONCLUSION", level=1, page_break=True)
    
    add_sec_heading("14.1 Summary of Technical Achievements", level=2, page_break=False)
    add_p(
        "The ShopSphere capstone project successfully demonstrates the end-to-end design, implementation, and empirical validation of an "
        "enterprise-grade e-commerce database management and analytics system on MongoDB Community Server 8.0, FastAPI, and React TypeScript."
    )
    add_p(
        "Through rigorous architectural modeling, the system proves that document-oriented databases provide superior data locality and read "
        "throughput for commercial retail applications compared to traditional relational models. Denormalizing order items and shipping addresses "
        "into embedded subdocuments guarantees historical transaction immutability and eliminates expensive SQL JOIN operations. Simultaneously, "
        "referencing customers and products via ObjectIds prevents uncontrolled data duplication."
    )
    add_p(
        "The platform ingests over 100,000 authentic records from the Brazilian E-Commerce Public Dataset by Olist, proving that NoSQL systems can "
        "maintain strict data hygiene via `$jsonSchema` validators, partial unique indexes, and idempotent bulk upserts without compromising "
        "polymorphic flexibility. All 12 automated test suites pass cleanly in 0.69 seconds, verifying that ShopSphere fulfills all technical "
        "and academic objectives."
    )

    add_sec_heading("14.2 Pedagogical and Engineering Insights", level=2, page_break=False)
    add_p(
        "This project provided invaluable software engineering lessons in the realities of handling authentic big data. Moving beyond idealized "
        "textbook examples to reconcile messy real-world CSVs, UTF-8 BOM encoding, anonymized contact fields, and standalone database transaction "
        "fallbacks imparted deep practical competence in modern database systems engineering."
    )

    # =========================================================================
    # SECTION 23: FUTURE SCOPE
    # =========================================================================
    add_sec_heading("15. FUTURE SCOPE", level=1, page_break=True)
    
    add_sec_heading("15.1 Replica Set Deployment & Multi-Document ACID Transactions", level=2, page_break=False)
    add_p(
        "Future iterations will transition MongoDB from a standalone instance to a 3-node Replica Set (Primary-Secondary-Arbiter). "
        "This will unlock native multi-document ACID transactions across collections via `client.start_session()` and provide automatic "
        "failover high availability."
    )

    add_sec_heading("15.2 Sharding & Distributed Horizontal Scaling", level=2, page_break=False)
    add_p(
        "To support global enterprise scale exceeding millions of orders per month, horizontal sharding will be implemented using customer "
        "geographic region (e.g. Brazilian state/postal prefix) as a shard key. This will distribute database I/O across independent shard clusters."
    )

    add_sec_heading("15.3 Vector Search & AI-Powered Product Recommendations", level=2, page_break=False)
    add_p(
        "Integrating MongoDB Atlas Vector Search will enable semantic product search and personalized recommendation carousels. Product text "
        "descriptions and images can be embedded into dense vector embeddings using transformer models, allowing natural language queries such as "
        "\"waterproof outdoor running gear\"."
    )

    add_sec_heading("15.4 Change Streams & Real-Time Event Architecture", level=2, page_break=False)
    add_p(
        "Deploying MongoDB Change Streams (`watch()`) will enable an event-driven architecture. Real-time updates to stock levels or order statuses "
        "can be pushed directly to connected web clients via WebSockets without requiring periodic client polling."
    )

    add_sec_heading("15.5 Security Hardening (JWT, RBAC, Field-Level Encryption)", level=2, page_break=False)
    add_p(
        "Enterprise production deployment will incorporate JSON Web Token (JWT) authentication, Role-Based Access Control (RBAC) separating "
        "Store Administrators from Customer accounts, and MongoDB Client-Side Field Level Encryption (CSFLE) to encrypt sensitive financial records."
    )

    # =========================================================================
    # SECTION 24: REFERENCES / BIBLIOGRAPHY
    # =========================================================================
    add_sec_heading("16. REFERENCES / BIBLIOGRAPHY", level=1, page_break=True)
    
    references = [
        ("Brewer, E. A. (2000)", "Towards robust distributed systems. In Proceedings of the Nineteenth ACM Symposium on Principles of Distributed Computing (PODC '00), Portland, OR, USA, pp. 7–10. https://doi.org/10.1145/343477.343502"),
        ("Cattell, R. (2011)", "Scalable SQL and NoSQL data stores. ACM SIGMOD Record, 39(4), 12–27. https://doi.org/10.1145/1978915.1978919"),
        ("Gilbert, S., & Lynch, N. (2002)", "Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services. ACM SIGACT News, 33(2), 51–59. https://doi.org/10.1145/564585.564601"),
        ("Meta Platforms (2024)", "React 18 Architecture: Concurrent Mode, Automatic Batching, and Virtual DOM Reconciliation. Meta Open Source Documentation. https://react.dev"),
        ("MongoDB Inc. (2026)", "MongoDB Community Server 8.0 Manual: WiredTiger Storage Engine Architecture, B-Tree Indexing, and Aggregation Pipeline Optimization. MongoDB Technical Documentation. https://www.mongodb.com/docs/manual/"),
        ("MongoDB Inc. (2026)", "PyMongo 4.x Driver Documentation: Connection Pooling, Safe Transactions, and Bulk Write Operations. https://pymongo.readthedocs.io/"),
        ("Olist & Kaggle (2018)", "Brazilian E-Commerce Public Dataset by Olist: 100k Orders with Product, Customer, Payment, and Review Details. Kaggle Public Datasets. https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce"),
        ("Ramírez, S. (2024)", "FastAPI: High-Performance, Asynchronous Web Framework for Python 3.8+ Based on Standard Type Hints and Starlette. https://fastapi.tiangolo.com/"),
        ("Stonebraker, M. (2010)", "SQL databases v. NoSQL databases. Communications of the ACM, 53(4), 10–11. https://doi.org/10.1145/1721654.1721659"),
        ("You, E. (2024)", "Vite: Next Generation Frontend Tooling with Native ES Modules and Rolldown Bundler. https://vitejs.dev/")
    ]

    for author, citation in references:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_auth = p.add_run(f"{author}. ")
        r_auth.bold = True
        r_auth.font.name = "Times New Roman"
        r_auth.font.size = Pt(10.5)
        r_cit = p.add_run(citation)
        r_cit.font.name = "Times New Roman"
        r_cit.font.size = Pt(10.5)

    # =========================================================================
    # SECTION 25: APPENDIX
    # =========================================================================
    add_sec_heading("17. APPENDIX", level=1, page_break=True)
    
    add_sec_heading("Appendix A: Complete MongoDB Shell Commands & Verification Scripts", level=2, page_break=False)
    add_p("Essential MongoDB shell (`mongosh`) commands to inspect and verify the ShopSphere database:")
    add_code_block(
        '// Connect to MongoDB and switch to ShopSphere Olist database\n'
        'use shopsphere_olist\n\n'
        '// Display all collections and document counts\n'
        'db.getCollectionNames().forEach(function(col) {\n'
        '  print(col + ": " + db.getCollection(col).countDocuments() + " documents");\n'
        '});\n\n'
        '// Inspect active indexes on products collection\n'
        'db.products.getIndexes();\n\n'
        '// Run explain plan on SKU point lookup\n'
        'db.products.find({ "sku": "OLIST-PE-1E9E8EF0" }).explain("executionStats");\n\n'
        '// Verify collection schema validator\n'
        'db.getCollectionInfos({ "name": "products" })[0].options.validator;'
    )

    add_sec_heading("Appendix B: Data Dictionary & Field Specifications Table", level=2, page_break=False)
    add_p("Table 9 outlines the data dictionary across primary ShopSphere entities.")

    dict_table = [
        ("products._id", "ObjectId", "Yes", "Primary key generated via deterministic UUID5 hash"),
        ("products.sku", "String", "Yes", "Unique stock keeping unit index (e.g. OLIST-PE-1E9E8EF0)"),
        ("products.price", "Double", "Yes", "Unit selling price, validated >= 0.01"),
        ("products.stock_quantity", "Int32", "Yes", "Available inventory units (0 for untracked Olist items)"),
        ("customers.email", "String/null", "No", "Customer email; partial unique index allows nulls"),
        ("orders.items", "Array", "Yes", "Embedded array of line item snapshots (minItems: 1)"),
        ("orders.status", "String", "Yes", "Order state machine: pending, confirmed, shipped, delivered, cancelled"),
        ("orders.is_historical", "Boolean", "Yes", "Flag marking imported records immutable"),
        ("reviews.rating", "Int32", "Yes", "Customer feedback score between 1 and 5"),
        ("inventory_movements.change_quantity", "Int32", "Yes", "Integer stock delta (+/-) logged in permanent audit trail")
    ]
    add_styled_table(["Field Name / Path", "BSON Type", "Required", "Semantic Description & Validation Constraints"], dict_table, col_widths=[1.8, 1.0, 0.8, 3.0])

    add_sec_heading("Appendix C: Step-by-Step Project Setup & Execution Guide", level=2, page_break=False)
    add_p("Instructions for reproducing the development environment on Windows 11/10:")
    add_code_block(
        '# Step 1: Clone workspace and navigate to project folder\n'
        'cd D:\\Mongo_db-project\\ShopSphere\n\n'
        '# Step 2: Set up Python virtual environment and backend dependencies\n'
        'cd backend\n'
        'python -m venv venv\n'
        '.\\venv\\Scripts\\Activate.ps1\n'
        'pip install -r requirements.txt\n\n'
        '# Step 3: Run Olist dataset importer\n'
        'python scripts\\import_dataset.py --db-name shopsphere_olist\n\n'
        '# Step 4: Execute automated backend test suite\n'
        'pytest -v\n\n'
        '# Step 5: Launch FastAPI backend server\n'
        'uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload\n\n'
        '# Step 6: In a new terminal, launch Vite React frontend\n'
        'cd D:\\Mongo_db-project\\ShopSphere\\frontend\n'
        'npm install\n'
        'npm run dev -- --host 127.0.0.1 --port 5173'
    )

    add_sec_heading("Appendix D: Top 15 Academic Viva Voce Questions & Model Answers", level=2, page_break=False)
    
    viva_qas = [
        ("Q1: Why choose MongoDB over PostgreSQL for this e-commerce system?",
         "A1: MongoDB provides natural data locality through embedded documents, allowing orders, items, payments, and shipping addresses to be retrieved in a single disk read without expensive multi-table SQL joins. It also provides polymorphic schema flexibility for diverse product categories and native JSON Schema validation."),
        ("Q2: How does ShopSphere guarantee historical price immutability in orders?",
         "A2: By denormalizing purchased line items into an embedded array inside the order document at checkout. Each item stores its product_name, sku, unit_price, and quantity as an immutable snapshot, insulating historical records from future catalog price adjustments."),
        ("Q3: How does the system handle null customer emails without violating unique index constraints?",
         "A3: ShopSphere deploys a MongoDB Partial Unique Index with `partialFilterExpression: {\"email\": {\"$type\": \"string\"}}`. This enforces uniqueness exclusively on real string email values while allowing 99,000+ authentic anonymized records with null emails to coexist safely."),
        ("Q4: What is the difference between an IXSCAN and a COLLSCAN in MongoDB?",
         "A4: A COLLSCAN sequentially reads every document in a collection from disk/cache. An IXSCAN traverses a B-Tree index structure to locate exact document pointers. In ShopSphere, profiling with explain('executionStats') proved that an IXSCAN examined 1 key and 1 document in 0.0 ms, whereas a COLLSCAN examined all 32,951 documents sequentially."),
        ("Q5: How does the Olist dataset importer guarantee idempotency on repeated runs?",
         "A5: The importer generates deterministic BSON ObjectIds using UUID5 hashing on external identifiers and executes writes using PyMongo's `bulk_write` API with `UpdateOne(..., upsert=True)`. Repeated executions update existing records rather than duplicating them."),
        ("Q6: Why are 775 orders skipped during dataset import?",
         "A6: In the raw Kaggle dataset, 775 orders contained zero line items in `olist_order_items_dataset.csv`. Because ShopSphere enforces a collection-level `$jsonSchema` requiring `items` to be an array with `minItems: 1`, these empty orders are skipped to maintain database integrity."),
        ("Q7: How does ShopSphere handle transactions on standalone MongoDB instances?",
         "A7: Multi-document ACID transactions in MongoDB require a Replica Set oplog. On standalone local instances, ShopSphere implements an atomic two-phase compensation pattern: single-document stock decrements are executed first, with compensating reversal updates triggered if order creation fails."),
        ("Q8: How does the $facet aggregation stage work in the Analytics module?",
         "A8: The `$facet` stage allows executing multiple parallel aggregation sub-pipelines within a single stage over the same incoming document stream, returning status distributions and overall order summaries in a single query round-trip."),
        ("Q9: What is the purpose of the WiredTiger storage engine's Snappy compression?",
         "A9: Snappy provides low-CPU block-level compression for documents and indexes, reducing disk storage footprint by 50% to 70% and increasing effective in-memory working set capacity."),
        ("Q10: Why are database namespaces separated into shopsphere_olist, shopsphere, and shopsphere_test?",
         "A10: To ensure total isolation. `shopsphere_olist` houses 100k authentic historical records marked immutable; `shopsphere` serves as an operational demo sandbox; and `shopsphere_test` is dynamically populated and dropped during automated test runs with zero side-effects.")
    ]

    for q, a in viva_qas:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        r_q = p.add_run(q)
        r_q.bold = True
        r_q.font.name = "Times New Roman"
        r_q.font.size = Pt(10.5)
        r_q.font.color.rgb = RGBColor(30, 58, 138)

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_before = Pt(0)
        p_a.paragraph_format.space_after = Pt(6)
        p_a.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_a = p_a.add_run(a)
        r_a.font.name = "Times New Roman"
        r_a.font.size = Pt(10)

    # Save Document
    doc.save(DOCX_PATH)
    print(f"Report DOCX successfully generated at: {DOCX_PATH}")

if __name__ == "__main__":
    build_document()
