from os.path import dirname, basename, isfile
import glob
import os
import importlib
import inspect
from bspider.crawlers.basic_crawler import BasicCrawler


def get_crawler_class_dict():
    current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    # current_module_name = os.path.splitext(os.path.basename(current_dir))[0]

    output_list = {}
    for filename in glob.glob(current_dir + "/*.py"):
        name = os.path.splitext(os.path.basename(filename))[0]

        # Ignore __ files
        if name.startswith("__"):
            continue
        module = importlib.import_module(".crawlers." + name, package='crawler')

        for member in inspect.getmembers(module, inspect.isclass):
            class_in_module = member[1]

            if class_in_module.__name__.upper() == 'CRAWLERABSTRACT':
                continue

            if class_in_module and class_in_module != BasicCrawler and issubclass(class_in_module, BasicCrawler):
                output_list[class_in_module.__name__.upper()] = class_in_module
    return output_list

# sample:
#   {
#       'CHINANEWS': <class Chinanews>,
#       'BAIJIA': <class Baijia>,
#       ...
#   }
crawler_class_dict = get_crawler_class_dict()

# sample: [<class Chinanews>, <class Baijia>, ...]
crawler_class_list = [crawler_name for crawler_name in crawler_class_dict]
