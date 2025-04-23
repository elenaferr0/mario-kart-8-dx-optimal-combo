import json
import re

def create_markdown_table(data):
    markdown = "# Mario Kart 8 Deluxe - Optimal Combinations\n\n"

    for category, items in data.items():
        # Format the category name for the header
        category_name = category.replace("_", " ").title()
        
        # Get the number of solutions for each component
        driver_solutions = items["driver"]["solution"].split(",")
        body_solutions = items["body"]["solution"].split(",")
        tire_solutions = items["tire"]["solution"].split(",")
        glider_solutions = items["glider"]["solution"].split(",")
        
        # Get the URLs for each component
        driver_urls = items["driver"]["url"].split(",")
        body_urls = items["body"]["url"].split(",")
        tire_urls = items["tire"]["url"].split(",")
        glider_urls = items["glider"]["url"].split(",")
        
        # Create the header row with colspan
        markdown += f"## {category_name}\n\n"
        markdown += "| Component | Solution |\n"
        markdown += "|-----------|----------|\n"
        
        # Create rows for each driver
        markdown += "| **Driver** | |\n"
        for i, driver in enumerate(driver_solutions):
            driver = driver.strip()
            url = driver_urls[i].strip()
            markdown += f"| | {driver} <img src=\"{url}\" alt=\"{driver}\" style=\"height: 30px; border-radius: 5px; padding: 2px;\"> |\n"
        
        # Create rows for each body
        markdown += "| **Body** | |\n"
        for i, body in enumerate(body_solutions):
            body = body.strip()
            url = body_urls[i].strip()
            markdown += f"| | {body} <img src=\"{url}\" alt=\"{body}\" style=\"height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;\"> |\n"
        
        # Create rows for each tire
        markdown += "| **Tire** | |\n"
        for i, tire in enumerate(tire_solutions):
            tire = tire.strip()
            url = tire_urls[i].strip()
            markdown += f"| | {tire} <img src=\"{url}\" alt=\"{tire}\" style=\"height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;\"> |\n"
        
        # Create rows for each glider
        markdown += "| **Glider** | |\n"
        for i, glider in enumerate(glider_solutions):
            glider = glider.strip()
            url = glider_urls[i].strip()
            markdown += f"| | {glider} <img src=\"{url}\" alt=\"{glider}\" style=\"height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;\"> |\n"
        
        markdown += "\n\n"
    
    return markdown

# Read and parse the JSON data
with open('outputs/solutions.json', 'r') as file:
    json_data = json.load(file)

# Generate the markdown table
markdown_table = create_markdown_table(json_data)

# Write the markdown to a file
with open('outputs/RESULTS.md', 'w') as file:
    file.write(markdown_table)

print("Markdown table has been generated and saved to 'RESULTS.md'")
