import tkinter as tk
from bs4 import BeautifulSoup as soup
import requests

class App:
    def __init__(self, root, img):
        self.root = root
        self.logo = img

        self.Labels()
        self.Entries()
        self.Texts()
        self.Buttons()

    def Labels(self):
        tk.Label(root,
                 text="       WELCOME TO\n                  "
                      "                      LYRICS FINDER!\nIT'S A PLACE WHERE\nALL SEARCHES END!​",
                 font=("Comic Sans MS", 12),
                 justify=tk.LEFT).grid(row=0,
                                       column=0,
                                       columnspan=15,
                                       sticky='w',
                                       padx=10)
        tk.Label(root,
                 image=self.logo).grid(row=0,
                                       column=2,
                                       columnspan=6,
                                       sticky='eswn')
        tk.Label(root,
                 text='Enter song name: ', font=("Comic Sans MS", 10),
                 justify=tk.LEFT).grid(row=1,
                                       column=0,
                                       sticky='w',
                                       padx=10)
        tk.Label(root,
                 text='Enter a number of the song:',
                 font=("Comic Sans MS", 10)).grid(row=4,
                                               column=0,
                                               sticky='w',
                                               padx=10)
        self.LABELtitle_artist = tk.Label(root,
                                          text='Title - Artist',
                                          font=("Comic Sans MS", 20))

        self.LABELtitle_artist.grid(row=4,
                                    column=2,
                                    columnspan=10)
    def Entries(self):
        self.ENTRYsongname= tk.Entry(root, font=("Comic Sans MS", 10))
        self.ENTRYsongname.grid(row=2,
                                column=0,
                                sticky='eswn',
                                padx=5)

        self.ENTRYsongnum = tk.Entry(root, font=("Comic Sans MS", 10))
        self.ENTRYsongnum.grid(row=5,
                               column=0,
                               sticky='eswn',
                               padx=5)

    def Texts(self):
        self.artists = tk.Text(root, width=40, font=("Comic Sans MS", 10))
        self.artists.grid(row=6,
                          column=0,
                          padx=5,
                          columnspan=2)

        self.lyrics = tk.Text(root, width=70,  font=("Comic Sans MS", 10))
        self.lyrics.grid(row=6,
                         column=2,
                         columnspan=6)
    def Buttons(self):
        tk.Button(root,
                  text='Previous', font=("Comic Sans MS", 10),
                  command=self.prev_page).grid(row=7,
                                               column=0,
                                               sticky='eswn',
                                               padx=5)
        tk.Button(root,
                  text='Next', font=("Comic Sans MS", 10),
                  command=self.next_page).grid(row=7,
                                               column=1,

                                               sticky='eswn',
                                               padx=5)
        tk.Button(root,
                  text='SUBMIT', font=("Comic Sans MS", 10),
                  width=20,
                  command=self.query).grid(row=2,
                                           column=1,
                                           sticky='eswn',
                                           padx=5)
        tk.Button(root,
                  text='SHOW LYRICS!', font=("Comic Sans MS", 10),
                  command=self.show_lyrics).grid(row=5,
                                                 column=1,
                                                 sticky='eswn',
                                                 padx=5)
    def query(self):
        self.SONG = self.ENTRYsongname.get()

        self.curr_page = 1
        self.LABELtitle_artist.config(text='Title - Artist')
        self.surf_pages()

    def prev_page(self):
        if self.curr_page > 1:
            self.curr_page -= 1
        self.surf_pages()

    def next_page(self):
        self.curr_page += 1
        self.surf_pages()

    def surf_pages(self):
        song_path = '+'.join(self.SONG.lower().split(' '))
        page = requests.get(
            'https://search.azlyrics.com/search.php?q={}&w=songs&p={}'.format(song_path, self.curr_page))
        parsed = soup(page.content, 'html.parser')
        songs = parsed.find_all(class_='text-left visitedlyr')
        b_tag_list = [song.find_all('b') for song in songs]
        self.song_list = [' / '.join(tag_content.get_text() for tag_content in b_tag) for b_tag in b_tag_list]
        self.song_urls = [song.find('a', href=True)['href'] for song in songs]

        if self.song_list == []:
            self.artists.delete(1.0, tk.END)
            self.artists.insert(tk.END,
                                'Э, песни под названием \'{}\' НЕТ! \n Ты уверен в себе?'.format(self.SONG))
        else:
            result = '\n'
            for i in range(len(self.song_list)):
                result += ('{}. {}'.format(i + 1, self.song_list[i]) + '\n')
            self.artists.delete(1.0, tk.END)
            self.artists.insert(tk.END, result)
        return self.song_list

    def show_lyrics(self):
        song_num = self.ENTRYsongnum.get()
        song_num = int(song_num)

        if self.song_list != []:
            if 0 < song_num <= len(self.song_list):
                lyrics_url = self.song_urls[song_num-1]
                song_name = self.song_list[song_num-1]
                self.LABELtitle_artist.config(text=song_name)

                lyrics_page = requests.get(lyrics_url)
                parsed_lyrics_page = soup(lyrics_page.content, 'html.parser')
                lyrics = parsed_lyrics_page.find_all('div', class_=None)[0].get_text().strip()

                self.lyrics.delete(1.0, tk.END)
                self.lyrics.insert(tk.END, lyrics)
                return lyrics

if __name__ == '__main__':
    root = tk.Tk()
    root.title(' Lyrics Finder')
    root.iconbitmap('ikonka.ico')
    img = tk.PhotoImage(file='kartinka.gif').subsample(2, 2)

    thunder = App(root, img)
    root.mainloop()