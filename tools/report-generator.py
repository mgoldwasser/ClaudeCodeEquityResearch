#!/usr/bin/env python3
"""
Research Report Generator
=========================
Generates PDF reports, charts, probability distributions, and executive summaries
from equity research analysis output.

Usage:
    python tools/report-generator.py pdf --input output/TICKER-research-note.md --output output/TICKER-report.pdf
    python tools/report-generator.py charts --scenarios-file scenarios.json --output output/charts/
    python tools/report-generator.py executive-summary --input output/TICKER-research-note.md --output output/TICKER-exec-summary.pdf
    python tools/report-generator.py histogram --scenarios-file scenarios.json --output output/charts/outcome-dist.png
    python tools/report-generator.py sensitivity --wacc-range 7,12 --tgr-range 1,4 --values-file values.json --output output/charts/sensitivity.png
    python tools/report-generator.py waterfall --components-file components.json --output output/charts/waterfall.png

Dependencies:
    pip install matplotlib reportlab
"""

import argparse
import json
import sys
import os
import re
from typing import Dict, List, Optional, Tuple


# ============================================================
# CHART GENERATION (matplotlib)
# ============================================================

def generate_probability_histogram(scenarios: List[Dict], output_path: str,
                                   current_price: float = None, ticker: str = "") -> str:
    """
    Generate bar chart of bull/base/bear price scenarios with probabilities.
    Each scenario: {"name": str, "price": float, "probability": float}
    """
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.ticker as mticker
    except ImportError:
        return "Error: matplotlib required. Install: pip install matplotlib"

    fig, ax = plt.subplots(figsize=(10, 6))

    names = [s["name"] for s in scenarios]
    prices = [s["price"] for s in scenarios]
    probs = [s["probability"] for s in scenarios]

    # Color coding: bear=red, base=blue, bull=green
    colors = []
    for name in names:
        name_lower = name.lower()
        if "bear" in name_lower or "worst" in name_lower:
            colors.append('#e74c3c')
        elif "bull" in name_lower or "best" in name_lower:
            colors.append('#2ecc71')
        else:
            colors.append('#3498db')

    bars = ax.bar(names, prices, color=colors, width=0.6, edgecolor='white', linewidth=1.5)

    # Add probability labels on bars
    for bar, prob, price in zip(bars, probs, prices):
        ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + max(prices) * 0.02,
                f'${price:,.0f}\n({prob:.0%} prob)',
                ha='center', va='bottom', fontweight='bold', fontsize=11)

    # Expected value line
    ev = sum(p * pr for p, pr in zip(prices, probs))
    ax.axhline(y=ev, color='#e67e22', linestyle='--', linewidth=2, label=f'Expected Value: ${ev:,.2f}')

    # Current price line
    if current_price:
        ax.axhline(y=current_price, color='#95a5a6', linestyle=':', linewidth=1.5,
                    label=f'Current Price: ${current_price:,.2f}')

    ax.set_ylabel('Price ($)', fontsize=12)
    ax.set_title(f'{ticker + " — " if ticker else ""}Scenario Price Distribution', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax.set_ylim(0, max(prices) * 1.25)

    # Style
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return f"Saved histogram to {output_path}"


def generate_return_distribution(scenarios: List[Dict], output_path: str,
                                 current_price: float = None, ticker: str = "") -> str:
    """
    Generate a probability-weighted return distribution chart.
    Shows both discrete scenario bars and a fitted normal curve overlay.
    """
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        return "Error: matplotlib and numpy required. Install: pip install matplotlib numpy"

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    prices = [s["price"] for s in scenarios]
    probs = [s["probability"] for s in scenarios]
    names = [s["name"] for s in scenarios]

    if current_price:
        returns = [(p - current_price) / current_price * 100 for p in prices]
    else:
        returns = prices  # Use prices directly if no current price

    # Left panel: Scenario probability bars
    colors = ['#e74c3c' if r < 0 else '#2ecc71' if r > 15 else '#3498db' for r in returns]
    bars = ax1.bar(names, probs, color=colors, width=0.6, edgecolor='white', linewidth=1.5)
    for bar, prob, ret in zip(bars, probs, returns):
        label = f'{prob:.0%}\n({ret:+.1f}%)' if current_price else f'{prob:.0%}'
        ax1.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.02,
                 label, ha='center', va='bottom', fontweight='bold', fontsize=10)
    ax1.set_ylabel('Probability', fontsize=11)
    ax1.set_title('Scenario Probabilities', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, max(probs) * 1.35)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Right panel: Continuous distribution
    ev = sum(p * pr for p, pr in zip(prices, probs))
    variance = sum(pr * (p - ev) ** 2 for p, pr in zip(prices, probs))
    std = variance ** 0.5

    x = np.linspace(min(prices) * 0.7, max(prices) * 1.3, 200)
    if std > 0:
        pdf = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - ev) / std) ** 2)
    else:
        pdf = np.zeros_like(x)

    ax2.plot(x, pdf, color='#2c3e50', linewidth=2)
    ax2.fill_between(x, pdf, alpha=0.15, color='#3498db')

    # Mark scenarios
    for s in scenarios:
        color = '#e74c3c' if 'bear' in s['name'].lower() else '#2ecc71' if 'bull' in s['name'].lower() else '#3498db'
        ax2.axvline(x=s['price'], color=color, linestyle='--', alpha=0.7, linewidth=1.5)
        ax2.text(s['price'], ax2.get_ylim()[1] * 0.85 if ax2.get_ylim()[1] > 0 else 0.01,
                 f" {s['name']}\n ${s['price']:,.0f}", fontsize=9, color=color)

    # Mark EV
    ax2.axvline(x=ev, color='#e67e22', linewidth=2, linestyle='-')
    ax2.text(ev, ax2.get_ylim()[1] * 0.95 if ax2.get_ylim()[1] > 0 else 0.01,
             f' EV: ${ev:,.2f}', fontweight='bold', color='#e67e22', fontsize=10)

    if current_price:
        ax2.axvline(x=current_price, color='#95a5a6', linewidth=1.5, linestyle=':')

    ax2.set_xlabel('Price ($)', fontsize=11)
    ax2.set_ylabel('Probability Density', fontsize=11)
    ax2.set_title('Price Distribution', fontsize=12, fontweight='bold')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    fig.suptitle(f'{ticker + " — " if ticker else ""}Outcome Distribution Analysis',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return f"Saved distribution chart to {output_path}"


def generate_sensitivity_heatmap(wacc_values: List[float], tgr_values: List[float],
                                 price_matrix: List[List[float]], output_path: str,
                                 current_price: float = None, ticker: str = "") -> str:
    """
    Generate WACC vs Terminal Growth Rate sensitivity heatmap.
    price_matrix[i][j] = implied price at wacc_values[i] and tgr_values[j]
    """
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        return "Error: matplotlib and numpy required. Install: pip install matplotlib numpy"

    fig, ax = plt.subplots(figsize=(10, 7))

    data = np.array(price_matrix)

    # Color map: green = high price, red = low price
    im = ax.imshow(data, cmap='RdYlGn', aspect='auto')

    # Labels
    ax.set_xticks(range(len(tgr_values)))
    ax.set_xticklabels([f'{v:.1f}%' for v in tgr_values])
    ax.set_yticks(range(len(wacc_values)))
    ax.set_yticklabels([f'{v:.1f}%' for v in wacc_values])

    ax.set_xlabel('Terminal Growth Rate', fontsize=12)
    ax.set_ylabel('WACC', fontsize=12)
    ax.set_title(f'{ticker + " — " if ticker else ""}DCF Sensitivity: WACC vs Terminal Growth',
                 fontsize=13, fontweight='bold')

    # Cell values
    for i in range(len(wacc_values)):
        for j in range(len(tgr_values)):
            val = data[i, j]
            # Bold the cell closest to current price
            weight = 'bold' if current_price and abs(val - current_price) < current_price * 0.05 else 'normal'
            color = 'white' if val < np.median(data) else 'black'
            ax.text(j, i, f'${val:,.0f}', ha='center', va='center',
                    fontsize=9, fontweight=weight, color=color)

    plt.colorbar(im, label='Implied Share Price ($)')
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return f"Saved sensitivity heatmap to {output_path}"


def generate_waterfall_chart(components: List[Dict], output_path: str,
                             ticker: str = "") -> str:
    """
    Generate price target waterfall chart showing buildup.
    Each component: {"name": str, "value": float, "type": "add"|"subtract"|"total"}
    """
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        return "Error: matplotlib and numpy required. Install: pip install matplotlib numpy"

    fig, ax = plt.subplots(figsize=(12, 7))

    names = [c["name"] for c in components]
    values = [c["value"] for c in components]
    types = [c.get("type", "add") for c in components]

    # Calculate cumulative for waterfall
    cumulative = 0
    bottoms = []
    heights = []
    colors = []

    for val, typ in zip(values, types):
        if typ == "total":
            bottoms.append(0)
            heights.append(val)
            colors.append('#2c3e50')
        elif typ == "subtract" or val < 0:
            bottoms.append(cumulative + val)
            heights.append(abs(val))
            colors.append('#e74c3c')
            cumulative += val
        else:
            bottoms.append(cumulative)
            heights.append(val)
            colors.append('#2ecc71')
            cumulative += val

    bars = ax.bar(names, heights, bottom=bottoms, color=colors, width=0.6,
                  edgecolor='white', linewidth=1.5)

    # Add value labels
    for bar, bottom, height, val in zip(bars, bottoms, heights, values):
        y_pos = bottom + height / 2
        label = f'${val:,.0f}' if abs(val) >= 1 else f'${val:,.2f}'
        ax.text(bar.get_x() + bar.get_width() / 2., y_pos,
                label, ha='center', va='center', fontweight='bold',
                fontsize=10, color='white')

    # Connector lines
    for i in range(len(components) - 1):
        if types[i] != "total":
            y = bottoms[i] + heights[i] if values[i] >= 0 else bottoms[i]
            ax.plot([i + 0.3, i + 0.7], [cumulative if i == len(components) - 2 else bottoms[i+1] + heights[i+1] if types[i+1] == "total" else bottoms[i] + heights[i]] * 2,
                    color='gray', linewidth=0.8, linestyle='--')

    ax.set_ylabel('Price ($)', fontsize=12)
    ax.set_title(f'{ticker + " — " if ticker else ""}Price Target Derivation',
                 fontsize=14, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return f"Saved waterfall chart to {output_path}"


# ============================================================
# PDF GENERATION (reportlab)
# ============================================================

def markdown_to_pdf(input_path: str, output_path: str, chart_dir: str = None) -> str:
    """
    Convert markdown research note to PDF.
    Embeds charts from chart_dir if available.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            PageBreak, Image, KeepTogether
        )
        from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    except ImportError:
        return "Error: reportlab required. Install: pip install reportlab"

    with open(input_path, 'r') as f:
        content = f.read()

    # Setup PDF
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(
        name='ReportTitle',
        parent=styles['Title'],
        fontSize=20,
        spaceAfter=6,
        textColor=HexColor('#1a1a2e'),
    ))
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading1'],
        fontSize=14,
        spaceBefore=20,
        spaceAfter=8,
        textColor=HexColor('#16213e'),
        borderWidth=1,
        borderColor=HexColor('#e8e8e8'),
        borderPadding=4,
    ))
    styles.add(ParagraphStyle(
        name='SubHeader',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=12,
        spaceAfter=6,
        textColor=HexColor('#0f3460'),
    ))
    styles.add(ParagraphStyle(
        name='BodyText2',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name='BoldBody',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        fontName='Helvetica-Bold',
    ))
    styles.add(ParagraphStyle(
        name='SmallText',
        parent=styles['BodyText'],
        fontSize=8,
        leading=10,
        textColor=HexColor('#666666'),
    ))

    elements = []

    # Parse markdown sections
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            elements.append(Spacer(1, 6))
            i += 1
            continue

        # Title (# )
        if line.startswith('# ') and not line.startswith('## '):
            title = line[2:].strip()
            elements.append(Paragraph(title, styles['ReportTitle']))
            elements.append(Spacer(1, 4))

        # Section header (## )
        elif line.startswith('## '):
            header = line[3:].strip()
            # Remove numbering like "1. " or "2. "
            header = re.sub(r'^\d+\.\s*', '', header)
            elements.append(Paragraph(header, styles['SectionHeader']))

        # Subsection (### )
        elif line.startswith('### '):
            subheader = line[4:].strip()
            elements.append(Paragraph(subheader, styles['SubHeader']))

        # Table (|)
        elif line.startswith('|') and '|' in line[1:]:
            # Collect table rows
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                row_text = lines[i].strip()
                # Skip separator rows (|---|---|)
                if re.match(r'\|[\s\-:|]+\|', row_text):
                    i += 1
                    continue
                cells = [c.strip() for c in row_text.split('|')[1:-1]]
                table_rows.append(cells)
                i += 1
            i -= 1  # Back up one since the outer loop increments

            if table_rows:
                # Create table
                col_count = max(len(r) for r in table_rows)
                # Pad short rows
                for r in table_rows:
                    while len(r) < col_count:
                        r.append('')

                # Convert to Paragraphs for word wrapping
                table_data = []
                for ri, row in enumerate(table_rows):
                    style = styles['BoldBody'] if ri == 0 else styles['BodyText2']
                    table_data.append([Paragraph(str(c), style) for c in row])

                # Calculate column widths
                available_width = 6.5 * inch
                col_width = available_width / col_count

                t = Table(table_data, colWidths=[col_width] * col_count)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f0f0f0')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#1a1a2e')),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#ffffff'), HexColor('#f9f9f9')]),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ]))
                elements.append(t)
                elements.append(Spacer(1, 8))

        # Bold text (**text**)
        elif line.startswith('**') and line.endswith('**'):
            text = line.strip('*').strip()
            elements.append(Paragraph(f'<b>{text}</b>', styles['BodyText2']))

        # List items (- or *)
        elif line.startswith('- ') or line.startswith('* '):
            text = line[2:]
            # Handle bold within list items
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            elements.append(Paragraph(f'&bull; {text}', styles['BodyText2']))

        # Horizontal rule (---)
        elif line.startswith('---'):
            elements.append(Spacer(1, 12))

        # Code block (```)
        elif line.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            code_text = '\n'.join(code_lines)
            elements.append(Paragraph(
                f'<font face="Courier" size="8">{code_text}</font>',
                styles['BodyText2']
            ))

        # Regular text
        else:
            # Handle inline bold
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
            # Handle inline code
            text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
            elements.append(Paragraph(text, styles['BodyText2']))

        i += 1

    # Embed charts if available
    if chart_dir and os.path.isdir(chart_dir):
        chart_files = sorted([f for f in os.listdir(chart_dir) if f.endswith(('.png', '.jpg'))])
        if chart_files:
            elements.append(PageBreak())
            elements.append(Paragraph('Charts & Visualizations', styles['SectionHeader']))
            for cf in chart_files:
                chart_path = os.path.join(chart_dir, cf)
                try:
                    img = Image(chart_path, width=6 * inch, height=4 * inch)
                    img.hAlign = 'CENTER'
                    elements.append(img)
                    elements.append(Spacer(1, 12))
                    elements.append(Paragraph(
                        cf.replace('.png', '').replace('-', ' ').title(),
                        styles['SmallText']
                    ))
                    elements.append(Spacer(1, 20))
                except Exception:
                    elements.append(Paragraph(f'[Chart not loaded: {cf}]', styles['SmallText']))

    # Disclaimer
    elements.append(Spacer(1, 30))
    elements.append(Paragraph(
        '<i>This research note was generated by the Equity Research Swarm system. '
        'All analysis is for informational purposes only and does not constitute investment advice. '
        'Verify all data independently before making investment decisions.</i>',
        styles['SmallText']
    ))

    # Build PDF
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    doc.build(elements)
    return f"Saved PDF to {output_path}"


def generate_executive_summary_pdf(input_path: str, output_path: str,
                                   chart_path: str = None) -> str:
    """
    Generate a standalone 1-2 page executive summary PDF.
    Extracts key information from the full research note.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
        )
        from reportlab.lib.enums import TA_LEFT, TA_CENTER
    except ImportError:
        return "Error: reportlab required. Install: pip install reportlab"

    with open(input_path, 'r') as f:
        content = f.read()

    # Extract key fields from markdown
    def extract_field(pattern, default="N/A"):
        match = re.search(pattern, content, re.MULTILINE)
        return match.group(1).strip() if match else default

    ticker = extract_field(r'^# (\w+)')
    company = extract_field(r'^# \w+\s*[—–-]\s*(.+)', 'Company')
    rating = extract_field(r'\*\*Rating:\*\*\s*(.+)')
    price_target = extract_field(r'\*\*Price Target:\*\*\s*(.+)')
    current_price = extract_field(r'\*\*Current Price:\*\*\s*(.+)')
    upside = extract_field(r'\*\*Implied Upside/Downside:\*\*\s*(.+)')
    conviction = extract_field(r'\*\*Conviction Rating:\*\*\s*(.+)')
    market_cap = extract_field(r'\*\*Market Cap:\*\*\s*(.+)')
    sector = extract_field(r'\*\*Sector:\*\*\s*(.+)')

    # Extract executive summary section
    exec_match = re.search(
        r'## 1\. Executive Summary\s*\n(.*?)(?=\n---|\n## )',
        content, re.DOTALL
    )
    exec_summary = exec_match.group(1).strip() if exec_match else "Executive summary not found."

    # Extract bull/base/bear
    bull_match = re.search(r'### Bull Case.*?—.*?Implied Price:\s*\$?([\d,.]+)\s*\n(.*?)(?=\n###|\n---)', content, re.DOTALL)
    base_match = re.search(r'### Base Case.*?—.*?Implied Price:\s*\$?([\d,.]+)\s*\n(.*?)(?=\n###|\n---)', content, re.DOTALL)
    bear_match = re.search(r'### Bear Case.*?—.*?Implied Price:\s*\$?([\d,.]+)\s*\n(.*?)(?=\n###|\n---)', content, re.DOTALL)

    # Setup PDF
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        rightMargin=0.75 * inch, leftMargin=0.75 * inch,
        topMargin=0.5 * inch, bottomMargin=0.5 * inch,
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='ExecTitle', parent=styles['Title'],
        fontSize=22, spaceAfter=4, textColor=HexColor('#1a1a2e'),
    ))
    styles.add(ParagraphStyle(
        name='ExecSubtitle', parent=styles['Normal'],
        fontSize=12, spaceAfter=12, textColor=HexColor('#666666'),
    ))
    styles.add(ParagraphStyle(
        name='ExecBody', parent=styles['BodyText'],
        fontSize=11, leading=15, spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name='ExecBold', parent=styles['BodyText'],
        fontSize=11, leading=15, fontName='Helvetica-Bold',
    ))

    elements = []

    # Header
    elements.append(Paragraph(f'{ticker} — {company}', styles['ExecTitle']))
    elements.append(Paragraph('Executive Summary & Investment Thesis', styles['ExecSubtitle']))

    # Key metrics table
    metrics_data = [
        ['Rating', rating, 'Price Target', price_target],
        ['Current Price', current_price, 'Upside/Downside', upside],
        ['Conviction', conviction, 'Market Cap', market_cap],
        ['Sector', sector, '', ''],
    ]
    metrics_table = Table(metrics_data, colWidths=[1.5 * inch, 1.75 * inch, 1.5 * inch, 1.75 * inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#f0f4f8')),
        ('BACKGROUND', (2, 0), (2, -1), HexColor('#f0f4f8')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(metrics_table)
    elements.append(Spacer(1, 16))

    # Executive Summary
    elements.append(Paragraph('<b>Investment Thesis</b>', styles['ExecBold']))
    # Clean markdown formatting
    clean_summary = re.sub(r'\[.*?\]', '', exec_summary)
    clean_summary = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', clean_summary)
    elements.append(Paragraph(clean_summary, styles['ExecBody']))

    # Scenarios
    elements.append(Spacer(1, 8))
    elements.append(Paragraph('<b>Scenario Analysis</b>', styles['ExecBold']))

    scenario_data = [['Scenario', 'Price', 'Summary']]
    for label, match in [('Bull', bull_match), ('Base', base_match), ('Bear', bear_match)]:
        if match:
            price = f'${match.group(1)}'
            desc = match.group(2).strip()[:120]
            desc = re.sub(r'\[.*?\]', '', desc)
            scenario_data.append([label, price, desc])
        else:
            scenario_data.append([label, 'N/A', 'Not specified'])

    scenario_table = Table(scenario_data, colWidths=[1 * inch, 1 * inch, 4.5 * inch])
    scenario_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#ffffff'), HexColor('#f9f9f9')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(scenario_table)

    # Embed probability chart if available
    if chart_path and os.path.exists(chart_path):
        elements.append(Spacer(1, 16))
        try:
            img = Image(chart_path, width=5.5 * inch, height=3.5 * inch)
            img.hAlign = 'CENTER'
            elements.append(img)
        except Exception:
            pass

    # Disclaimer
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        '<i>Generated by Equity Research Swarm. For informational purposes only. '
        'Not investment advice.</i>',
        ParagraphStyle('Disclaimer', parent=styles['Normal'], fontSize=7,
                       textColor=HexColor('#999999'))
    ))

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    doc.build(elements)
    return f"Saved executive summary PDF to {output_path}"


def generate_all_charts(scenarios_file: str, output_dir: str,
                        current_price: float = None, ticker: str = "") -> str:
    """Generate all chart types from a scenarios file."""
    with open(scenarios_file) as f:
        data = json.load(f)

    scenarios = data.get("scenarios", data) if isinstance(data, dict) else data
    cp = current_price or data.get("current_price")
    tk = ticker or data.get("ticker", "")

    os.makedirs(output_dir, exist_ok=True)
    results = []

    # Histogram
    result = generate_probability_histogram(
        scenarios, os.path.join(output_dir, "scenario-histogram.png"), cp, tk
    )
    results.append(result)

    # Distribution
    result = generate_return_distribution(
        scenarios, os.path.join(output_dir, "return-distribution.png"), cp, tk
    )
    results.append(result)

    # Sensitivity heatmap (if data provided)
    if isinstance(data, dict) and "sensitivity" in data:
        sens = data["sensitivity"]
        result = generate_sensitivity_heatmap(
            sens["wacc_values"], sens["tgr_values"], sens["price_matrix"],
            os.path.join(output_dir, "sensitivity-heatmap.png"), cp, tk
        )
        results.append(result)

    # Waterfall (if data provided)
    if isinstance(data, dict) and "waterfall" in data:
        result = generate_waterfall_chart(
            data["waterfall"], os.path.join(output_dir, "price-waterfall.png"), tk
        )
        results.append(result)

    return "\n".join(results)


# ============================================================
# CLI INTERFACE
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Research Report Generator — PDFs, Charts, Executive Summaries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  pdf                Convert markdown research note to PDF
  charts             Generate all charts from scenarios file
  executive-summary  Generate standalone exec summary PDF
  histogram          Generate scenario probability histogram
  distribution       Generate return distribution chart
  sensitivity        Generate WACC/TGR sensitivity heatmap
  waterfall          Generate price target waterfall chart
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Generation command")

    # PDF
    pdf_parser = subparsers.add_parser("pdf", help="Markdown to PDF")
    pdf_parser.add_argument("--input", required=True, help="Input markdown file")
    pdf_parser.add_argument("--output", required=True, help="Output PDF file")
    pdf_parser.add_argument("--charts-dir", help="Directory with chart images to embed")

    # Charts
    charts_parser = subparsers.add_parser("charts", help="Generate all charts")
    charts_parser.add_argument("--scenarios-file", required=True, help="JSON scenarios file")
    charts_parser.add_argument("--output", required=True, help="Output directory for charts")
    charts_parser.add_argument("--current-price", type=float, help="Current stock price")
    charts_parser.add_argument("--ticker", default="", help="Stock ticker")

    # Executive summary
    exec_parser = subparsers.add_parser("executive-summary", help="Generate exec summary PDF")
    exec_parser.add_argument("--input", required=True, help="Input markdown research note")
    exec_parser.add_argument("--output", required=True, help="Output PDF file")
    exec_parser.add_argument("--chart", help="Probability chart image to embed")

    # Histogram
    hist_parser = subparsers.add_parser("histogram", help="Scenario histogram")
    hist_parser.add_argument("--scenarios-file", required=True, help="JSON scenarios file")
    hist_parser.add_argument("--output", required=True, help="Output PNG file")
    hist_parser.add_argument("--current-price", type=float, help="Current price for reference")
    hist_parser.add_argument("--ticker", default="", help="Stock ticker")

    # Distribution
    dist_parser = subparsers.add_parser("distribution", help="Return distribution chart")
    dist_parser.add_argument("--scenarios-file", required=True, help="JSON scenarios file")
    dist_parser.add_argument("--output", required=True, help="Output PNG file")
    dist_parser.add_argument("--current-price", type=float, help="Current price")
    dist_parser.add_argument("--ticker", default="", help="Stock ticker")

    # Sensitivity
    sens_parser = subparsers.add_parser("sensitivity", help="Sensitivity heatmap")
    sens_parser.add_argument("--values-file", required=True, help="JSON with wacc/tgr/prices")
    sens_parser.add_argument("--output", required=True, help="Output PNG file")
    sens_parser.add_argument("--current-price", type=float, help="Current price")
    sens_parser.add_argument("--ticker", default="", help="Stock ticker")

    # Waterfall
    wf_parser = subparsers.add_parser("waterfall", help="Price target waterfall")
    wf_parser.add_argument("--components-file", required=True, help="JSON with components")
    wf_parser.add_argument("--output", required=True, help="Output PNG file")
    wf_parser.add_argument("--ticker", default="", help="Stock ticker")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "pdf":
        result = markdown_to_pdf(args.input, args.output, args.charts_dir)

    elif args.command == "charts":
        result = generate_all_charts(args.scenarios_file, args.output,
                                     args.current_price, args.ticker)

    elif args.command == "executive-summary":
        result = generate_executive_summary_pdf(args.input, args.output, args.chart)

    elif args.command == "histogram":
        with open(args.scenarios_file) as f:
            data = json.load(f)
        scenarios = data.get("scenarios", data) if isinstance(data, dict) else data
        result = generate_probability_histogram(scenarios, args.output,
                                                args.current_price, args.ticker)

    elif args.command == "distribution":
        with open(args.scenarios_file) as f:
            data = json.load(f)
        scenarios = data.get("scenarios", data) if isinstance(data, dict) else data
        result = generate_return_distribution(scenarios, args.output,
                                              args.current_price, args.ticker)

    elif args.command == "sensitivity":
        with open(args.values_file) as f:
            data = json.load(f)
        result = generate_sensitivity_heatmap(
            data["wacc_values"], data["tgr_values"], data["price_matrix"],
            args.output, args.current_price, args.ticker
        )

    elif args.command == "waterfall":
        with open(args.components_file) as f:
            components = json.load(f)
        result = generate_waterfall_chart(components, args.output, args.ticker)

    else:
        parser.print_help()
        sys.exit(1)

    print(result)


if __name__ == "__main__":
    main()
