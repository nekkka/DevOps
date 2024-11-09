import os
import curses
import pyfiglet

NAV_UP = 259
NAV_DOWN = 258
NAV_NEXT_PAGE = 'next'
NAV_PREV_PAGE = 'prev'

def welcome(stdscr):
    ascii_art = pyfiglet.figlet_format("User Management CLI")
    stdscr.addstr(ascii_art, curses.color_pair(1))
    stdscr.refresh()
    stdscr.addstr("\nPress any key to continue...\n")
    stdscr.refresh()
    stdscr.getch()

def list_users():
    users = os.popen("cut -d: -f1 /etc/passwd").read().splitlines()
    return users

def display_users(users, page, page_size=5):
    total_pages = (len(users) // page_size) + (1 if len(users) % page_size else 0)
    start = (page - 1) * page_size
    end = start + page_size
    current_page_users = users[start:end]
    
    return total_pages, current_page_users

def add_user(stdscr):
    username = ""
    stdscr.addstr("Enter new username: ")
    stdscr.refresh()
    curses.echo()
    username = stdscr.getstr().decode('utf-8')
    os.system(f"sudo useradd {username}")
    stdscr.addstr(f"Successfully added user '{username}'!\n", curses.color_pair(2))
    stdscr.refresh()

def delete_user(stdscr, user):
    confirm = ""
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

def lock_user(stdscr, user):
    confirm = ""
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

def unlock_user(user):
    os.system(f"sudo usermod -U {user}")
    print(f"User '{user}' unlocked.")

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Page title color
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Success color
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    # Error color
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Lock info color
    
    stdscr.clear()
    welcome(stdscr)

    page = 1
    users = list_users()
    page_size = 5

    while True:
        stdscr.clear()
        total_pages, current_page_users = display_users(users, page, page_size)
        stdscr.addstr(f"Page {page} of {total_pages}\n", curses.color_pair(1))

        for i, user in enumerate(current_page_users, start=1):
            stdscr.addstr(f"{i}. {user}\n")
        
        stdscr.addstr("\nChoose action (n=new user, d=delete user, l=lock user, u=unlock user, q=quit, ↑/↓=navigate): ")
        stdscr.refresh()

        action = stdscr.getch()

        if action == ord('n'):
            add_user(stdscr)
            users = list_users()
        elif action == ord('d'):
            stdscr.addstr("Enter username to delete: ")
            stdscr.refresh()
            curses.echo()
            selected_user = stdscr.getstr().decode('utf-8')
            if selected_user in users:
                delete_user(stdscr, selected_user)
                users = list_users()
            else:
                stdscr.addstr("User not found.\n", curses.color_pair(3))
                stdscr.refresh()
        elif action == ord('l'):
            stdscr.addstr("Enter username to lock: ")
            stdscr.refresh()
            curses.echo()
            selected_user = stdscr.getstr().decode('utf-8')
            if selected_user in users:
                lock_user(stdscr, selected_user)
            else:
                stdscr.addstr("User not found.\n", curses.color_pair(3))
                stdscr.refresh()
        elif action == ord('u'):
            stdscr.addstr("Enter username to unlock: ")
            stdscr.refresh()
            curses.echo()
            selected_user = stdscr.getstr().decode('utf-8')
            if selected_user in users:
                unlock_user(selected_user)
            else:
                stdscr.addstr("User not found.\n", curses.color_pair(3))
                stdscr.refresh()
        elif action == NAV_NEXT_PAGE and page < total_pages:
            page += 1
        elif action == NAV_PREV_PAGE and page > 1:
            page -= 1
        elif action == NAV_UP and page > 1:
            page -= 1
        elif action == NAV_DOWN and page < total_pages:
            page += 1
        elif action == ord('q'):
            stdscr.addstr("Exiting...\n", curses.color_pair(4))
            stdscr.refresh()
            break
        else:
            stdscr.addstr("Invalid action. Please try again.\n", curses.color_pair(3))
            stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
