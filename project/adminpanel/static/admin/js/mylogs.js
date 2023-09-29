const App = {
    data() {
    return {
      Logs: 'нет логов',
      getClass: 'switch-btn'
    }
  },
  delimiters: ['[[', ']]'],
  created() {
    // запрос списка заметок
    this.get_bot_logs().then((data) => {
      this.Logs = data;
    }).catch((error) => {
      console.error('Ошибка при получении данных:', error);
    });
  },
  methods: {
    async get_flask_logs() {
        try {
            const res = await fetch(
                'http://localhost:5000/api/flask-logs', {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json'}
                }
            )
        const data_res = await res.text()
        return data_res
        } catch(error) {
            return error
        }
    },
    async get_bot_logs() {
        try {
            const res = await fetch(
                'http://localhost:5000/api/bot-logs', {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json'}
                }
            )
        const data_res = await res.text()
        return data_res
        } catch(error) {
            return error
        }
    },
//    переключение логов
    makeSwitch() {
        if (this.getClass === 'switch-btn switch-on') {
            this.getClass = 'switch-btn'
            this.get_bot_logs().then((data) => {
                this.Logs = data;
            }).catch((error) => {
                console.error('Ошибка при получении данных:', error);
            });
        } else {
            this.getClass = 'switch-btn switch-on'
            this.get_flask_logs().then((data) => {
              this.Logs = data;
            }).catch((error) => {
              console.error('Ошибка при получении данных:', error);
            });
        }
    }
  },
}


const app = Vue.createApp(App)
app.mount('#app')