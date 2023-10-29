import os
from jinja2 import Environment, FileSystemLoader
from BUML.metamodel.structural.structural import DomainModel
from generators.generator_interface import GeneratorInterface


class SQLGenerator(GeneratorInterface):
    TYPES = {
        "int": "int",
        "str": "varchar(100)",
        "float": "float8",
        "bool": "bool",
        "time": "time",
        "date": "date",
        "datetime": "timestamp",
        "timedelta": "interval",
    }

    def __init__(self, model: DomainModel, output_dir: str = None, sql_dialect = None):
        super().__init__(model, output_dir)
        self.sql_dialect = sql_dialect

    def generate(self):
        file_name = "tables.sql"
        working_path = os.path.abspath('')
        templates_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "templates")
        if self.output_dir != None:
            file_path = os.path.join(self.output_dir, file_name)
        else:
            os.makedirs(os.path.join(working_path, "output"), exist_ok=True)
            file_path = os.path.join(working_path, "output", file_name)
        env = Environment(loader=FileSystemLoader(templates_path), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template('sql_template.sql.j2')
        with open(file_path, mode="w") as f:
            generated_code = template.render(model=self.model, types=self.TYPES, sql_dialect=self.sql_dialect)
            f.write(generated_code)
            print("Code generated in the location: " + file_path)