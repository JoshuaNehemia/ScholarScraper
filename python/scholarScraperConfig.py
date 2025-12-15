class ScholarScraperConfig:
    _is_verbose = False
    def __init__(self, is_verbose: bool = False):
        self._is_verbose = is_verbose

    # Getter
    def is_verbose(self):
        return self._is_verbose
    
    # Setter    
    def set_verbosity(self, is_verbose: bool):
        self._is_verbose = is_verbose
