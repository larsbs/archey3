@module_register("wm")
class wmDisplay(display):
    def render(self):
        if self.state.config.get('wm', 'manual', fallback=False):
            return "WM", self.state.config.get('wm', 'manual')
        wm = ''
        for key in WM_DICT.keys():
            if self.process_exists(key):
                wm = key
                break
        return "WM", WM_DICT[wm]
