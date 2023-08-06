import logging


class DiagnosticsCheckError(Exception):
    pass


class Checker(object):
    LEVEL = "level"
    TEXT = "text"
    HEADER = "header"
    SUMMARY = "summary"
    returnable = {LEVEL: 0, TEXT: "", HEADER: "", SUMMARY: ""}

    def __init__(self):
        self.level = 0
        self.text = ""
        self.header = ""
        self.summary = ""

    @property
    def results(self):
        return {
            self.LEVEL: self.level,
            self.TEXT: self.text,
            self.HEADER: self.header,
            self.SUMMARY: self.summary,
        }

    def _set_summary_from_list_of_lines(self, list_of_lines):
        self.summary = "\n".join(list_of_lines)

    def _check(self, experiment):
        pass

    def check(self, experiment):
        try:
            self._check(experiment)
            return self.results
        except Exception as e:
            logging.error(e)
            raise DiagnosticsCheckError(
                (
                    "there was a problem running one of the diagnostics "
                    "checks ({}): {}".format(self.__class__.__name__, e)
                )
            )
