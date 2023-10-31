import textwrap
from plugins.lingo_plugin import ILingoPlugin
from config import Platform
import os
import utils
import re


class LingoIOS(ILingoPlugin):
    
    __platform: Platform
    __main_language = ""
    __project_dir = None

    def __update_strings_file(self, df, language, filename, dir):
        if not utils.check_is_dir(dir):
            utils.log_err(f"target save path: \"{dir}\" must be a directory")
            exit()
        
        write_mode = 'a' if self.__platform.mode == 'append' else 'w'
        
        file_path = os.path.join(dir, filename)
        
        with open(file_path, write_mode) as file:
            if write_mode == 'w' or utils.is_empty_file(file_path):
                file.write(utils.do_not_edit_tips())
            for _, row in df.iterrows():
                if not re.search(r'(?<!\\)"', row[language]):
                    value = row[language]
                else:
                    value = row[language].replace('"', '\\"')
                value = value.replace('\n', '\\n')
                file.write(f'"{row["key"]}" = "{value}";\n')
                
    def __create_lproj_dir(self, language):
        files = os.listdir(self.__platform.proj_root_path)
        for file in files:
            if file.endswith(".xcodeproj"):
                self.__project_dir = os.path.join(self.__platform.proj_root_path, file) .split(".")[0]
        if self.__project_dir == None:
            utils.log_err("Please provide the directory where the .xcodeproj file is located.")
            exit()
                
        output = os.path.join(self.__project_dir, "Resources", "Localization")
        # create output dir if not exist.
        if not os.path.exists(output):
            os.makedirs(output, exist_ok=True)
            
        generated_output = os.path.join(self.__project_dir, "Resources", "Generated")
         # create generated dir if not exist.
        if not os.path.exists(generated_output):
            os.makedirs(generated_output, exist_ok=True)
        
        # exit if output path is not a dir.
        if not utils.check_is_dir(output):
            utils.log_err(f"{output} must be a dir")
            exit()
        
        # create lproj dir if not exist.
        lproj_path = os.path.join(output, f"{language}.lproj")
        if not os.path.exists(lproj_path):
            os.mkdir(lproj_path)
        return lproj_path
    
    def post_load(self):
        utils.log("Executing swiftgen...")
        yml_path = os.path.join(self.__project_dir, 'swiftgen.yml')
        if not utils.check_is_file(yml_path):
            utils.run(['swiftgen', 'config', 'init'], cwd=self.__project_dir)
            with open(yml_path, 'a') as file:
                config = textwrap.dedent(f"""
                            strings:
                                inputs: ./Resources/Localization/{self.__main_language}.lproj
                                outputs:
                                    templateName: structured-swift5
                                    output: ./Resources/Generated/Strings.swift
                            """)
                file.write(config)
        utils.run(["swiftgen"], cwd=self.__project_dir)
        
        
    def pre_load(self):
        utils.log("Check dependencies...")
        swiftgen = "swiftgen"
        if utils.get_command_path(swiftgen) == None:
            utils.log("Installing Swiftgen...")
            utils.install_with_brew(swiftgen)
            

    def load(self, csv_df, platform: Platform):
        self.pre_load()
        self.__platform = platform
        # get languages from csv file
        languages = csv_df.columns[1:]
        utils.log(f"Initiating localization.")
        for index, language in enumerate(languages):
            dir = self.__create_lproj_dir(language)
            if index == 0:
                self.__main_language = language
            filename = f'Localizable.strings'
            utils.log(f"[{language}] localization done.")
            self.__update_strings_file(csv_df, language, filename, dir)
        self.post_load()
        



