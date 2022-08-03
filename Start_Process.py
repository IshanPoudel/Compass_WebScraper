from Get_all_links_from_website import get_all_links
from Get_values_for_each_house_and_store import get_values_for_each_house_and_store
from Corelate import corelate
from sql_to_excel import export_to_excel

get_all_links()
print("I am getting all the links.")
get_values_for_each_house_and_store()
corelate()
export_to_excel()

