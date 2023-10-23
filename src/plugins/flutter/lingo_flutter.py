import json
from config import Platform
from plugins.lingo_plugin import ILingoPlugin
import os
import utils

class LingoFlutter(ILingoPlugin):
    
    __platform: Platform
    
    def __create_output_dir(self):
        if not utils.check_is_dir(self.__platform.output):
            os.makedirs(self.__platform.output, exist_ok=True)
    
    def __update_json_file(self, language, df):
        data = {}
        path = os.path.join(self.__platform.output, f"{language}.json")
        if self.__platform.mode == "append" and utils.check_is_file(path):
            with open(path, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    print("JSON file is not in standard format")
                    data = {}
        
        with open(path, 'w') as file:
            for index, row in df.iterrows():
                data[row["key"]] = row[language]
            json.dump(data, file, indent=4, ensure_ascii=False)
                
            
    
    def pre_load(self):
        pass
    
    def post_load(self):
        pass
    
    def load(self, csv_df, platform: Platform):
        self.__platform = platform
        languages = csv_df.columns[1:]
        self.__create_output_dir()
        for language in languages:
            self.__update_json_file(language, csv_df)

    
    