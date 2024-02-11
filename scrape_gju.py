import requests
from bs4 import BeautifulSoup
import urllib.parse

def scrape_gju_staff(staff_name, page):
    try:
        base_url = 'https://www.gju.edu.jo/content/staff-directory-2882'
        page_url = f'{base_url}?og_group_school_department_target_id=All&combine=&page={page}'
        response = requests.get(page_url, verify=False)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all staff details on the page
            staff_details = soup.find_all('td', {'class': 'views-field views-field-title-field-et'})

            for staff_detail in staff_details:
                name_element = staff_detail.find('span', {'class': 'staff-title'})
                if name_element:
                    name = name_element.text.strip().lower()

                    # Check if the given name is contained in the staff member name
                    if staff_name in name:
                        # Extract staff member email using your original method
                        email_link = staff_detail.find_next('a', href=lambda href: href and href.startswith('mailto:'))

                        if email_link:
                            email = urllib.parse.unquote(email_link['href'][7:])  # Decode URL encoding

                            # Additional information
                            responsibility = staff_detail.find_next('div', {'class': 'staff-responsibility'})
                            office = staff_detail.find_next('div', {'class': 'staff-office'})
                            telephone = staff_detail.find_next('div', {'class': 'staff-tel'})

                            return {
                                'success': True,
                                'email': email,
                                'responsibility': responsibility.text.strip() if responsibility else '',
                                'office': office.text.strip() if office else '',
                                'telephone': telephone.text.strip() if telephone else ''
                            }

            # Check if there is a next page
            next_page_link = soup.find('li', {'class': 'pager-next'})
            if next_page_link and next_page_link.a:
                page += 1
                # Recursively call the function for the next page
                return scrape_gju_staff(staff_name, page)
            else:
                return {'success': False, 'error': 'Staff member not found on any page'}
        else:
            return {'success': False, 'error': f'Failed to retrieve the page. Status Code: {response.status_code}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
