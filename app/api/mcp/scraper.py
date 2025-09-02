
import requests
from bs4 import BeautifulSoup
import json

def scrape_course_data():
    base_url = "https://courses.sci.pitt.edu"
    courses_url = f"{base_url}/courses"

    response = requests.get(courses_url)
    soup = BeautifulSoup(response.content, "html.parser")

    course_links = []
    for tab_pane in soup.find_all("div", class_="tab-pane"):
        for course_link in tab_pane.find_all("a"):
            course_links.append(base_url + course_link["href"])

    all_courses_data = []
    for course_link in course_links:
        course_response = requests.get(course_link)
        course_soup = BeautifulSoup(course_response.content, "html.parser")

        course_data = {}

        # Course Name and Number
        h1_tag = course_soup.find("h1")
        if h1_tag:
            course_data["title"] = h1_tag.text.strip()

        # Description
        description_p = h1_tag.find_next_sibling("p")
        if description_p:
            course_data["description"] = description_p.text.strip()

        # Other details
        details_p = course_soup.find("p", recursive=False)
        if details_p:
            for span in details_p.find_all("span", style="font-weight:bold"):
                key = span.text.strip().replace(":", "").lower().replace(" ", "_")
                value = span.next_sibling.strip()
                course_data[key] = value
        
        # Sections
        course_data["sections"] = []
        sections_h2 = course_soup.find("h2", text="Current Sections")
        if sections_h2:
            for course_div in sections_h2.find_next_siblings("div", class_="course"):
                term_h3 = course_div.find("h3")
                if term_h3:
                    term = term_h3.text.strip()
                    table = course_div.find("table")
                    if table:
                        headers = [header.text.strip() for header in table.find_all("th")]
                        for row in table.find("tbody").find_all("tr"):
                            section_data = {"term": term}
                            cells = row.find_all("td")
                            for i, cell in enumerate(cells):
                                header_name = headers[i].lower().replace(" ", "_").replace(".","")
                                section_data[header_name] = cell.text.strip()
                            course_data["sections"].append(section_data)

        all_courses_data.append(course_data)

    return all_courses_data

if __name__ == "__main__":
    course_data = scrape_course_data()
    with open("course_data.json", "w") as f:
        json.dump(course_data, f, indent=4)
