from collections import UserDict

class Tag():
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return self.__value
    
    def __repr__(self):
        return self.__value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, tag: str):
        if isinstance(tag, str):
            result = tag.lower().replace(" ","")
            self.__value = result

class Note():
    def __init__(self, title: str, text: str, tags):
        self.title = title
        self.text = text
        self.__tags = set()
        self.tags = tags

    def __str__(self):
        return self.title
    
    def __repr__(self):
        title_str = f'{self.title}'
        text_str = f'{self.text}'
        tags_str = f"{','.join([str(tag) for tag in self.__tags])}"
        return title_str + text_str + tags_str

    def add_tag(self, tags):
        new_tag = [tag for tag in tags]
        for i in new_tag:
            self.__tags.add(i)

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, tags):
        if isinstance(tags, str):
            self.__tags.add(tags)
        elif isinstance(tags, list):
            for tag in tags:
                self.__tags.add(tag)

        
    def change_title(self, new_title):
        old_title = self.title
        self.title = new_title
        return f"Title: '{old_title}' change to '{new_title}'"
    
    def change_text(self, new_text):
        old_text = self.text
        self.text = new_text
        return f"Title: '{old_text}' change to '{new_text}'"
    
    def change_tags(self, new_tag):
        try:
            old_tag = ','.join(self.__tags)
        except TypeError:
            old_tag = 'tags are missing'
        self.__tags = new_tag
        return f"Tags: '{old_tag}' change to '{new_tag}'"
    

class NoteBook(UserDict):

    def add_notes(self, note: Note):
        if self.get(note.title):
            return f'{note.title} is already exists'
        
        self.data[note.title] = note
        return f'{note.title.title()} is successfully added in notes'
    
    def remove_note(self, word: str):
        for note in self.data.values():
            if word.lower() == note.title.lower():
                remove_note = note.title
        self.data.pop(remove_note)
        return word, self


    def to_dict(self):
        data = {}
        for note in self.data.values():
            data.update({str(note.title): {"title": note.title,
                                    "text": note.text,
                                    "tags": [str(i) for i in note.tags]}})
        return data

    def from_dict(self, data):
        for note in data:
            nt = data[note]
            self.add_notes(Note(nt['title'],
                                nt['text'],
                                [Tag(i) for i in nt['tags']]))
    
    def show_all(self):
        return self.data
    
    def find(self, word: str):
        data = []
        
        for note in self.data.values():
            
            if word.lower() in note.__repr__():
                data.append(note) 
        
            return data
        else:
            "Nothing found"    
    

    def paginator(self, notes_num):
        start = 0
        while True:
            # превращаем в список ключи словаря и слайсим
            result_keys = list(self.data)[start: start + notes_num]
            # превращаем список ключей словаря в список строк с форматом "ключ : [значение]"
            result_list = [f"{key}: {self.data.get(key).title},{self.data.get(key).text},{self.data.get(key).tags}" for key in result_keys]
            if not result_keys:
                break
            yield '\n'.join(result_list)
            start += notes_num



if __name__=='__main__':
    ...