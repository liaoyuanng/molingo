from plugins.lingo_plugin import ILingoPlugin
import pandas
import pathlib
from config import Platform
import os
import utils
import re


class LingoIOS(ILingoPlugin):
    
    __platform: Platform

    def __conver_excel_to_csv(excel):
        df = pandas.read_excel(excel)
        df.to_csv(index=False)
        return df


    def __update_strings_file(self, df, language, filename, dir):
        if not utils.check_is_dir(dir):
            raise RuntimeError(f"target save path: \"{dir}\" must be a directory")
        
        write_mode = 'a' if self.__platform.mode == 'append' else 'w'
        
        file_path = os.path.join(dir, filename)
        
        with open(file_path, write_mode) as file:
            if write_mode == 'w' or utils.is_empty_file(file_path):
                file.write(utils.do_not_edit_tips())
            for index, row in df.iterrows():
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

    def load(self, file, platform: Platform):
        # using magic number is better
        file_extension = pathlib.Path(file).suffix
        df = None
        if (file_extension == '.xls' or file_extension == '.xlsx'):
            df = self.__conver_excel_to_csv(file)
        elif file_extension == '.csv':
            df = pandas.read_csv(file)
        else:
            raise RuntimeError(f"not support {file_extension} file, only support `csv` or `xlsx` file")
        self.__platform = platform
        
        # remove all n/a data
        df.dropna(how="all",axis=0,inplace=True)

        # remove all unnamed columns
        filtered_df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # get languages from csv file
        languages = filtered_df.columns[1:]
        for language in languages:
            dir = self.__create_lproj_dir(self, language)
            filename = f'{language}.strings'
            self.__update_strings_file(self, filtered_df, language, filename, dir)
        



