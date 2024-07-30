import os
import textwrap

from jinja2 import Environment, FileSystemLoader

from besser.BUML.metamodel.state_machine.bot import Bot
from besser.BUML.metamodel.structural import Method
from besser.generators import GeneratorInterface


class BBFGenerator(GeneratorInterface):
    """
    BBFGenerator is a class that implements the GeneratorInterface and is responsible for generating
    the bot code, using the BESSER Bot Framework (BBF), based on an input bot model.

    Args:
        model (Bot): A bot model.
        output_dir (str, optional): The output directory where the generated code will be saved. Defaults to None.
    """
    def __init__(self, model: Bot, output_dir: str = None):
        super().__init__(model, output_dir)

    def generate(self):
        """
        Generates the BBF bot code and saves it to the specified output directory.
        If the output directory was not specified, the code generated will be stored in the <current directory>/output
        folder.
        """

        # TODO: TelegramPlatform.add_handler() not implemented in generator
        # TODO: Verify imports are added when necessary
        # TODO: Platform name not safe (hardcoded 'websocket_platform' and 'telegram_platform' in jinja template), when accessed from body can be different name
        # TODO: Global variables?
        # -->   (OPTION 1) bot.create_global_var(name: str, type: type, value: Any) --> not supports "custom" values (e.g. x = bot.get_name() )
        # -->   (OPTION 2) bot.add_code_line('x = bot.get_name()')

        def is_class(obj, name):
            return obj.__class__.__name__ == name

        def is_type(obj, type_name: str):
            return type(obj).__name__ == type_name

        def replace_bot_session_with_session_in_signature(func: Method) -> str:
            if func:
                code = func.code.replace('BotSession', 'Session')
                return textwrap.dedent(code)
            else:
                return None

        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path))
        env.globals['is_class'] = is_class
        env.globals['is_type'] = is_type
        env.globals['replace_bot_session_with_session_in_signature'] = replace_bot_session_with_session_in_signature
        bot_template = env.get_template('bbf_bot_template.py.j2')
        bot_path = self.build_generation_path(file_name=f"{self.model.name}.py")
        with open(bot_path, mode="w") as f:
            generated_code = bot_template.render(bot=self.model)
            f.write(generated_code)
            print("Bot script generated in the location: " + bot_path)
        config_template = env.get_template('bbf_config_template.py.j2')
        config_path = self.build_generation_path(file_name="config.ini")
        with open(config_path, mode="w") as f:
            properties = sorted(self.model.properties, key=lambda prop: prop.section)
            generated_code = config_template.render(properties=properties)
            f.write(generated_code)
            print("Bot config file generated in the location: " + config_path)
