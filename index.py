from flask import Flask, request, render_template_string
from openai import OpenAI
import requests
from readability import Document

client = OpenAI()

app = Flask(__name__)


# Function to get summary of URL content using OpenAI API
def get_url_summary(url):
    # Fetch the content of the URL
    response = requests.get(url)
    content = response.text

    # Use readability library to get the main content of the webpage
    doc = Document(content)
    main_content = doc.summary()

    # Use OpenAI API to get the summary
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {
                "role": "user",
                "content": f"Please sum up the content of this URL and give 10 takeways : {main_content}, add 2 BR balise after summary and one  between each takeways",
            },
        ],
    )
    summary = completion.choices[0].message.content
    return summary


@app.route("/")
def index():
    url = request.args.get("url", "")
    summary = get_url_summary(url) if url else "No URL provided"
    html_content = f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>URL Display</title>
        <style>
          body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #000;
            color: #fff;
          }}
          .container {{
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #333;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
          }}
          h1, h2 {{
            color: #fff;
          }}
          p {{
            color: #ccc;
          }}
          a {{
            color: #1e90ff;
            text-decoration: none;
          }}
          a:hover {{
            text-decoration: underline;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h1>URL Display</h1>
          <p>The URL you provided is: <a href="{url}">{url}</a></p>
          <h2>Summary</h2>
          <p>{summary}</p>
        </div>
      </body>
    </html>
    """
    return render_template_string(html_content)


if __name__ == "__main__":
    app.run(debug=True)
