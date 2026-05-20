"""
VERA-AZ: Verification Engine for Results & Accountability - Arizona
Type 4 Dyslexia Screening using AASA and AZELLA Assessment Data
HB 2170 "Say Dyslexia" Compliance Support

H-EDU.Solutions | https://h-edu.solutions
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

APP_PASSWORD = "vera2026"

# Arizona colors
AZ_BLUE = "#002868"
AZ_RED = "#BF0A30"
AZ_COPPER = "#C87533"
AZ_GOLD = "#FFD700"

# ============================================================================
# SAMPLE DATA - Arizona Districts (Alphabetical Order)
# ============================================================================

def load_districts():
    """Load Arizona district data (alphabetical order)."""
    districts_data = [
        ("04", "Chandler Unified", 44000, 5280, 12.0, 92.5, "A"),
        ("05", "Gilbert Public Schools", 36000, 3600, 10.0, 94.1, "A"),
        ("06", "Glendale Elementary", 12500, 3125, 25.0, 85.2, "B"),
        ("07", "Mesa Public Schools", 64000, 11520, 18.0, 87.8, "B"),
        ("08", "Phoenix Union HSD", 27000, 6750, 25.0, 82.4, "B"),
        ("09", "Scottsdale Unified", 22000, 2200, 10.0, 93.6, "A"),
        ("10", "Tempe Elementary", 11000, 2420, 22.0, 86.5, "B"),
        ("11", "Tucson Unified", 42000, 12600, 30.0, 78.9, "C"),
    ]

    df = pd.DataFrame(districts_data, columns=[
        'district_id', 'district_name', 'total_students',
        'ell_count', 'ell_percent', 'graduation_rate', 'letter_grade'
    ])
    return df


def load_azella_data():
    """Load sample AZELLA assessment data."""
    azella_data = []

    districts = [
        ("04", "Chandler Unified"),
        ("05", "Gilbert Public Schools"),
        ("06", "Glendale Elementary"),
        ("07", "Mesa Public Schools"),
        ("08", "Phoenix Union HSD"),
        ("09", "Scottsdale Unified"),
        ("10", "Tempe Elementary"),
        ("11", "Tucson Unified"),
    ]

    for district_id, district_name in districts:
        for grade in range(3, 9):
            for year in [2024, 2025]:
                # Generate realistic AZELLA scores (scale 1-5: Pre-Emergent to Proficient)
                base_speaking = 2.8 + (grade * 0.08)
                base_writing = 2.4 + (grade * 0.06)

                # District-specific variation
                if district_id == "11":  # Tucson - highest EL%, larger delta
                    speaking_adj = 0.5
                    writing_adj = -0.3
                elif district_id == "06":  # Glendale
                    speaking_adj = 0.4
                    writing_adj = -0.2
                elif district_id in ["04", "09"]:  # Higher performing
                    speaking_adj = 0.3
                    writing_adj = 0.2
                else:
                    speaking_adj = 0.35
                    writing_adj = 0.0

                azella_data.append({
                    'district_id': district_id,
                    'district_name': district_name,
                    'grade': grade,
                    'year': year,
                    'total_tested': 800 + (grade * 50) if district_id in ["07", "11"] else 300 + (grade * 30),
                    'listening_avg': min(5.0, base_speaking + speaking_adj + 0.1),
                    'speaking_avg': min(5.0, base_speaking + speaking_adj),
                    'reading_avg': min(5.0, base_writing + writing_adj + 0.15),
                    'writing_avg': min(5.0, base_writing + writing_adj),
                    'overall_avg': min(5.0, (base_speaking + speaking_adj + base_writing + writing_adj) / 2 + 0.2)
                })

    return pd.DataFrame(azella_data)


def load_aasa_data():
    """Load sample AASA (Arizona's Academic Standards Assessment) data."""
    aasa_data = []

    districts = [
        ("04", "Chandler Unified"),
        ("05", "Gilbert Public Schools"),
        ("06", "Glendale Elementary"),
        ("07", "Mesa Public Schools"),
        ("08", "Phoenix Union HSD"),
        ("09", "Scottsdale Unified"),
        ("10", "Tempe Elementary"),
        ("11", "Tucson Unified"),
    ]

    for district_id, district_name in districts:
        for grade in range(3, 9):
            for year in [2024, 2025]:
                for subject in ['ELA', 'Math']:
                    # Generate realistic AASA proficiency (4 levels: Minimally, Partially, Proficient, Highly)
                    if district_id in ["04", "05", "09"]:  # High performing
                        proficient_plus = 62 + (grade * 0.5)
                        highly_proficient = 28 + (grade * 0.6)
                    elif district_id == "11":  # Lower performing
                        proficient_plus = 38 + (grade * 0.4)
                        highly_proficient = 12 + (grade * 0.3)
                    else:  # Average
                        proficient_plus = 48 + (grade * 0.4)
                        highly_proficient = 18 + (grade * 0.4)

                    aasa_data.append({
                        'district_id': district_id,
                        'district_name': district_name,
                        'grade': grade,
                        'subject': subject,
                        'year': year,
                        'total_tested': 5000 + (grade * 200) if district_id in ["07", "11", "04"] else 2000 + (grade * 100),
                        'proficient_plus_pct': min(90, proficient_plus),
                        'highly_proficient_pct': min(60, highly_proficient)
                    })

    return pd.DataFrame(aasa_data)


# ============================================================================
# ARIZONA STANDARDS DATA
# ============================================================================

def load_arizona_standards():
    """Load sample Arizona Academic Standards data."""
    standards = [
        # ELA Grade 3
        ("3.RF.3", "Grade 3", "ELA", "Reading Foundations", "Phonics",
         "Know and apply grade-level phonics and word analysis skills in decoding words."),
        ("3.RF.4", "Grade 3", "ELA", "Reading Foundations", "Fluency",
         "Read with sufficient accuracy and fluency to support comprehension."),
        ("3.RL.1", "Grade 3", "ELA", "Reading Literature", "Key Ideas",
         "Ask and answer questions to demonstrate understanding of a text, referring explicitly to the text."),
        ("3.RL.2", "Grade 3", "ELA", "Reading Literature", "Theme",
         "Recount stories and determine their central message, lesson, or moral."),
        ("3.W.1", "Grade 3", "ELA", "Writing", "Opinion",
         "Write opinion pieces on topics or texts, supporting a point of view with reasons."),

        # Math Grade 3
        ("3.OA.A.1", "Grade 3", "Math", "Operations", "Multiplication",
         "Interpret products of whole numbers, e.g., interpret 5 x 7 as the total number of objects in 5 groups of 7."),
        ("3.NF.A.1", "Grade 3", "Math", "Fractions", "Understanding",
         "Understand a fraction 1/b as the quantity formed by 1 part when a whole is partitioned into b equal parts."),
        ("3.MD.C.5", "Grade 3", "Math", "Measurement", "Area",
         "Recognize area as an attribute of plane figures and understand concepts of area measurement."),

        # ELA Grade 4
        ("4.RL.1", "Grade 4", "ELA", "Reading Literature", "Key Ideas",
         "Refer to details and examples in a text when explaining what the text says explicitly."),
        ("4.W.1", "Grade 4", "ELA", "Writing", "Opinion",
         "Write opinion pieces on topics or texts, supporting a point of view with reasons and information."),

        # Math Grade 4
        ("4.NBT.A.1", "Grade 4", "Math", "Number Operations", "Place Value",
         "Recognize that in a multi-digit whole number, a digit in one place represents ten times what it represents in the place to its right."),
        ("4.NF.A.1", "Grade 4", "Math", "Fractions", "Equivalence",
         "Explain why a fraction a/b is equivalent to a fraction (n x a)/(n x b) by using visual fraction models."),
    ]

    df = pd.DataFrame(standards, columns=[
        'standard_code', 'grade', 'subject', 'strand', 'standard', 'description'
    ])
    return df


# ============================================================================
# AUTHENTICATION
# ============================================================================

def check_password():
    st.session_state.authenticated = True
    return True


# ============================================================================
# TYPE 4 DETECTION
# ============================================================================

def compute_type4_analysis(azella_df, district_id, grade, year):
    """
    Compute Type 4 (oral-written delta) analysis for a district.
    Delta = Speaking Score - Writing Score
    Flag threshold: Delta > 0.6 points (on AZELLA 1-5 scale)
    """
    filtered = azella_df[
        (azella_df['district_id'] == district_id) &
        (azella_df['grade'] == grade) &
        (azella_df['year'] == year)
    ]

    if filtered.empty:
        return None

    row = filtered.iloc[0]

    speaking = row['speaking_avg']
    writing = row['writing_avg']
    delta = speaking - writing

    flagged = delta > 0.6

    return {
        'district_id': district_id,
        'district_name': row['district_name'],
        'grade': grade,
        'year': year,
        'speaking_avg': speaking,
        'writing_avg': writing,
        'delta': delta,
        'flagged': flagged,
        'total_tested': row['total_tested'],
        'estimated_flagged': int(row['total_tested'] * 0.18) if flagged else int(row['total_tested'] * 0.06)
    }


# ============================================================================
# DASHBOARD PAGES
# ============================================================================

def render_overview(districts_df, azella_df, aasa_df):
    """Render the overview dashboard."""
    st.header("Arizona Education Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Districts", len(districts_df))
    with col2:
        st.metric("Total Students", f"{districts_df['total_students'].sum():,}")
    with col3:
        st.metric("English Learners", f"{districts_df['ell_count'].sum():,}")
    with col4:
        avg_grad = districts_df['graduation_rate'].mean()
        st.metric("Avg Graduation Rate", f"{avg_grad:.1f}%")

    st.divider()

    st.subheader("Pilot Districts")

    display_df = districts_df.copy()
    display_df['ell_percent'] = display_df['ell_percent'].apply(lambda x: f"{x:.1f}%")
    display_df['graduation_rate'] = display_df['graduation_rate'].apply(lambda x: f"{x:.1f}%")
    display_df.columns = ['District ID', 'District Name', 'Total Students', 'EL Count', 'EL %', 'Grad Rate', 'Letter Grade']

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.subheader("English Learner Population by District")

    fig = px.bar(
        districts_df.sort_values('ell_count', ascending=True),
        x='ell_count',
        y='district_name',
        orientation='h',
        color='ell_percent',
        color_continuous_scale=[[0, '#ffffff'], [0.5, AZ_BLUE], [1, AZ_COPPER]],
        labels={'ell_count': 'English Learners', 'district_name': 'District', 'ell_percent': 'EL %'}
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def render_standards_browser(standards_df):
    """Render the Arizona Standards browser."""
    st.header("Arizona Academic Standards Browser")

    st.markdown("""
    **Arizona Academic Standards** define what students should know and be able to do
    at each grade level. Browse standards by grade, subject, and strand.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        grade_options = ["All Grades"] + sorted(standards_df['grade'].unique().tolist())
        selected_grade = st.selectbox("Grade Level", grade_options)

    with col2:
        subject_options = ["All Subjects"] + sorted(standards_df['subject'].unique().tolist())
        selected_subject = st.selectbox("Subject", subject_options)

    with col3:
        search_query = st.text_input("Search Standards", placeholder="e.g., 'fractions' or '3.RF'")

    filtered = standards_df.copy()
    if selected_grade != "All Grades":
        filtered = filtered[filtered['grade'] == selected_grade]
    if selected_subject != "All Subjects":
        filtered = filtered[filtered['subject'] == selected_subject]
    if search_query:
        mask = (
            filtered['standard_code'].str.contains(search_query, case=False, na=False) |
            filtered['description'].str.contains(search_query, case=False, na=False) |
            filtered['standard'].str.contains(search_query, case=False, na=False)
        )
        filtered = filtered[mask]

    st.divider()
    st.write(f"Showing {len(filtered)} standards")

    for _, row in filtered.iterrows():
        badge_color = AZ_BLUE if row['subject'] == 'ELA' else AZ_COPPER

        st.markdown(f"""
        <div style="padding: 12px; margin: 8px 0; border-left: 4px solid {badge_color}; background: #f9f9f9;">
            <span style="background: {badge_color}; color: white; padding: 2px 8px; font-size: 0.75rem; border-radius: 3px;">{row['subject']}</span>
            <span style="background: #666; color: white; padding: 2px 8px; font-size: 0.75rem; border-radius: 3px; margin-left: 5px;">{row['grade']}</span>
            <strong style="margin-left: 10px;">{row['standard_code']}</strong>
            <span style="margin-left: 10px; color: #666;">| {row['strand']} - {row['standard']}</span>
            <p style="margin: 8px 0 0 0; color: #333;">{row['description']}</p>
        </div>
        """, unsafe_allow_html=True)


def render_azella_analysis(azella_df, districts_df):
    """Render AZELLA assessment analysis."""
    st.header("AZELLA Analysis")

    st.markdown("""
    **AZELLA** (Arizona English Language Learner Assessment) measures English proficiency
    across four domains: Listening, Speaking, Reading, and Writing on a 1-5 scale.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        district = st.selectbox("Select District", options=districts_df['district_name'].tolist(), key="azella_district")

    with col2:
        grade = st.selectbox("Select Grade", options=list(range(3, 9)), key="azella_grade")

    with col3:
        year = st.selectbox("Select Year", options=[2025, 2024], key="azella_year")

    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]

    filtered = azella_df[
        (azella_df['district_id'] == district_id) &
        (azella_df['grade'] == grade) &
        (azella_df['year'] == year)
    ]

    if not filtered.empty:
        row = filtered.iloc[0]

        st.divider()

        st.subheader("AZELLA Domain Scores")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Listening", f"{row['listening_avg']:.2f}")
        with col2:
            st.metric("Speaking", f"{row['speaking_avg']:.2f}")
        with col3:
            st.metric("Reading", f"{row['reading_avg']:.2f}")
        with col4:
            st.metric("Writing", f"{row['writing_avg']:.2f}")

        domains = ['Listening', 'Speaking', 'Reading', 'Writing']
        scores = [row['listening_avg'], row['speaking_avg'], row['reading_avg'], row['writing_avg']]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=domains,
            y=scores,
            marker_color=[AZ_BLUE, AZ_COPPER, AZ_BLUE, AZ_COPPER],
            text=[f"{s:.2f}" for s in scores],
            textposition='outside'
        ))
        fig.update_layout(
            title=f"AZELLA Domain Scores - {district} - Grade {grade} ({year})",
            yaxis_title="Proficiency Level (1-5)",
            yaxis_range=[0, 5.5],
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        oral_avg = (row['listening_avg'] + row['speaking_avg']) / 2
        written_avg = (row['reading_avg'] + row['writing_avg']) / 2
        gap = oral_avg - written_avg

        st.subheader("Oral vs Written Gap")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Oral Average", f"{oral_avg:.2f}", help="(Listening + Speaking) / 2")
        with col2:
            st.metric("Written Average", f"{written_avg:.2f}", help="(Reading + Writing) / 2")
        with col3:
            delta_color = "normal" if gap < 0.4 else "inverse"
            st.metric("Gap", f"{gap:+.2f}", delta=f"{'Flag' if gap > 0.5 else 'OK'}", delta_color=delta_color)


def render_type4_detection(azella_df, districts_df):
    """Render Type 4 detection analysis."""
    st.header("Type 4 Detection")

    st.markdown("""
    **Type 4 dyslexia candidates** demonstrate strong oral communication but
    struggle with written expression. VERA-AZ identifies these students by
    analyzing the delta between AZELLA Speaking and Writing domain scores.

    **Flag Threshold:** Speaking - Writing delta > 0.6 points
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        district = st.selectbox("Select District", options=districts_df['district_name'].tolist(), key="type4_district")

    with col2:
        grade = st.selectbox("Select Grade", options=list(range(3, 9)), key="type4_grade")

    with col3:
        year = st.selectbox("Select Year", options=[2025, 2024], key="type4_year")

    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]

    result = compute_type4_analysis(azella_df, district_id, grade, year)

    if result:
        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Speaking Score", f"{result['speaking_avg']:.2f}")
        with col2:
            st.metric("Writing Score", f"{result['writing_avg']:.2f}")
        with col3:
            st.metric("Delta", f"{result['delta']:+.2f}")
        with col4:
            status = "FLAGGED" if result['flagged'] else "OK"
            st.metric("Status", status)

        st.subheader("Oral-Written Delta Analysis")

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Speaking',
            x=['Score'],
            y=[result['speaking_avg']],
            marker_color=AZ_COPPER,
            text=[f"{result['speaking_avg']:.2f}"],
            textposition='outside'
        ))

        fig.add_trace(go.Bar(
            name='Writing',
            x=['Score'],
            y=[result['writing_avg']],
            marker_color=AZ_BLUE,
            text=[f"{result['writing_avg']:.2f}"],
            textposition='outside'
        ))

        fig.update_layout(
            title=f"Speaking vs Writing - {district} - Grade {grade}",
            barmode='group',
            yaxis_range=[0, 5.5],
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)

        if result['flagged']:
            st.error(f"""
            **Type 4 Flag Triggered**

            This grade level shows a significant oral-written gap (delta: {result['delta']:+.2f}).

            - **Estimated students affected:** {result['estimated_flagged']} of {result['total_tested']} tested
            - **Recommended action:** Individual screening under Move On When Reading protocols
            - **HB 2170 Compliance:** Ensure IEPs indicate dyslexia diagnosis where applicable
            """)
        else:
            st.success(f"""
            **No Type 4 Flag**

            The oral-written gap for this grade level is within normal range (delta: {result['delta']:+.2f}).

            - **Students tested:** {result['total_tested']}
            - **Continue monitoring:** Regular AZELLA domain analysis recommended
            """)

        st.subheader(f"All Grades - {district} ({year})")

        all_grades_data = []
        for g in range(3, 9):
            r = compute_type4_analysis(azella_df, district_id, g, year)
            if r:
                all_grades_data.append(r)

        if all_grades_data:
            grades_df = pd.DataFrame(all_grades_data)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=grades_df['grade'],
                y=grades_df['speaking_avg'],
                name='Speaking',
                mode='lines+markers',
                line=dict(color=AZ_COPPER, width=3),
                marker=dict(size=10)
            ))
            fig.add_trace(go.Scatter(
                x=grades_df['grade'],
                y=grades_df['writing_avg'],
                name='Writing',
                mode='lines+markers',
                line=dict(color=AZ_BLUE, width=3),
                marker=dict(size=10)
            ))

            fig.update_layout(
                title="Speaking vs Writing Across Grades",
                xaxis_title="Grade",
                yaxis_title="Proficiency Level",
                yaxis_range=[0, 5.5],
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)


def render_aasa_analysis(aasa_df, districts_df):
    """Render AASA assessment analysis."""
    st.header("AASA Analysis")

    st.markdown("""
    **AASA** (Arizona's Academic Standards Assessment) measures student achievement
    in ELA and Mathematics for grades 3-8, aligned to Arizona Academic Standards.
    """)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        district = st.selectbox("Select District", options=districts_df['district_name'].tolist(), key="aasa_district")

    with col2:
        grade = st.selectbox("Select Grade", options=list(range(3, 9)), key="aasa_grade")

    with col3:
        subject = st.selectbox("Select Subject", options=['ELA', 'Math'], key="aasa_subject")

    with col4:
        year = st.selectbox("Select Year", options=[2025, 2024], key="aasa_year")

    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]

    filtered = aasa_df[
        (aasa_df['district_id'] == district_id) &
        (aasa_df['grade'] == grade) &
        (aasa_df['subject'] == subject) &
        (aasa_df['year'] == year)
    ]

    if not filtered.empty:
        row = filtered.iloc[0]

        st.divider()

        st.subheader("Achievement Level Distribution")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Proficient or Higher", f"{row['proficient_plus_pct']:.1f}%")
        with col2:
            st.metric("Highly Proficient", f"{row['highly_proficient_pct']:.1f}%")

        levels = ['Proficient+', 'Highly Proficient']
        values = [row['proficient_plus_pct'], row['highly_proficient_pct']]
        colors = [AZ_COPPER, AZ_BLUE]

        fig = go.Figure(data=[
            go.Bar(x=levels, y=values, marker_color=colors, text=[f"{v:.1f}%" for v in values], textposition='outside')
        ])
        fig.update_layout(
            title=f"AASA {subject} Performance - {district} - Grade {grade} ({year})",
            yaxis_title="Percentage",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)


def render_export(azella_df, aasa_df, districts_df):
    """Render data export page."""
    st.header("Export Data")

    st.markdown("Download assessment data for further analysis.")

    district = st.selectbox("Select District (or All)", options=["All Districts"] + districts_df['district_name'].tolist())

    year = st.selectbox("Select Year", options=[2025, 2024])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("AZELLA Data")
        if district == "All Districts":
            export_azella = azella_df[azella_df['year'] == year]
        else:
            district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]
            export_azella = azella_df[(azella_df['district_id'] == district_id) & (azella_df['year'] == year)]

        st.dataframe(export_azella, use_container_width=True, hide_index=True)

        csv_azella = export_azella.to_csv(index=False)
        st.download_button("Download AZELLA CSV", csv_azella, f"vera_az_azella_{year}.csv", "text/csv", use_container_width=True)

    with col2:
        st.subheader("AASA Data")
        if district == "All Districts":
            export_aasa = aasa_df[aasa_df['year'] == year]
        else:
            district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]
            export_aasa = aasa_df[(aasa_df['district_id'] == district_id) & (aasa_df['year'] == year)]

        st.dataframe(export_aasa, use_container_width=True, hide_index=True)

        csv_aasa = export_aasa.to_csv(index=False)
        st.download_button("Download AASA CSV", csv_aasa, f"vera_az_aasa_{year}.csv", "text/csv", use_container_width=True)


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.set_page_config(
        page_title="VERA-AZ | Arizona Type 4 Detection & AZELLA Analysis",
        page_icon="🌵",
        layout="wide"
    )

    st.markdown(f"""
    <style>
        .stApp {{
            background-color: #fafafa;
        }}
        .block-container {{
            padding-top: 2rem;
        }}
        h1, h2, h3 {{
            color: {AZ_BLUE};
        }}
        .stButton > button {{
            background-color: {AZ_BLUE};
            color: white;
        }}
        .stButton > button:hover {{
            background-color: {AZ_COPPER};
            color: white;
        }}
    </style>
    """, unsafe_allow_html=True)

    if not check_password():
        return

    districts_df = load_districts()
    azella_df = load_azella_data()
    aasa_df = load_aasa_data()
    standards_df = load_arizona_standards()

    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: {AZ_BLUE}; margin: 0;">VERA-AZ</h2>
        <p style="color: #666; font-size: 0.85rem; margin-top: 5px;">Arizona Implementation</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        ["Overview", "Standards Browser", "AZELLA Analysis", "Type 4 Detection", "AASA Analysis", "Export Data"]
    )

    st.sidebar.divider()

    st.sidebar.markdown("""
    **Data Sources:**
    - Arizona Academic Standards
    - AASA (Academic Assessment)
    - AZELLA (ELL Assessment)
    - ADE Accountability

    **Type 4 Detection:**
    - Speaking vs Writing delta
    - Flag threshold: > 0.6 points

    **Legislation:**
    - HB 2170 "Say Dyslexia"
    - Move On When Reading

    ---

    [H-EDU.Solutions](https://h-edu.solutions)
    """)

    if page == "Overview":
        render_overview(districts_df, azella_df, aasa_df)
    elif page == "Standards Browser":
        render_standards_browser(standards_df)
    elif page == "AZELLA Analysis":
        render_azella_analysis(azella_df, districts_df)
    elif page == "Type 4 Detection":
        render_type4_detection(azella_df, districts_df)
    elif page == "AASA Analysis":
        render_aasa_analysis(aasa_df, districts_df)
    elif page == "Export Data":
        render_export(azella_df, aasa_df, districts_df)


if __name__ == "__main__":
    main()
