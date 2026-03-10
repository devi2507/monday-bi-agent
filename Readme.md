# Monday.com Business Intelligence Agent

An AI-powered Business Intelligence Agent that allows founders and executives to ask natural language questions about their business data stored in monday.com boards.

The agent integrates with monday.com Work Orders and Deals boards, cleans messy real-world data, and provides meaningful insights about pipeline health, operational performance, and project execution.

---

# Features

## 1. Monday.com Integration
The system connects directly to monday.com using the monday GraphQL API.

It dynamically fetches data from:
- Work Orders board
- Deals board

No CSV data is hardcoded in the system.

---

## 2. Conversational AI Interface
Users interact with the system through a conversational chatbot built using Streamlit.

The chatbot allows founders to ask questions such as:

- How many projects are completed?
- What does our current pipeline look like?
- Are there projects not started yet?
- Prepare a leadership update

---

## 3. Data Resilience

Real-world business data is messy. The system handles:

- Missing values
- Duplicate records
- Inconsistent date formats
- Irregular text formatting

The `data_cleaning.py` module normalizes and prepares the data before analysis.

---

## 4. Business Intelligence Insights

The AI agent generates insights including:

- Operational performance
- Pipeline health
- Completion rates
- Work order status
- Leadership summaries

The system combines both Work Orders and Deals data to produce meaningful business insights rather than just raw numbers.

---

## 5. Leadership Updates

The agent can generate leadership summaries suitable for executive reporting.

Example query:

