import pymysql
import xlrd
import xlwt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from operator import itemgetter
import re
import os

csv_file_path = 'F:/1/'
csv_filename = '0226.csv'
database = 'csvdata'
table_name = '0226'

data = pd.read_csv(csv_file_path + csv_filename)
