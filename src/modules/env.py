@module_register("env")
class envDisplay(display):
    def __init__(self, **kwargs):
        try:
            self.arg1 = kwargs["args"][0]
        except IndexError:
            self.state.logger.error("Did not get any arguments, require one, the env variable to display.")
            raise
        super().__init__(**kwargs)

    def render(self):
        argvalue = getenv(self.arg1.upper())
        return ('$' + self.arg1.upper(), argvalue)
