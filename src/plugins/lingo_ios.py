from plugins.lingo_plugin import ILingoPlugin
import csv
import pandas
import json
import pathlib
from config import Platform
import os
import utils


class LingoIOS(ILingoPlugin):
    
    __platform: Platform

    def __conver_excel_to_csv(excel):
        df = pandas.read_excel(excel)
        df.to_csv(index=False)
        return df


    def __create_strings_file(self, df, language, filename):
        output = self.__platform.output
        if not utils.checkDirPath(output):
            # TODO: fixme
            raise RuntimeError("output not a dir")

        with open(os.path.join(output, filename), 'w') as file:
        #     for index, row in df.iterrows():
        #         pass
                # file.write(f'"{row["key"]}" = "{row[language]}";\n\n')

    def load(self, file, platform: Platform):
        file_extension = pathlib.Path(file).suffix
        df = None
        if (file_extension == '.xls' or file_extension == '.xlsx'):
            df = self.__conver_excel_to_csv(file)
        elif file_extension == '.csv':
            df = pandas.read_csv(file)
        else:
            raise RuntimeError(f"not support {file_extension} file, only support `csv` or `xlsx` file")
        self.__platform = platform
        
        df.dropna(how="all",axis=0,inplace=True)

        filtered_df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        print(filtered_df)
        languages = filtered_df.columns[1:]
        print(languages)
        for language in languages:
            filename = f'{language}.strings'
            self.__create_strings_file(df, language, filename)
        



