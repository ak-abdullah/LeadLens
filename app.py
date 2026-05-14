import gradio as gr
from agent import run_agent

def research_company(company_name):
    if not company_name.strip():
        return "Please enter a company name."
    result = run_agent(company_name)
    return result

app = gr.Interface(
    fn=research_company,
    inputs=gr.Textbox(
        placeholder="Enter company name e.g. Stripe, Notion, Vercel",
        label="Company Name"
    ),
    outputs=gr.Textbox(
        label="Generated Outreach Message",
        lines=10
    ),
    title="LeadLens 🔍",
    description="Enter a company name. LeadLens researches them and writes a personalized outreach message.",
)

if __name__ == "__main__":
    app.launch()