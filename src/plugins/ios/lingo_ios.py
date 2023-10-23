from plugins.lingo_plugin import ILingoPlugin
from config import Platform
import os
import utils
import re


class LingoIOS(ILingoPlugin):
    
    __platform: Platform
    __main_language = ""

    def __update_strings_file(self, df, language, filename, dir):
        if not utils.check_is_dir(dir):
            raise RuntimeError(f"target save path: \"{dir}\" must be a directory")
        
        write_mode = 'a' if self.__platform.mode == 'append' else 'w'
        
        file_path = os.path.join(dir, filename)
        
        with open(file_path, write_mode) as file:
            if write_mode == 'w' or utils.is_empty_file(file_path):
                file.write(utils.do_not_edit_tips())
            for row in df.iterrows():
                if not re.search(r'(?<!\\)"', row[language]):
                    value = row[language]
                else:
                    value = row[language].replace('"', '\\"')
                file.write(f'"{row["key"]}" = "{value}"\n\n')
                
    def __create_lproj_dir(self, language):
        output = self.__platform.output
        if not os.path.exists(output):
            os.mkdir(output)
        if not utils.check_is_dir(output):
            raise RuntimeError(f"{output} must be a dir")
        lproj_path = os.path.join(output, f"{language}.lproj")
        if not os.path.exists(lproj_path):
            os.mkdir(lproj_path)
        return lproj_path
    
    def post_load(self):
        autogen_dir = os.path.join(self.__platform.output, "molingo")
        if not utils.check_is_dir(autogen_dir):
            os.makedirs(autogen_dir, exist_ok=True)
            utils.run['swiftgen', 'config', 'init']
            with open(os.path.join(autogen_dir, 'swiftgen.yml'), 'a') as file:
                file.write(f"""
                           strings:
                             inputs: {self.__main_language}
                             outputs:
                               templateName: structured-swift5
                               output: ../Resources/Generated/Strings.swift
                           """)
        utils.run["swiftgen"]
        
        
    def pre_load(self):
        swiftgen = "swiftgen"
        if utils.get_command_path(swiftgen) == None:
            utils.install_with_brew(swiftgen)

    def load(self, csv_df, platform: Platform):
        self.pre_load()
        self.__platform = platform
        # get languages from csv file
        languages = csv_df.columns[1:]
        for index, language in languages:
            dir = self.__create_lproj_dir(language)
            if index == 0:
                self.__main_language = dir
            filename = f'{language}.strings'
            self.__update_strings_file(csv_df, language, filename, dir)
        



