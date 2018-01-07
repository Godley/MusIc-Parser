
class Part(object):

    def __str__(self):
        st = ""
        if hasattr(self, "name"):
            st += "name:" + self.name
        for stave in self.measures.keys():
            st += "\n"
            st += "Staff: "
            st += str(stave)
            st += "\n\r Details: \r"
            for key in self.measures[stave]:
                st += "Measure: "
                st += str(key)
                st += str(self.measures[stave][key])
            st += "\n--------------------------------------------------------"
        return st
