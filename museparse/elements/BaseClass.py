
class Base(object):

    """
    A class which ensures all subclasses have a basic override of the to string method, and a toLily method
    """

    def __init__(self):
        self.indent = 1

    def to_lily(self):
        '''
        Method which in any sub classes produces a string, which is a line of lilypond scripting representing the class
        and its variables.

        :return: None, but would normally return str.
        '''
        raise(NotImplementedError)

    def __str__(self):
        st = str(type(self))
        values = vars(self)
        for key in values.keys():
            if key == "indent":
                continue
            st += "\n"
            for i in range(self.indent):
                st += "\t"
            if not isinstance(
                    values[key],
                    dict) and not isinstance(
                    values[key],
                    list):
                try:
                    values[key].indent = self.indent + 1
                except:
                    pass
                st += key + " : "
                try:
                    st += str(values[key])
                except:
                    st += "None"

            if isinstance(values[key], list):
                if len(values[key]) > 0:
                    st += key + " : "
                    for item in values[key]:
                        if not isinstance(
                            item,
                            str) and not isinstance(
                            item,
                            int) and not isinstance(
                            item,
                                float):
                            item.indent = self.indent + 1
                        st += str(item) + "\n"
            if isinstance(values[key], dict):
                if len(values[key]) > 0:
                    st += key + " : "
                    for k in values[key].keys():
                        if not isinstance(
                            values[key][k],
                            str) and not isinstance(
                            values[key][k],
                            int) and not isinstance(
                            values[key][k],
                                float):
                            values[key][k].indent = self.indent + 1
                        st += key + " : " + str(values[key][k])
        return st
