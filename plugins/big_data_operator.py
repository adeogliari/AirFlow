from airflow.models import BaseOperator
import pandas as pd


class BigDataOperator(BaseOperator):

    def __init__(self, path_to_csv_file: str, path_to_save_file: str, separator: str = ';', file_type: str = 'parquet',
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self.path_to_csv_file = path_to_csv_file
        self.path_to_save_file = path_to_save_file
        self.separator = separator
        self.file_type = file_type

    def execute(self, context):
        try:
            self.log.info(f"Lendo o arquivo CSV de {self.path_to_csv_file}")
            df = pd.read_csv(self.path_to_csv_file, sep=self.separator)

            if self.file_type == 'parquet':
                self.log.info(f"Salvando o arquivo como Parquet em {self.path_to_save_file}")
                df.to_parquet(self.path_to_save_file)
            elif self.file_type == 'json':
                self.log.info(f"Salvando o arquivo como JSON em {self.path_to_save_file}")
                df.to_json(self.path_to_save_file)
            else:
                raise ValueError('file_type must be parquet or json')

        except Exception as e:
            self.log.error(f"Erro ao processar o arquivo: {e}")
            raise