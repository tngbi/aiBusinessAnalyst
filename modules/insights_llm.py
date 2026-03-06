
from openai import OpenAI

client = OpenAI()

def generate_insights(kpis):

    prompt = f'''
    Analyze the following business KPIs and produce insights:

    {kpis}
    '''

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text
