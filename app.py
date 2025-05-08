import streamlit as st
import openai
import pandas as pd
import json
import os

st.set_page_config(page_title="DPDPA Compliance Checker", layout="wide")
st.title("📜 DPDPA Compliance Checker")

# --- API Key from Secrets ---
api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=api_key)

# --- Hardcoded Chapter and Policy Texts ---
dpdpa_chapter_text = """
CHAPTER II
OBLIGATIONS OF DATA FIDUCIARY

Section 4. Grounds for processing personal data.
Sub-section (1) of Section 4. -  A person may process the personal data of a Data Principal only in accordance with the provisions of this Act and for a lawful purpose—
  (a) for which the Data Principal has given her consent; or
  (b) for certain legitimate uses.

Sub-section (2) of Section 4. -  For the purposes of this section, the expression “lawful purpose” means any purpose which is not expressly forbidden by law.

Section 5. Notice.
Sub-section (1) of Section 5. - Every request made to a Data Principal under section 6 for consent shall be accompanied or preceded by a notice given by the Data Fiduciary to the Data Principal, informing her—
  (i) the personal data and the purpose for which the same is proposed to be processed;
  (ii) the manner in which she may exercise her rights under sub-section (4) of section 6 and section 13; and
  (iii) the manner in which the Data Principal may make a complaint to the Board, in such manner and as may be prescribed.

Sub-section (2) of Section 5. - Where a Data Principal has given her consent for processing personal data before the commencement of this Act—
  (a) the Data Fiduciary shall, as soon as reasonably practicable, give the Data Principal a notice with the above information;
  (b) the Data Fiduciary may continue processing unless the Data Principal withdraws her consent.

Sub-section (3) of Section 5. - The Data Fiduciary shall provide the notice in English or any language under the Eighth Schedule of the Constitution.

Section 6. Consent.
Sub-section (1) of Section 6. - Consent shall be free, specific, informed, unconditional, unambiguous, and signify agreement by clear affirmative action, limited to necessary personal data for the specified purpose.

Sub-section (2) of Section 6. - Any infringing part of consent shall be invalid to the extent of infringement.

Sub-section (3) of Section 6. - Every consent request must be in clear and plain language, accessible in English or Eighth Schedule languages, with Data Protection Officer contact where applicable.

Sub-section (4) of Section 6. - Data Principals can withdraw consent anytime, with ease comparable to giving consent.

Sub-section (5) of Section 6. - Withdrawal consequences must be borne by the Data Principal and do not affect prior lawful processing.

Sub-section (6) of Section 6. - After withdrawal, Data Fiduciaries and Processors must cease processing unless otherwise required by law.

Sub-section (7) of Section 6. - Consent can be managed through a Consent Manager registered with the Board.

Sub-section (8) of Section 6. - Consent Managers act on behalf of Data Principals and are accountable to them.

Sub-section (9) of Section 6. - Consent Managers must be registered as prescribed.

Sub-section (10) of Section 6. - Data Fiduciary must prove that notice was given and consent was valid, if challenged.

Section 7. Certain legitimate uses.
Personal data may be processed without consent for:
  (a) Voluntarily provided personal data for specified purposes without expressed objection.
  (b) Subsidy, benefit, certificate, etc., provided by the State.
  (c) Performance of State functions or in the interest of sovereignty, integrity, or security.
  (d) Legal obligations to disclose information.
  (e) Compliance with court orders or judgments.
  (f) Medical emergencies.
  (g) Public health emergencies.
  (h) Disaster situations.
  (i) Employment purposes like corporate espionage prevention.

Section 8. General obligations of Data Fiduciary.
Sub-section (1) of Section 8. - Data Fiduciary is responsible for compliance regardless of agreements with Processors.

Sub-section (2) of Section 8. - Data Fiduciary may engage Processors only under valid contracts.

Sub-section (3) of Section 8. - If personal data is used for decisions affecting Data Principals or disclosed, ensure completeness, accuracy, and consistency.

Sub-section (4) of Section 8. - Implement technical and organisational measures to ensure compliance.

Sub-section (5) of Section 8. - Protect personal data using reasonable security safeguards against breaches.

Sub-section (6) of Section 8. - Notify the Board and affected Data Principals in case of breaches, as prescribed.

Sub-section (7) of Section 8. - Erase personal data upon withdrawal of consent or when the specified purpose is no longer served, unless legally required to retain.

Sub-section (8) of Section 8. - "Specified purpose no longer served" deemed if Data Principal does not approach the Fiduciary within prescribed time.

Sub-section (9) of Section 8. - Publish business contact info of DPO or designated grievance redressal officer.

Sub-section (10) of Section 8. - Establish an effective grievance redressal mechanism.

Sub-section (11) of Section 8. - Clarification: lack of contact by Data Principal within time period implies specified purpose is no longer served.

Section 9. Processing of personal data of children.
Sub-section (1) of Section 9. - Before processing, obtain verifiable parental or guardian consent.

Sub-section (2) of Section 9. - No detrimental processing that harms the child's well-being.

Sub-section (3) of Section 9. - No tracking, behavioural monitoring, or targeted advertising to children.

Sub-section (4) of Section 9. - Exemptions may be prescribed for certain Data Fiduciaries or purposes.

Sub-section (5) of Section 9. - Safe processing standards may allow higher age exemptions.

Section 10. Additional obligations of Significant Data Fiduciaries.
Sub-section (1) of Section 10. - Significant Data Fiduciaries notified by Government based on volume, sensitivity, sovereignty impact, etc.

Sub-section (2) of Section 10. - Must:
  (a) Appoint a Data Protection Officer (DPO) based in India, responsible to the Board.
  (b) Appoint an independent Data Auditor.
  (c) Undertake:
    (i) Periodic Data Protection Impact Assessments,
    (ii) Periodic audits,
    (iii) Other prescribed compliance measures.
"""

privacy_policy_text = """
Information we collect
We collect information to provide better services to all of our users – from figuring out basic stuff like which language you speak,
to more complex things like which ads you’ll find most useful, the people who matter most to you online, or which
YouTube videos you might like.
We collect information in the following ways:
Information you give us. For example, many of our services require you to sign up for a Google Account. When you
do, we’ll ask for personal information, like your name, email address, telephone number or credit card to store with your
account. If you want to take full advantage of the sharing features we offer, we might also ask you to create a publicly
visible Google Profile, which may include your name and photo.
Information we get from your use of our services. We collect information about the services that you use and how
you use them, like when you watch a video on YouTube, visit a website that uses our advertising services, or view and
interact with our ads and content. This information includes:
Device information
We collect device-specific information (such as your hardware model, operating system version, unique device
identifiers, and mobile network information including phone number). Google may associate your device
identifiers or phone number with your Google Account.
Log information
When you use our services or view content provided by Google, we automatically collect and store certain
information in server logs. This includes:
details of how you used our service, such as your search queries.
telephony log information like your phone number, calling-party number, forwarding numbers, time and
date of calls, duration of calls, SMS routing information and types of calls.
Internet protocol address.
device event information such as crashes, system activity, hardware settings, browser type, browser
language, the date and time of your request and referral URL.
cookies that may uniquely identify your browser or your Google Account.
Location information
When you use Google services, we may collect and process information about your actual location. We use
various technologies to determine location, including IP address, GPS, and other sensors that may, for
example, provide Google with information on nearby devices, Wi-Fi access points and cell towers.
Unique application numbers
Certain services include a unique application number. This number and information about your installation (for
example, the operating system type and application version number) may be sent to Google when you install or
uninstall that service or when that service periodically contacts our servers, such as for automatic updates.
Local storage
We may collect and store information (including personal information) locally on your device using mechanisms
such as browser web storage (including HTML 5) and application data caches.
Cookies and similar technologies
We and our partners use various technologies to collect and store information when you visit a Google service,
and this may include using cookies or similar technologies to identify your browser or device. We also use these
technologies to collect and store information when you interact with services we offer to our partners, such as
advertising services or Google features that may appear on other sites. Our Google Analytics product helps
businesses and site owners analyze the traffic to their websites and apps. When used in conjunction with our
advertising services, such as those using the DoubleClick cookie, Google Analytics information is linked, by the
Google Analytics customer or by Google, using Google technology, with information about visits to
multiple sites.
Information we collect when you are signed in to Google, in addition to information we obtain about you from partners, may be
associated with your Google Account. When information is associated with your Google Account, we treat it as personal
information. For more information about how you can access, manage or delete information that is associated with your Google
Account, visit the Transparency and choice section of this policy.
How we use information we collect
We use the information we collect from all of our services to provide, maintain, protect and improve them, to develop new
ones, and to protect Google and our users. We also use this information to offer you tailored content – like giving you more
relevant search results and ads.
We may use the name you provide for your Google Profile across all of the services we offer that require a Google Account. In
addition, we may replace past names associated with your Google Account so that you are represented consistently across all
our services. If other users already have your email, or other information that identifies you, we may show them your publicly
visible Google Profile information, such as your name and photo.
If you have a Google Account, we may display your Profile name, Profile photo, and actions you take on Google or on third-
party applications connected to your Google Account (such as +1’s, reviews you write and comments you post) in our services,
including displaying in ads and other commercial contexts. We will respect the choices you make to limit sharing or visibility
settings in your Google Account.
When you contact Google, we keep a record of your communication to help solve any issues you might be facing. We may use
your email address to inform you about our services, such as letting you know about upcoming changes or improvements.
We use information collected from cookies and other technologies, like pixel tags, to improve your user experience and the
overall quality of our services. One of the products we use to do this on our own services is Google Analytics. For example, by
saving your language preferences, we’ll be able to have our services appear in the language you prefer. When showing you
tailored ads, we will not associate an identifier from cookies or similar technologies with sensitive categories, such as those
based on race, religion, sexual orientation or health.
Our automated systems analyze your content (including emails) to provide you personally relevant product features, such as
customized search results, tailored advertising, and spam and malware detection.
We may combine personal information from one service with information, including personal information, from other
Google services – for example to make it easier to share things with people you know. Depending on your account
settings, your activity on other sites and apps may be associated with your personal information in order to improve Google’s
services and the ads delivered by Google.
We will ask for your consent before using information for a purpose other than those that are set out in this Privacy Policy.
Google processes personal information on our servers in many countries around the world. We may process your personal
information on a server located outside the country where you live.
"""

# --- DPDPA Sections ---
dpdpa_sections = [
    "Section 4 — Grounds for Processing Personal Data",
    "Section 5 — Notice",
    "Section 6 — Consent",
    "Section 7 — Certain Legitimate Uses",
    "Section 8 — General Obligations of Data Fiduciary",
    "Section 9 — Processing of Personal Data of Children",
    "Section 10 — Additional Obligations of Significant Data Fiduciaries"
]

# --- GPT Function ---
def analyze_section(section_text, policy_text, full_chapter_text):
    prompt = f"""
You are a DPDPA compliance expert. Your task is to assess whether an organization's policy complies with the Digital Personal Data Protection Act, 2023 (India) — specifically Sections 4 to 10 under Chapter II. 

You must **read each sentence in the policy** and compare it with the legal **checklist of obligations derived from the assigned DPDPA Section**.

==========================================================
ORGANIZATION POLICY:
\"\"\"{policy_text}\"\"\"

DPDPA SECTION UNDER REVIEW:
\"\"\"{section_text}\"\"\"

==========================================================
INSTRUCTIONS:

1. **Understand the Law in Simple Terms**
   - Read the DPDPA Section carefully and explain it in your own words in simple, layman-friendly language.
   - Capture *every important legal requirement* from the section.

2. **Checklist Mapping**
   - Refer to the official checklist of obligations provided for this section.
   - For each checklist item do following- 
      - Go through the policy *sentence by sentence* and see if that sentence addresses the checklist item.
      - **Only count an item as covered if it is explicitly and clearly mentioned in the policy with correct context. Vague, generic, or partial references must be marked as unmatched. Do not assume implied meaning — legal clarity is required.**
      - Do not make assumptions.
      - This needs to be shown in the output - "Checklist Items" - In this -  mention the checklist item, whether it matches or not, the sentence/s from policy to which this checklist item matches and what is the justification for it getting matched.

3. **Classification**
   - Match Level:
     - "Fully Compliant": All checklist items are covered clearly.
     - "Partially Compliant": At least one item is missing or only vaguely mentioned.
     - "Non-Compliant": No checklist item is covered.
   - Severity (only for Partially Compliant):
     - Minor = 1 missing item
     - Medium = 2–3 missing items
     - Major = 4 or more missing / any critical clause missing
   - Compliance Points:
     - Fully Compliant = 1.0
     - Partially Compliant:
        - Minor = 0.75
        - Medium = 0.5
        - Major = 0.25
     - Non-Compliant = 0.0

4. **Suggested Rewrite**
   - This is an extremely important step so do this properly. For the section do the following points - 
      - Review the **checklist** for this section again and identify which items are **missing** from the policy.
      - For each missing item, write **1 sentence** that can be added to the policy to ensure compliance.
      - The rewrite should be a clear, implementable policy statement for each missing item.
==========================================================
OUTPUT FORMAT (strict JSON):
{{
  "DPDPA Section": "...",
  "DPDPA Section Meaning": "...",
  "Checklist Items": [
    {{
      "Item": "...",
      "Matched": true/false,
      "Matched Sentences": ["...", "..."],
      "Justification": "..."
    }},
    ...
  ],
  "Match Level": "...",
  "Severity": "...",
  "Compliance Points": "...",
  "Suggested Rewrite": "..."
}}

==========================================================
CHECKLIST TO USE:


**Section 4: Grounds for Processing Personal Data**

1. ☐ Personal data is processed **only** for lawful purposes.
2. ☐ Lawful purpose must be:

   * ☐ Backed by **explicit consent** from the Data Principal **OR**
   * ☐ Falls under **legitimate uses** as per Section 7.
3. ☐ Lawful purpose must **not be expressly forbidden** by any law.

**Section 5: Notice Before Consent**

1. ☐ Notice is provided **before or at the time** of requesting consent.
2. Notice must clearly mention:

   * ☐ What **personal data** is being collected.
   * ☐ The **purpose** of processing.
   * ☐ How to **exercise rights** under Section 6(4) and Section 13.
   * ☐ How to **lodge complaints** with the Board.
3. ☐ For existing data collected **before DPDPA**, retrospective notice must also be issued as soon as practicable with all points above.

**Section 6: Consent and Its Management**

1. ☐ Consent is **free, specific, informed, unconditional, and unambiguous**.
2. ☐ Consent is **given via clear affirmative action**.
3. ☐ Consent is **limited to specified purpose only**.
4. ☐ Consent can be **withdrawn** at any time.
5. ☐ Data Fiduciary shall **cease processing** upon withdrawal (unless legally required).
6. ☐ Consent Manager is available (if applicable):

   * ☐ Consent Manager is **registered** and functions independently.
   * ☐ Consent Manager allows:

     * ☐ Giving, managing, and withdrawing consent easily.
     * ☐ Logs consent history for audit.
7. ☐ Data Fiduciary must honor withdrawal requests promptly.
8. ☐ Retention of personal data stops unless required by law.

**Section 7: Legitimate Uses (No Consent Needed)**

Processing without consent is allowed **only** if it meets the following (tick applicable):

* ☐ For specified government subsidies/services/licenses.
* ☐ For State functions (e.g., national security, law enforcement).
* ☐ To comply with legal obligations.
* ☐ Under court orders or judgments.
* ☐ For medical emergencies or disasters.
* ☐ For employment-related purposes with safeguards.
* ☐ For corporate security or internal fraud prevention.
  Each use must:

  * ☐ Be **necessary** and **proportionate**.
  * ☐ Adhere to standards/rules to be prescribed.

**Section 8: General Obligations of Data Fiduciary**

1. ☐ Fiduciary is fully accountable for processing by itself or its Data Processor.
2. ☐ Processing must be under a valid **contract** with the Data Processor.
3. ☐ If data is to:

   * ☐ Influence decisions or
   * ☐ Be shared with other Fiduciaries,
     → Then data must be:

     * ☐ Complete
     * ☐ Accurate
     * ☐ Consistent
4. ☐ Implement **technical and organisational measures** for compliance.
5. ☐ Take **reasonable security safeguards** to prevent breaches.
6. ☐ Report data breaches to:

   * ☐ Data Protection Board
   * ☐ Affected Data Principals
7. ☐ Erase data when:

   * ☐ Consent is withdrawn, OR
   * ☐ Purpose is no longer being served
   * ☐ Also instruct Data Processor to erase it.
8. ☐ Define time periods for retention based on inactivity of Data Principal.
9. ☐ Publish business contact info of DPO or responsible officer.
10. ☐ Establish a grievance redressal mechanism.

**Section 9: Processing Children’s Data**

1. ☐ Verifiable **parental/guardian consent** is obtained before processing data of:

   * ☐ Children (<18 years)
   * ☐ Persons with lawful guardians
2. ☐ No processing that causes **detrimental effect** to child’s well-being.
3. ☐ No **tracking, behavioral monitoring**, or **targeted advertising** directed at children.
4. ☐ Follow any **exemptions** as notified (for class of fiduciaries or safe processing).
5. ☐ Central Govt. may relax obligations if processing is **verifiably safe** and meets minimum age threshold.

**Section 10: Significant Data Fiduciary (SDF) Obligations**

Only applies if declared as SDF:

1. ☐ Appoint a **Data Protection Officer (DPO)**:

   * ☐ Based in India
   * ☐ Reports to board/similar authority
   * ☐ Point of contact for grievance redressal
2. ☐ Appoint an **independent Data Auditor**.
3. ☐ Conduct:

   * ☐ Periodic **Data Protection Impact Assessments**
   * ☐ **Audits** of data processing
   * ☐ Any other measures as may be prescribed
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content

# --- Execution ---
if st.button("🚀 Run Compliance Check"):
    results = []
    with st.spinner("Analyzing each DPDPA section..."):
        for section in dpdpa_sections:
            try:
                section_response = analyze_section(section, privacy_policy_text, dpdpa_chapter_text)
                parsed_section = json.loads(section_response)
                results.append(parsed_section)
            except Exception as e:
                st.error(f"❌ Error analyzing {section}: {e}")

    if results:
        df = pd.DataFrame(results)
        st.success("✅ Analysis Completed!")
        st.dataframe(df)

        # Download button
        excel_filename = "DPDPA_Compliance_SectionWise_Final.xlsx"
        df.to_excel(excel_filename, index=False)
        with open(excel_filename, "rb") as f:
            st.download_button("📥 Download Excel", f, file_name=excel_filename)

        # Compliance Score
        try:
            scored_points = df['Compliance Points'].astype(float).sum()
            total_points = len(dpdpa_sections) * 1.0
            score = (scored_points / total_points) * 100
            st.metric("🎯 Compliance Score", f"{score:.2f}%")
        except:
            st.warning("⚠️ Could not compute score. Check data types.")