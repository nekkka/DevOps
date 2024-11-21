<h1>CLI-приложение на Python, для работы над юзерами на операционке Linux</h1>


<h3>Что можно делать:</h3>
<ul>
        <li>Просматривать список пользователей</li>
        <li>Добавлять новых пользователей</li>
        <li>Удалять существующих пользователей</li>
        <li>Блокировать и разблокировать учетные записи пользователей</li>
    </ul>



<h3>Установки:</h3>

<pre>
        sudo apt update
        sudo apt install -y python3 python3-pip libncurses5-dev libncursesw5-dev
        pip install pyfiglet
</pre>



<h3>Какие библиотеки понадобятся?</h3>
<ul>
        <li><strong>os</strong> — работа с операционной системой.</li>
        <li><strong>curses</strong> — создание текстового пользовательского интерфейса.</li>
        <li><strong>pyfiglet</strong> — генерация ASCII-арта для красивого интерфейса.</li>
        <li><strong>subprocess</strong> — выполнение системных команд и получение их результатов.</li>
    </ul>


<h2>Функции и их назначение:</h2>
    <h3>1. welcome</h3>
    <pre>
    def welcome(stdscr):
        ascii_art = pyfiglet.figlet_format("User Management CLI")
        stdscr.addstr(ascii_art, curses.color_pair(1))
        stdscr.refresh()
        stdscr.addstr("\nPress any key to continue...\n")
        stdscr.refresh()
        stdscr.getch()
    </pre>
    <p><b>Описание:</b> Отображает приветственное сообщение в виде ASCII-арта. stdscr: основной экран для вывода.
</p>

<h3>2. list_users</h3>
    <pre>
    def list_users():
        users = os.popen("cut -d: -f1 /etc/passwd").read().splitlines()
        return users
    </pre>
    <p><b>Описание:</b> Получает список всех юзеров в системе.</p>

<h3>3. display_users</h3>
    <pre>
    def display_users(users, page, page_size=5):
        total_pages = (len(users) // page_size) + (1 if len(users) % page_size else 0)
        start = (page - 1) * page_size
        end = start + page_size
        current_page_users = users[start:end]
        return total_pages, current_page_users
    </pre>
    <p><b>Описание:</b> Отображает юзеров, делит весь список пользователей на страницы размером в 5 пользователей максимум (на странице).</p>

<h3>4. add_user</h3>
    <pre>
    def add_user(stdscr):
        stdscr.addstr("Enter new username: ")
        stdscr.refresh()
        curses.echo()
        username = stdscr.getstr().decode('utf-8')
        os.system(f"sudo useradd {username}")
        stdscr.addstr(f"Successfully added user '{username}'!\n", curses.color_pair(2))
        stdscr.refresh()
    </pre>
    <p><b>Описание:</b> Добавляет нового юзера в систему. Запрашивает имя пользователя и использует команду useradd для его создания.
</p>

<h3>5. delete_user</h3>
    <pre>
    def delete_user(stdscr, user):
        stdscr.addstr(f"Are you sure you want to delete user '{user}'? (y/n): ")
        stdscr.refresh()
        curses.echo()
        confirm = stdscr.getstr().decode('utf-8').lower()
        if confirm == 'y':
            os.system(f"sudo userdel {user}")
            stdscr.addstr(f"Successfully deleted user '{user}'!\n", curses.color_pair(3))
        else:
            stdscr.addstr("Deletion cancelled.\n", curses.color_pair(1))
        stdscr.refresh()
    </pre>
    <p><b>Описание:</b> Удаляет указанного юзера. При удалении уточняет, точно ли необходимо удалить именно этого юзера.
</p>

<h3>6. lock_user</h3>
    <pre>
    def lock_user(stdscr, user):
        stdscr.addstr(f"Are you sure you want to lock user '{user}'? (y/n): ")
        stdscr.refresh()
        curses.echo()
        confirm = stdscr.getstr().decode('utf-8').lower()
        if confirm == 'y':
            os.system(f"sudo usermod -L {user}")
            stdscr.addstr(f"User '{user}' locked.\n", curses.color_pair(4))
        else:
            stdscr.addstr("Lock cancelled.\n", curses.color_pair(1))
        stdscr.refresh()
    </pre>
    <p><b>Описание:</b> Блокирует учетную запись указанного юзера.</p>

 <h3>7. unlock_user</h3>
    <pre>
    def unlock_user(user):
        os.system(f"sudo usermod -U {user}")
        print(f"User '{user}' unlocked.")
    </pre>
    <p><b>Описание:</b> Разблокирует учетную запись указанного юзера.</p>

<h2>Использование программы</h2>
    <ol>
        <li>Склонируйте репозиторий на свой сервер:
            <pre>git clone https://github.com/nekkka/DevOps</pre>
        </li>
        <li>Перейдите в папку проекта:
            <pre>(условно)cd DevOps</pre>
        </li>
        <li>Запустите программу:
            <pre>python3 my_tears.py</pre>
        </li>
    </ol>

<h3>Навигация в программе</h3>
    <p>Используйте клавиши для выполнения действий:</p>
    <ul>
        <li><b>n</b> — добавить нового пользователя</li>
        <li><b>d</b> — удалить пользователя</li>
        <li><b>l</b> — заблокировать пользователя</li>
        <li><b>u</b> — разблокировать пользователя</li>
        <li><b>q</b> — выйти из программы</li>
        <li><b>Стрелки</b> — навигация по страницам пользователей</li>
    </ul>

![image](https://github.com/user-attachments/assets/6db5d556-cd6e-48ea-80d1-d35305f08645)

![image](https://github.com/user-attachments/assets/97a2f559-f504-4e10-ac7b-74f54bec2296)
![image](https://github.com/user-attachments/assets/bf637bae-131f-4efa-b931-68db28224a2c)
![image](https://github.com/user-attachments/assets/40e02054-701a-4557-8f13-2b22cdb0aac2)
![image](https://github.com/user-attachments/assets/a26dae5c-cbc4-427b-a8d2-732a4c91514c)
![image](https://github.com/user-attachments/assets/45e06663-9c52-45a4-9625-ee43d6c41595)
![image](https://github.com/user-attachments/assets/fb5b1320-b639-4cf7-a1b8-056d50c22088)







