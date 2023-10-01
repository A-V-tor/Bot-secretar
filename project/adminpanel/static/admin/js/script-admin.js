import json from './.env.json' assert { type: "json" };


const App = {
  data() {
    return {
      valueForNote: '',
      notes: [],
      notesUrl: json.notesUrl,
      authorizationKey: json.authorizationKey,
      getBt: true,
      activeButtons: [], // массив булевых для блокировки кнопок
      buttonClasses: [] // классы для отображения переключателя блокировки кнопки "Удалить"
    }
  },
  created() {
    // запрос списка заметок
    this.get_data_notes().then((data) => {
      this.notes = data;
      this.fillListBtDisabled()
    }).catch((error) => {
      console.error('Ошибка при получении данных:', error);
    });
  },
  delimiters: ['[[', ']]'],
  methods: {
    async addNote() {
      if (this.valueForNote.trim() !== '' && this.valueForNote.length < 282) {
        if (this.valueForNote.trim().includes('http')) {

          let regularMatchLink = /https?:\/\/\S+/
          let link = this.valueForNote.match(regularMatchLink)

          //              удаляем ссылку из текста
          let textNoLink = this.valueForNote.replace(regularMatchLink, '')
          //              если текст отсутствует, добавляем метку
          if (textNoLink.trim() === "") {
            textNoLink = 'Неизвестная ссылка'
          }

          this.notes.push(`<a href="${link}" class="link-note" target="_blank">${textNoLink}</a>`)
          try {
            const res = await fetch(this.notesUrl, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json', 'Authorization': this.authorizationKey},
              body : JSON.stringify({data: `<a href="${link}" class="link-note" target="_blank">${textNoLink}</a>`})
            });
            if (!res.ok) {
              throw new Error('Сетевой ответ не был успешным');
            }
            const data_res = await res.json();
            this.valueForNote = ''
            return data_res.res; // Обращение к свойству 'res' в JSON-ответе
          } catch (error) {
            return []; // Возвращаем пустой массив в случае ошибки
          }

        } else {
          this.notes.push(this.valueForNote)
          try {
            const res = await fetch(this.notesUrl, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json', 'Authorization': this.authorizationKey },
              body : JSON.stringify({data: this.valueForNote})
            });
            if (!res.ok) {
              throw new Error('Сетевой ответ не был успешным');
            }
            const data_res = await res.json();
            this.valueForNote = ''
            return data_res.res; // Обращение к свойству 'res' в JSON-ответе
          } catch (error) {
            return []; // Возвращаем пустой массив в случае ошибки
          }
        }
      }
    },
    async delNote(indx) {
      this.notes.splice(indx++, 1)
      this.makeSwitchDisabled(indx-1)
      try {
        const res = await fetch(this.notesUrl, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json', 'Authorization': this.authorizationKey},
          body : JSON.stringify({id: indx})
        });
        if (!res.ok) {
          throw new Error('Сетевой ответ не был успешным');
        }
        const data_res = await res.json();
        return data_res.res; // Обращение к свойству 'res' в JSON-ответе
      } catch (error) {
        return []; // Возвращаем пустой массив в случае ошибки
      }
    },
    check_text_note(text) {
      if (text.trim().toLowerCase().includes('github')) {
        return 'github'
      } else if (text.trim().toLowerCase().includes('secret')) {
        return 'secret'
      } else { return false }
    },
    getNoteButtonClasses(note) {
      const noteType = this.check_text_note(note);
      switch (noteType) {
        case 'github':
          return 'btn btn-note btn-note-github';
        case 'secret':
          return 'btn btn-note btn-note-secret';
        default:
          return 'btn btn-note';
      }
    },
    async get_data_notes() {
      try {
        const res = await fetch(this.notesUrl, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json', 'Authorization': this.authorizationKey }
        });
        if (!res.ok) {
          throw new Error('Сетевой ответ не был успешным');
        }
        const data_res = await res.json();
        return data_res.all_notes; // Обращение к свойству 'res' в JSON-ответе
      } catch (error) {
        return []; // Возвращаем пустой массив в случае ошибки
      }
    },
    makeSwitchDisabled(indx) {
        // переключение доступности кнопки "Удалить"
        if (this.buttonClasses[indx] === 'switch-on-2') {
            this.buttonClasses[indx] = '' // отображение блокировки
        } else {
            this.buttonClasses[indx] = 'switch-on-2' // отображение доступности взаимодействия
        }
        if (this.activeButtons[indx]) {
            this.activeButtons[indx] = false; // Открываем кнопку

          } else {
            this.activeButtons[indx] = true; // Закрываем кнопку

          }
    },
    fillListBtDisabled() {
        // заполнить массив изначально заблокированными свойствами
        for (let i = 0; i < this.notes.length; i++) {
        this.activeButtons[i] = true; // Изначально все кнопки закрыты
        }
    }

  },

}

const app = Vue.createApp(App)
app.mount('#app')
