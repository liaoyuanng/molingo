import json
from config import Platform
from plugins.lingo_plugin import ILingoPlugin
import os
import utils

class LingoFlutter(ILingoPlugin):
    
    __platform: Platform
    
    def __create_output_dir(self):
        output_path = os.path.join(self.__platform.proj_root_path, "assets", "locales")
        if not utils.check_is_dir(output_path):
            os.makedirs(output_path, exist_ok=True)
        return output_path
    
    def __update_json_file(self, language, df, output):
        data = {}
        path = os.path.join(output, f"{language}.json")
        if self.__platform.mode == "append" and utils.check_is_file(path):
            with open(path, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    utils.log_err("JSON file is not in standard format")
                    exit()
        
        with open(path, 'w') as file:
            for index, row in df.iterrows():
                data[row["key"]] = row[language]
            json.dump(data, file, indent=4, ensure_ascii=False)
            
            
    def __get_pub_spec_dir(self):
        for root, dirs, files in os.walk(self.__platform.proj_root_path):
            if 'pubspec.yaml' in files:
                return root
        utils.log_err(f"Can not find pubspec.yaml in project({self.__platform.proj_root_path})")
        exit(0)
                
            
    
    def pre_load(self):
        utils.log("Check dependencies...")
        if utils.get_command_path("get") == None:
            flutter = utils.get_command_path("flutter")
            if flutter == None:
                utils.log_err("install gex-cli failed, flutter command not found")
                exit()
            utils.log("Installing getx-cli...")
            utils.run([flutter, 'pub', 'global', 'activate', 'get_cli'])
    
    
    def post_load(self):
        utils.log("Executing get-cli")
        pubspec_path = self.__get_pub_spec_dir()
        utils.run(["get", "generate", "locales"], cwd=pubspec_path)
        
    
    def load(self, csv_df, platform: Platform):
        self.pre_load()
        self.__platform = platform
        languages = csv_df.columns[1:]
        utils.log(f"Initiating localization.")
        output_path = self.__create_output_dir()
        for language in languages:
            self.__update_json_file(language, csv_df, output_path)
            utils.log(f"[{language}] localization done.")
        self.post_load()

    
    