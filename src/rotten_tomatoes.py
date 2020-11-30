# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
import json, random
from time import sleep
from datetime import datetime

# %%


def get_best_movies(year):

    driver = webdriver.Chrome(chrome_options=chrome_options)

    url = "https://www.rottentomatoes.com/top/bestofrt/?year={}".format(year)

    driver.get(url)

    body = driver.find_element_by_xpath(
        '//*[@id="top_movies_main"]/div/table/tbody'
    )

    movie_tags = body.find_elements(By.TAG_NAME, 'tr')

    return driver, movie_tags


# %%
def dump_movie_info(year, movie_name, movie_url, dump_to=None):
    driver = webdriver.Chrome(chrome_options=chrome_options)

    xpath_to_text = lambda string: driver.find_element_by_xpath(string).text

    tomato_dic = {
        'Year': year,
        'Film Name': movie_name,
    }

    print(year, movie_name)

    driver.get(movie_url)

    for k in [1, 2, 3, 4, 5]:
        xpath = '//*[@id="mainColumn"]/section[{}]/div/div/ul'.format(k)
        try:
            movie_info_parent_tag = driver.find_element_by_xpath(xpath)
            break
        except:
            if k == 4:
                raise Exception("Movie Info Table was not found")

    movie_info_tags = movie_info_parent_tag.find_elements(By.TAG_NAME, 'li')

    for row in movie_info_tags:
        key, val = [r.text for r in row.find_elements(By.TAG_NAME, 'div')]
        tomato_dic[key.split(':')[0]] = val

    score_xpaths = {
        'Synopsis':
            '//*[@id="topSection"]/div[2]/div[1]/section/p',
        'Critics Consensus':
            '//*[@id="movieSynopsis"]',
        'Tomatometer Score':
            '//*[@id="tomato_meter_link"]/span[2]',
        'Tomatometer Total Count':
            '//*[@id="topSection"]/div[2]/div[1]/section/section/div[1]/div/small',
        'Audience Score':
            '//*[@id="topSection"]/div[2]/div[1]/section/section/div[2]/h2/a/span[2]',
        'Audience User Ratings':
            '//*[@id="topSection"]/div[2]/div[1]/section/section/div[2]/div/strong'
    }

    for key, xpath in score_xpaths.items():
        try:
            text = xpath_to_text(xpath)
        except:
            text = 'INFO NOT YET AVAILABLE'
        finally:
            tomato_dic[key] = text
    """

    tomatometer_score_xpath = '//*[@id="tomato_meter_link"]/span[2]'
    tomatometer_count_xpath = '//*[@id="topSection"]/div[2]/div[1]/section/section/div[1]/div/small'
    audience_score_xpath = '//*[@id="topSection"]/div[2]/div[1]/section/section/div[2]/h2/a/span[2]'
    audience_ratings_xpath = '//*[@id="topSection"]/div[2]/div[1]/section/section/div[2]/div/strong'
 
    
    tomato_dic['Synopsis'] =  xpath_to_text('//*[@id="topSection"]/div[2]/div[1]/section/p')
    
    tomato_dic['Critics Consensus'] = xpath_to_text('//*[@id="movieSynopsis"]')

    tomato_dic['Tomatometer Score'] = int(xpath_to_text(tomatometer_score_xpath)[:-1])
    
    tomato_dic['Tomatometer Total Count'] = int(xpath_to_text(tomatometer_count_xpath))
    
    tomato_dic['Audience Score'] = int(xpath_to_text(audience_score_xpath)[:-1])
    
    tomato_dic['Audience User Ratings'] = xpath_to_text(audience_ratings_xpath).split(':')[-1]
    """
    tomato_json = json.dumps(tomato_dic)
    with open(dump_to, 'a+') as f:
        f.write(tomato_json + '\n')

    driver.quit()


# %%
def get_years_and_last_id(init_year=1950, final_year=2020):
    random.seed(5555)
    years = [x for x in range(init_year, final_year + 1)]
    random.shuffle(years)

    with open('../logs/last_analyzed_year_id', 'r') as f:
        last_id = int(f.read())

    return years, last_id


def get_current_year(init_year=1950, final_year=2020):

    years, last_id = get_years_and_last_id(
        init_year=init_year, final_year=final_year
    )
    result = None if last_id == -2 else years[last_id + 1]
    return result


def update_year_id(init_year=1950, final_year=2020):

    years, last_id = get_years_and_last_id(
        init_year=init_year, final_year=final_year
    )
    result = -2 if years[last_id + 1] == years[-1] else last_id + 1

    with open('../logs/last_analyzed_year_id', 'w+') as f:
        f.write(str(result))


def get_movies_per_year(year, dump_to_file):

    movie_urls = []
    movie_names = []
    driver, movie_tags = get_best_movies(year)
    for movie_tag in movie_tags:

        td_tag = movie_tag.find_elements(By.TAG_NAME, 'td')[2]
        link_tag = td_tag.find_elements(By.TAG_NAME, 'a')[0]
        movie_urls.append(link_tag.get_attribute('href'))
        movie_names.append(link_tag.text)

    driver.quit()

    for url, name in zip(movie_urls, movie_names):

        dump_movie_info(year, name, url, dump_to=dump_to_file)
        sleep(1 + random.random())


def get_filename():

    dt_now = datetime.now()
    ldt = dt_now.ctime().split(' ')
    fdt = ldt[:-2] + ldt[-2].split(':') + ldt[-1:]
    dt_str = '_'.join(fdt)
    json_file = '../data/raw/rotten_tomatoes_{}.json'.format(dt_str)

    return json_file


# %%

chrome_options = Options()
chrome_options.add_argument("--headless")


def main():

    json_file = get_filename()
    init_year = 2010
    final_year = 2011
    while True:

        year = get_current_year(init_year, final_year)

        if year is None:
            print('All years have been scraped...')
            break

        get_movies_per_year(year, json_file)
        update_year_id(init_year, final_year)


# %%
main()

# %%
