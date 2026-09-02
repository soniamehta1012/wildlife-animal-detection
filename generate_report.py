import subprocess
from collections import defaultdict
import datetime
import io
import os
import sys
import html
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# -------------------------------------------------------------
# CONFIGURATION: Institution &amp; Department Details
# -------------------------------------------------------------
COLLEGE_NAME = &quot;Swami Keshvanand Institute of Technology,Management &amp; Gramothan,
Jaipur&quot;

DEPARTMENT_NAME = &quot;Department of Computer Science &amp; Engineering&quot;
# -------------------------------------------------------------
def get_repo_info():
    &quot;&quot;&quot;Extracts the exact repository name and branch reliably in GitHub Codespaces.&quot;&quot;&quot;
    repo_name = &quot;Project-Repository&quot;
    branch_name = &quot;main&quot;
    try:
        root_path = subprocess.check_output([&#39;git&#39;, &#39;rev-parse&#39;, &#39;--show-toplevel&#39;], encoding=&#39;utf-
8&#39;).strip()
        repo_name = os.path.basename(root_path)
    except Exception:
        try:
            remote_url = subprocess.check_output([&#39;git&#39;, &#39;config&#39;, &#39;--get&#39;, &#39;remote.origin.url&#39;],
encoding=&#39;utf-8&#39;).strip()
            repo_name = remote_url.rstrip(&#39;/&#39;).split(&#39;/&#39;)[-1].replace(&#39;.git&#39;, &#39;&#39;)
        except Exception:
            repo_name = os.path.basename(os.getcwd())
    try:
        branch_name = subprocess.check_output([&#39;git&#39;, &#39;rev-parse&#39;, &#39;--abbrev-ref&#39;, &#39;HEAD&#39;],
encoding=&#39;utf-8&#39;).strip()
    except Exception:
        pass
    return repo_name, branch_name
def get_git_metrics(interval=&quot;weekly&quot;):
    &quot;&quot;&quot;
    Parses Git commit logs.
    Supported intervals: &#39;weekly&#39;, &#39;monthly&#39;, &#39;final&#39;
    &quot;&quot;&quot;
    today = datetime.date.today()
    git_args = [&#39;git&#39;, &#39;log&#39;, &#39;--no-merges&#39;, &#39;--pretty=format:COMMIT|||%h|||%an|||%ad|||%s&#39;, &#39;--
date=short&#39;, &#39;--numstat&#39;]
   
    if interval == &quot;weekly&quot;:
        since_date = (today - datetime.timedelta(days=7)).strftime(&quot;%Y-%m-%d&quot;)

        git_args.append(f&quot;--since={since_date}&quot;)
        scope_title = f&quot;Last 7 Days (Since {since_date})&quot;
    elif interval == &quot;monthly&quot;:
        since_date = (today - datetime.timedelta(days=30)).strftime(&quot;%Y-%m-%d&quot;)
        git_args.append(f&quot;--since={since_date}&quot;)
        scope_title = f&quot;Last 30 Days (Since {since_date})&quot;
    else:
        scope_title = &quot;Complete Project Lifecycle (All Commits)&quot;
    try:
        raw_output = subprocess.check_output(git_args, encoding=&#39;utf-8&#39;, errors=&#39;replace&#39;)
    except subprocess.CalledProcessError:
        print(&quot;[ERROR] Git command failed. Please ensure you are inside a Git repository.&quot;)
        return None, None, None, scope_title
    students = defaultdict(lambda: {&quot;commits&quot;: 0, &quot;added&quot;: 0, &quot;deleted&quot;: 0, &quot;active_days&quot;: set()})
    timeline_activity = defaultdict(lambda: defaultdict(int))
    student_logs = defaultdict(list)
    current_author = None
    current_date_str = None

    for line in raw_output.strip().split(&#39;\n&#39;):
        line = line.strip()
        if not line:
            continue
           
        if line.startswith(&#39;COMMIT|||&#39;):
            parts = line.split(&#39;|||&#39;)
            if len(parts) &gt;= 5:
                sha = parts[1].strip()
                author = parts[2].strip()
                date_str = parts[3].strip()
                msg = parts[4].strip()
            else:
                continue
               

            # --- IGNORE AUTOMATED BOTS ---
            if &quot;bot&quot; in author.lower() or &quot;github-actions&quot; in author.lower():
                current_author = None
                continue
            # -----------------------------
           
            current_author = author
            current_date_str = date_str
           
            students[current_author][&quot;commits&quot;] += 1
            students[current_author][&quot;active_days&quot;].add(current_date_str)
            student_logs[current_author].append((date_str, sha, msg))
           
            try:
                dt = datetime.datetime.strptime(current_date_str, &quot;%Y-%m-%d&quot;).date()
                if interval == &quot;weekly&quot;:
                    period_key = dt.strftime(&quot;%a (%b %d)&quot;)
                elif interval == &quot;monthly&quot;:
                    period_key = f&quot;{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}&quot;
                else:
                    period_key = dt.strftime(&quot;%Y-%m&quot;)
                timeline_activity[period_key][current_author] += 1
            except Exception:
                pass

        elif current_author and not line.startswith(&#39;COMMIT|||&#39;):
            parts = line.split()
            if len(parts) &gt;= 2 and parts[0].isdigit() and parts[1].isdigit():
                students[current_author][&quot;added&quot;] += int(parts[0])
                students[current_author][&quot;deleted&quot;] += int(parts[1])

    return students, timeline_activity, student_logs, scope_title

def create_charts(students, timeline_activity, interval):

    &quot;&quot;&quot;Generates visual workload and trend charts.&quot;&quot;&quot;
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8))
    authors = list(students.keys())
    periods = sorted(timeline_activity.keys())

    # 1. Timeline Line Chart
    if periods and authors:
        for author in authors:
            counts = [timeline_activity[p].get(author, 0) for p in periods]
            ax1.plot(periods, counts, marker=&#39;o&#39;, linewidth=2, label=author)
        ax1.set_title(f&quot;Commit Timeline ({interval.capitalize()})&quot;, fontsize=10, fontweight=&#39;bold&#39;)
        ax1.set_ylabel(&quot;Commits&quot;)
        ax1.tick_params(axis=&#39;x&#39;, rotation=30)
        ax1.grid(True, linestyle=&#39;--&#39;, alpha=0.5)
        ax1.legend(fontsize=8)
    else:
        ax1.text(0.5, 0.5, &quot;No commits found in this interval&quot;, ha=&#39;center&#39;, va=&#39;center&#39;)

    # 2. Net LOC Bar Chart
    if authors:
        net_loc = [students[a][&quot;added&quot;] - students[a][&quot;deleted&quot;] for a in authors]
        colors_list = [&#39;#4E79A7&#39;, &#39;#F28E2B&#39;, &#39;#E15759&#39;, &#39;#76B7B2&#39;, &#39;#59A14F&#39;]
        ax2.bar(authors, net_loc, color=colors_list[:len(authors)], width=0.45)
        ax2.set_title(&quot;Net Lines of Code Written&quot;, fontsize=10, fontweight=&#39;bold&#39;)
        ax2.set_ylabel(&quot;LOC (Added - Deleted)&quot;)
        ax2.grid(axis=&#39;y&#39;, linestyle=&#39;--&#39;, alpha=0.5)
    else:
        ax2.text(0.5, 0.5, &quot;No LOC changes recorded&quot;, ha=&#39;center&#39;, va=&#39;center&#39;)

    plt.tight_layout()
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format=&#39;png&#39;, dpi=200)
    plt.close()
    img_buffer.seek(0)

    return Image(img_buffer, width=500, height=170)

def generate_pdf(interval=&quot;weekly&quot;):
    repo_name, branch_name = get_repo_info()
    students, timeline_activity, student_logs, scope_title = get_git_metrics(interval)

    if students is None:
        return

    date_stamp = datetime.date.today().strftime(&quot;%Y-%m-%d&quot;)
   
    if interval == &quot;weekly&quot;:
        report_title = &quot;Weekly Progress Report (Form-3)&quot;
        doc_name = f&quot;{repo_name}_Weekly_Progress_Report_Form-3_{date_stamp}.pdf&quot;
    elif interval == &quot;monthly&quot;:
        report_title = &quot;Monthly Progress Report (Form-3)&quot;
        doc_name = f&quot;{repo_name}_Monthly_Progress_Report_Form-3_{date_stamp}.pdf&quot;
    else:
        report_title = &quot;Final Project Evaluation Report&quot;
        doc_name = f&quot;{repo_name}_Final_Report_{date_stamp}.pdf&quot;

    doc = SimpleDocTemplate(
        doc_name,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
   
    college_style = ParagraphStyle(
        &#39;CollegeStyle&#39;, parent=styles[&#39;Heading1&#39;],

        fontSize=13.5, leading=17, textColor=colors.HexColor(&quot;#0F172A&quot;), alignment=1,
spaceAfter=2
    )
    dept_style = ParagraphStyle(
        &#39;DeptStyle&#39;, parent=styles[&#39;Normal&#39;],
        fontSize=9.5, leading=13, textColor=colors.HexColor(&quot;#475569&quot;), alignment=1, spaceAfter=6
    )
    title_style = ParagraphStyle(
        &#39;TitleStyle&#39;, parent=styles[&#39;Heading2&#39;],
        fontSize=13, leading=17, textColor=colors.HexColor(&quot;#1A365D&quot;), alignment=1, spaceAfter=5
    )
    repo_style = ParagraphStyle(
        &#39;RepoStyle&#39;, parent=styles[&#39;Normal&#39;],
        fontSize=9.5, leading=14, textColor=colors.HexColor(&quot;#0F172A&quot;), spaceAfter=3
    )
    meta_style = ParagraphStyle(
        &#39;MetaStyle&#39;, parent=styles[&#39;Normal&#39;],
        fontSize=8.5, textColor=colors.HexColor(&quot;#64748B&quot;), spaceAfter=8
    )
    section_style = ParagraphStyle(
        &#39;SectionStyle&#39;, parent=styles[&#39;Heading2&#39;],
        fontSize=10.5, leading=14, textColor=colors.HexColor(&quot;#0F172A&quot;), spaceBefore=7,
spaceAfter=4
    )
    sub_section_style = ParagraphStyle(
        &#39;SubSectionStyle&#39;, parent=styles[&#39;Heading3&#39;],
        fontSize=9, leading=12, textColor=colors.HexColor(&quot;#2563EB&quot;), spaceBefore=5,
spaceAfter=2
    )
    msg_style = ParagraphStyle(
        &#39;MsgStyle&#39;, parent=styles[&#39;Normal&#39;],
        fontSize=8, leading=10, textColor=colors.HexColor(&quot;#1E293B&quot;)
    )
    meta_cell_style = ParagraphStyle(

        &#39;MetaCellStyle&#39;, parent=styles[&#39;Normal&#39;],
        fontSize=8, leading=10, textColor=colors.HexColor(&quot;#475569&quot;), alignment=1
    )
    marks_style = ParagraphStyle(
        &#39;MarksStyle&#39;, parent=styles[&#39;Normal&#39;],
        fontSize=9, leading=12, textColor=colors.HexColor(&quot;#0F172A&quot;), alignment=1
    )
    sig_block_style = ParagraphStyle(
        &#39;SigBlockStyle&#39;, parent=styles[&#39;Normal&#39;],
        fontSize=9, leading=15, textColor=colors.HexColor(&quot;#0F172A&quot;), alignment=0
    )

    story = []

    # 1. Header with College &amp; Department Name and Form-3 Title
    story.append(Paragraph(f&quot;&lt;b&gt;{html.escape(COLLEGE_NAME)}&lt;/b&gt;&quot;, college_style))
    story.append(Paragraph(f&quot;&lt;b&gt;{html.escape(DEPARTMENT_NAME)}&lt;/b&gt;&quot;, dept_style))
    story.append(Paragraph(f&quot;&lt;u&gt;&lt;b&gt;{report_title}&lt;/b&gt;&lt;/u&gt;&quot;, title_style))
    story.append(Spacer(1, 3))

    # 2. Metadata (Repo, Branch, Scope, Date)
    story.append(Paragraph(f&quot;&lt;b&gt;Project Repository:&lt;/b&gt; &lt;font
color=&#39;#2563EB&#39;&gt;&lt;b&gt;{html.escape(repo_name)}&lt;/b&gt;&lt;/font&gt; &amp;nbsp;|&amp;nbsp; &lt;b&gt;Branch:&lt;/b&gt;
&lt;code&gt;{html.escape(branch_name)}&lt;/code&gt;&quot;, repo_style))
    story.append(Paragraph(f&quot;&lt;b&gt;Evaluation Window:&lt;/b&gt; {scope_title} &amp;nbsp;|&amp;nbsp;
&lt;b&gt;Generated On:&lt;/b&gt; {datetime.date.today().strftime(&#39;%B %d, %Y&#39;)}&quot;, meta_style))

    # 3. Individual Summary Table
    story.append(Paragraph(&quot;1. Individual Contribution Breakdown&quot;, section_style))
    total_commits = sum(data[&quot;commits&quot;] for data in students.values())
    table_data = [[&quot;Student Name&quot;, &quot;Commits (%)&quot;, &quot;Lines Added&quot;, &quot;Lines Deleted&quot;, &quot;Net LOC&quot;,
&quot;Active Days&quot;]]
   
    if students:

        for name, data in students.items():
            pct = (data[&quot;commits&quot;] / total_commits * 100) if total_commits &gt; 0 else 0
            net = data[&quot;added&quot;] - data[&quot;deleted&quot;]
            table_data.append([
                html.escape(name),
                f&quot;{data[&#39;commits&#39;]} ({pct:.1f}%)&quot;,
                f&quot;+{data[&#39;added&#39;]:,}&quot;,
                f&quot;-{data[&#39;deleted&#39;]:,}&quot;,
                f&quot;{net:,}&quot;,
                f&quot;{len(data[&#39;active_days&#39;])} days&quot;
            ])
    else:
        table_data.append([&quot;No commits found in this period. Run with &#39;final&#39; to see all commits.&quot;, &quot;-&quot;,
&quot;-&quot;, &quot;-&quot;, &quot;-&quot;, &quot;-&quot;])

    table = Table(table_data, colWidths=[120, 80, 80, 80, 80, 100])
    table.setStyle(TableStyle([
        (&#39;BACKGROUND&#39;, (0, 0), (-1, 0), colors.HexColor(&quot;#1E293B&quot;)),
        (&#39;TEXTCOLOR&#39;, (0, 0), (-1, 0), colors.whitesmoke),
        (&#39;ALIGN&#39;, (0, 0), (-1, -1), &#39;CENTER&#39;),
        (&#39;ALIGN&#39;, (0, 1), (0, -1), &#39;LEFT&#39;),
        (&#39;FONTNAME&#39;, (0, 0), (-1, 0), &#39;Helvetica-Bold&#39;),
        (&#39;FONTSIZE&#39;, (0, 0), (-1, -1), 8),
        (&#39;BOTTOMPADDING&#39;, (0, 0), (-1, -1), 3.5),
        (&#39;TOPPADDING&#39;, (0, 0), (-1, -1), 3.5),
        (&#39;GRID&#39;, (0, 0), (-1, -1), 0.5, colors.HexColor(&quot;#CBD5E1&quot;)),
        (&#39;ROWBACKGROUNDS&#39;, (0, 1), (-1, -1), [colors.white, colors.HexColor(&quot;#F8FAFC&quot;)]),
    ]))
    story.append(table)
    story.append(Spacer(1, 6))

    # 4. Visual Charts
    story.append(Paragraph(&quot;2. Visual Trends &amp; Volume&quot;, section_style))
    chart_image = create_charts(students, timeline_activity, interval)

    story.append(chart_image)
    story.append(Spacer(1, 6))

    # 5. Detailed Commit Logs per Student WITH Vertically Merged Mentor Marks
    story.append(Paragraph(f&quot;3. Detailed Commit Logs &amp; Mentor Evaluation
({interval.capitalize()})&quot;, section_style))
    if not student_logs:
        story.append(Paragraph(&quot;&lt;i&gt;No commit logs found for this timeframe.&lt;/i&gt;&quot;, styles[&#39;Normal&#39;]))
    else:
        for student_name, logs in student_logs.items():
            student_section = []
            student_section.append(Paragraph(f&quot;&lt;b&gt;Student:&lt;/b&gt; {html.escape(student_name)} —
&lt;i&gt;{len(logs)} commit(s)&lt;/i&gt;&quot;, sub_section_style))
           
            log_table_data = [[&quot;Date&quot;, &quot;Hash&quot;, &quot;Commit Message&quot;, &quot;Mentor Marks (/10)&quot;]]
           
            # Place the clean marking line in the first row
            first_date, first_sha, first_msg = logs[0]
            safe_msg = html.escape(first_msg) if first_msg else &quot;(No commit message)&quot;
            log_table_data.append([
                Paragraph(first_date, meta_cell_style),
                Paragraph(f&quot;&lt;code&gt;{first_sha}&lt;/code&gt;&quot;, meta_cell_style),
                Paragraph(safe_msg, msg_style),
                Paragraph(&quot;&lt;b&gt;_____ / 10&lt;/b&gt;&quot;, marks_style)
            ])
           
            # Subsequent commit rows have blank placeholder for merged cell
            for date_val, sha_val, msg_val in logs[1:]:
                safe_msg = html.escape(msg_val) if msg_val else &quot;(No commit message)&quot;
                log_table_data.append([
                    Paragraph(date_val, meta_cell_style),
                    Paragraph(f&quot;&lt;code&gt;{sha_val}&lt;/code&gt;&quot;, meta_cell_style),
                    Paragraph(safe_msg, msg_style),
                    &quot;&quot;

                ])
           
            num_rows = len(log_table_data)
            log_table = Table(log_table_data, colWidths=[65, 50, 335, 90])
           
            t_style = [
                (&#39;BACKGROUND&#39;, (0, 0), (-1, 0), colors.HexColor(&quot;#475569&quot;)),
                (&#39;TEXTCOLOR&#39;, (0, 0), (-1, 0), colors.whitesmoke),
                (&#39;ALIGN&#39;, (0, 0), (-1, -1), &#39;LEFT&#39;),
                (&#39;ALIGN&#39;, (3, 0), (3, -1), &#39;CENTER&#39;),
                (&#39;FONTNAME&#39;, (0, 0), (-1, 0), &#39;Helvetica-Bold&#39;),
                (&#39;FONTSIZE&#39;, (0, 0), (-1, -1), 7.5),
                (&#39;BOTTOMPADDING&#39;, (0, 0), (-1, -1), 2.5),
                (&#39;TOPPADDING&#39;, (0, 0), (-1, -1), 2.5),
                (&#39;GRID&#39;, (0, 0), (-1, -1), 0.5, colors.HexColor(&quot;#CBD5E1&quot;)),
                (&#39;ROWBACKGROUNDS&#39;, (0, 1), (2, -1), [colors.white, colors.HexColor(&quot;#F8FAFC&quot;)]),
                (&#39;SPAN&#39;, (3, 1), (3, num_rows - 1)),              # Vertically merge mentor marks column
                (&#39;VALIGN&#39;, (3, 1), (3, num_rows - 1), &#39;MIDDLE&#39;),     # Vertically center the marks line
                (&#39;BACKGROUND&#39;, (3, 1), (3, num_rows - 1), colors.HexColor(&quot;#FEF3C7&quot;)), # Accent for
marks area
            ]
           
            log_table.setStyle(TableStyle(t_style))
            student_section.append(log_table)
            student_section.append(Spacer(1, 5))
            story.append(KeepTogether(student_section))

    # 6. Symmetrical Signatures
    story.append(Spacer(1, 16))
   
    mentor_cell = [
        Paragraph(&quot;&lt;b&gt;Name:&lt;/b&gt; ___________________________&quot;, sig_block_style),
        Paragraph(&quot;&lt;b&gt;Designation:&lt;/b&gt; Project Mentor&quot;, sig_block_style),
        Spacer(1, 6),

        Paragraph(&quot;&lt;b&gt;Signature:&lt;/b&gt; ________________________&quot;, sig_block_style),
    ]
   
    coordinator_cell = [
        Paragraph(&quot;&lt;b&gt;Name:&lt;/b&gt; ___________________________&quot;, sig_block_style),
        Paragraph(&quot;&lt;b&gt;Designation:&lt;/b&gt; Lab Coordinator&quot;, sig_block_style),
        Spacer(1, 6),
        Paragraph(&quot;&lt;b&gt;Signature:&lt;/b&gt; ________________________&quot;, sig_block_style),
    ]

    sig_table = Table([[mentor_cell, coordinator_cell]], colWidths=[270, 270])
    sig_table.setStyle(TableStyle([
        (&#39;VALIGN&#39;, (0, 0), (-1, -1), &#39;TOP&#39;),
        (&#39;LEFTPADDING&#39;, (0, 0), (0, -1), 0),
        (&#39;LEFTPADDING&#39;, (1, 0), (1, -1), 40),
        (&#39;RIGHTPADDING&#39;, (0, 0), (-1, -1), 0),
        (&#39;BOTTOMPADDING&#39;, (0, 0), (-1, -1), 0),
        (&#39;TOPPADDING&#39;, (0, 0), (-1, -1), 0),
    ]))
   
    story.append(KeepTogether(sig_table))

    doc.build(story)
    print(f&quot;\n[SUCCESS] Generated: {doc_name}&quot;)
    print(f&quot; -&gt; Found {len(students)} student(s) and {total_commits} total commits.&quot;)

if __name__ == &quot;__main__&quot;:
    chosen_interval = sys.argv[1].lower() if len(sys.argv) &gt; 1 else &quot;weekly&quot;
    generate_pdf(chosen_interval)
