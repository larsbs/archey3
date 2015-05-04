@module_register("de")
class deDisplay(display):
    def render(self):
        if self.state.config.get('de', 'manual', fallback=False):
            return "DE", self.state.config.get('de', 'manual')
        de = ''
        for key in DE_DICT.keys():
            if self.process_exists(key):
                de = key
                break
        return "DE", DE_DICT[de]
