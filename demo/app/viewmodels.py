from djviewmodels.viewmodels import Viewmodel
from . import models


class Note(Viewmodel):
    model = models.Note

    def note_prop(self):
        return "I'm a note view model property!"
