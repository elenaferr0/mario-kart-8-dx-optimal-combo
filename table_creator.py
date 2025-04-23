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


def create_pareto_optimal_markdown_table(data):
    markdown = "# Mario Kart 8 Deluxe - Pareto Dominance\n\n"
    for category, items in data.items():
        # Format the category name for the header
        category_name = category.replace("_", " ").title()
        markdown += f"## {category_name}\n\n"
        markdown += "| Status    | Solution |\n"
        markdown += "|-----------|----------|\n"

        # Add Dominated solutions in separate rows
        if "dominated" in items and items["dominated"]:
            markdown += "| **Dominated** | |\n"
            for item in items["dominated"]:
                names = [name.strip() for name in item["name"].split(",")]
                urls_list = [url.strip() for url in item["url"].split(",")]
                # Ensure we have the same number of names and URLs (handle potential mismatches)
                num_solutions = max(len(names), len(urls_list))
                for i in range(num_solutions):
                    name = names[i] if i < len(names) else ""
                    url = urls_list[i] if i < len(urls_list) else ""
                    img_tag = f'<img src="{url}" alt="{name}" style="height: 30px; border-radius: 5px; padding: 2px;">' if url else ""
                    markdown += f"| | {name} {img_tag} |\n"

        # Add Optimal solutions in separate rows
        if "optimal" in items and items["optimal"]:
            markdown += "| **Optimal** | |\n"
            for item in items["optimal"]:
                names = [name.strip() for name in item["name"].split(",")]
                urls_list = [url.strip() for url in item["url"].split(",")]
                # Ensure we have the same number of names and URLs
                num_solutions = max(len(names), len(urls_list))
                for i in range(num_solutions):
                    name = names[i] if i < len(names) else ""
                    url = urls_list[i] if i < len(urls_list) else ""
                    img_tag = f'<img src="{url}" alt="{name}" style="height: 30px; border-radius: 5px; padding: 2px;">' if url else ""
                    markdown += f"| | {name} {img_tag} |\n"

        markdown += "\n"

    return markdown


with open('results/solutions.json', 'r') as file:
    solutions_data = json.load(file)
markdown_table = create_markdown_table(solutions_data)
with open('results/OPTIMIZATION.md', 'w') as file:
    file.write(markdown_table)
print("Markdown table has been generated and saved to 'OPTIMIZATION.md'.")

with open('results/pareto_optimal.json', 'r') as file:
    pareto_data = json.load(file)
markdown_pareto_table = create_pareto_optimal_markdown_table(pareto_data)
with open('results/PARETO.md', 'w') as file:
    file.write(markdown_pareto_table)
print("Pareto optimal markdown table has been generated and saved to 'PARETO.md'.")
