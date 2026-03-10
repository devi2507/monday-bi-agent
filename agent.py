from groq import Groq

# Initialize Groq client
client = Groq(api_key="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")


# --------------------------------------------------
# Leadership Update Generator
# --------------------------------------------------

def generate_leadership_update(work_df, deals_df):

    total_work_orders = len(work_df)
    total_deals = len(deals_df)

    completed = 0
    not_started = 0

    if "Execution Status" in work_df.columns:
        completed = work_df[work_df["Execution Status"] == "Completed"].shape[0]
        not_started = work_df[work_df["Execution Status"] == "Not Started"].shape[0]

    completion_rate = 0
    if total_work_orders > 0:
        completion_rate = round((completed / total_work_orders) * 100, 2)

    update = f"""
### Leadership Update

**Operations**
• Total Work Orders: {total_work_orders}  
• Completed: {completed}  
• Not Started: {not_started}  
• Completion Rate: {completion_rate}%

**Sales Pipeline**
• Total Deals: {total_deals}

**Key Insights**
• Operations completion rate is {completion_rate}%.
• Pipeline size suggests current sales momentum.

**Recommendations**
• Prioritize incomplete projects.
• Monitor deal pipeline conversion.
"""

    return update


# --------------------------------------------------
# Main Agent
# --------------------------------------------------

def ask_agent(question, deals_df, work_df):

    question_lower = question.lower()

    # ---------------------------------------------
    # Leadership Update Shortcut
    # ---------------------------------------------
    if "leadership update" in question_lower or "leadership summary" in question_lower:
        return generate_leadership_update(work_df, deals_df)

    # ---------------------------------------------
    # Data Quality Detection
    # ---------------------------------------------
    missing_values = (deals_df == "Unknown").sum().sum() + (work_df == "Unknown").sum().sum()

    # ---------------------------------------------
    # Create summarized context (reduce token usage)
    # ---------------------------------------------
    context = f"""
Business Data Summary

Deals Board:
Total Deals: {len(deals_df)}

Work Orders Board:
Total Work Orders: {len(work_df)}

Sample Deals Data:
{deals_df.head(3).to_string()}

Sample Work Orders Data:
{work_df.head(3).to_string()}
"""

    # ---------------------------------------------
    # AI Prompt
    # ---------------------------------------------
    prompt = f"""
You are an AI Business Intelligence assistant helping founders understand their company data.

Instructions:
- Provide concise, clear answers.
- Focus on business insights rather than raw numbers.
- If the question refers to a field not present in the dataset, ask a clarifying question.
- Mention limitations if the dataset appears incomplete.
- Keep answers short and structured.

Data Context:
{context}

User Question:
{question}

Data Quality:
There are approximately {missing_values} missing or unknown values in the dataset.

Respond with short, clear insights.
"""

    # ---------------------------------------------
    # Call Groq Model
    # ---------------------------------------------
    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        return "⚠️ Unable to generate response due to API error. Please try again."