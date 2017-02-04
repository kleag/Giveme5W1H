class Document:

    def __init__(self, title, desc=None, text=None):

        self.raw_title = title
        self.raw_description = desc
        self.raw_text = text

        self.length = 0
        self.section_offsets = []
        self.sentences = []
        self.tokens = []
        self.posTags = []
        self.posTrees = []
        self.nerTags = []

        self.questions = {'what': [], 'who': [], 'why': [], 'where': [], 'when': []}
        self.annotations = {'what': [], 'who': [], 'why': [], 'where': [], 'when': []}

    def __str__(self):
        return ("""
Title: %s

Description: %s

What: %s
When: %s
Where: %s
Who: %s
Why: %s
        """ % (self.raw_title,
               self.raw_description,
               self.questions['what'],
               self.questions['when'],
               self.questions['where'],
               self.questions['who'],
               self.questions['why']))

if __name__ == '__main__':
    doc = Document('Titel', 'Beschreibung')
    doc.questions['who'] = 'Me'
    doc.questions['where'] = 'Test'

    print(doc)
