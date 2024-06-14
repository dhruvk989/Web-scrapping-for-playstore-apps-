from bs4 import BeautifulSoup
import pandas as pd
import os

def extract_reviews_to_excel(html_file_paths, output_folder):
    for html_file_path in html_file_paths:
        # Read the HTML file
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all review entries
        review_entries = soup.find_all('tr')[1:]  # skipping the header row

        # Function to extract rating
        def extract_rating(rating_td):
            # Count the number of <i> tags with class 'fa-star' to determine the rating
            return len(rating_td.find_all('i', class_='fa-star'))

        # Extracting the data
        data_with_ratings_and_dates = []

        for entry in review_entries:
            # Extracting the rating
            rating_td = entry.find_all('td')[1]  # Rating is in the second td
            rating = extract_rating(rating_td)

            # Extracting the name and content
            content_td = entry.find_all('td')[-2]  # Content is in the second last td
            content_html = str(content_td)
            name_start = content_html.find('by <strong>') + len('by <strong>')
            name_end = content_html.find('</strong>', name_start)
            name = content_html[name_start:name_end]
            content_full = content_td.get_text(strip=True)

            # Handling the special case where the name is attached to the content
            by_name_attached = f"by{name}"
            if content_full.startswith(by_name_attached):
                content = content_full.replace(by_name_attached, '', 1).strip()
            elif content_full.startswith(f"by {name}"):
                content = content_full.replace(f"by {name}", '', 1).strip()
            else:
                content = content_full

            # Extracting date
            date_td = entry.find('td', class_='date')
            date = date_td.get_text(strip=True) if date_td else None

            data_with_ratings_and_dates.append((name, rating, content, date))

        # Convert the data to DataFrame
        df_reviews = pd.DataFrame(data_with_ratings_and_dates, columns=['Name', 'Rating', 'Content', 'Date'])

        # Create an output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Save to Excel
        excel_file_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(html_file_path))[0]}.xlsx")
        df_reviews.to_excel(excel_file_path, index=False)

        print(f"Data extracted and saved to {excel_file_path}")

# Example usage:
html_file_paths = [
      r'C:\Users\user\Desktop\New folder (2)\olyv.html',
   r'C:\Users\user\Desktop\New folder (2)\ANQ.html',
     r'C:\Users\user\Desktop\New folder (2)\sunstone.html',
      r'C:\Users\user\Desktop\New folder (2)\Ant Mobi.html',
        r'C:\Users\user\Desktop\New folder (2)\Otipy.html',
     r'C:\Users\user\Desktop\New folder (2)\CheQ.html',
     r'C:\Users\user\Desktop\New folder (2)\Jungle rummy.html',
    r'C:\Users\user\Desktop\New folder (2)\fancall.html',
          r'C:\Users\user\Desktop\New folder (2)\Kissht.html',
     r'C:\Users\user\Desktop\New folder (2)\lifestyle.html',
     r'C:\Users\user\Desktop\New folder (2)\Mykinara.html',
     r'C:\Users\user\Desktop\New folder (2)\MyTeam11.html',
     r'C:\Users\user\Desktop\New folder (2)\NNNOW.html',
      r'C:\Users\user\Desktop\New folder (2)\ruperdree.html',
     r'C:\Users\user\Desktop\New folder (2)\Pepperfry.html',
           r'C:\Users\user\Desktop\New folder (2)\ring.html',
     r'C:\Users\user\Desktop\New folder (2)\Rummy Passion.html',
     r'C:\Users\user\Desktop\New folder (2)\Rummy Titans.html',
     r'C:\Users\user\Desktop\New folder (2)\Rummycom.html',
    r'C:\Users\user\Desktop\New folder (2)\Stanza Living.html',
    r'C:\Users\user\Desktop\New folder (2)\Vision11.html',
       r'C:\Users\user\Desktop\New folder (2)\zag.html',
       r'C:\Users\user\Desktop\New folder (2)\Zupee.html',
]

output_folder = r'C:\Users\user\Desktop\scrapp data (2)\individual_excels'
extract_reviews_to_excel(html_file_paths, output_folder)
